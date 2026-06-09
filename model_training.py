import joblib
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor

from data_preprocessing import StockDataPreprocessor


class StockModelTrainer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.preprocessor = StockDataPreprocessor(file_path)

        self.df = None
        self.X = None
        self.y = None

        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

        self.models = {}
        self.results = {}
        self.best_model = None
        self.best_model_name = None

    # ================= PREPARE DATA =================
    def prepare_data(self):
        """
        Run preprocessing and prepare train/test sets
        """
        self.df = self.preprocessor.preprocess()
        self.X, self.y = self.preprocessor.get_features_target()

        # Train-test split
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X,
            self.y,
            test_size=0.2,
            random_state=42,
            shuffle=False
        )

        print("Data prepared successfully")

    # ================= DEFINE MODELS =================
    def initialize_models(self):
        """
        Define ML models
        """
        self.models = {
            "Linear Regression": LinearRegression(),

            "Random Forest": RandomForestRegressor(
                n_estimators=200,
                max_depth=10,
                random_state=42
            ),

            "Gradient Boosting": GradientBoostingRegressor(
                n_estimators=200,
                learning_rate=0.05,
                random_state=42
            )
        }

        print("Models initialized")

    # ================= TRAIN MODEL =================
    def train_model(self, model_name, model):
        """
        Train a single model
        """
        print(f"\nTraining {model_name}...")

        model.fit(self.X_train, self.y_train)

        predictions = model.predict(self.X_test)

        mae = mean_absolute_error(self.y_test, predictions)
        rmse = np.sqrt(mean_squared_error(self.y_test, predictions))
        r2 = r2_score(self.y_test, predictions)

        self.results[model_name] = {
            "model": model,
            "MAE": round(mae, 4),
            "RMSE": round(rmse, 4),
            "R2 Score": round(r2, 4)
        }

        print(f"{model_name} completed")
        print(f"MAE: {mae:.4f}")
        print(f"RMSE: {rmse:.4f}")
        print(f"R2 Score: {r2:.4f}")

    # ================= TRAIN ALL MODELS =================
    def train_all_models(self):
        """
        Train all defined models
        """
        for model_name, model in self.models.items():
            self.train_model(model_name, model)

    # ================= SELECT BEST MODEL =================
    def select_best_model(self):
        """
        Select model with highest R2 score
        """
        best_score = -999

        for model_name, metrics in self.results.items():
            if metrics["R2 Score"] > best_score:
                best_score = metrics["R2 Score"]
                self.best_model = metrics["model"]
                self.best_model_name = model_name

        print(f"\nBest Model Selected: {self.best_model_name}")
        print(f"Best R2 Score: {best_score}")

    # ================= SAVE MODEL =================
    def save_model(self):
        """
        Save best model
        """
        if self.best_model is not None:
            joblib.dump(self.best_model, "best_stock_model.pkl")
            print("Best model saved as best_stock_model.pkl")

    # ================= SAVE FEATURES =================
    def save_feature_columns(self):
        """
        Save feature column names
        """
        feature_columns = list(self.X.columns)
        joblib.dump(feature_columns, "feature_columns.pkl")

        print("Feature columns saved")

    # ================= FEATURE IMPORTANCE =================
    def feature_importance(self):
        """
        Get feature importance if supported
        """
        if hasattr(self.best_model, "feature_importances_"):
            importance = dict(
                zip(
                    self.X.columns,
                    self.best_model.feature_importances_
                )
            )

            sorted_importance = dict(
                sorted(
                    importance.items(),
                    key=lambda x: x[1],
                    reverse=True
                )
            )

            print("\nFeature Importance:")
            for feature, score in sorted_importance.items():
                print(f"{feature}: {score:.4f}")

            return sorted_importance

        else:
            print("Feature importance not available for this model")
            return None

    # ================= RESULTS SUMMARY =================
    def model_results(self):
        """
        Return model comparison
        """
        return self.results

    # ================= TRAIN PIPELINE =================
    def run_training_pipeline(self):
        """
        Full training pipeline
        """
        print("Starting training pipeline...")

        self.prepare_data()
        self.initialize_models()
        self.train_all_models()
        self.select_best_model()
        self.save_model()
        self.save_feature_columns()
        self.feature_importance()

        print("\nTraining pipeline completed")

        return self.results


# ================= DIRECT RUN =================
if __name__ == "__main__":
    trainer = StockModelTrainer("dataset.csv")

    results = trainer.run_training_pipeline()

    print("\nMODEL COMPARISON:")
    for model_name, metrics in results.items():
        print(f"\n{model_name}")
        print(metrics)