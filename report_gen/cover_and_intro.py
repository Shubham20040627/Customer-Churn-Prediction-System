"""
Generates Title Page, Front Matter, and Chapter 1: Introduction.
"""

from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from report_gen.doc_utils import (
    add_styled_heading, add_body_p, add_bullet_p, add_callout_box,
    add_styled_table, format_paragraph
)

def build_cover_page(doc):
    p_pre = doc.add_paragraph()
    format_paragraph(p_pre, space_before=36, space_after=12)
    p_pre.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_uni = p_pre.add_run("ACADEMIC PROJECT REPORT\nDEPARTMENT OF COMPUTER SCIENCE & ENGINEERING")
    r_uni.font.name = "Calibri"
    r_uni.font.size = Pt(13)
    r_uni.font.bold = True
    r_uni.font.color.rgb = RGBColor(113, 128, 150)

    p_title = doc.add_paragraph()
    format_paragraph(p_title, space_before=24, space_after=18)
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t = p_title.add_run("CUSTOMER CHURN PREDICTION SYSTEM USING NOSQL (MONGODB), PYTHON, AND MACHINE LEARNING")
    r_t.font.name = "Calibri"
    r_t.font.size = Pt(22)
    r_t.font.bold = True
    r_t.font.color.rgb = RGBColor(26, 54, 93)

    p_sub = doc.add_paragraph()
    format_paragraph(p_sub, space_before=0, space_after=36)
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_s = p_sub.add_run("A Scalable Document-Oriented Architecture for Customer Retention Analytics, Preprocessed ML Inference, and Audit Logging")
    r_s.font.name = "Calibri"
    r_s.font.size = Pt(13)
    r_s.font.italic = True
    r_s.font.color.rgb = RGBColor(74, 85, 104)

    p_meta = doc.add_paragraph()
    format_paragraph(p_meta, space_before=48, space_after=12)
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_meta.add_run("Submitted in partial fulfillment of the requirements for the course of\n")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(11)
    r_sub.font.color.rgb = RGBColor(45, 55, 72)
    
    r_deg = p_meta.add_run("BACHELOR OF TECHNOLOGY / MASTER OF TECHNOLOGY\nIN COMPUTER SCIENCE & ENGINEERING\n\n")
    r_deg.font.name = "Calibri"
    r_deg.font.size = Pt(12)
    r_deg.font.bold = True
    r_deg.font.color.rgb = RGBColor(43, 108, 176)

    # Submission Table
    tbl = doc.add_table(rows=2, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r in tbl.rows:
        for c in r.cells:
            c.width = Inches(3.2)
    
    c00 = tbl.cell(0, 0).paragraphs[0]
    format_paragraph(c00)
    r_s1 = c00.add_run("Submitted By:\n")
    r_s1.font.bold = True
    r_s1.font.size = Pt(11)
    r_s2 = c00.add_run("Student Name: [Candidate Name]\nRoll Number: [University Roll No.]\nAcademic Session: 2025 - 2026")
    r_s2.font.size = Pt(10.5)

    c01 = tbl.cell(0, 1).paragraphs[0]
    format_paragraph(c01)
    c01.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_g1 = c01.add_run("Under the Guidance of:\n")
    r_g1.font.bold = True
    r_g1.font.size = Pt(11)
    r_g2 = c01.add_run("Project Supervisor: [Guide Name]\nDesignation: Assistant Professor\nDepartment of CSE")
    r_g2.font.size = Pt(10.5)

    doc.add_page_break()

def build_front_matter(doc):
    # Certificate
    add_styled_heading(doc, "BONAFIDE CERTIFICATE", level=1)
    add_body_p(
        doc,
        "This is to certify that the project report titled \"CUSTOMER CHURN PREDICTION SYSTEM USING NOSQL (MONGODB), PYTHON, AND MACHINE LEARNING\" is the bonafide work carried out by [Candidate Name] (Roll No: [University Roll No.]) in partial fulfillment of the requirements for the award of the Degree in Computer Science and Engineering during the academic session 2025-2026."
    )
    add_body_p(
        doc,
        "The project demonstrates a fully functional end-to-end integration between MongoDB Community Server as a scalable document-oriented database, Scikit-learn machine learning pipelines using Logistic Regression, and a Flask-based web application for real-time customer churn inference and persistent logging."
    )
    
    p_sign = doc.add_paragraph()
    format_paragraph(p_sign, space_before=48, space_after=24)
    r_sg = p_sign.add_run("Project Supervisor / Guide\t\t\t\tHead of Department\nDepartment of Computer Science & Engineering\t\tDepartment of Computer Science & Engineering")
    r_sg.font.name = "Calibri"
    r_sg.font.size = Pt(10.5)
    r_sg.font.bold = True

    doc.add_page_break()

    # Declaration
    add_styled_heading(doc, "CANDIDATE DECLARATION", level=1)
    add_body_p(
        doc,
        "I hereby declare that the work presented in this project report entitled \"CUSTOMER CHURN PREDICTION SYSTEM USING NOSQL (MONGODB), PYTHON, AND MACHINE LEARNING\" was carried out by me under the supervision of my faculty guide. The content embodied in this report has not been submitted for the award of any other degree or diploma to any other institute or university."
    )
    add_body_p(
        doc,
        "All primary datasets, software architectures, algorithms, and analytical conclusions have been authentically implemented, benchmarked on local MongoDB Community Server instances, and evaluated using rigorous data science standards with zero data leakage between training and evaluation partitions."
    )
    
    p_cand = doc.add_paragraph()
    format_paragraph(p_cand, space_before=36, space_after=12)
    p_cand.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_cd = p_cand.add_run("Signature of Candidate:\n[Candidate Name]\nRoll No: [University Roll No.]\nDate: 02-11-2026")
    r_cd.font.name = "Calibri"
    r_cd.font.size = Pt(10.5)

    doc.add_page_break()

    # Abstract
    add_styled_heading(doc, "ABSTRACT", level=1)
    add_body_p(
        doc,
        "Customer churn—the rate at which subscribers discontinue their business relationships with a service provider—poses a multi-billion dollar threat across telecommunications, Software-as-a-Service (SaaS), streaming, and financial industries. Identifying at-risk customers prior to contract cancellation enables proactive retention strategies, saving organizations substantial capital compared to new customer acquisition costs. However, modern behavioral telemetry generates massive volumes of semi-structured customer activity records that traditional Relational Database Management Systems (RDBMS) struggle to ingest, query, and scale with low latency."
    )
    add_body_p(
        doc,
        "This project engineers an enterprise-grade, full-stack Machine Learning and NoSQL software system leveraging MongoDB Community Server as the core document database. The system models over 500,000 customer documents across five specialized collections (customers_train, customers_test, customers_train_split, customers_test_split, and churn_predictions). Using PyMongo, an automated stratified 70/30 data partitioning pipeline was implemented to completely eliminate data leakage. Preprocessing was designed using Scikit-learn's ColumnTransformer, combining median numerical imputation, standard scaling, mode categorical imputation, and one-hot encoding."
    )
    add_body_p(
        doc,
        "A regularized Logistic Regression classifier optimized with the L-BFGS algorithm and balanced class weighting was trained on 308,582 customer records and evaluated on an independent test partition of 132,250 records. The model attained authentic performance metrics: 89.51% Accuracy, 93.99% Precision, 87.06% Recall, 90.39% F1-Score, and an outstanding ROC-AUC score of 0.9596. A responsive Flask web application connects user input directly to the serialized model pipeline (Joblib), computes instantaneous churn probabilities, and asynchronously persists every prediction as an embedded BSON audit document into MongoDB. This project proves that modern NoSQL databases provide superior architectural agility, high-throughput writes, and seamless synergy with data science pipelines."
    )
    
    add_callout_box(
        doc,
        "Key Project Highlights",
        "• Database: MongoDB Community Server hosting 505,000+ total customer documents.\n"
        "• Algorithmic Framework: Scikit-learn Pipeline with ColumnTransformer and regularized Logistic Regression.\n"
        "• Accuracy & Discriminative Power: 89.51% Accuracy, 93.99% Precision, 0.9596 ROC-AUC.\n"
        "• Full-Stack Interface: Flask MVC architecture logging real-time inferences into MongoDB collections.",
        box_type="success"
    )

    doc.add_page_break()

    # Table of Contents
    add_styled_heading(doc, "TABLE OF CONTENTS", level=1)
    toc_data = [
        ["Chapter 1", "Introduction and Project Overview", "6"],
        ["Chapter 2", "Literature Survey and State-of-the-Art Analysis", "11"],
        ["Chapter 3", "Project Aim and Specific Objectives", "18"],
        ["Chapter 4", "Dataset Analysis, Statistics, and NoSQL Schema Design", "20"],
        ["Chapter 5", "System Design and Architectural Methodology", "26"],
        ["Chapter 6", "Implementation, Full Code Listings, and Visual Walkthroughs", "33"],
        ["Chapter 7", "Experimental Results, Console Logs, and Performance Discussion", "42"],
        ["Chapter 8", "Conclusion, Critical Findings, and Future Research Scope", "48"],
        ["Chapter 9", "Academic Viva-Voce Comprehensive Q&A Guide", "51"],
        ["Chapter 10", "References and Academic Bibliography", "55"]
    ]
    add_styled_table(doc, ["Chapter Number", "Chapter Title / Module Description", "Page No."], toc_data, col_widths=[1.5, 4.2, 0.9])

    doc.add_page_break()

def build_chapter_1(doc):
    add_styled_heading(doc, "CHAPTER 1: INTRODUCTION", level=1)
    
    add_styled_heading(doc, "1.1 Background and Context", level=2)
    add_body_p(
        doc,
        "In the contemporary global economy, subscription-based business models dominate major commercial verticals including telecommunications, Software-as-a-Service (SaaS), digital media streaming, cloud infrastructure, and fintech banking. In these recurring-revenue paradigms, sustained organizational profitability is directly contingent upon maximizing customer lifetime value (CLV) and minimizing customer attrition, commonly termed 'customer churn'."
    )
    add_body_p(
        doc,
        "Customer churn occurs when an active subscriber discontinues their paid subscription or migrates to a commercial competitor. Industry benchmarks consistently demonstrate that acquiring a new customer is between five to seven times more expensive than retaining an existing client (Customer Acquisition Cost vs. Customer Retention Cost). Furthermore, empirical research in customer relationship management reveals that a modest 5% reduction in customer churn can yield between a 25% and 95% increase in cumulative organizational profits."
    )
    add_body_p(
        doc,
        "Historically, commercial enterprises addressed churn reactively—intervening only after a customer initiated account cancellation or ceased payment. However, in competitive digital markets, reactive retention fails because the consumer's decision to defect has already solidified. Modern competitive advantage necessitates proactive retention: leveraging historical behavioral telemetry, payment records, service usage patterns, and support interaction logs to forecast which subscribers exhibit high defection risk before they submit a cancellation request."
    )

    add_styled_heading(doc, "1.2 The Paradigm Shift to NoSQL Databases in Analytics", level=2)
    add_body_p(
        doc,
        "The proliferation of ubiquitous telemetry, web-scale user activity tracking, and Internet of Things (IoT) monitoring has fundamentally altered enterprise data characteristics. Modern customer interaction datasets exhibit the classic 'Three Vs' of Big Data: high Volume, high Velocity, and high Variety. Traditional Relational Database Management Systems (RDBMS)—grounded in Edgar F. Codd's relational model established in 1970—were architected for structured, static-schema transactional records under strict ACID (Atomicity, Consistency, Isolation, Durability) guarantees."
    )
    add_body_p(
        doc,
        "While RDBMS technologies such as PostgreSQL and MySQL remain exceptional for financial ledgers and relational transactions, they present severe architectural bottlenecks when applied to high-throughput, exploratory data science and real-time behavioral analytics:"
    )
    
    add_bullet_p(doc, "Relational schemas necessitate explicit, predefined Data Definition Language (DDL) migrations. Altering a table schema across hundreds of millions of historical customer interaction records induces costly table locks and administrative downtime.", bold_prefix="1. Rigid Schema Constraints: ")
    add_bullet_p(doc, "Normalized relational architectures decompose customer profiles across dozens of disparate tables (e.g., customer_master, subscription_details, payment_history, support_tickets). Reconstructing a customer's analytical profile requires multi-table JOIN operations that consume exponential CPU cycles and memory as data volumes scale.", bold_prefix="2. Expensive JOIN Operations: ")
    add_bullet_p(doc, "RDBMS platforms scale vertically (upward scaling via expensive hardware upgrades) rather than horizontally across commodity server clusters, creating hardware cost ceilings for large-scale enterprise telemetry.", bold_prefix="3. Horizontal Scalability Impediments: ")
    add_bullet_p(doc, "Relational databases enforce strict row-locking mechanisms optimized for read-heavy consistency rather than high-velocity write throughput required when thousands of distributed microservices continuously log real-time inference telemetry.", bold_prefix="4. Write Throughput Bottlenecks: ")

    add_body_p(
        doc,
        "To resolve these architectural limitations, Not Only SQL (NoSQL) databases emerged. Among NoSQL paradigms—Key-Value, Wide-Column, Graph, and Document Stores—document-oriented databases, predominantly MongoDB, have gained preeminent adoption for analytical workflows. MongoDB stores records as semi-structured, binary-encoded JSON documents known as BSON (Binary JSON). Each document encapsulates all relevant customer attributes, nested arrays, and subdocuments within a single self-contained entity, entirely eliminating the necessity for costly JOIN operations."
    )

    add_styled_heading(doc, "1.3 MongoDB's Role in Modern Machine Learning Architectures", level=2)
    add_body_p(
        doc,
        "The integration between MongoDB Community Server and Python's data science ecosystem (PyMongo, Pandas, Scikit-learn) creates a natural, frictionless workflow for enterprise machine learning. MongoDB's dynamic document schema allows customer profiles to evolve over time without breaking existing analytical pipelines. For instance, new behavioral metrics—such as mobile app session durations, customer sentiment scores, or streaming bitrates—can be incorporated into customer documents dynamically."
    )
    add_body_p(
        doc,
        "Furthermore, MongoDB's WiredTiger storage engine provides enterprise-class concurrency control through document-level locking, checkpointing, and transparent Snappy data compression. When deploying machine learning models to production, MongoDB acts not merely as a cold data warehouse for training historical models, but as an active, high-throughput operational data store that simultaneously serves incoming web requests and persists real-time prediction logs (inference telemetry) with sub-millisecond write latencies."
    )

    add_styled_heading(doc, "1.4 Problem Statement", level=2)
    add_body_p(
        doc,
        "Subscription-based enterprises possess vast historical datasets containing customer demographics, subscription types, contract terms, tenure, usage frequency, support ticket logs, and payment histories. However, these organizations face a dual challenge: (1) managing and querying massive, high-velocity datasets exceeding half a million records without database latency degradation, and (2) implementing an accurate, transparent, and reproducible machine learning classification model capable of predicting customer churn in real time while guaranteeing zero data leakage."
    )
    add_body_p(
        doc,
        "This project addresses this exact dual challenge by engineering a complete, production-ready system that integrates MongoDB Community Server with a Scikit-learn Logistic Regression pipeline and a responsive Flask web application. The system ingests 505,000+ customer records, enforces stratified 70/30 partitioning directly at the database layer, trains a regularized classifier with balanced class weighting, and provides an interactive user interface that logs all incoming predictions into a dedicated NoSQL collection."
    )

    add_styled_heading(doc, "1.5 Scope and Academic Significance", level=2)
    add_body_p(
        doc,
        "The academic and practical scope of this project encompasses:"
    )
    add_bullet_p(doc, "Designing, importing, indexing, and managing a 505,000+ document database (customerChurnDB) using MongoDB Community Server and PyMongo.", bold_prefix="Database Engineering: ")
    add_bullet_p(doc, "Developing a modular, stratified data-splitting script (split_mongodb_data.py) that isolates 308,582 training records from 132,250 independent test records to ensure strict zero data leakage.", bold_prefix="Data Pipeline Architecture: ")
    add_bullet_p(doc, "Constructing an automated Scikit-learn Pipeline incorporating SimpleImputer, StandardScaler, OneHotEncoder, and balanced Logistic Regression.", bold_prefix="Machine Learning Engineering: ")
    add_bullet_p(doc, "Conducting rigorous mathematical evaluation yielding authentic metrics (89.51% Accuracy, 93.99% Precision, 87.06% Recall, 90.39% F1-Score, 0.9596 ROC-AUC).", bold_prefix="Statistical Verification: ")
    add_bullet_p(doc, "Deploying a Model-View-Controller (MVC) Flask application featuring real-time inference, sample population, and persistent audit logging into MongoDB.", bold_prefix="Full-Stack Web Deployment: ")

    doc.add_page_break()
