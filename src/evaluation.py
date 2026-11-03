"""
Model Evaluation and Metrics Reporting Module
Loads saved evaluation metrics, computes metrics dynamically if needed,
and provides clear explanations for each metric suitable for project demonstration.
"""

import sys
import os
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import config
    from src.database import db_manager
except ImportError:
    from .. import config
    from .database import db_manager


METRIC_EXPLANATIONS = {
    "accuracy": {
        "title": "Accuracy",
        "description": "The proportion of total predictions that the model got correct (both churners and loyal customers).",
        "formula": "Accuracy = (True Positives + True Negatives) / Total Predictions",
        "interpretation": "High accuracy indicates general classification success across both classes."
    },
    "precision": {
        "title": "Precision (Positive Predictive Value)",
        "description": "Out of all customers the model flagged as 'Likely to Churn', the percentage that actually churned.",
        "formula": "Precision = True Positives / (True Positives + False Positives)",
        "interpretation": "High precision avoids wasting retention marketing budgets on false alarms."
    },
    "recall": {
        "title": "Recall (Sensitivity / True Positive Rate)",
        "description": "Out of all customers who actually churned, the percentage that our model successfully caught.",
        "formula": "Recall = True Positives / (True Positives + False Negatives)",
        "interpretation": "High recall ensures you do not miss at-risk customers who need immediate intervention."
    },
    "f1_score": {
        "title": "F1-Score",
        "description": "The harmonic mean of Precision and Recall, balancing false positives and false negatives.",
        "formula": "F1-Score = 2 * (Precision * Recall) / (Precision + Recall)",
        "interpretation": "Particularly valuable in churn problems where class distributions can be skewed."
    },
    "roc_auc": {
        "title": "ROC-AUC Score",
        "description": "Area Under the Receiver Operating Characteristic curve. Measures how well the model separates churners from loyal customers across all probability thresholds.",
        "formula": "Ranges from 0.5 (random guess) to 1.0 (perfect classification)",
        "interpretation": "An ROC-AUC above 0.85 indicates strong discriminatory ability."
    },
    "confusion_matrix": {
        "title": "Confusion Matrix",
        "description": "A 2x2 contingency table breaking down True Negatives, False Positives, False Negatives, and True Positives.",
        "formula": "[[TN, FP], [FN, TP]]",
        "interpretation": "Reveals exactly where the model makes errors versus where it succeeds."
    }
}


def evaluate_model_on_test_collection(model_path=None, sample_limit=None):
    """
    Evaluates the saved model pipeline directly on the 'customers_test_split' collection.
    Loads test records from MongoDB, performs inference, computes evaluation metrics,
    and returns the evaluated performance dictionary.
    """
    import joblib
    from sklearn.metrics import (
        accuracy_score,
        precision_score,
        recall_score,
        f1_score,
        roc_auc_score,
        confusion_matrix,
        classification_report
    )

    path = model_path or config.MODEL_PATH
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model artifact not found at '{path}'. Train the model first with 'python src/train_model.py'.")

    print("\n" + "="*65)
    print("CUSTOMER CHURN PREDICTION - TEST COLLECTION EVALUATION")
    print("="*65)
    print(f"Loading model artifact from: {path}")
    model = joblib.load(path)

    test_collection = config.COLLECTIONS.get("test", "customers_test_split")
    print(f"Loading test records from MongoDB collection '{test_collection}'...")
    test_df = db_manager.get_test_dataframe(collection_name=test_collection, limit=sample_limit)
    if test_df.empty:
        raise ValueError(f"Test collection '{test_collection}' is empty or could not be loaded!")

    print(f"  -> Retrieved {len(test_df):,} test records.")

    X_test = test_df[config.ALL_FEATURE_COLUMNS]
    y_test = test_df[config.TARGET_COLUMN].astype(int)

    print("Running automated inference on test records...")
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    acc = float(accuracy_score(y_test, y_pred))
    prec = float(precision_score(y_test, y_pred, zero_division=0))
    rec = float(recall_score(y_test, y_pred, zero_division=0))
    f1 = float(f1_score(y_test, y_pred, zero_division=0))
    roc = float(roc_auc_score(y_test, y_proba))
    cm = confusion_matrix(y_test, y_pred).tolist()

    print("\n" + "-"*65)
    print(f"EVALUATION RESULTS ON '{test_collection}' ({len(test_df):,} SAMPLES)")
    print("-"*65)
    print(f"  Accuracy:         {acc:.4f} ({acc*100:.2f}%)")
    print(f"  Precision:        {prec:.4f} ({prec*100:.2f}%)")
    print(f"  Recall:           {rec:.4f} ({rec*100:.2f}%)")
    print(f"  F1-Score:         {f1:.4f} ({f1*100:.2f}%)")
    print(f"  ROC-AUC Score:    {roc:.4f}")
    print(f"  Confusion Matrix: TN={cm[0][0]:,}, FP={cm[0][1]:,}, FN={cm[1][0]:,}, TP={cm[1][1]:,}")
    print("-"*65)

    return {
        "collection": test_collection,
        "sample_count": len(test_df),
        "accuracy": round(acc, 4),
        "precision": round(prec, 4),
        "recall": round(rec, 4),
        "f1_score": round(f1, 4),
        "roc_auc": round(roc, 4),
        "confusion_matrix": cm,
        "classification_report": classification_report(y_test, y_pred, output_dict=True)
    }


def get_evaluation_data():
    """
    Retrieves evaluation metrics from reports/metrics.json.
    Returns:
        dict: Structured evaluation report, status, and explanations.
    """
    if not os.path.exists(config.METRICS_PATH):
        return {
            "available": False,
            "message": "Evaluation report not found. Please train the model first by running 'python src/train_model.py'.",
            "metrics": None,
            "explanations": METRIC_EXPLANATIONS
        }

    try:
        with open(config.METRICS_PATH, "r") as f:
            metrics_data = json.load(f)

        return {
            "available": True,
            "message": "Model evaluation report loaded successfully.",
            "metrics": metrics_data,
            "explanations": METRIC_EXPLANATIONS
        }
    except Exception as err:
        return {
            "available": False,
            "message": f"Failed to read evaluation metrics file: {str(err)}",
            "metrics": None,
            "explanations": METRIC_EXPLANATIONS
        }


if __name__ == "__main__":
    if os.path.exists(config.MODEL_PATH):
        evaluate_model_on_test_collection()
    else:
        print(f"Model artifact not found at {config.MODEL_PATH}. Checking saved metrics report...")
        data = get_evaluation_data()
        print("Evaluation Data Available:", data["available"])

