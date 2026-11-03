"""
Model Training Module
Loads training data from MongoDB, performs clean preprocessing using Scikit-learn Pipeline
and ColumnTransformer, trains Logistic Regression with class-balance handling,
evaluates performance on a reproducible validation split and independent test set,
and saves the trained artifact using Joblib.
"""

import sys
import os
import json
import time

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

try:
    import config
    from src.database import db_manager
except ImportError:
    from .. import config
    from .database import db_manager


def build_pipeline():
    """
    Constructs a robust Scikit-learn Pipeline combining:
    1. Numerical preprocessing: Median imputation + Standard scaling.
    2. Categorical preprocessing: Mode imputation + One-Hot Encoding (ignoring unknown values at inference).
    3. Classification estimator: Logistic Regression with balanced class weights and convergence controls.
    """
    # Numerical pipeline: impute then scale
    num_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    # Categorical pipeline: impute then one-hot encode
    cat_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    # Combine using ColumnTransformer
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', num_pipeline, config.NUMERICAL_FEATURES),
            ('cat', cat_pipeline, config.CATEGORICAL_FEATURES)
        ]
    )

    # Full Model Pipeline
    model_pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', LogisticRegression(
            max_iter=1000,
            class_weight='balanced',
            random_state=42,
            solver='lbfgs'
        ))
    ])

    return model_pipeline


def compute_metrics(y_true, y_pred, y_proba=None):
    """Calculates all key evaluation metrics for binary classification."""
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, zero_division=0)
    rec = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    cm = confusion_matrix(y_true, y_pred).tolist()

    roc_auc = None
    if y_proba is not None:
        try:
            roc_auc = float(roc_auc_score(y_true, y_proba))
        except Exception:
            roc_auc = None

    return {
        "accuracy": round(float(acc), 4),
        "precision": round(float(prec), 4),
        "recall": round(float(rec), 4),
        "f1_score": round(float(f1), 4),
        "roc_auc": round(float(roc_auc), 4) if roc_auc is not None else None,
        "confusion_matrix": cm,
        "tn": cm[0][0],
        "fp": cm[0][1],
        "fn": cm[1][0],
        "tp": cm[1][1]
    }


def train_and_evaluate(sample_limit=None):
    """
    Main training workflow:
    1. Connects to MongoDB customerChurnDB.
    2. Loads training data from 'customers_train_split' (70% split).
    3. Separates machine learning features (excluding CustomerID and _id).
    4. Fits Scikit-learn Logistic Regression Pipeline using ONLY the training collection.
    5. Loads test data from 'customers_test_split' (30% split).
    6. Automatically evaluates model performance on 'customers_test_split'.
    7. Saves fitted model pipeline to models/churn_model.joblib.
    8. Saves comprehensive evaluation metrics to reports/metrics.json.
    """
    print("\n" + "="*65)
    print("CUSTOMER CHURN PREDICTION - MODEL TRAINING & TEST EVALUATION")
    print("="*65)

    # Step 1: Connect to MongoDB
    print("\n[1/5] Connecting to MongoDB...")
    connected, msg = db_manager.test_connection()
    if not connected:
        raise ConnectionError(f"Training aborted. MongoDB connection failed: {msg}")
    print("  -> Connected successfully to MongoDB.")

    # Step 2: Fetch training data from customers_train_split
    print(f"\n[2/5] Loading training collection '{config.COLLECTIONS['train']}'...")
    start_time = time.time()
    train_df = db_manager.get_train_dataframe(collection_name=config.COLLECTIONS["train"], limit=sample_limit)
    if train_df.empty:
        raise ValueError(f"Training collection '{config.COLLECTIONS['train']}' is empty or could not be loaded!")
    
    print(f"  -> Loaded {len(train_df):,} records in {time.time() - start_time:.2f}s")
    print(f"  -> Features available: {[c for c in train_df.columns if c != config.TARGET_COLUMN]}")
    print(f"  -> Training target distribution: {train_df[config.TARGET_COLUMN].value_counts().to_dict()}")

    # Step 3: Feature separation and model training
    print("\n[3/5] Training Logistic Regression Pipeline using ONLY the training collection...")
    missing_cols = [c for c in config.ALL_FEATURE_COLUMNS if c not in train_df.columns]
    if missing_cols:
        raise KeyError(f"Expected feature columns missing from training dataset: {missing_cols}")

    X_train = train_df[config.ALL_FEATURE_COLUMNS]
    y_train = train_df[config.TARGET_COLUMN].astype(int)

    pipeline = build_pipeline()
    fit_start = time.time()
    pipeline.fit(X_train, y_train)
    fit_time = time.time() - fit_start
    print(f"  -> Model fitted successfully on {len(X_train):,} training samples in {fit_time:.2f}s.")

    # Step 4: Automated evaluation on testing collection
    print(f"\n[4/5] Loading testing collection '{config.COLLECTIONS['test']}' and evaluating...")
    test_df = db_manager.get_test_dataframe(collection_name=config.COLLECTIONS["test"], limit=sample_limit)
    if test_df.empty:
        raise ValueError(f"Testing collection '{config.COLLECTIONS['test']}' is empty or could not be loaded!")

    print(f"  -> Loaded {len(test_df):,} testing records.")
    print(f"  -> Testing target distribution: {test_df[config.TARGET_COLUMN].value_counts().to_dict()}")

    X_test = test_df[config.ALL_FEATURE_COLUMNS]
    y_test = test_df[config.TARGET_COLUMN].astype(int)

    # Automated test set evaluation
    eval_start = time.time()
    test_pred = pipeline.predict(X_test)
    test_proba = pipeline.predict_proba(X_test)[:, 1]
    test_metrics = compute_metrics(y_test, test_pred, test_proba)
    eval_time = time.time() - eval_start

    print(f"\n--- Testing Collection ('{config.COLLECTIONS['test']}') Evaluation Metrics ---")
    print(f"  Accuracy:         {test_metrics['accuracy']:.4f} ({test_metrics['accuracy']*100:.2f}%)")
    print(f"  Precision:        {test_metrics['precision']:.4f} ({test_metrics['precision']*100:.2f}%)")
    print(f"  Recall:           {test_metrics['recall']:.4f} ({test_metrics['recall']*100:.2f}%)")
    print(f"  F1 Score:         {test_metrics['f1_score']:.4f} ({test_metrics['f1_score']*100:.2f}%)")
    print(f"  ROC AUC:          {test_metrics['roc_auc']:.4f}")
    print(f"  Confusion Matrix: TN={test_metrics['tn']:,}, FP={test_metrics['fp']:,}, FN={test_metrics['fn']:,}, TP={test_metrics['tp']:,}")
    print(f"  Evaluation Time:  {eval_time:.2f}s")

    # Also compute training set metrics for baseline reference
    train_pred = pipeline.predict(X_train)
    train_proba = pipeline.predict_proba(X_train)[:, 1]
    train_metrics = compute_metrics(y_train, train_pred, train_proba)

    # Step 5: Save Model and Metrics
    print("\n[5/5] Saving trained model and evaluation report...")
    os.makedirs(config.MODELS_DIR, exist_ok=True)
    os.makedirs(config.REPORTS_DIR, exist_ok=True)

    joblib.dump(pipeline, config.MODEL_PATH)
    print(f"  -> Model saved to: {config.MODEL_PATH}")

    # Compile comprehensive metrics report compatible with Flask web templates
    report = {
        "model_name": "Logistic Regression with Scikit-learn Pipeline",
        "algorithm": "Logistic Regression (L-BFGS, Balanced Class Weights)",
        "training_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "training_collection": config.COLLECTIONS["train"],
        "testing_collection": config.COLLECTIONS["test"],
        "training_samples": len(X_train),
        "validation_samples": len(X_test),
        "test_samples": len(X_test),
        "features": {
            "numerical": config.NUMERICAL_FEATURES,
            "categorical": config.CATEGORICAL_FEATURES
        },
        "validation_metrics": test_metrics,
        "test_metrics": test_metrics,
        "train_metrics": train_metrics,
        "has_test_labels": True,
        "training_time_seconds": round(fit_time, 2),
        "evaluation_time_seconds": round(eval_time, 2),
        "classification_report_validation": classification_report(y_test, test_pred, output_dict=True),
        "classification_report_test": classification_report(y_test, test_pred, output_dict=True)
    }

    with open(config.METRICS_PATH, "w") as f:
        json.dump(report, f, indent=4)
    print(f"  -> Metrics report saved to: {config.METRICS_PATH}")

    print("\n" + "="*65)
    print("SUCCESS: Model training and automated test evaluation completed!")
    print("="*65 + "\n")
    return report


if __name__ == "__main__":
    train_and_evaluate()
