import joblib
import pandas as pd
import numpy as np

from data_preprocessing import StockDataPreprocessor


class StockPredictor:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path

        self.model = None
        self.feature_columns = None
        self.preprocessor = StockDataPreprocessor(dataset_path)

        self.df = None

    # ================= LOAD MODEL =================
    def load_model(self):
        """
        Load trained ML model and feature columns
        """
        try:
            self.model = joblib.load("best_stock_model.pkl")
            self.feature_columns = joblib.load("feature_columns.pkl")

            print("Model loaded successfully")

        except Exception as e:
            print(f"Model loading error: {e}")

    # ================= LOAD DATA =================
    def load_processed_data(self):
        """
        Load processed stock dataset
        """
        try:
            self.df = self.preprocessor.preprocess()

            print("Processed dataset loaded")

        except Exception as e:
            print(f"Dataset loading error: {e}")

    # ================= PREPARE INPUT =================
    def prepare_latest_input(self):
        """
        Prepare latest row input for prediction
        """
        try:
            latest = self.df.iloc[-1]

            input_data = pd.DataFrame([{
                "Open": latest["Open"],
                "High": latest["High"],
                "Low": latest["Low"],
                "Volume": latest["Volume"],
                "Daily_Return": latest["Daily_Return"],
                "Price_Diff": latest["Price_Diff"],
                "Pct_Change": latest["Pct_Change"],
                "MA7": latest["MA7"],
                "MA30": latest["MA30"],
                "Volatility": latest["Volatility"],
                "HL_Spread": latest["HL_Spread"],
                "Volume_Change": latest["Volume_Change"]
            }])

            # Ensure correct column order
            input_data = input_data[self.feature_columns]

            return input_data

        except Exception as e:
            print(f"Input preparation error: {e}")
            return None

    # ================= PREDICT =================
    def predict_next_close(self):
        """
        Predict next closing price
        """
        try:
            input_data = self.prepare_latest_input()

            prediction = float(
                self.model.predict(input_data)[0]
            )

            current_price = float(
                self.df.iloc[-1]["Close"]
            )

            price_change = prediction - current_price
            pct_change = (price_change / current_price) * 100

            trend = (
                "Bullish"
                if prediction > current_price
                else "Bearish"
            )

            # Simple confidence estimation
            confidence = max(
                50,
                round(100 - abs(pct_change), 2)
            )

            result = {
                "current_price": round(current_price, 2),
                "predicted_price": round(prediction, 2),
                "price_change": round(price_change, 2),
                "percentage_change": round(pct_change, 2),
                "trend": trend,
                "confidence": confidence
            }

            return result

        except Exception as e:
            print(f"Prediction error: {e}")
            return None

    # ================= PREDICT FUTURE SERIES =================
    def predict_future_days(self, days=5):
        """
        Predict multiple future prices (basic rolling prediction)
        """
        try:
            predictions = []

            current_row = self.df.iloc[-1].copy()

            for day in range(days):
                input_data = pd.DataFrame([{
                    "Open": current_row["Open"],
                    "High": current_row["High"],
                    "Low": current_row["Low"],
                    "Volume": current_row["Volume"],
                    "Daily_Return": current_row["Daily_Return"],
                    "Price_Diff": current_row["Price_Diff"],
                    "Pct_Change": current_row["Pct_Change"],
                    "MA7": current_row["MA7"],
                    "MA30": current_row["MA30"],
                    "Volatility": current_row["Volatility"],
                    "HL_Spread": current_row["HL_Spread"],
                    "Volume_Change": current_row["Volume_Change"]
                }])

                input_data = input_data[self.feature_columns]

                next_prediction = float(
                    self.model.predict(input_data)[0]
                )

                predictions.append(
                    round(next_prediction, 2)
                )

                # Update row for next loop
                current_row["Close"] = next_prediction
                current_row["Open"] = next_prediction
                current_row["High"] = next_prediction * 1.01
                current_row["Low"] = next_prediction * 0.99

            return predictions

        except Exception as e:
            print(f"Future prediction error: {e}")
            return []

    # ================= PREDICTION SUMMARY =================
    def generate_prediction_summary(self):
        """
        Generate human-readable prediction analysis
        """
        prediction = self.predict_next_close()

        if prediction is None:
            return "Prediction unavailable"

        summary = f"""
        Current stock price is ${prediction['current_price']}.
        Predicted next closing price is ${prediction['predicted_price']}.
        Expected movement is {prediction['percentage_change']}%.
        Market trend appears {prediction['trend']}.
        Prediction confidence is {prediction['confidence']}%.
        """

        return summary.strip()

    # ================= RUN PIPELINE =================
    def run_prediction(self):
        """
        Full prediction pipeline
        """
        self.load_model()
        self.load_processed_data()

        prediction_result = self.predict_next_close()

        return prediction_result


# ================= DIRECT RUN TEST =================
if __name__ == "__main__":
    predictor = StockPredictor("dataset.csv")

    predictor.load_model()
    predictor.load_processed_data()

    result = predictor.predict_next_close()

    print("\nNEXT DAY PREDICTION:")
    print(result)

    print("\n5-DAY FORECAST:")
    print(predictor.predict_future_days(days=5))

    print("\nPREDICTION SUMMARY:")
    print(predictor.generate_prediction_summary())