import pandas as pd
import numpy as np


class StockDataPreprocessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None

    # ================= LOAD DATA =================
    def load_data(self):
        """
        Load stock CSV dataset
        """
        try:
            self.df = pd.read_csv(self.file_path)

            print("Dataset loaded successfully")
            return self.df

        except Exception as e:
            print(f"Error loading dataset: {e}")
            return None

    # ================= PARSE DATE =================
    def parse_date(self):
        """
        Convert Date column to datetime
        """
        try:
            self.df["Date"] = pd.to_datetime(
                self.df["Date"],
                errors="coerce"
            )
            self.df.dropna(subset=["Date"], inplace=True)

            print("Date column parsed successfully")

        except Exception as e:
            print(f"Date parsing error: {e}")

    # ================= SORT DATA =================
    def sort_data(self):
        """
        Sort stock data by date
        """
        try:
            self.df = self.df.sort_values("Date")
            self.df.reset_index(drop=True, inplace=True)

            print("Dataset sorted by date")

        except Exception as e:
            print(f"Sorting error: {e}")

    # ================= HANDLE MISSING VALUES =================
    def handle_missing_values(self):
        """
        Fill missing values
        """
        try:
            missing_before = self.df.isnull().sum().sum()

            # Forward fill then backward fill
            self.df.ffill(inplace=True)
            self.df.bfill(inplace=True)

            missing_after = self.df.isnull().sum().sum()

            print(f"Missing values before: {missing_before}")
            print(f"Missing values after: {missing_after}")

        except Exception as e:
            print(f"Missing value handling error: {e}")

    # ================= FEATURE ENGINEERING =================
    def create_features(self):
        """
        Create finance analytical features
        """
        try:
            # Daily Return
            self.df["Daily_Return"] = self.df["Close"].pct_change()

            # Price Difference
            self.df["Price_Diff"] = self.df["Close"] - self.df["Open"]

            # Percentage Change
            self.df["Pct_Change"] = (
                (self.df["Close"] - self.df["Open"])
                / self.df["Open"]
            ) * 100

            # Moving Averages
            self.df["MA7"] = self.df["Close"].rolling(window=7).mean()
            self.df["MA30"] = self.df["Close"].rolling(window=30).mean()

            # Volatility
            self.df["Volatility"] = (
                self.df["Close"].rolling(window=7).std()
            )

            # High-Low Spread
            self.df["HL_Spread"] = self.df["High"] - self.df["Low"]

            # Volume Change
            self.df["Volume_Change"] = self.df["Volume"].pct_change()

            print("Feature engineering completed")

        except Exception as e:
            print(f"Feature engineering error: {e}")

    # ================= TARGET CREATION =================
    def create_target(self):
        """
        Create next-day close price target
        """
        try:
            self.df["Target"] = self.df["Close"].shift(-1)

            print("Prediction target created")

        except Exception as e:
            print(f"Target creation error: {e}")

    # ================= FINAL CLEAN =================
    def final_clean(self):
        """
        Final cleaning after feature creation
        """
        try:
            # Fill rolling NaNs
            self.df.bfill(inplace=True)

            # Drop any remaining NaN
            self.df.dropna(inplace=True)

            self.df.reset_index(drop=True, inplace=True)

            print("Final cleaning completed")

        except Exception as e:
            print(f"Final cleaning error: {e}")

    # ================= PREPROCESS PIPELINE =================
    def preprocess(self):
        """
        Run complete preprocessing pipeline
        """
        self.load_data()
        self.parse_date()
        self.sort_data()
        self.handle_missing_values()
        self.create_features()
        self.create_target()
        self.final_clean()

        return self.df

    # ================= FEATURE SELECTION =================
    def get_features_target(self):
        """
        Return ML-ready X and y
        """
        feature_columns = [
            "Open",
            "High",
            "Low",
            "Volume",
            "Daily_Return",
            "Price_Diff",
            "Pct_Change",
            "MA7",
            "MA30",
            "Volatility",
            "HL_Spread",
            "Volume_Change"
        ]

        X = self.df[feature_columns]
        y = self.df["Target"]

        return X, y

    # ================= SUMMARY =================
    def dataset_summary(self):
        """
        Return dataset information
        """
        summary = {
            "Rows": self.df.shape[0],
            "Columns": self.df.shape[1],
            "Column Names": list(self.df.columns),
            "Missing Values": self.df.isnull().sum().to_dict(),
            "Data Types": self.df.dtypes.astype(str).to_dict()
        }

        return summary


# ================= DIRECT RUN TEST =================
if __name__ == "__main__":
    preprocessor = StockDataPreprocessor("dataset.csv")

    processed_df = preprocessor.preprocess()

    print("\nProcessed Dataset Preview:")
    print(processed_df.head())

    print("\nDataset Summary:")
    print(preprocessor.dataset_summary())