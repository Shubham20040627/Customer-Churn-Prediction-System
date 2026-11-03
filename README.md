# Customer Churn Prediction System Using MongoDB, Python, and Logistic Regression

A complete, production-ready college NoSQL project integrating **MongoDB Community Server**, **Python**, **Scikit-learn**, and **Flask**. This system predicts whether a customer is likely to leave a subscription service (churn), explains model performance with real statistical metrics, and persists all inference events directly into a NoSQL collection.

---

## 1. Project Introduction
Customer churn represents the loss of clients or subscribers. Predicting churn enables businesses to take proactive retention actions before customers cancel their contracts. This project demonstrates how a modern NoSQL database (**MongoDB**) integrates with a complete Python machine learning workflow and an interactive web interface.

## 2. Problem Statement
Subscription-based businesses (e.g., telecom, SaaS, streaming services) experience recurring revenue loss when customers churn. Manually identifying at-risk accounts across hundreds of thousands of users is impractical. By leveraging historical behavior, payment delays, contract terms, and customer activity stored in MongoDB, this project predicts individual churn risk and saves all predictions for auditing and analysis.

## 3. Objectives
- **NoSQL Database Integration**: Query and store large datasets (440,000+ records) efficiently using MongoDB and PyMongo.
- **Machine Learning Workflow**: Preprocess data using Scikit-learn Pipelines, prevent data leakage, and train a Logistic Regression classifier.
- **Model Evaluation**: Compute and display authentic performance metrics (Accuracy, Precision, Recall, F1-Score, ROC-AUC, Confusion Matrix).
- **Inference Persistence**: Automatically store every web-based customer prediction into MongoDB's `churn_predictions` collection.
- **Beginner-Friendly Architecture**: Clean, modular code structure using Flask, HTML5, and external CSS without unnecessary heavy frameworks.

---

## 4. Technologies Used
| Technology | Role in Project |
| :--- | :--- |
| **Python 3.10+ / 3.14** | Core programming language for data processing, machine learning, and web backend. |
| **MongoDB Community Server** | Primary NoSQL database hosting training records, test sets, and prediction logs. |
| **MongoDB Compass** | GUI client to visually explore documents, collections, and query results. |
| **PyMongo** | Official Python driver used to connect and interact with MongoDB. |
| **Pandas & NumPy** | Fast data wrangling, DataFrame conversions, and numerical operations. |
| **Scikit-learn** | Feature scaling, One-Hot Encoding, Logistic Regression, and metric evaluations. |
| **Joblib** | Serialization library to save and load the trained ML pipeline without retraining. |
| **Flask** | Lightweight Python web framework serving the dashboard, form, and history routes. |
| **HTML5 & Vanilla CSS** | Clean, responsive user interface with external styling (`static/css/style.css`). |

---

## 5. System Workflow Architecture
```
+-----------------------------------------------------------------------+
|                         MongoDB Database                              |
|                       (customerChurnDB)                               |
|                                                                       |
|  [customers_train]   (440k docs)       [customers_test] (64k docs)    |
+----------+-------------------------------------+----------------------+
           |                                     |
           | PyMongo Query                       | PyMongo Query
           v                                     v
+-----------------------+               +-------------------------------+
|  src/database.py      |               |  src/data_exploration.py      |
|  - Data loading       |               |  - Schema inspection          |
|  - Projection & Clean |               |  - Summary statistics         |
+----------+------------+               +-------------------------------+
           |
           v
+-----------------------------------------------------------------------+
|  src/train_model.py                                                   |
|  1. Split Train & Validation (80/20 Stratified)                       |
|  2. ColumnTransformer (StandardScaler for numerical, OneHot for cat)  |
|  3. Fit Logistic Regression (L-BFGS, Balanced Class Weights)          |
|  4. Evaluate on Validation Split + Independent Test Collection        |
|  5. Save Model Pipeline -> models/churn_model.joblib                  |
|  6. Save Report         -> reports/metrics.json                       |
+-----------------------------------------------------------------------+
                                  |
                                  v
+-----------------------------------------------------------------------+
|  Flask Web Application (app.py)                                       |
|                                                                       |
|  /            -> Dashboard with live MongoDB counts & stats           |
|  /predict     -> Interactive Form -> src/predict.py -> Prediction     |
|  /history     -> Live table querying churn_predictions collection    |
|  /evaluation  -> Authentic accuracy, confusion matrix, metric report |
+----------------------------------+------------------------------------+
                                   |
                                   | Persist Prediction
                                   v
                   +-------------------------------+
                   | MongoDB Collection            |
                   | `churn_predictions`           |
                   | (Input + Result + Probability)|
                   +-------------------------------+
```

---

## 6. MongoDB Database and Collection Design
The database name is **`customerChurnDB`**. It contains three primary collections:

### 1. `customers_train` (Existing Dataset)
Contains historical customer records used to train and validate the classification model.
- **Total Documents**: 440,833
- **Primary Fields**: `CustomerID`, `Age`, `Gender`, `Tenure`, `Usage Frequency`, `Support Calls`, `Payment Delay`, `Subscription Type`, `Contract Length`, `Total Spend`, `Last Interaction`, `Churn` (Target: 0 = Loyal, 1 = Churned).

### 2. `customers_test` (Existing Dataset)
Independent test partition used for unbiased model verification.
- **Total Documents**: 64,374
- **Primary Fields**: Identical schema to training data.

### 3. `churn_predictions` (New Predictions Collection)
Created automatically when users submit predictions through the website.
- **Document Structure**:
```json
{
  "_id": ObjectId("6ac9d4aaca5daedd984aaaf4"),
  "timestamp": ISODate("2026-10-10T06:01:14Z"),
  "formatted_time": "2026-10-10 11:31:14",
  "customer_features": {
    "Age": 45.0,
    "Gender": "Female",
    "Tenure": 48.0,
    "Usage Frequency": 24.0,
    "Support Calls": 1.0,
    "Payment Delay": 0.0,
    "Subscription Type": "Premium",
    "Contract Length": "Annual",
    "Total Spend": 920.0,
    "Last Interaction": 4.0
  },
  "prediction_code": 0,
  "prediction_label": "Unlikely to Churn",
  "churn_probability": 0.7,
  "loyal_probability": 99.3,
  "model_used": "Logistic Regression with Pipeline Preprocessing"
}
```

---

## 7. Machine Learning Algorithm Explanation
### Why Logistic Regression?
Logistic Regression is the foundational statistical machine learning algorithm for binary classification problems:
1. **Probabilistic Output**: It computes a probability $P(Y=1|X) = \frac{1}{1 + e^{-z}}$, allowing us to show confidence percentages (e.g., "78% Churn Probability") rather than just a black-box label.
2. **Interpretability**: The learned coefficients indicate whether a feature (like payment delay or contract type) increases or decreases churn risk.
3. **NoSQL Alignment**: Fast to train, low memory footprint, and highly interpretable.
4. **Handling Imbalance**: We use `class_weight='balanced'` to prevent bias toward the majority class.

---

## 8. Data Preprocessing Steps
All preprocessing steps are bundled inside a Scikit-learn `Pipeline` and `ColumnTransformer` to guarantee **no data leakage**:
1. **Identifier Exclusion**: `_id` and `CustomerID` are excluded from model features.
2. **Missing Value Imputation**:
   - Numerical columns: Replaced with median via `SimpleImputer(strategy='median')`.
   - Categorical columns: Replaced with mode via `SimpleImputer(strategy='most_frequent')`.
3. **Numerical Standardization**: `StandardScaler` standardizes features to zero mean and unit variance ($z = \frac{x - \mu}{\sigma}$).
4. **Categorical Encoding**: `OneHotEncoder(handle_unknown='ignore')` maps categories (`Gender`, `Subscription Type`, `Contract Length`) into binary dummy columns.

---

## 9. Model Evaluation Metrics (Real Calculated Results)
Evaluated on an 80/20 stratified validation holdout from `customers_train`:

| Metric | Score | Business Interpretation |
| :--- | :--- | :--- |
| **Accuracy** | **89.46%** | Proportion of all customer predictions that were completely correct. |
| **Precision** | **93.94%** | Out of all customers flagged as churners, 93.94% actually churned (few false alarms). |
| **Recall** | **87.03%** | Out of all actual churners, 87.03% were successfully caught by the model. |
| **F1-Score** | **90.35%** | Harmonic mean of precision and recall, balancing false alarms against missed churners. |
| **ROC-AUC** | **0.9590** | Area Under ROC Curve; near 1.0 indicates outstanding discriminatory capability. |

### Confusion Matrix (Validation Set: 88,167 Samples)
```
                   Predicted Loyal (0)     Predicted Churn (1)
Actual Loyal (0)   35,359 (TN)             2,808 (FP)
Actual Churn (1)    6,486 (FN)            43,514 (TP)
```

---

## 10. Complete Folder Structure
```
NoSQLProject/
├── app.py                      # Flask web application entry point & routes
├── config.py                   # Centralized configuration (Mongo URI, features, paths)
├── requirements.txt            # Python dependencies
├── README.md                   # Full college project documentation
├── .gitignore                  # Git ignore rules
├── models/
│   ├── .gitkeep
│   └── churn_model.joblib      # Serialized trained model & preprocessing pipeline
├── reports/
│   ├── .gitkeep
│   └── metrics.json            # Real computed evaluation metrics & reports
├── src/
│   ├── __init__.py             # Python package marker
│   ├── database.py             # PyMongo connection, queries, & prediction persistence
│   ├── data_exploration.py     # Terminal EDA and dataset inspection script
│   ├── train_model.py          # Model training, validation split, & Joblib export
│   ├── predict.py              # Single-instance inference & DB logging logic
│   └── evaluation.py           # Evaluation report loader & educational descriptions
├── templates/
│   ├── base.html               # Master layout with navbar, alerts, & footer
│   ├── index.html              # Home dashboard with live MongoDB counters
│   ├── predict.html            # Customer prediction form, sample presets, & result card
│   ├── history.html            # Prediction history table with live MongoDB records
│   ├── evaluation.html         # Evaluation dashboard with confusion matrix & metrics
│   └── error.html              # Friendly troubleshooting & error handling view
└── static/
    └── css/
        └── style.css           # Premium responsive external CSS stylesheet
```

---

## 11. Purpose of Every Major Python File

- **`config.py`**: Contains all configurable variables in a single place (MongoDB connection URI, database name, collection names, feature lists, form defaults). Prevents hardcoding across files.
- **`src/database.py`**: Encapsulates all MongoDB operations. Provides `get_dashboard_counts()` for live statistics, `get_train_dataframe()` for loading data, `save_prediction()` for inserting new predictions into `churn_predictions`, and `get_prediction_history()` for audit trails.
- **`src/data_exploration.py`**: Connects to MongoDB, prints summary statistics, column data types, missing values, and target distributions to the console.
- **`src/train_model.py`**: Builds the `ColumnTransformer` and `Pipeline`, fits Logistic Regression on training records, evaluates performance on validation and independent test splits, and exports `churn_model.joblib` and `metrics.json`.
- **`src/predict.py`**: Caches the trained pipeline in memory so Flask does not reload or retrain on every request. Validates incoming web form fields, generates churn probability, and saves results into MongoDB.
- **`src/evaluation.py`**: Reads `reports/metrics.json` and prepares structured data and educational explanations for the `/evaluation` web route.
- **`app.py`**: Runs the Flask application, wires templates to backend functions, and handles HTTP requests (`/`, `/predict`, `/history`, `/evaluation`).

---

## 12. Prerequisites and Installation Steps

### Prerequisites
1. **Python 3.10+** (Tested and verified on Windows).
2. **MongoDB Community Server** installed and running on port `27017`.
3. **MongoDB Compass** (optional, recommended for viewing collections visually).

### Step-by-Step Windows Terminal Commands

#### Step 1: Open Terminal in Project Directory
```powershell
cd c:\Users\Shubham\NoSQLProject
```

#### Step 2: (Optional) Create & Activate Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### Step 3: Install Required Dependencies
```powershell
pip install -r requirements.txt
```

#### Step 4: Verify MongoDB is Running
```powershell
python -c "from pymongo import MongoClient; print('Databases:', MongoClient('mongodb://localhost:27017/').list_database_names())"
```
*Expected output includes `customerChurnDB`.*

#### Step 5: Explore Dataset Directly from MongoDB
```powershell
python src/data_exploration.py
```

#### Step 6: Train and Evaluate the Model
```powershell
python src/train_model.py
```
*This loads the training data from MongoDB, trains the Logistic Regression pipeline, prints accuracy and confusion matrix, and saves `models/churn_model.joblib` and `reports/metrics.json`.*

#### Step 7: Launch the Flask Web Application
```powershell
python app.py
```

#### Step 8: Open in Your Browser
Open your browser and navigate to:
```
http://127.0.0.1:5000/
```

---

## 13. Expected Website Functionality

1. **Dashboard (`/`)**:
   - Shows live counts: `440,833` training records, `64,374` testing records, and saved prediction counts.
   - Displays model status badge (**Ready for Inference**).
   - Visualizes system workflow and MongoDB collections.
2. **Predict Customer Churn (`/predict`)**:
   - Form with 10 actual dataset features (Age, Gender, Tenure, Usage, Support Calls, Payment Delay, Subscription Type, Contract, Spend, Last Interaction).
   - Quick testing buttons: **"Fill Loyal Customer Sample"** and **"Fill High Churn Risk Sample"** for easy 1-click testing.
   - Instant visual result: Green for "Unlikely to Churn", Red for "Likely to Churn" with probability breakdown meter and MongoDB Document ID confirmation.
3. **Prediction History (`/history`)**:
   - Table showing all predictions made through the website, sorted by most recent first.
   - Shows customer profile, predicted label, churn probability, and MongoDB `_id`.
4. **Model Evaluation (`/evaluation`)**:
   - Real calculated metrics: Accuracy (89.46%), Precision (93.94%), Recall (87.03%), F1-Score (90.35%), ROC-AUC (0.959).
   - 2x2 Confusion Matrix with True Negatives, False Positives, False Negatives, and True Positives.
   - Comparison with independent test dataset (`customers_test`).
   - Detailed statistical explanations of each metric.

---

## 14. Common Errors and Troubleshooting

| Problem | Cause | Solution |
| :--- | :--- | :--- |
| `ServerSelectionTimeoutError: localhost:27017` | MongoDB Community service is stopped. | Open Windows Services (`services.msc`), find **MongoDB Server**, and click **Start**. Or run `net start MongoDB` as Administrator. |
| `FileNotFoundError: churn_model.joblib` | Model has not been trained yet. | Run `python src/train_model.py` in your terminal. |
| Form Input Error (`Feature must be a valid number`) | Non-numerical text entered in numerical input. | Ensure values like Age, Tenure, and Spend contain numbers only. Use the preset buttons. |
| `Database customerChurnDB not found` | The Kaggle dataset was not imported yet. | Import the CSV files into collections `customers_train` and `customers_test` using MongoDB Compass. |

---

## 15. Future Scope
- **Advanced Ensemble Models**: Implement Random Forest or Gradient Boosting (XGBoost/LightGBM) to compare non-linear performance against Logistic Regression.
- **Automated Retention Actions**: Connect MongoDB Change Streams to send retention discounts or alerts when high-risk churners are identified.
- **RESTful API**: Expose `/api/v1/predict` JSON endpoint for third-party CRM system integrations.
- **Time-Series Cohort Analysis**: Track customer churn trends on a monthly cohort timeline.
