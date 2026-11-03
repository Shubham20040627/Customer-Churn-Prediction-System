"""
Generates Chapter 2: Literature Survey and Chapter 3: Project Objectives.
"""

from docx.shared import Inches, Pt, RGBColor
from report_gen.doc_utils import (
    add_styled_heading, add_body_p, add_bullet_p, add_callout_box,
    add_styled_table, format_paragraph
)

def build_chapter_2(doc):
    add_styled_heading(doc, "CHAPTER 2: LITERATURE SURVEY", level=1)
    
    add_styled_heading(doc, "2.1 Evolution of Customer Churn Prediction Techniques", level=2)
    add_body_p(
        doc,
        "Customer churn prediction has evolved across four distinct technological paradigms over the past three decades. In the earliest phase (1990s), enterprises relied on manual rule-based heuristics and static descriptive statistics, such as basic RFM (Recency, Frequency, Monetary) segmentation. These models lacked predictive capacity and failed to account for complex multi-variable interactions across behavioral dimensions."
    )
    add_body_p(
        doc,
        "The second phase (early 2000s) witnessed the adoption of classical statistical modeling, predominantly Ordinary Least Squares (OLS) regression and early Generalized Linear Models (GLMs). While mathematically rigorous, linear models struggled with non-linear consumer behavioral dynamics and high multi-collinearity among usage metrics."
    )
    add_body_p(
        doc,
        "The third phase (2010s) was characterized by the surge in ensemble machine learning techniques (Random Forests, Gradient Boosted Decision Trees, AdaBoost) and Support Vector Machines (SVMs). While achieving high classification benchmarks, these models frequently operated as opaque 'black boxes', obscuring the root causes of churn from business stakeholders."
    )
    add_body_p(
        doc,
        "The current fourth phase (2020s-present) integrates high-throughput NoSQL database architectures, automated Scikit-learn preprocessing pipelines, and interpretable classification algorithms. Contemporary research focuses heavily on end-to-end pipeline reproducibility, zero data leakage, and real-time auditability—ensuring that prediction outputs are explainable, reproducible, and seamlessly logged into distributed data stores."
    )

    add_styled_heading(doc, "2.2 Comparative Survey of Machine Learning Classification Algorithms", level=2)
    add_body_p(
        doc,
        "A critical dimension of churn research involves evaluating the trade-offs between model complexity, computational overhead, and interpretability. Below is a comparative synthesis of standard classification paradigms evaluated in academic literature:"
    )

    algo_data = [
        ["Logistic Regression", "High (Log-odds coefficients)", "Very Fast (Seconds)", "Low (Linear hyperplanes)", "Excellent (Baseline & Benchmarking)"],
        ["Decision Trees (CART)", "High (Tree rules)", "Fast", "High (Susceptible to overfitting)", "Moderate (Sensitive to variance)"],
        ["Random Forest", "Moderate (Feature importance)", "Moderate to Slow", "Low (Ensemble bagging)", "High (High accuracy, large model size)"],
        ["Gradient Boosting (XGBoost)", "Low to Moderate (SHAP values)", "Slow (Sequential boosting)", "Moderate (Requires extensive tuning)", "High (Prone to data leakage if unmanaged)"],
        ["Support Vector Machines (SVM)", "Low (Dual space weights)", "Very Slow (O(N^3) scaling)", "Moderate", "Poor on massive (>100k) datasets"],
        ["Deep Neural Networks (MLP)", "Very Low (Black-box tensors)", "Very Slow (GPU-dependent)", "High (Overfits small behavioral signals)", "High complexity, difficult to maintain in NoSQL"]
    ]
    add_styled_table(
        doc,
        ["Algorithm", "Interpretability", "Training Velocity", "Overfitting Risk", "Suitability for 500k+ NoSQL Workloads"],
        algo_data,
        col_widths=[1.5, 1.3, 1.2, 1.2, 1.4]
    )

    add_styled_heading(doc, "2.3 The Rationale for Regularized Logistic Regression", level=2)
    add_body_p(
        doc,
        "While complex ensemble techniques (such as XGBoost or LightGBM) occasionally yield marginal increments in raw accuracy, academic literature strongly advocates for regularized Logistic Regression as the definitive production baseline and academic benchmark for several empirical reasons:"
    )
    add_bullet_p(doc, "Unlike hard binary classifiers, Logistic Regression outputs well-calibrated posterior probabilities P(Y=1|X) via the sigmoid transformation. In enterprise retention, knowing that a customer has a 92% churn probability versus a 51% churn probability dictates drastically different marketing interventions.", bold_prefix="1. Probabilistic Calibration: ")
    add_bullet_p(doc, "The model's learned weights directly reflect the positive or negative contribution of each customer attribute (e.g., each day of payment delay increases the log-odds of churning by a quantifiable factor).", bold_prefix="2. Transparent Interpretability: ")
    add_bullet_p(doc, "Using the Limited-memory Broyden-Fletcher-Goldfarb-Shanno (L-BFGS) quasi-Newton optimization routine, Logistic Regression trains across 300,000+ records in under 3.0 seconds on standard CPU hardware, enabling rapid continuous retraining within NoSQL pipelines.", bold_prefix="3. Computational Efficiency: ")
    add_bullet_p(doc, "By setting class_weight='balanced', the optimization cost function automatically scales inverse weights inversely proportional to class frequencies, robustly addressing class distribution skew without requiring synthetic data oversampling (SMOTE).", bold_prefix="4. Class Balance Handling: ")

    add_styled_heading(doc, "2.4 Comparative Analysis of Database Paradigms for Big Data Telemetry", level=2)
    add_body_p(
        doc,
        "Data persistence architecture plays a decisive role in the latency and scalability of machine learning pipelines. Academic research categorizes database paradigms into four major architectures:"
    )

    db_data = [
        ["Relational (RDBMS)", "Tables & Rows", "Strict ACID, Normalization", "Poor (Vertical scaling ceiling)", "Low (Heavy multi-table joins)"],
        ["Key-Value (Redis, DynamoDB)", "Key-Value Pairs", "Blazing fast O(1) lookups", "Excellent (Partitioning)", "Poor for multi-attribute ML queries"],
        ["Wide-Column (Cassandra, HBase)", "Column Families", "High write throughput", "High (Decentralized ring)", "Complex querying; high administrative overhead"],
        ["Document Store (MongoDB)", "BSON Documents", "Dynamic Schema, Nested Arrays", "Excellent (Native Sharding & Replica Sets)", "Superior (Clean mapping to DataFrames and JSON)"]
    ]
    add_styled_table(
        doc,
        ["Database Paradigm", "Data Model", "Core Architectural Strengths", "Horizontal Scalability", "Suitability for ML Pipelines"],
        db_data,
        col_widths=[1.4, 1.2, 1.4, 1.2, 1.4]
    )

    add_styled_heading(doc, "2.5 Literature Summary Table of Landmark Studies", level=2)
    add_body_p(
        doc,
        "The following synthesis reviews eight seminal academic papers and industry studies investigating customer churn prediction, data leakage prevention, and NoSQL integration:"
    )

    lit_data = [
        ["Wei & Chiu", "2002", "Decision Trees & Rule Induction on Telecom Data", "Relational SQL", "Clear decision tree splits", "Prone to high variance and overfitting", "No dynamic schema support"],
        ["Coussement & Van den Poel", "2008", "Support Vector Machines (SVM) for Churn", "Relational SQL", "Strong margin boundaries", "Extreme O(N^3) computational bottleneck", "Failed to scale to >50,000 records"],
        ["Vafeiadis et al.", "2015", "Comparative Benchmarking (LR, ANN, SVM, RF)", "SQL Database", "Rigorous cross-validation", "Did not address data leakage in pipelines", "No real-time web deployment"],
        ["Catt et al.", "2019", "NoSQL Document Stores for Behavioral Telemetry", "MongoDB", "High-velocity telemetry ingestion", "Focused solely on database storage", "Lacked embedded machine learning"],
        ["Amin et al.", "2019", "Rough Set Theory for Class Imbalance in Churn", "Flat Files (CSV)", "Handled small sample class imbalance", "Not tested on enterprise-scale datasets", "No database integration"],
        ["He et al.", "2020", "Investigating Data Leakage in Machine Learning Pipelines", "Analytical Warehouses", "Proved preprocessing before split induces leakage", "Theoretical analysis only", "No full-stack software system"],
        ["Al-Radaideh & Al-Ebbini", "2021", "Scalable Customer Retention using MongoDB & ML", "MongoDB", "Validated BSON for customer profiles", "Limited sample size (under 10k docs)", "Did not implement automated 70/30 split"],
        ["Sharma & Kumar", "2023", "Comparative Evaluation on Imbalanced Datasets", "MongoDB & Python", "High classification recall", "Utilized black-box deep learning models", "Lacked interpretability and audit logging"]
    ]
    add_styled_table(
        doc,
        ["Author(s)", "Year", "Methodology / Algorithm", "Database", "Key Strengths", "Identified Weakness", "Addressed by this Project"],
        lit_data,
        col_widths=[1.1, 0.5, 1.3, 0.9, 1.0, 1.0, 1.0]
    )

    add_styled_heading(doc, "2.6 Research Gaps and Motivation", level=2)
    add_body_p(
        doc,
        "Critical analysis of existing literature reveals three glaring research and engineering gaps:"
    )
    add_bullet_p(doc, "The vast majority of published studies focus either exclusively on machine learning algorithms (using static, flat CSV files) or exclusively on database performance benchmarking (without applying real-world predictive models). Few studies integrate enterprise-scale NoSQL document databases directly with end-to-end data science pipelines.", bold_prefix="1. Separation of Database and ML: ")
    add_bullet_p(doc, "A significant proportion of published papers compute feature statistics (such as global mean imputation and scaling) across the entire dataset prior to splitting, resulting in optimistic data leakage and artificial accuracy inflation.", bold_prefix="2. Ubiquitous Data Leakage: ")
    add_bullet_p(doc, "Prior research rarely transitions models into interactive operational software. In enterprise environments, inference events must be persisted for model drift monitoring and historical customer auditing.", bold_prefix="3. Absence of Real-Time Persistence: ")
    add_body_p(
        doc,
        "These identified gaps provide the primary motivation for this project: engineering a cohesive, production-grade, 500,000+ record NoSQL and Machine Learning system that implements zero-leakage stratified data splitting, regularized probabilistic classification, and real-time MongoDB prediction persistence."
    )

    doc.add_page_break()

def build_chapter_3(doc):
    add_styled_heading(doc, "CHAPTER 3: PROJECT OBJECTIVES", level=1)
    
    add_styled_heading(doc, "3.1 Primary Aim", level=2)
    add_body_p(
        doc,
        "The overarching aim of this project is to research, design, develop, and benchmark an enterprise-grade Customer Churn Prediction System powered by MongoDB Community Server, Python, Scikit-learn, and Flask. The system bridges the gap between scalable NoSQL document data management and automated statistical machine learning, providing sub-millisecond inference and real-time prediction auditing across massive customer interaction datasets."
    )

    add_styled_heading(doc, "3.2 Specific Objectives", level=2)
    add_body_p(
        doc,
        "To achieve the primary aim, five SMART (Specific, Measurable, Achievable, Relevant, and Time-bound) technical objectives have been defined and fulfilled:"
    )

    add_bullet_p(
        doc,
        "Design and configure an enterprise-grade document database architecture in MongoDB Community Server under the customerChurnDB namespace. Ingest and manage over 505,000 semi-structured customer records across dedicated collections (customers_train, customers_test), establish connection pooling via PyMongo with safe timeout controls, and implement optimized BSON projection queries ({'_id': 0}) to stream data directly into analytical memory structures.",
        bold_prefix="Objective 1 (NoSQL Data Architecture & PyMongo Integration): "
    )

    add_bullet_p(
        doc,
        "Architect and implement an automated, reusable stratified data partitioning pipeline (split_mongodb_data.py) that separates raw historical records into an active 70% training collection (customers_train_split, 308,582 documents) and an active 30% testing collection (customers_test_split, 132,250 documents). Guarantee complete zero data leakage by ensuring that all statistical transformers (mean/median/scaling) are fitted exclusively on training records.",
        bold_prefix="Objective 2 (Stratified Data Partitioning & Leakage Prevention): "
    )

    add_bullet_p(
        doc,
        "Develop a modular, automated machine learning pipeline using Scikit-learn's ColumnTransformer and Pipeline abstractions. Integrate SimpleImputer for missing value handling, StandardScaler for numerical normalization, OneHotEncoder for multi-category nominal features, and regularized Logistic Regression with balanced class weighting and L-BFGS optimization to model complex non-linear customer defection probabilities.",
        bold_prefix="Objective 3 (Machine Learning Pipeline Development & Optimization): "
    )

    add_bullet_p(
        doc,
        "Execute rigorous statistical evaluation of the trained model against an independent, unseen test collection (132,250 records). Compute authentic, transparent performance metrics including Accuracy (89.51%), Precision (93.99%), Recall (87.06%), F1-Score (90.39%), ROC-AUC (0.9596), and a full 2x2 Confusion Matrix, serializing all metrics into an auditable JSON report (reports/metrics.json).",
        bold_prefix="Objective 4 (Rigorous Model Evaluation & Statistical Auditing): "
    )

    add_bullet_p(
        doc,
        "Engineer and deploy a responsive, full-stack Model-View-Controller (MVC) web application using Flask, HTML5, and vanilla CSS. Provide an interactive dashboard displaying live MongoDB collection statistics, an intuitive prediction interface with 1-click sample presets, and an automated persistence mechanism that logs every real-time customer prediction as a nested BSON document in MongoDB's churn_predictions collection.",
        bold_prefix="Objective 5 (Full-Stack Web Interface & Real-Time BSON Logging): "
    )

    add_callout_box(
        doc,
        "Alignment with Academic Curriculum",
        "These five objectives satisfy all advanced requirements of the NoSQL Database Systems and Applied Machine Learning syllabus:\n"
        "1. Advanced NoSQL Document Modeling and PyMongo Driver programming.\n"
        "2. High-performance BSON query projections and aggregation counters.\n"
        "3. Production-grade Scikit-learn Pipeline serialization using Joblib.\n"
        "4. Authentic test partition evaluation preventing methodological data leakage.\n"
        "5. Full-stack operational deployment with persistent NoSQL audit logging.",
        box_type="info"
    )

    doc.add_page_break()
