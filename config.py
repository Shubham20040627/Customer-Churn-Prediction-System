import os

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# MongoDB Configuration
# Configurable in one place; supports environment variable override if needed
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

# Metadata for web form rendering, defaults, and validation
FEATURE_METADATA = [
    {
        "name": "Age",
        "label": "Customer Age",
        "type": "number",
        "min": 18,
        "max": 100,
        "step": 1,
        "default": 35,
        "unit": "years",
        "description": "Customer age in years (18-100)"
    },
    {
        "name": "Gender",
        "label": "Gender",
        "type": "select",
        "options": ["Female", "Male"],
        "default": "Female",
        "description": "Customer gender"
    },
    {
        "name": "Tenure",
        "label": "Tenure (Months)",
        "type": "number",
        "min": 1,
        "max": 120,
        "step": 1,
        "default": 24,
        "unit": "months",
        "description": "Duration the customer has been with the service"
    },
    {
        "name": "Usage Frequency",
        "label": "Usage Frequency",
        "type": "number",
        "min": 0,
        "max": 50,
        "step": 1,
        "default": 14,
        "unit": "times/month",
        "description": "Average service usage frequency per month"
    },
    {
        "name": "Support Calls",
        "label": "Support Calls",
        "type": "number",
        "min": 0,
        "max": 25,
        "step": 1,
        "default": 2,
        "unit": "calls",
        "description": "Number of customer support inquiries made"
    },
    {
        "name": "Payment Delay",
        "label": "Payment Delay (Days)",
        "type": "number",
        "min": 0,
        "max": 60,
        "step": 1,
        "default": 5,
        "unit": "days",
        "description": "Average delay in paying monthly bills"
    },
    {
        "name": "Subscription Type",
        "label": "Subscription Tier",
        "type": "select",
        "options": ["Basic", "Standard", "Premium"],
        "default": "Standard",
        "description": "Subscribed service tier"
    },
    {
        "name": "Contract Length",
        "label": "Contract Length",
        "type": "select",
        "options": ["Monthly", "Quarterly", "Annual"],
        "default": "Annual",
        "description": "Billing agreement contract duration"
    },
    {
        "name": "Total Spend",
        "label": "Total Spend ($)",
        "type": "number",
        "min": 10,
        "max": 5000,
        "step": 1,
        "default": 650,
        "unit": "USD",
        "description": "Cumulative amount spent by customer ($)"
    },
    {
        "name": "Last Interaction",
        "label": "Last Interaction (Days Ago)",
        "type": "number",
        "min": 0,
        "max": 60,
        "step": 1,
        "default": 10,
        "unit": "days ago",
        "description": "Days since the customer last interacted with the service"
    }
]

# Flask App Configuration
FLASK_SECRET_KEY = os.getenv("SECRET_KEY", "customer-churn-nosql-secret-key-2026")
FLASK_DEBUG = True
FLASK_PORT = 5000
FLASK_HOST = "127.0.0.1"
