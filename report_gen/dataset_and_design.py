"""
Generates Chapter 4: Dataset Analysis & Specification and Chapter 5: System Design and Methodology.
"""

from docx.shared import Inches, Pt, RGBColor
from report_gen.doc_utils import (
    add_styled_heading, add_body_p, add_bullet_p, add_callout_box,
    add_code_block, add_styled_table, format_paragraph
)

def build_chapter_4(doc):
    add_styled_heading(doc, "CHAPTER 4: DATASET ANALYSIS AND NOSQL SCHEMA DESIGN", level=1)
    
    add_styled_heading(doc, "4.1 Dataset Provenance and Volume", level=2)
    add_body_p(
        doc,
        "The primary empirical foundation of this project is derived from the comprehensive Kaggle Customer Churn Prediction Dataset, representative of commercial enterprise subscription services (telecommunications, digital streaming, and SaaS platforms). The raw dataset comprises 505,207 total customer interaction records divided into two primary historical files:"
    )
    add_bullet_p(doc, "Contains 440,833 complete customer interaction documents used as the baseline pool for model training and cross-validation.", bold_prefix="1. Training Partition (customers_train): ")
    add_bullet_p(doc, "Contains 64,374 independent customer documents reserved for secondary independent validation.", bold_prefix="2. Testing Partition (customers_test): ")
    add_body_p(
        doc,
        "To maintain rigorous data science integrity and support authentic academic evaluation, the system executes an automated 70/30 stratified split directly on the training pool, producing two active working collections:"
    )
    add_bullet_p(doc, "Exactly 308,582 customer documents used exclusively to fit the machine learning transformers and the Logistic Regression classifier.", bold_prefix="• customers_train_split (70%): ")
    add_bullet_p(doc, "Exactly 132,250 customer documents held strictly separate for unbiased model evaluation.", bold_prefix="• customers_test_split (30%): ")

    add_styled_heading(doc, "4.2 Comprehensive Data Dictionary", level=2)
    add_body_p(
        doc,
        "The dataset encompasses twelve distinct features reflecting demographic profiles, subscription contracts, monetary value, and customer support engagement. Below is the detailed technical specification:"
    )

    data_dict = [
        ["CustomerID", "Integer / Long", "Unique identifier for customer tracking (Excluded from ML)", "1 to 500,000", "None (ID)"],
        ["Age", "Float / Integer", "Customer age in years", "18 to 100", "Demographic"],
        ["Gender", "String / Categorical", "Customer gender ('Female', 'Male')", "Female / Male", "Demographic"],
        ["Tenure", "Float / Integer", "Months of continuous subscription tenure", "1 to 120", "Relationship Length"],
        ["Usage Frequency", "Float / Integer", "Average monthly platform usage sessions", "0 to 50", "Platform Engagement"],
        ["Support Calls", "Float / Integer", "Number of calls placed to customer assistance", "0 to 20", "Friction / Dissatisfaction"],
        ["Payment Delay", "Float / Integer", "Days payment overdue past the billing cycle", "0 to 60", "Financial Distress"],
        ["Subscription Type", "String / Categorical", "Customer tier ('Basic', 'Standard', 'Premium')", "Basic, Standard, Premium", "Monetary Tier"],
        ["Contract Length", "String / Categorical", "Billing duration ('Monthly', 'Quarterly', 'Annual')", "Monthly, Quarterly, Annual", "Commitment Level"],
        ["Total Spend", "Float / Double", "Cumulative lifetime monetary revenue from customer", "100.0 to 5,000.0", "Customer Value (CLV)"],
        ["Last Interaction", "Float / Integer", "Days elapsed since the customer's last service activity", "0 to 60", "Recent Activity Recency"],
        ["Churn (Target)", "Integer (0 or 1)", "Binary ground truth target: 0 = Loyal, 1 = Churned", "0 or 1", "Target Variable"]
    ]
    add_styled_table(
        doc,
        ["Field Name", "MongoDB / Python Type", "Operational Description", "Observed Range", "Business Role"],
        data_dict,
        col_widths=[1.2, 1.2, 2.0, 1.1, 1.1]
    )

    add_styled_heading(doc, "4.3 MongoDB Database and Collection Architecture", level=2)
    add_body_p(
        doc,
        "The database is structured within MongoDB Community Server under the database namespace customerChurnDB. It manages five distinct collections with specialized operational roles:"
    )

    col_data = [
        ["customers_train", "440,833", "Original Raw Training Pool", "Historical training baseline; preserved intact."],
        ["customers_test", "64,374", "Original Raw Test Pool", "Secondary independent test collection."],
        ["customers_train_split", "308,582", "Active 70% Training Collection", "Exclusive source of data for fitting Scikit-learn Pipeline."],
        ["customers_test_split", "132,250", "Active 30% Test Collection", "Unbiased validation set for computing authentic metrics."],
        ["churn_predictions", "Dynamic (5+)", "Operational Inference Logs", "Stores real-time web predictions as nested BSON audit logs."]
    ]
    add_styled_table(
        doc,
        ["Collection Name", "Document Count", "Architectural Role", "Operational Lifecycle & Usage"],
        col_data,
        col_widths=[1.6, 0.9, 1.6, 2.5]
    )

    add_styled_heading(doc, "4.4 Document Schema Design and BSON Representation", level=2)
    add_body_p(
        doc,
        "In contrast to rigid relational DDL, MongoDB utilizes dynamic BSON documents. However, this application enforces strict application-level document modeling. Below are the two primary document schemas:"
    )

    add_body_p(doc, "Schema A: Customer Behavioral Profile Document (Stored in customer collections):", italic_prefix="")
    add_code_block(doc, """{
  "_id": ObjectId("6707bf35d648939c36d0f19c"),
  "CustomerID": 184920,
  "Age": 42.0,
  "Gender": "Male",
  "Tenure": 18.0,
  "Usage Frequency": 12.0,
  "Support Calls": 4.0,
  "Payment Delay": 14.0,
  "Subscription Type": "Standard",
  "Contract Length": "Monthly",
  "Total Spend": 480.0,
  "Last Interaction": 22.0,
  "Churn": 1
}""")

    add_body_p(doc, "Schema B: Real-Time Inference Audit Document (Stored in churn_predictions collection):", italic_prefix="")
    add_body_p(
        doc,
        "Notice the powerful use of NoSQL nested subdocuments (customer_features embedded within the audit document), providing complete atomicity for each prediction event:"
    )
    add_code_block(doc, """{
  "_id": ObjectId("6ac9d4aaca5daedd984aaaf4"),
  "timestamp": ISODate("2026-10-10T06:01:14Z"),
  "formatted_time": "2026-10-10 11:31:14",
  "customer_features": {
    "Age": 45.0,
    "Gender": "Female",
    "Tenure": 12.0,
    "Usage Frequency": 10.0,
    "Support Calls": 5.0,
    "Payment Delay": 15.0,
    "Subscription Type": "Standard",
    "Contract Length": "Monthly",
    "Total Spend": 450.0,
    "Last Interaction": 20.0
  },
  "prediction_code": 1,
  "prediction_label": "Likely to Churn",
  "churn_probability": 100.0,
  "loyal_probability": 0.0,
  "model_used": "Logistic Regression with Pipeline Preprocessing"
}""")

    doc.add_page_break()

def build_chapter_5(doc):
    add_styled_heading(doc, "CHAPTER 5: SYSTEM DESIGN AND METHODOLOGY", level=1)
    
    add_styled_heading(doc, "5.1 Architectural Overview", level=2)
    add_body_p(
        doc,
        "The system is architected as an end-to-end, multi-tier data science and web platform adhering to the Model-View-Controller (MVC) architectural design pattern. The platform seamlessly coordinates five distinct tiers:"
    )
    add_bullet_p(doc, "Hosts customer collections and persists inference events with document-level locking.", bold_prefix="1. Persistence Tier (MongoDB): ")
    add_bullet_p(doc, "Singleton DatabaseManager implementing connection pooling, BSON projections, and CRUD routines.", bold_prefix="2. Data Access Tier (PyMongo): ")
    add_bullet_p(doc, "ColumnTransformer and regularized Logistic Regression classifier serialized via Joblib.", bold_prefix="3. Machine Learning Tier (Scikit-learn): ")
    add_bullet_p(doc, "Flask application managing HTTP routes, request validation, and view coordination.", bold_prefix="4. Application Controller Tier (Flask): ")
    add_bullet_p(doc, "HTML5, Jinja2 templating, and vanilla CSS providing a responsive client interface.", bold_prefix="5. Presentation Tier (Web UI): ")

    add_styled_heading(doc, "5.2 System Architecture Diagram", level=2)
    add_body_p(
        doc,
        "The structural flow and component interactions are illustrated in the system architecture diagram below:"
    )
    add_code_block(doc, """+-----------------------------------------------------------------------+
|                         MongoDB Database                              |
|                       (customerChurnDB)                               |
|                                                                       |
|  [customers_train_split]   (308k docs)   [customers_test_split] (132k) |
+----------+-------------------------------------+----------------------+
           |                                     |
           | PyMongo Query ({'_id': 0})          | PyMongo Query
           v                                     v
+-----------------------+               +-------------------------------+
|  src/database.py      |               |  src/evaluation.py            |
|  - DatabaseManager    |               |  - Test set metrics           |
|  - Connection Pooling |               |  - Confusion matrix           |
+----------+------------+               +-------------------------------+
           |
           v
+-----------------------------------------------------------------------+
|  src/train_model.py                                                   |
|  1. Load 308,582 training records from customers_train_split          |
|  2. ColumnTransformer (StandardScaler for numerical, OneHot for cat)  |
|  3. Fit Logistic Regression (L-BFGS solver, Balanced Class Weights)   |
|  4. Evaluate on customers_test_split (132,250 records)                |
|  5. Serialize Model Pipeline -> models/churn_model.joblib             |
|  6. Serialize Metrics Report -> reports/metrics.json                  |
+-----------------------------------------------------------------------+
                                  |
                                  v
+-----------------------------------------------------------------------+
|  Flask Web Application (app.py)                                       |
|  /            -> Dashboard with live MongoDB stats & counts           |
|  /predict     -> Interactive Form -> src/predict.py -> Inference      |
|  /history     -> Live table querying churn_predictions collection    |
|  /evaluation  -> Authentic accuracy, confusion matrix, viva guide     |
+----------------------------------+------------------------------------+
                                   |
                                   | Insert BSON Document
                                   v
                   +-------------------------------+
                   | MongoDB Collection            |
                   | `churn_predictions`           |
                   | (Input + Result + Probability)|
                   +-------------------------------+""")

    add_styled_heading(doc, "5.3 Data Flow Diagrams (DFD)", level=2)
    add_body_p(
        doc,
        "To illustrate how information propagates through the system across different granularities, three Data Flow Diagrams are defined:"
    )
    
    add_body_p(doc, "DFD Level 0: Context Diagram", bold_prefix="• ")
    add_body_p(
        doc,
        "The Level 0 diagram models the global boundary. The User submits customer behavioral attributes to the Churn Prediction System and receives the Churn Risk Classification, Probability Score, and MongoDB Reference ID. Simultaneously, the system queries and updates the MongoDB Database."
    )
    add_code_block(doc, """   +------+       Customer Attributes       +-------------------------+
   |      | ------------------------------> |                         |
   | User |                                 | Churn Prediction System |
   |      | <------------------------------ |                         |
   +------+   Prediction, Probability & ID  +-------------------------+
                                                         ^
                                                         | Read Train/Test Data
                                                         | Write Prediction Logs
                                                         v
                                            +-------------------------+
                                            |   MongoDB Database      |
                                            |   (customerChurnDB)     |
                                            +-------------------------+""")

    add_body_p(doc, "DFD Level 1: Data Processing and Training Pipeline", bold_prefix="• ")
    add_body_p(
        doc,
        "The Level 1 diagram decomposes the training lifecycle: (1.1) Query MongoDB with BSON projection, (1.2) Impute missing values and encode categorical features, (1.3) Scale numerical vectors, (1.4) Train Logistic Regression with L-BFGS, (1.5) Evaluate against independent test split, and (1.6) Serialize artifacts to disk."
    )

    add_styled_heading(doc, "5.4 Mathematical Foundation of Logistic Regression", level=2)
    add_body_p(
        doc,
        "Logistic Regression is a foundational generalized linear model designed for binary classification. Given an input feature vector X = [x1, x2, ..., xn], the linear combination of inputs and model weights beta is formulated as:"
    )
    add_code_block(doc, "z = beta_0 + beta_1 * x_1 + beta_2 * x_2 + ... + beta_n * x_n = beta^T * X")
    add_body_p(
        doc,
        "To map this real-valued scalar z from (-infinity, +infinity) into a bounded probability interval [0, 1], the logistic sigmoid activation function is applied:"
    )
    add_code_block(doc, "P(Y=1 | X) = sigma(z) = 1 / (1 + e^(-z))")
    add_body_p(
        doc,
        "The probability of the customer remaining loyal (Y=0) is trivially the complement:"
    )
    add_code_block(doc, "P(Y=0 | X) = 1 - P(Y=1 | X) = e^(-z) / (1 + e^(-z))")
    add_body_p(
        doc,
        "The log-odds (logit transformation) expresses the logarithm of the ratio of churn probability to loyal probability as a strictly linear function of the input features:"
    )
    add_code_block(doc, "ln( P(Y=1|X) / (1 - P(Y=1|X)) ) = beta_0 + sum(beta_i * x_i)")
    add_body_p(
        doc,
        "To optimize the parameter vector beta across m training samples, the model minimizes the Binary Cross-Entropy (Log-Loss) cost function with L2 ridge regularization:"
    )
    add_code_block(doc, "J(beta) = - (1/m) * sum_{j=1}^m [ y^(j) * ln(p^(j)) + (1 - y^(j)) * ln(1 - p^(j)) ] + (1 / (2*C)) * ||beta||^2")
    add_body_p(
        doc,
        "Where y^(j) in {0, 1} represents the ground truth label, p^(j) represents the predicted churn probability, and C represents the inverse regularization strength. Optimization is carried out via the Limited-memory BFGS (L-BFGS) algorithm, which approximates the inverse Hessian matrix without storing the full n x n matrix, enabling fast convergence across 300,000+ customer records."
    )

    add_styled_heading(doc, "5.5 System Hardware and Software Requirements", level=2)
    req_data = [
        ["Operating System", "Windows 10 / 11 (64-bit), Linux Ubuntu 20.04+, macOS", "Windows 11 (Tested Environment)"],
        ["Python Runtime", "Python 3.10.x, 3.11.x, 3.12.x, 3.14.x", "Python 3.14.x (64-bit)"],
        ["NoSQL Database", "MongoDB Community Server 6.0 / 7.0 / 8.0", "MongoDB Community Server on localhost:27017"],
        ["Database Client", "MongoDB Compass / mongosh (Optional)", "MongoDB Compass (Visual document inspection)"],
        ["Core Libraries", "PyMongo, Pandas, NumPy, Scikit-learn, Joblib, Flask", "PyMongo 4.6+, Scikit-learn 1.3+, Flask 3.0+"],
        ["Processor (CPU)", "Intel Core i3 / AMD Ryzen 3 or higher", "Intel Core i5 / i7 / Ryzen 5 (Multithreaded)"],
        ["System Memory (RAM)", "Minimum 4 GB RAM (8 GB Recommended for 500k docs)", "8 GB / 16 GB High-Speed RAM"],
        ["Disk Storage", "Minimum 2 GB free disk space", "Fast SSD Storage"]
    ]
    add_styled_table(
        doc,
        ["System Component", "Minimum Specification", "Verified Testing Environment"],
        req_data,
        col_widths=[1.8, 2.5, 2.3]
    )

    doc.add_page_break()
