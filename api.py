from pathlib import Path
import os

import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sklearn.ensemble import RandomForestRegressor

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

# ================= CONFIG =================
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "dataset.csv"
load_dotenv(BASE_DIR / ".env")

# ================= FASTAPI APP =================
app = FastAPI(title="FinSight AI API", version="1.0.0")

# ================= CORS =================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================= LOAD DATASET =================
def load_and_prepare_data() -> pd.DataFrame:
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"dataset.csv not found at: {DATA_FILE}")

    data = pd.read_csv(DATA_FILE)

    required_columns = {"Date", "Open", "High", "Low", "Close", "Volume"}
    missing_columns = required_columns - set(data.columns)
    if missing_columns:
        raise ValueError(f"Missing columns in dataset: {', '.join(sorted(missing_columns))}")

    # Auto-detect date format. This works with '2015-01-02 16:00:00' and many other common formats.
    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
    data = data.dropna(subset=["Date"]).sort_values("Date").reset_index(drop=True)

    numeric_columns = ["Open", "High", "Low", "Close", "Volume"]
    data[numeric_columns] = data[numeric_columns].apply(pd.to_numeric, errors="coerce")
    data = data.dropna(subset=numeric_columns).reset_index(drop=True)

    # ================= FEATURE ENGINEERING =================
    data["Daily_Return"] = data["Close"].pct_change()
    data["MA7"] = data["Close"].rolling(window=7, min_periods=1).mean()
    data["MA30"] = data["Close"].rolling(window=30, min_periods=1).mean()
    data["Volatility"] = data["Close"].rolling(window=7, min_periods=1).std().fillna(0)

    # ================= TARGET =================
    data["Target"] = data["Close"].shift(-1)
    data = data.dropna().reset_index(drop=True)
    return data


df = load_and_prepare_data()

# ================= MODEL TRAINING =================
FEATURES = ["Open", "High", "Low", "Volume", "MA7", "MA30", "Volatility"]
X = df[FEATURES]
y = df["Target"]

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# ================= REQUEST MODEL =================
class ChatRequest(BaseModel):
    message: str


# ================= STOCK DATA ENDPOINT =================
@app.get("/stock-data")
def get_stock_data():
    stock_df = df.copy()
    stock_df["Date"] = stock_df["Date"].dt.strftime("%Y-%m-%d")
    return stock_df[["Date", "Open", "High", "Low", "Close", "Volume"]].to_dict(orient="records")


# ================= ANALYTICS ENDPOINT =================
@app.get("/analytics")
def get_analytics():
    latest = df.iloc[-1]

    volatility_score = round(float(latest["Volatility"]), 2)
    support_level = round(float(df["Low"].tail(10).min()), 2)
    resistance_level = round(float(df["High"].tail(10).max()), 2)

    ma_signal = "Bullish" if latest["MA7"] > latest["MA30"] else "Bearish"
    market_signal = "UPTREND" if latest["Close"] > latest["MA7"] else "DOWNTREND"

    if volatility_score > 1.0:
        risk_score = "High"
    elif volatility_score > 0.5:
        risk_score = "Medium"
    else:
        risk_score = "Low"

    ai_insights = (
        f"Stock is currently showing a {market_signal}. "
        f"Moving average crossover suggests a {ma_signal} signal. "
        f"Volatility score is {volatility_score}, indicating {risk_score.lower()} risk conditions. "
        f"Support level is near ${support_level} and resistance is near ${resistance_level}."
    )

    portfolio_analysis = (
        f"Portfolio risk appears {risk_score}. "
        f"Consider diversification if volatility increases. "
        f"Current trend signal suggests {market_signal.lower()} market behavior."
    )

    return {
        "volatility": volatility_score,
        "support": support_level,
        "resistance": resistance_level,
        "ma_signal": ma_signal,
        "market_signal": market_signal,
        "risk_score": risk_score,
        "ai_insights": ai_insights,
        "portfolio_analysis": portfolio_analysis,
    }


# ================= PREDICTION ENDPOINT =================
@app.get("/prediction")
def get_prediction():
    latest = df.iloc[-1]

    input_data = pd.DataFrame([{feature: latest[feature] for feature in FEATURES}])
    predicted_price = float(model.predict(input_data)[0])
    current_price = float(latest["Close"])

    trend = "Bullish" if predicted_price > current_price else "Bearish"
    difference_pct = abs(predicted_price - current_price) / current_price * 100 if current_price else 0
    confidence = round(max(0, min(100, 100 - difference_pct)), 2)

    return {
        "current_price": round(current_price, 2),
        "predicted_price": round(predicted_price, 2),
        "trend": trend,
        "confidence": confidence,
    }


# ================= AI CHATBOT ENDPOINT =================
@app.post("/chat")
def chat_with_ai(request: ChatRequest):
    user_message = request.message.strip()
    latest = df.iloc[-1]

    stock_summary = (
        f"Open: {latest['Open']}, High: {latest['High']}, Low: {latest['Low']}, "
        f"Close: {latest['Close']}, Volume: {latest['Volume']}, "
        f"MA7: {round(float(latest['MA7']), 2)}, MA30: {round(float(latest['MA30']), 2)}, "
        f"Volatility: {round(float(latest['Volatility']), 2)}"
    )

    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key or OpenAI is None:
        return {
            "reply": (
                "Local analysis: Based on the latest data, "
                f"{stock_summary}. Add your OPENAI_API_KEY in .env to enable the full AI chatbot."
            )
        }

    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful financial AI assistant. "
                        "Use the provided stock data and answer clearly. "
                        "Do not give guaranteed investment advice.\n\n"
                        f"Latest stock data: {stock_summary}"
                    ),
                },
                {"role": "user", "content": user_message},
            ],
            temperature=0.7,
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"AI service error: {e}"

    return {"reply": reply}


# ================= ROOT =================
@app.get("/")
def home():
    return {"message": "FinSight AI Backend Running", "docs": "/docs"}

# Run using: uvicorn api:app --reload
