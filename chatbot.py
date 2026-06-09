import os
from dotenv import load_dotenv
from openai import OpenAI

from data_preprocessing import StockDataPreprocessor
from analytics import StockAnalytics
from prediction import StockPredictor

# ================= LOAD ENV =================
load_dotenv()


class FinSightAIChatbot:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path

        self.preprocessor = StockDataPreprocessor(dataset_path)
        self.analytics = StockAnalytics(dataset_path)
        self.predictor = StockPredictor(dataset_path)

        self.df = None

        # ================= LOAD API KEY =================
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY not found. Please check your .env file"
            )

        # ================= OPENAI CLIENT =================
        self.client = OpenAI(api_key=api_key)

    # ================= LOAD DATA =================
    def load_data(self):
        """
        Load stock data and initialize modules
        """
        try:
            self.df = self.preprocessor.preprocess()

            self.analytics.load_data()

            self.predictor.load_model()
            self.predictor.load_processed_data()

            print("AI chatbot data loaded successfully")

        except Exception as e:
            print(f"Data loading error: {e}")

    # ================= BUILD CONTEXT =================
    def build_financial_context(self):
        """
        Create financial context for AI
        """
        try:
            latest = self.df.iloc[-1]

            analytics_result = self.analytics.get_full_analytics()
            prediction_result = self.predictor.predict_next_close()

            context = f"""
STOCK DATA SUMMARY

Latest Market Data:
Open: {latest['Open']}
High: {latest['High']}
Low: {latest['Low']}
Close: {latest['Close']}
Volume: {latest['Volume']}

Technical Indicators:
MA7: {latest['MA7']}
MA30: {latest['MA30']}
Volatility: {latest['Volatility']}
Daily Return: {latest['Daily_Return']}

ANALYTICS:
Market Signal: {analytics_result['market_signal']}
MA Signal: {analytics_result['ma_signal']}
Risk Score: {analytics_result['risk_score']}
Support Level: {analytics_result['support']}
Resistance Level: {analytics_result['resistance']}
Momentum: {analytics_result['momentum']}
Trend Strength: {analytics_result['trend_strength']}
Volume Signal: {analytics_result['volume_signal']}

PREDICTION:
Current Price: {prediction_result['current_price']}
Predicted Price: {prediction_result['predicted_price']}
Trend: {prediction_result['trend']}
Confidence: {prediction_result['confidence']}%
"""
            return context

        except Exception as e:
            print(f"Context generation error: {e}")
            return "Stock context unavailable"

    # ================= ASK AI =================
    def ask_ai(self, user_message):
        """
        Send user finance question to OpenAI
        """
        try:
            financial_context = self.build_financial_context()

            system_prompt = f"""
You are FinSight AI, an expert financial AI assistant.

Your responsibilities:

- Analyze stock trends
- Explain stock movement
- Explain prediction results
- Explain volatility
- Explain risk
- Explain bullish/bearish signals
- Answer finance questions professionally

Rules:

- Use simple finance language
- Be professional
- Be clear
- Do NOT give legal investment advice
- Use stock data context

STOCK CONTEXT:
{financial_context}
"""

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ],
                temperature=0.7,
                max_tokens=500
            )

            reply = response.choices[0].message.content

            return reply

        except Exception as e:
            return f"AI service error: {str(e)}"

    # ================= QUICK SUMMARY =================
    def quick_market_summary(self):
        """
        Generate automatic AI market summary
        """
        prompt = """
Summarize today's stock market behavior.
Explain trend, risk, and prediction clearly.
"""
        return self.ask_ai(prompt)

    # ================= EXPLAIN PREDICTION =================
    def explain_prediction(self):
        """
        Explain prediction result
        """
        prompt = """
Explain why the stock prediction is moving in that direction.
Mention trend, volatility, and technical indicators.
"""
        return self.ask_ai(prompt)

    # ================= EXPLAIN RISK =================
    def explain_risk(self):
        """
        Explain stock risk
        """
        prompt = """
Explain stock risk conditions and volatility in simple finance language.
"""
        return self.ask_ai(prompt)

    # ================= MAIN CHAT ENTRY =================
    def run_chat(self, user_message):
        """
        Main chatbot function
        """
        self.load_data()

        return self.ask_ai(user_message)


# ================= DIRECT RUN TEST =================
if __name__ == "__main__":
    chatbot = FinSightAIChatbot("dataset.csv")

    chatbot.load_data()

    print("\n=== QUICK MARKET SUMMARY ===")
    print(chatbot.quick_market_summary())

    print("\n=== AI CHAT TEST ===")
    user_question = "Is the stock bullish right now?"
    response = chatbot.ask_ai(user_question)

    print(f"\nQ: {user_question}")
    print(f"A: {response}")