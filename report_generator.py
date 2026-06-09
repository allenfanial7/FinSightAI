from datetime import datetime

from data_preprocessing import StockDataPreprocessor
from analytics import StockAnalytics
from prediction import StockPredictor
from chatbot import FinSightAIChatbot


class FinancialReportGenerator:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path

        self.preprocessor = StockDataPreprocessor(dataset_path)
        self.analytics = StockAnalytics(dataset_path)
        self.predictor = StockPredictor(dataset_path)
        self.chatbot = FinSightAIChatbot(dataset_path)

        self.df = None

    # ================= LOAD DATA =================
    def load_data(self):
        """
        Load required project modules
        """
        try:
            self.df = self.preprocessor.preprocess()

            self.analytics.load_data()

            self.predictor.load_model()
            self.predictor.load_processed_data()

            self.chatbot.load_data()

            print("Report modules loaded successfully")

        except Exception as e:
            print(f"Data loading error: {e}")

    # ================= STOCK SUMMARY =================
    def generate_stock_summary(self):
        """
        Generate latest stock summary
        """
        try:
            latest = self.df.iloc[-1]

            summary = f"""
================ STOCK SUMMARY ================

Date: {latest['Date']}

Open Price: ${round(latest['Open'], 2)}
High Price: ${round(latest['High'], 2)}
Low Price: ${round(latest['Low'], 2)}
Close Price: ${round(latest['Close'], 2)}

Trading Volume: {int(latest['Volume'])}

Daily Return: {round(latest['Daily_Return'], 4)}
Price Difference: {round(latest['Price_Diff'], 2)}
Percentage Change: {round(latest['Pct_Change'], 2)}%

7-Day Moving Average: {round(latest['MA7'], 2)}
30-Day Moving Average: {round(latest['MA30'], 2)}

Volatility: {round(latest['Volatility'], 2)}

"""
            return summary

        except Exception as e:
            return f"Stock summary error: {str(e)}"

    # ================= ANALYTICS SUMMARY =================
    def generate_analytics_summary(self):
        """
        Generate financial analytics report
        """
        try:
            analytics_result = self.analytics.get_full_analytics()

            summary = f"""
================ FINANCIAL ANALYTICS ================

Volatility Score: {analytics_result['volatility']}
Support Level: ${analytics_result['support']}
Resistance Level: ${analytics_result['resistance']}

Moving Average Signal: {analytics_result['ma_signal']}
Market Signal: {analytics_result['market_signal']}

Risk Score: {analytics_result['risk_score']}
Volume Signal: {analytics_result['volume_signal']}
Momentum: {analytics_result['momentum']}
Trend Strength: {analytics_result['trend_strength']}

AI Insights:
{analytics_result['ai_insights']}

Portfolio Analysis:
{analytics_result['portfolio_analysis']}

"""
            return summary

        except Exception as e:
            return f"Analytics summary error: {str(e)}"

    # ================= PREDICTION SUMMARY =================
    def generate_prediction_summary(self):
        """
        Generate prediction report
        """
        try:
            prediction_result = self.predictor.predict_next_close()

            summary = f"""
================ STOCK PREDICTION ================

Current Price: ${prediction_result['current_price']}
Predicted Price: ${prediction_result['predicted_price']}

Price Change: ${prediction_result['price_change']}
Percentage Change: {prediction_result['percentage_change']}%

Trend Signal: {prediction_result['trend']}
Confidence Score: {prediction_result['confidence']}%

"""
            return summary

        except Exception as e:
            return f"Prediction summary error: {str(e)}"

    # ================= AI REPORT SUMMARY =================
    def generate_ai_summary(self):
        """
        Generate OpenAI finance summary
        """
        try:
            ai_summary = self.chatbot.quick_market_summary()

            summary = f"""
================ AI MARKET SUMMARY ================

{ai_summary}

"""
            return summary

        except Exception as e:
            return f"AI summary error: {str(e)}"

    # ================= FINAL REPORT =================
    def generate_full_report(self):
        """
        Combine complete report
        """
        try:
            report_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            report = f"""
=====================================================
           FinSight AI Financial Analysis Report
=====================================================

Generated On: {report_time}

"""

            report += self.generate_stock_summary()
            report += self.generate_analytics_summary()
            report += self.generate_prediction_summary()
            report += self.generate_ai_summary()

            report += """
=====================================================
           END OF REPORT
=====================================================
"""

            return report

        except Exception as e:
            return f"Full report generation error: {str(e)}"

    # ================= SAVE REPORT =================
    def save_report(self, filename="financial_report.txt"):
        """
        Save report to file
        """
        try:
            report = self.generate_full_report()

            with open(filename, "w", encoding="utf-8") as file:
                file.write(report)

            print(f"Report saved successfully as {filename}")

            return filename

        except Exception as e:
            print(f"Report saving error: {e}")
            return None

    # ================= RUN =================
    def run_report_generation(self):
        """
        Full report generation pipeline
        """
        self.load_data()

        return self.save_report()


# ================= DIRECT RUN TEST =================
if __name__ == "__main__":
    generator = FinancialReportGenerator("dataset.csv")

    generator.load_data()

    print("\nGenerating report...")

    filename = generator.save_report()

    if filename:
        print(f"\nReport created: {filename}")

        print("\nPreview:")
        print(generator.generate_full_report())