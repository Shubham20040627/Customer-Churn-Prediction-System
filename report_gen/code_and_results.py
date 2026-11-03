"""
Comprehensive Implementation, Full Code Listings, and Results Module
Provides complete code listings, 8 visual screenshot walkthroughs, and detailed experimental results.
"""

import os
from docx.shared import Inches, Pt, RGBColor
from report_gen.doc_utils import (
    add_styled_heading, add_body_p, add_bullet_p, add_callout_box,
    add_code_block, add_styled_table, format_paragraph, add_styled_image
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")

def build_chapter_6(doc):
    add_styled_heading(doc, "CHAPTER 6: IMPLEMENTATION, FULL CODE LISTINGS, AND SCREENSHOT WALKTHROUGHS", level=1)
    
    add_styled_heading(doc, "6.1 Software Architecture and Directory Organization", level=2)
    add_body_p(
        doc,
        "The project is structured according to modular software engineering standards, separating data access, machine learning modeling, and web presentation into decoupled tiers. Below is the complete directory layout:"
    )
    add_code_block(doc, """c:\\Users\\Shubham\\NoSQLProject\\
|-- app.py                     # Flask web application entry point & routing
|-- config.py                  # Central configuration, schema constants, feature lists
|-- split_mongodb_data.py      # Automated 70/30 stratified data splitting script
|-- requirements.txt           # Python dependency specifications
|-- models/
|   |-- churn_model.joblib     # Serialized Scikit-learn Pipeline artifact
|-- reports/
|   |-- metrics.json           # Comprehensive evaluation metrics & confusion matrix
|-- src/
|   |-- __init__.py            # Python package initialization
|   |-- database.py            # DatabaseManager singleton, PyMongo connection & persistence
|   |-- data_exploration.py    # Schema inspection & exploratory data analysis routines
|   |-- train_model.py         # ML Pipeline construction, L-BFGS training & evaluation
|   |-- predict.py             # ModelPredictor singleton, validation & BSON logging
|   |-- evaluation.py          # Metric loading, confusion matrix calculation & explanation
|-- templates/
|   |-- base.html              # Jinja2 master template with modern layout
|   |-- index.html             # Dashboard with live MongoDB statistics & architecture
|   |-- predict.html           # Interactive form with 1-click sample presets & result meter
|   |-- history.html           # Real-time tabular view of MongoDB prediction records
|   |-- evaluation.html        # Performance metrics, confusion matrix & viva guide
|-- static/
|   |-- css/
|       |-- style.css          # Responsive styling (colors, grid layout, animations)""")

    add_styled_heading(doc, "6.2 Complete Code Listing 1: config.py", level=2)
    add_body_p(
        doc,
        "The config.py module provides centralized parameterization across database, file paths, feature columns, and UI form metadata:"
    )
    add_code_block(doc, """import os

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# MongoDB Configuration
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DATABASE_NAME = "customerChurnDB"

# MongoDB Collection Names
COLLECTIONS = {
    "train": "customers_train_split",
    "test": "customers_test_split",
    "raw_train": "customers_train",
    "raw_test": "customers_test",
    "train_split": "customers_train_split",
    "test_split": "customers_test_split",
    "predictions": "churn_predictions"
}

# Machine Learning Artifact Paths
MODELS_DIR = os.path.join(BASE_DIR, "models")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
MODEL_PATH = os.path.join(MODELS_DIR, "churn_model.joblib")
METRICS_PATH = os.path.join(REPORTS_DIR, "metrics.json")

# Dataset Feature Definitions (inspected from customerChurnDB)
TARGET_COLUMN = "Churn"
IDENTIFIER_COLUMNS = ["_id", "CustomerID"]

NUMERICAL_FEATURES = [
    "Age",
    "Tenure",
    "Usage Frequency",
    "Support Calls",
    "Payment Delay",
    "Total Spend",
    "Last Interaction"
]

CATEGORICAL_FEATURES = [
    "Gender",
    "Subscription Type",
    "Contract Length"
]

ALL_FEATURE_COLUMNS = NUMERICAL_FEATURES + CATEGORICAL_FEATURES

# Dropdown options matching the actual MongoDB values
CATEGORICAL_OPTIONS = {
    "Gender": ["Female", "Male"],
    "Subscription Type": ["Basic", "Standard", "Premium"],
    "Contract Length": ["Monthly", "Quarterly", "Annual"]
}

FLASK_PORT = 5000
FLASK_DEBUG = True
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "customer-churn-nosql-secret-key-2026")""")

    add_styled_heading(doc, "6.3 Complete Code Listing 2: split_mongodb_data.py", level=2)
    add_body_p(
        doc,
        "The split_mongodb_data.py script performs a clean 70/30 stratified split directly on the customers_train collection and persists the resulting subsets into customers_train_split and customers_test_split:"
    )
    add_code_block(doc, """import sys, os, time
import pandas as pd
from pymongo import MongoClient
from sklearn.model_selection import train_test_split
import config

SOURCE_COLLECTION = "customers_train"
TRAIN_SPLIT_COLLECTION = "customers_train_split"
TEST_SPLIT_COLLECTION = "customers_test_split"

def split_and_save_data(mongo_uri=config.MONGO_URI, db_name=config.DATABASE_NAME, test_size=0.30):
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=4000)
    db = client[db_name]
    
    # 1. Fetch raw training records
    col_raw = db[SOURCE_COLLECTION]
    cursor = col_raw.find({config.TARGET_COLUMN: {"$ne": None}}, {"_id": 0})
    df = pd.DataFrame(list(cursor))
    print(f"Loaded {len(df):,} valid records from {SOURCE_COLLECTION}")
    
    # 2. Stratified 70/30 train/test split
    train_df, test_df = train_test_split(
        df, test_size=test_size, random_state=42, stratify=df[config.TARGET_COLUMN]
    )
    
    # 3. Clear target split collections
    col_train = db[TRAIN_SPLIT_COLLECTION]
    col_test = db[TEST_SPLIT_COLLECTION]
    col_train.drop()
    col_test.drop()
    
    # 4. Batch insert into MongoDB collections
    batch_size = 50000
    train_records = train_df.to_dict(orient="records")
    for i in range(0, len(train_records), batch_size):
        col_train.insert_many(train_records[i:i + batch_size])
        
    test_records = test_df.to_dict(orient="records")
    for i in range(0, len(test_records), batch_size):
        col_test.insert_many(test_records[i:i + batch_size])
        
    print(f"SUCCESS: Inserted {len(train_df):,} to {TRAIN_SPLIT_COLLECTION} and {len(test_df):,} to {TEST_SPLIT_COLLECTION}")

if __name__ == "__main__":
    split_and_save_data()""")

    add_styled_heading(doc, "6.4 Complete Code Listing 3: src/database.py", level=2)
    add_body_p(
        doc,
        "The src/database.py module implements the DatabaseManager singleton, managing connection pools, count queries, DataFrame conversions, and prediction persistence:"
    )
    add_code_block(doc, """import sys, os
from datetime import datetime, timezone
import pandas as pd
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import config

class DatabaseManager:
    def __init__(self, uri=None, db_name=None):
        self.uri = uri or config.MONGO_URI
        self.db_name = db_name or config.DATABASE_NAME
        self._client = None

    def get_client(self):
        if self._client is None:
            self._client = MongoClient(self.uri, serverSelectionTimeoutMS=4000, connectTimeoutMS=4000)
        return self._client

    def get_db(self):
        return self.get_client()[self.db_name]

    def test_connection(self):
        try:
            client = self.get_client()
            client.admin.command('ping')
            return True, "Successfully connected to MongoDB."
        except Exception as err:
            return False, f"Could not connect to MongoDB: {str(err)}"

    def get_dashboard_counts(self):
        connected, msg = self.test_connection()
        if not connected:
            return {"connected": False, "error": msg, "train_count": 0, "test_count": 0, "predictions_count": 0}
        try:
            db = self.get_db()
            return {
                "connected": True,
                "error": None,
                "train_count": db[config.COLLECTIONS.get("raw_train", "customers_train")].estimated_document_count(),
                "test_count": db[config.COLLECTIONS.get("raw_test", "customers_test")].estimated_document_count(),
                "predictions_count": db[config.COLLECTIONS["predictions"]].count_documents({}),
                "train_split_count": db[config.COLLECTIONS.get("train", "customers_train_split")].estimated_document_count(),
                "test_split_count": db[config.COLLECTIONS.get("test", "customers_test_split")].estimated_document_count()
            }
        except Exception as err:
            return {"connected": False, "error": str(err), "train_count": 0, "test_count": 0, "predictions_count": 0}

    def load_collection_as_dataframe(self, collection_name, limit=None, drop_missing_target=True):
        db = self.get_db()
        col = db[collection_name]
        query = {config.TARGET_COLUMN: {"$ne": None}} if drop_missing_target else {}
        cursor = col.find(query, {"_id": 0})
        if limit and limit > 0:
            cursor = cursor.limit(limit)
        return pd.DataFrame(list(cursor))

    def get_train_dataframe(self, collection_name=None, limit=None):
        target = collection_name or config.COLLECTIONS.get("train", "customers_train_split")
        return self.load_collection_as_dataframe(target, limit=limit, drop_missing_target=True)

    def get_test_dataframe(self, collection_name=None, limit=None):
        target = collection_name or config.COLLECTIONS.get("test", "customers_test_split")
        return self.load_collection_as_dataframe(target, limit=limit, drop_missing_target=False)

    def save_prediction(self, customer_input, prediction_code, prediction_label, probability):
        db = self.get_db()
        col = db[config.COLLECTIONS["predictions"]]
        doc = {
            "timestamp": datetime.now(timezone.utc),
            "formatted_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "customer_features": customer_input,
            "prediction_code": int(prediction_code),
            "prediction_label": prediction_label,
            "churn_probability": float(probability.get("churn", 0.0)),
            "loyal_probability": float(probability.get("loyal", 0.0)),
            "model_used": "Logistic Regression with Pipeline Preprocessing"
        }
        res = col.insert_one(doc)
        return str(res.inserted_id)

    def get_prediction_history(self, limit=100):
        try:
            db = self.get_db()
            col = db[config.COLLECTIONS["predictions"]]
            cursor = col.find().sort("timestamp", -1).limit(limit)
            records = []
            for doc in cursor:
                doc["_id"] = str(doc["_id"])
                records.append(doc)
            return records
        except Exception:
            return []

db_manager = DatabaseManager()""")

    add_styled_heading(doc, "6.5 Complete Code Listing 4: src/train_model.py", level=2)
    add_body_p(
        doc,
        "The src/train_model.py module constructs the Scikit-learn Pipeline, trains Logistic Regression with balanced class weights, evaluates on the unseen test split, and writes serialized artifacts:"
    )
    add_code_block(doc, """import sys, os, json, time
import joblib, pandas as pd, numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, roc_auc_score, confusion_matrix, classification_report)
import config
from src.database import db_manager

def build_pipeline():
    num_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    cat_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])
    preprocessor = ColumnTransformer(transformers=[
        ('num', num_pipeline, config.NUMERICAL_FEATURES),
        ('cat', cat_pipeline, config.CATEGORICAL_FEATURES)
    ])
    model_pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', LogisticRegression(
            max_iter=1000, class_weight='balanced', random_state=42, solver='lbfgs'
        ))
    ])
    return model_pipeline

def compute_metrics(y_true, y_pred, y_proba=None):
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, zero_division=0)
    rec = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    cm = confusion_matrix(y_true, y_pred).tolist()
    roc_auc = float(roc_auc_score(y_true, y_proba)) if y_proba is not None else None
    return {
        "accuracy": round(float(acc), 4), "precision": round(float(prec), 4),
        "recall": round(float(rec), 4), "f1_score": round(float(f1), 4),
        "roc_auc": round(float(roc_auc), 4) if roc_auc is not None else None,
        "confusion_matrix": cm, "tn": cm[0][0], "fp": cm[0][1], "fn": cm[1][0], "tp": cm[1][1]
    }

def train_and_evaluate(sample_limit=None):
    print("Loading training data from customers_train_split...")
    train_df = db_manager.get_train_dataframe(collection_name=config.COLLECTIONS["train"], limit=sample_limit)
    X_train = train_df[config.ALL_FEATURE_COLUMNS]
    y_train = train_df[config.TARGET_COLUMN].astype(int)

    pipeline = build_pipeline()
    fit_start = time.time()
    pipeline.fit(X_train, y_train)
    fit_time = time.time() - fit_start
    print(f"Model fitted on {len(X_train):,} training records in {fit_time:.2f}s")

    print("Loading test data from customers_test_split...")
    test_df = db_manager.get_test_dataframe(collection_name=config.COLLECTIONS["test"], limit=sample_limit)
    X_test = test_df[config.ALL_FEATURE_COLUMNS]
    y_test = test_df[config.TARGET_COLUMN].astype(int)

    test_pred = pipeline.predict(X_test)
    test_proba = pipeline.predict_proba(X_test)[:, 1]
    test_metrics = compute_metrics(y_test, test_pred, test_proba)

    # Save artifacts
    os.makedirs(config.MODELS_DIR, exist_ok=True)
    os.makedirs(config.REPORTS_DIR, exist_ok=True)
    joblib.dump(pipeline, config.MODEL_PATH)
    
    report = {
        "model_name": "Logistic Regression with Scikit-learn Pipeline",
        "algorithm": "Logistic Regression (L-BFGS, Balanced Class Weights)",
        "training_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "training_collection": config.COLLECTIONS["train"],
        "testing_collection": config.COLLECTIONS["test"],
        "training_samples": len(X_train), "test_samples": len(X_test),
        "test_metrics": test_metrics, "training_time_seconds": round(fit_time, 2)
    }
    with open(config.METRICS_PATH, "w") as f:
        json.dump(report, f, indent=4)
    print("Artifacts successfully saved to disk.")

if __name__ == "__main__":
    train_and_evaluate()""")

    add_styled_heading(doc, "6.6 Complete Code Listing 5: src/predict.py", level=2)
    add_body_p(
        doc,
        "The src/predict.py module provides single-record inference, validation against allowable categorical choices, and persistence to MongoDB:"
    )
    add_code_block(doc, """import sys, os, joblib, pandas as pd
import config
from src.database import db_manager

class ModelPredictor:
    def __init__(self, model_path=None):
        self.model_path = model_path or config.MODEL_PATH
        self._model = None

    def is_model_trained(self):
        return os.path.exists(self.model_path)

    def get_model(self):
        if not self.is_model_trained():
            raise FileNotFoundError("Model file not found. Train model first.")
        if self._model is None:
            self._model = joblib.load(self.model_path)
        return self._model

    def validate_and_format_input(self, input_data):
        cleaned_data = {}
        for num_feat in config.NUMERICAL_FEATURES:
            val = input_data.get(num_feat)
            if val is None or str(val).strip() == "":
                raise ValueError(f"Missing required numerical feature: '{num_feat}'")
            cleaned_data[num_feat] = float(val)
        for cat_feat in config.CATEGORICAL_FEATURES:
            val = input_data.get(cat_feat)
            if not val or str(val).strip() == "":
                raise ValueError(f"Missing required categorical feature: '{cat_feat}'")
            cleaned_data[cat_feat] = str(val).strip()
        return cleaned_data

    def predict(self, raw_input_data, save_to_db=True):
        model = self.get_model()
        cleaned_input = self.validate_and_format_input(raw_input_data)
        input_df = pd.DataFrame([cleaned_input], columns=config.ALL_FEATURE_COLUMNS)

        prediction_code = int(model.predict(input_df)[0])
        probabilities = model.predict_proba(input_df)[0]
        classes = list(model.classes_)
        churn_idx = classes.index(1) if 1 in classes else 1
        loyal_idx = classes.index(0) if 0 in classes else 0

        churn_pct = round(float(probabilities[churn_idx]) * 100, 2)
        loyal_pct = round(float(probabilities[loyal_idx]) * 100, 2)
        prediction_label = "Likely to Churn" if prediction_code == 1 else "Unlikely to Churn"
        risk_level = "High Churn Risk" if churn_pct >= 75.0 else ("Moderate Churn Risk" if prediction_code == 1 else "Loyal Customer (Low Risk)")

        saved_id = None
        if save_to_db:
            try:
                saved_id = db_manager.save_prediction(
                    customer_input=cleaned_input, prediction_code=prediction_code,
                    prediction_label=prediction_label, probability={"churn": churn_pct, "loyal": loyal_pct}
                )
            except Exception as err:
                print(f"Warning: Failed to save prediction to MongoDB: {err}")

        return {
            "prediction_code": prediction_code, "prediction_label": prediction_label,
            "churn_probability": churn_pct, "loyal_probability": loyal_pct,
            "risk_level": risk_level, "saved_id": saved_id, "inputs": cleaned_input
        }

predictor = ModelPredictor()""")

    add_styled_heading(doc, "6.7 Complete Code Listing 6: app.py (Flask Web Application)", level=2)
    add_body_p(
        doc,
        "The app.py file initializes the Flask application, manages routes for dashboard statistics, form submission, inference logging, and history rendering:"
    )
    add_code_block(doc, """import sys, os
from flask import Flask, render_template, request, flash, redirect, url_for
import config
from src.database import db_manager
from src.predict import predictor
from src.evaluation import get_evaluation_data

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = config.FLASK_SECRET_KEY

    if predictor.is_model_trained():
        try:
            predictor.get_model()
        except Exception:
            pass

    @app.route("/")
    def index():
        counts = db_manager.get_dashboard_counts()
        return render_template("index.html", active_page="home", stats=counts, model_trained=predictor.is_model_trained())

    @app.route("/predict", methods=["GET", "POST"])
    def predict_page():
        result = None
        form_data = None
        if request.method == "POST":
            try:
                form_data = request.form.to_dict()
                result = predictor.predict(form_data, save_to_db=True)
                flash(f"Prediction completed! Result: {result['prediction_label']} ({result['churn_probability']}%). Saved to MongoDB.", "success")
            except Exception as err:
                flash(f"Prediction Error: {str(err)}", "danger")
        return render_template("predict.html", active_page="predict", result=result, form_data=form_data, model_trained=predictor.is_model_trained())

    @app.route("/history")
    def history_page():
        history_records = db_manager.get_prediction_history(limit=100)
        return render_template("history.html", active_page="history", history=history_records, total_count=len(history_records))

    @app.route("/evaluation")
    def evaluation_page():
        data = get_evaluation_data()
        return render_template("evaluation.html", active_page="evaluation", **data)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=config.FLASK_PORT, debug=config.FLASK_DEBUG)""")

    add_styled_heading(doc, "6.8 Structured Walkthrough of Live Web Application Screenshots", level=2)
    add_body_p(
        doc,
        "Below are the actual high-resolution screenshots captured directly from the running web application, documenting the interface, input mechanisms, real-time probabilistic classification outputs, history logs, and statistical evaluation metrics:"
    )

    # Figure 6.1
    add_styled_heading(doc, "Figure 6.1: Live Web Application Dashboard Interface (Microsoft Edge)", level=3)
    add_body_p(doc, "Live screenshot of the application running in Microsoft Edge on localhost:5000, displaying connected MongoDB status and collection document badges across all 505,000+ customer records:")
    add_styled_image(
        doc,
        os.path.join(SCREENSHOTS_DIR, "ui_01_dashboard_edge.png"),
        "Figure 6.1: Live Web Application Dashboard Interface (Microsoft Edge running on http://127.0.0.1:5000/)",
        width_inches=6.0
    )

    # Figure 6.2
    add_styled_heading(doc, "Figure 6.2: Interactive Customer Churn Prediction Form (Microsoft Edge)", level=3)
    add_body_p(doc, "Screenshot of the prediction input form displaying numerical and categorical feature inputs alongside the 1-click testing presets ('Fill Loyal Customer Sample' and 'Fill High Churn Risk Sample'):")
    add_styled_image(
        doc,
        os.path.join(SCREENSHOTS_DIR, "ui_02_predict_form_edge.png"),
        "Figure 6.2: Interactive Customer Churn Prediction Input Form (Microsoft Edge running on http://127.0.0.1:5000/predict)",
        width_inches=6.0
    )

    # Figure 6.3
    add_styled_heading(doc, "Figure 6.3: Real-Time Inference Output - High Churn Risk (Microsoft Edge)", level=3)
    add_body_p(doc, "Live inference output for an at-risk customer profile (payment delay, monthly contract, high support calls) displaying 100% Churn Risk, probability meter, and MongoDB ObjectId persistence confirmation:")
    add_styled_image(
        doc,
        os.path.join(SCREENSHOTS_DIR, "ui_03_churn_result_edge.png"),
        "Figure 6.3: Real-Time Inference Output for High Churn Risk Customer (100.0% Churn Probability)",
        width_inches=6.0
    )

    # Figure 6.4
    add_styled_heading(doc, "Figure 6.4: Real-Time Inference Output - Loyal Customer Profile (Microsoft Edge)", level=3)
    add_body_p(doc, "Live inference output for a satisfied subscriber (annual contract, zero payment delays, long tenure) resulting in 'Unlikely to Churn' (0.0% Churn Risk, 100.0% Loyal Probability):")
    add_styled_image(
        doc,
        os.path.join(SCREENSHOTS_DIR, "ui_04_loyal_result_edge.png"),
        "Figure 6.4: Real-Time Inference Output for Loyal Customer Profile (0.0% Churn Probability)",
        width_inches=6.0
    )

    # Figure 6.5
    add_styled_heading(doc, "Figure 6.5: Live MongoDB Prediction History Auditing Table (Microsoft Edge)", level=3)
    add_body_p(doc, "Tabular history view dynamically querying MongoDB's churn_predictions collection, displaying customer profiles, timestamps, prediction labels, confidence scores, and BSON document ObjectIds:")
    add_styled_image(
        doc,
        os.path.join(SCREENSHOTS_DIR, "ui_05_history_edge.png"),
        "Figure 6.5: Real-Time Prediction History Table Querying MongoDB churn_predictions Collection",
        width_inches=6.0
    )

    # Figure 6.6
    add_styled_heading(doc, "Figure 6.6: Model Evaluation Dashboard & Confusion Matrix (Microsoft Edge)", level=3)
    add_body_p(doc, "Live evaluation interface displaying verified benchmark metrics (Accuracy 89.51%, Precision 93.99%, Recall 87.06%, ROC-AUC 0.9596), the 2x2 Confusion Matrix, and metric explanations:")
    add_styled_image(
        doc,
        os.path.join(SCREENSHOTS_DIR, "ui_06_evaluation_edge.png"),
        "Figure 6.6: Model Evaluation Dashboard Displaying Metrics and 2x2 Confusion Matrix",
        width_inches=6.0
    )

    doc.add_page_break()

def build_chapter_7(doc):
    add_styled_heading(doc, "CHAPTER 7: EXPERIMENTAL RESULTS AND PERFORMANCE DISCUSSION", level=1)
    
    add_styled_heading(doc, "7.1 Terminal Execution Logs and Verification", level=2)
    add_body_p(
        doc,
        "The end-to-end system was executed and verified on a live local MongoDB Community Server. Below are the authentic Windows 11 PowerShell terminal screenshots captured during database connection testing, collection enumeration, and stratified data partitioning:"
    )
    add_styled_image(
        doc,
        os.path.join(SCREENSHOTS_DIR, "terminal_01_mongo_connection_exact.png"),
        "Figure 7.1: Windows PowerShell - MongoDB Database Connection & Collection Enumeration Verification",
        width_inches=6.0
    )
    add_styled_image(
        doc,
        os.path.join(SCREENSHOTS_DIR, "terminal_02_data_splitting_exact.png"),
        "Figure 7.2: Windows PowerShell - Stratified 70/30 Data Partitioning Execution Output",
        width_inches=6.0
    )

    add_styled_heading(doc, "7.2 Model Training and Test Evaluation Output", level=2)
    add_body_p(
        doc,
        "Below is the exact Windows PowerShell console output generated during execution of src/train_model.py, demonstrating rapid training and unbiased evaluation on the independent test set in 2.87 seconds:"
    )
    add_styled_image(
        doc,
        os.path.join(SCREENSHOTS_DIR, "terminal_03_model_training_exact.png"),
        "Figure 7.3: Windows PowerShell - Scikit-learn Pipeline Fitting & Training Execution Output",
        width_inches=6.0
    )

    add_styled_heading(doc, "7.3 Authentic Performance Benchmark Metrics", level=2)
    add_body_p(
        doc,
        "The model's classification performance on the independent test partition (132,250 records) is captured in the terminal log and summarized in the table below:"
    )
    add_styled_image(
        doc,
        os.path.join(SCREENSHOTS_DIR, "terminal_04_model_evaluation_exact.png"),
        "Figure 7.4: Windows PowerShell - Unbiased Test Set Evaluation Metrics & Confusion Matrix Output",
        width_inches=6.0
    )

    metrics_data = [
        ["Overall Accuracy", "89.51%", "Proportion of total predictions correctly classified."],
        ["Precision (Positive Class)", "93.99%", "Out of all predicted churners, 93.99% actually churned."],
        ["Recall (Sensitivity)", "87.06%", "Out of all actual churners, the model successfully detected 87.06%."],
        ["F1-Score", "90.39%", "Harmonic mean of precision and recall; reflects balanced accuracy."],
        ["ROC-AUC Score", "0.9596", "Discriminative ability across all threshold cutoffs (Near perfect separation)."],
        ["Model Training Duration", "2.87 seconds", "Ultra-fast convergence across 308,582 records."],
        ["Inference Latency", "< 15 milliseconds", "Instantaneous prediction response for web users."]
    ]
    add_styled_table(
        doc,
        ["Performance Metric", "Observed Value", "Technical & Business Interpretation"],
        metrics_data,
        col_widths=[1.8, 1.3, 3.4]
    )

    add_styled_heading(doc, "7.4 Confusion Matrix Analysis", level=2)
    add_body_p(
        doc,
        "The 2x2 contingency confusion matrix on the 132,250 independent test records is detailed below:"
    )

    cm_data = [
        ["Actual Loyal (0)", "True Negatives (TN): 53,078", "False Positives (FP): 4,172"],
        ["Actual Churn (1)", "False Negatives (FN): 9,706", "True Positives (TP): 65,294"]
    ]
    add_styled_table(
        doc,
        ["Ground Truth \\ Predicted", "Predicted Loyal (0)", "Predicted Churn (1)"],
        cm_data,
        col_widths=[2.1, 2.2, 2.2]
    )

    add_styled_heading(doc, "7.5 Business Interpretation of False Positives vs. False Negatives", level=2)
    add_body_p(
        doc,
        "In customer retention economics, classification errors carry asymmetric operational costs:"
    )
    add_bullet_p(
        doc,
        "Occurs when a loyal customer is incorrectly classified as at-risk. The business cost is minimal—sending a promotional discount or loyalty voucher to a loyal customer slightly reduces margin but often reinforces brand loyalty.",
        bold_prefix="• False Positives (FP = 4,172 / 3.15%): "
    )
    add_bullet_p(
        doc,
        "Occurs when a customer who is about to churn is misclassified as loyal. The business consequence is severe—the enterprise fails to intervene, resulting in the permanent loss of recurring subscription revenue.",
        bold_prefix="• False Negatives (FN = 9,706 / 7.34%): "
    )
    add_body_p(
        doc,
        "With an exceptional Precision of 93.99% and Recall of 87.06%, the model successfully strikes an optimal trade-off, minimizing lost customer revenue while preventing marketing waste."
    )

    add_styled_heading(doc, "7.6 Real-Time MongoDB Persistence Verification", level=2)
    add_body_p(
        doc,
        "During live web application testing, test records were submitted via the Flask UI. Querying MongoDB directly confirmed that documents were inserted atomically into churn_predictions with proper BSON timestamps and probabilities:"
    )
    add_styled_image(
        doc,
        os.path.join(SCREENSHOTS_DIR, "terminal_05_mongo_history_query_exact.png"),
        "Figure 7.5: Windows PowerShell - Verification of Real-Time Prediction Persistence in MongoDB",
        width_inches=6.0
    )

    doc.add_page_break()
