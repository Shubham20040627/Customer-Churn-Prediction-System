"""
Customer Churn Prediction Inference Module
Loads the saved Scikit-learn Pipeline using Joblib and generates predictions
for new customer inputs entered via the web form.
Persists predictions into MongoDB customerChurnDB.churn_predictions.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import joblib
import pandas as pd
import numpy as np

try:
    import config
    from src.database import db_manager
except ImportError:
    from .. import config
    from .database import db_manager


class ModelPredictor:
    """Singleton predictor that loads the saved model into memory once."""

    def __init__(self, model_path=None):
        self.model_path = model_path or config.MODEL_PATH
        self._model = None

    def is_model_trained(self):
        """Checks if the trained model artifact exists on disk."""
        return os.path.exists(self.model_path)

    def get_model(self):
        """Loads and caches the model pipeline."""
        if not self.is_model_trained():
            raise FileNotFoundError(
                f"Model file not found at '{self.model_path}'. "
                "Please run 'python src/train_model.py' to train and save the model first."
            )

        if self._model is None:
            print(f"Loading trained ML model from: {self.model_path}")
            self._model = joblib.load(self.model_path)
        return self._model

    def validate_and_format_input(self, input_data):
        """
        Validates user-submitted input dictionary and converts data types
        to match model requirements.
        """
        cleaned_data = {}

        # Validate numerical features
        for num_feat in config.NUMERICAL_FEATURES:
            val = input_data.get(num_feat)
            if val is None or str(val).strip() == "":
                raise ValueError(f"Missing required numerical feature: '{num_feat}'")
            try:
                cleaned_data[num_feat] = float(val)
            except ValueError:
                raise ValueError(f"Feature '{num_feat}' must be a valid number, got: '{val}'")

        # Validate categorical features
        for cat_feat in config.CATEGORICAL_FEATURES:
            val = input_data.get(cat_feat)
            if not val or str(val).strip() == "":
                raise ValueError(f"Missing required categorical feature: '{cat_feat}'")
            val_clean = str(val).strip()
            # Verify against allowed options if defined
            allowed = config.CATEGORICAL_OPTIONS.get(cat_feat)
            if allowed and val_clean not in allowed:
                # Fallback: check case-insensitive match
                matched = next((opt for opt in allowed if opt.lower() == val_clean.lower()), None)
                if matched:
                    val_clean = matched
                else:
                    raise ValueError(f"Invalid value '{val}' for '{cat_feat}'. Allowed: {allowed}")
            cleaned_data[cat_feat] = val_clean

        return cleaned_data

    def predict(self, raw_input_data, save_to_db=True):
        """
        Executes inference for a single customer record and saves the result to MongoDB.

        Returns:
            dict containing:
                - prediction_code (0 or 1)
                - prediction_label ("Unlikely to Churn" or "Likely to Churn")
                - churn_probability (float, percentage)
                - loyal_probability (float, percentage)
                - risk_level ("Low Risk", "Moderate Risk", "High Risk")
                - saved_id (str MongoDB document ID or None)
        """
        model = self.get_model()

        # Step 1: Clean and format input data
        cleaned_input = self.validate_and_format_input(raw_input_data)

        # Step 2: Build single-row DataFrame with exact feature order
        input_df = pd.DataFrame([cleaned_input], columns=config.ALL_FEATURE_COLUMNS)

        # Step 3: Run prediction through pipeline
        prediction = model.predict(input_df)[0]
        prediction_code = int(prediction)

        # Probability calculation
        churn_pct = 0.0
        loyal_pct = 0.0
        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(input_df)[0]
            # Logistic regression class 0: Loyal, class 1: Churn
            classes = list(model.classes_)
            churn_idx = classes.index(1) if 1 in classes else 1
            loyal_idx = classes.index(0) if 0 in classes else 0

            churn_pct = round(float(probabilities[churn_idx]) * 100, 2)
            loyal_pct = round(float(probabilities[loyal_idx]) * 100, 2)

        # Label and risk level
        if prediction_code == 1:
            prediction_label = "Likely to Churn"
            if churn_pct >= 75.0:
                risk_level = "High Churn Risk"
            else:
                risk_level = "Moderate Churn Risk"
        else:
            prediction_label = "Unlikely to Churn"
            risk_level = "Loyal Customer (Low Risk)"

        # Step 4: Persist in MongoDB
        saved_id = None
        if save_to_db:
            try:
                saved_id = db_manager.save_prediction(
                    customer_input=cleaned_input,
                    prediction_code=prediction_code,
                    prediction_label=prediction_label,
                    probability={"churn": churn_pct, "loyal": loyal_pct}
                )
            except Exception as err:
                print(f"Warning: Failed to save prediction to MongoDB: {err}")

        return {
            "prediction_code": prediction_code,
            "prediction_label": prediction_label,
            "churn_probability": churn_pct,
            "loyal_probability": loyal_pct,
            "risk_level": risk_level,
            "saved_id": saved_id,
            "inputs": cleaned_input
        }


# Global singleton instance
predictor = ModelPredictor()
