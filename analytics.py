import pandas as pd
import numpy as np

from data_preprocessing import StockDataPreprocessor


class StockAnalytics:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.preprocessor = StockDataPreprocessor(dataset_path)
        self.df = None

    # ================= LOAD DATA =================
    def load_data(self):
        """
        Load processed stock dataset
        """
        try:
            self.df = self.preprocessor.preprocess()
            print("Processed stock data loaded")

        except Exception as e:
            print(f"Data loading error: {e}")

    # ================= VOLATILITY SCORE =================
    def calculate_volatility(self):
        """
        Calculate latest volatility score
        """
        try:
            latest_volatility = float(
                self.df["Volatility"].iloc[-1]
            )

            return round(latest_volatility, 2)

        except Exception as e:
            print(f"Volatility calculation error: {e}")
            return 0

    # ================= SUPPORT LEVEL =================
    def calculate_support(self):
        """
        Estimate support level
        """
        try:
            support = float(
                self.df["Low"].tail(10).min()
            )

            return round(support, 2)

        except Exception as e:
            print(f"Support calculation error: {e}")
            return 0

    # ================= RESISTANCE LEVEL =================
    def calculate_resistance(self):
        """
        Estimate resistance level
        """
        try:
            resistance = float(
                self.df["High"].tail(10).max()
            )

            return round(resistance, 2)

        except Exception as e:
            print(f"Resistance calculation error: {e}")
            return 0

    # ================= MOVING AVERAGE SIGNAL =================
    def moving_average_signal(self):
        """
        MA crossover signal
        """
        try:
            latest = self.df.iloc[-1]

            if latest["MA7"] > latest["MA30"]:
                return "Bullish"

            elif latest["MA7"] < latest["MA30"]:
                return "Bearish"

            else:
                return "Neutral"

        except Exception as e:
            print(f"MA signal error: {e}")
            return "Unknown"

    # ================= MARKET TREND =================
    def market_signal(self):
        """
        Detect current market trend
        """
        try:
            latest = self.df.iloc[-1]

            if latest["Close"] > latest["MA7"]:
                return "UPTREND"

            elif latest["Close"] < latest["MA7"]:
                return "DOWNTREND"

            else:
                return "SIDEWAYS"

        except Exception as e:
            print(f"Market signal error: {e}")
            return "Unknown"

    # ================= RISK SCORE =================
    def calculate_risk_score(self):
        """
        Generate stock risk score
        """
        try:
            volatility = self.calculate_volatility()

            if volatility > 1.5:
                return "High"

            elif volatility > 0.7:
                return "Medium"

            else:
                return "Low"

        except Exception as e:
            print(f"Risk score error: {e}")
            return "Unknown"

    # ================= VOLUME SPIKE DETECTION =================
    def detect_volume_spike(self):
        """
        Detect unusual trading volume
        """
        try:
            latest_volume = self.df["Volume"].iloc[-1]
            avg_volume = self.df["Volume"].tail(10).mean()

            if latest_volume > avg_volume * 1.5:
                return "Volume Spike Detected"

            elif latest_volume < avg_volume * 0.7:
                return "Low Trading Volume"

            else:
                return "Normal Volume"

        except Exception as e:
            print(f"Volume spike error: {e}")
            return "Unknown"

    # ================= PRICE MOMENTUM =================
    def price_momentum(self):
        """
        Calculate momentum based on recent closes
        """
        try:
            recent_close = self.df["Close"].tail(5)

            momentum = recent_close.iloc[-1] - recent_close.iloc[0]

            if momentum > 0:
                return "Positive"

            elif momentum < 0:
                return "Negative"

            else:
                return "Neutral"

        except Exception as e:
            print(f"Momentum error: {e}")
            return "Unknown"

    # ================= TREND STRENGTH =================
    def trend_strength(self):
        """
        Estimate trend strength
        """
        try:
            close_prices = self.df["Close"].tail(10)

            slope = np.polyfit(range(len(close_prices)), close_prices, 1)[0]

            if slope > 0.2:
                return "Strong Uptrend"

            elif slope > 0:
                return "Weak Uptrend"

            elif slope < -0.2:
                return "Strong Downtrend"

            else:
                return "Weak Downtrend"

        except Exception as e:
            print(f"Trend strength error: {e}")
            return "Unknown"

    # ================= AI INSIGHTS =================
    def generate_ai_insights(self):
        """
        Generate AI-style finance explanation
        """
        try:
            trend = self.market_signal()
            ma_signal = self.moving_average_signal()
            volatility = self.calculate_volatility()
            risk = self.calculate_risk_score()
            volume = self.detect_volume_spike()
            momentum = self.price_momentum()

            insights = f"""
            Current market shows a {trend}.
            Moving average crossover indicates a {ma_signal} signal.
            Volatility score is {volatility}, suggesting {risk.lower()} risk conditions.
            Trading activity indicates: {volume}.
            Recent price momentum appears {momentum.lower()}.
            """

            return insights.strip()

        except Exception as e:
            print(f"AI insights error: {e}")
            return "Insights unavailable"

    # ================= PORTFOLIO ANALYSIS =================
    def portfolio_analysis(self):
        """
        Generate portfolio-style risk analysis
        """
        try:
            risk = self.calculate_risk_score()
            trend = self.market_signal()
            momentum = self.price_momentum()

            analysis = f"""
            Portfolio risk level appears {risk}.
            Current market trend suggests {trend.lower()} behavior.
            Momentum is {momentum.lower()}.
            Consider diversification under high volatility.
            """

            return analysis.strip()

        except Exception as e:
            print(f"Portfolio analysis error: {e}")
            return "Portfolio analysis unavailable"

    # ================= FULL ANALYTICS =================
    def get_full_analytics(self):
        """
        Return complete analytics dictionary
        """
        return {
            "volatility": self.calculate_volatility(),
            "support": self.calculate_support(),
            "resistance": self.calculate_resistance(),
            "ma_signal": self.moving_average_signal(),
            "market_signal": self.market_signal(),
            "risk_score": self.calculate_risk_score(),
            "volume_signal": self.detect_volume_spike(),
            "momentum": self.price_momentum(),
            "trend_strength": self.trend_strength(),
            "ai_insights": self.generate_ai_insights(),
            "portfolio_analysis": self.portfolio_analysis()
        }

    # ================= RUN =================
    def run_analysis(self):
        """
        Full analytics pipeline
        """
        self.load_data()

        return self.get_full_analytics()


# ================= DIRECT RUN TEST =================
if __name__ == "__main__":
    analytics = StockAnalytics("dataset.csv")

    analytics.load_data()

    result = analytics.get_full_analytics()

    print("\nSTOCK ANALYTICS:")
    for key, value in result.items():
        print(f"{key}: {value}")