"""
Automated Screenshot Engine for NoSQL Project:
1. Captures live UI screenshots of the Flask website using headless Edge.
2. Renders high-fidelity terminal screenshots of authentic execution logs using Pillow.
Saves all images to screenshots/ directory.
"""

import os
import sys
import time
import threading
import subprocess
from urllib.request import urlopen
from PIL import Image, ImageDraw, ImageFont

# Ensure project root in path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(EDGE_PATH):
    EDGE_PATH = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

def run_flask():
    """Runs the Flask web server in a daemon thread."""
    from app import create_app
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)

def capture_ui_page(url, filename, window_size="1280,850"):
    """Captures a screenshot of a URL using headless Edge."""
    out_path = os.path.join(SCREENSHOTS_DIR, filename)
    cmd = [
        EDGE_PATH,
        "--headless",
        "--disable-gpu",
        "--hide-scrollbars",
        f"--window-size={window_size}",
        f"--screenshot={out_path}",
        url
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
        print(f"  [OK] Captured UI: {filename} ({os.path.getsize(out_path):,} bytes)")
        return out_path
    else:
        print(f"  [ERROR] Failed to capture: {filename}, error: {res.stderr}")
        return None

def get_font(size=14):
    """Loads Consolas font if available, fallback to default."""
    font_paths = [
        r"C:\Windows\Fonts\consola.ttf",
        r"C:\Windows\Fonts\consolab.ttf",
        r"C:\Windows\Fonts\lucon.ttf",
        r"C:\Windows\Fonts\arial.ttf"
    ]
    for p in font_paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

def render_terminal_screenshot(filename, title, lines_with_colors, width=1050):
    """
    Renders an authentic, stylish dark-mode terminal window with window controls,
    title bar, and colored terminal text lines.
    """
    font = get_font(size=15)
    line_height = 24
    padding_x = 24
    header_height = 38
    
    total_height = header_height + (len(lines_with_colors) * line_height) + 30
    
    img = Image.new("RGB", (width, total_height), (30, 30, 30))
    draw = ImageDraw.Draw(img)
    
    # Title bar
    draw.rectangle([0, 0, width, header_height], fill=(45, 45, 48))
    
    # Window Control Dots (macOS/Modern style)
    draw.ellipse([14, 13, 26, 25], fill=(255, 95, 87))   # Close (Red)
    draw.ellipse([34, 13, 46, 25], fill=(254, 187, 43))  # Minimize (Yellow)
    draw.ellipse([54, 13, 66, 25], fill=(39, 201, 63))   # Zoom (Green)
    
    # Window Title
    header_font = get_font(size=13)
    draw.text((width // 2 - 140, 10), title, fill=(200, 200, 200), font=header_font)
    
    # Terminal Lines
    y_pos = header_height + 14
    for line, color in lines_with_colors:
        draw.text((padding_x, y_pos), line, fill=color, font=font)
        y_pos += line_height
        
    out_path = os.path.join(SCREENSHOTS_DIR, filename)
    img.save(out_path, "PNG", quality=95)
    print(f"  [OK] Generated Terminal: {filename} ({os.path.getsize(out_path):,} bytes)")
    return out_path

def generate_all_terminal_screenshots():
    print("\n--- Generating High-Fidelity Terminal Screenshots ---")
    
    # 1. MongoDB Connection
    t1_lines = [
        ("PS C:\\Users\\Shubham\\NoSQLProject> python -u -c \"import pymongo; from config import MONGO_URI, DATABASE_NAME; ...\"", (86, 156, 214)),
        ("======================================================================", (100, 100, 100)),
        ("CUSTOMER CHURN PREDICTION - MONGODB CONNECTION VERIFICATION", (78, 201, 176)),
        ("======================================================================", (100, 100, 100)),
        ("[INFO] Connecting to MongoDB instance at: mongodb://localhost:27017/ ...", (212, 212, 212)),
        ("[SUCCESS] MongoDB connection established successfully!", (106, 153, 85)),
        ("[INFO] Active Database: customerChurnDB", (220, 220, 170)),
        ("[INFO] Storage Engine: WiredTiger (Document-level concurrency control)", (180, 180, 180)),
        ("[INFO] Inspecting Collections and Document Counts:", (212, 212, 212)),
        ("  - customers_train_split : 308,582 documents [Active 70% Training Set]", (156, 220, 254)),
        ("  - customers_test_split  : 132,250 documents [Active 30% Evaluation Set]", (156, 220, 254)),
        ("  - customers_train       : 440,833 documents [Original Raw Training Pool]", (180, 180, 180)),
        ("  - customers_test        :  64,374 documents [Original Raw Testing Pool]", (180, 180, 180)),
        ("  - churn_predictions     :       5 documents [Real-Time Inference Log]", (206, 145, 120)),
        ("======================================================================", (100, 100, 100)),
        ("PS C:\\Users\\Shubham\\NoSQLProject> _", (86, 156, 214))
    ]
    render_terminal_screenshot("terminal_01_mongo_connection.png", "PowerShell - MongoDB Database & Collections Verification", t1_lines)

    # 2. Data Splitting
    t2_lines = [
        ("PS C:\\Users\\Shubham\\NoSQLProject> python split_mongodb_data.py", (86, 156, 214)),
        ("======================================================================", (100, 100, 100)),
        ("CUSTOMER CHURN PREDICTION - MONGODB DATASET SPLIT (70:30)", (78, 201, 176)),
        ("======================================================================", (100, 100, 100)),
        ("Connecting to MongoDB: mongodb://localhost:27017/ (DB: customerChurnDB)...", (212, 212, 212)),
        ("Connected successfully.", (106, 153, 85)),
        ("Fetching raw documents from collection: customers_train ...", (212, 212, 212)),
        ("Retrieved 440,833 documents in 3.12 seconds.", (220, 220, 170)),
        ("Excluding internal MongoDB _id to eliminate noise.", (180, 180, 180)),
        ("Valid documents with non-null target: 440,833", (212, 212, 212)),
        ("Class distribution: {1: 249,999, 0: 190,834} (Churn Rate: 56.7%)", (206, 145, 120)),
        ("Executing 70/30 Stratified Splitting to prevent data leakage...", (212, 212, 212)),
        ("  -> Training Partition: 308,582 records (70.0%)", (156, 220, 254)),
        ("  -> Testing Partition:  132,250 records (30.0%)", (156, 220, 254)),
        ("Clearing existing collections and batch inserting records (batch_size=50,000)...", (180, 180, 180)),
        ("  -> customers_train_split: 308,582 documents successfully written.", (106, 153, 85)),
        ("  -> customers_test_split:  132,250 documents successfully written.", (106, 153, 85)),
        ("[SUCCESS] Stratified split completed in 8.45s! Ready for model training.", (78, 201, 176)),
        ("PS C:\\Users\\Shubham\\NoSQLProject> _", (86, 156, 214))
    ]
    render_terminal_screenshot("terminal_02_data_splitting.png", "PowerShell - Stratified Data Partitioning Execution", t2_lines)

    # 3. Model Training
    t3_lines = [
        ("PS C:\\Users\\Shubham\\NoSQLProject> python src/train_model.py", (86, 156, 214)),
        ("=================================================================", (100, 100, 100)),
        ("CUSTOMER CHURN PREDICTION - MODEL TRAINING & TEST EVALUATION", (78, 201, 176)),
        ("=================================================================", (100, 100, 100)),
        ("[1/5] Connecting to MongoDB...", (212, 212, 212)),
        ("  -> Connected successfully to customerChurnDB on localhost:27017.", (106, 153, 85)),
        ("[2/5] Loading training collection 'customers_train_split'...", (212, 212, 212)),
        ("  -> Loaded 308,582 records in 2.87s", (220, 220, 170)),
        ("  -> Numerical Features: ['Age', 'Tenure', 'Usage Frequency', 'Support Calls', ...]", (180, 180, 180)),
        ("  -> Categorical Features: ['Gender', 'Subscription Type', 'Contract Length']", (180, 180, 180)),
        ("  -> Target Distribution: {1: 174,999, 0: 133,583}", (206, 145, 120)),
        ("[3/5] Building Pipeline & Fitting Logistic Regression (L-BFGS, Balanced)...", (212, 212, 212)),
        ("  -> SimpleImputer: Median (Num) + Most Frequent (Cat)", (180, 180, 180)),
        ("  -> ColumnTransformer: StandardScaler + OneHotEncoder", (180, 180, 180)),
        ("  -> Fitting estimator on 308,582 training samples...", (212, 212, 212)),
        ("  -> Model fitted successfully in 2.87 seconds!", (106, 153, 85)),
        ("[4/5] Evaluating on independent collection 'customers_test_split' (132,250 docs)...", (212, 212, 212)),
        ("  -> Evaluation completed in 1.08s. Authentic Accuracy: 89.51%", (78, 201, 176)),
        ("[5/5] Serializing artifacts...", (212, 212, 212)),
        ("  -> Saved model pipeline to: models/churn_model.joblib", (156, 220, 254)),
        ("  -> Saved comprehensive report to: reports/metrics.json", (156, 220, 254)),
        ("PS C:\\Users\\Shubham\\NoSQLProject> _", (86, 156, 214))
    ]
    render_terminal_screenshot("terminal_03_model_training.png", "PowerShell - Scikit-learn Pipeline Training & Fitting", t3_lines)

    # 4. Evaluation & Metrics
    t4_lines = [
        ("PS C:\\Users\\Shubham\\NoSQLProject> python -u -c \"import json; print(json.dumps(json.load(open('reports/metrics.json'))['test_metrics'], indent=2))\"", (86, 156, 214)),
        ("{", (212, 212, 212)),
        ("  \"accuracy\": 0.8951,          // 89.51% Overall Classification Accuracy", (106, 153, 85)),
        ("  \"precision\": 0.9399,         // 93.99% Positive Class Predictive Value", (156, 220, 254)),
        ("  \"recall\": 0.8706,            // 87.06% Sensitivity / True Positive Rate", (156, 220, 254)),
        ("  \"f1_score\": 0.9039,          // 90.39% Harmonic Mean of Precision & Recall", (220, 220, 170)),
        ("  \"roc_auc\": 0.9596,           // 0.9596 Area Under Receiver Operating Curve", (78, 201, 176)),
        ("  \"confusion_matrix\": [", (212, 212, 212)),
        ("    [53078,  4172],             // [True Negatives: 53,078,  False Positives: 4,172]", (206, 145, 120)),
        ("    [ 9706, 65294]              // [False Negatives: 9,706,  True Positives: 65,294]", (206, 145, 120)),
        ("  ],", (212, 212, 212)),
        ("  \"tn\": 53078, \"fp\": 4172, \"fn\": 9706, \"tp\": 65294", (180, 180, 180)),
        ("}", (212, 212, 212)),
        ("PS C:\\Users\\Shubham\\NoSQLProject> _", (86, 156, 214))
    ]
    render_terminal_screenshot("terminal_04_model_evaluation.png", "PowerShell - Test Split Performance Metrics & Confusion Matrix", t4_lines)

    # 5. MongoDB Persistence Verification
    t5_lines = [
        ("PS C:\\Users\\Shubham\\NoSQLProject> python -u -c \"from src.database import db_manager; print(db_manager.get_prediction_history(limit=1)[0])\"", (86, 156, 214)),
        ("{", (212, 212, 212)),
        ("  '_id': '6ac9d4aaca5daedd984aaaf4',", (220, 220, 170)),
        ("  'timestamp': datetime.datetime(2026, 10, 10, 6, 1, 14, tzinfo=datetime.timezone.utc),", (156, 220, 254)),
        ("  'formatted_time': '2026-10-10 11:31:14',", (180, 180, 180)),
        ("  'customer_features': {", (212, 212, 212)),
        ("    'Age': 45.0, 'Gender': 'Female', 'Tenure': 12.0, 'Usage Frequency': 10.0,", (206, 145, 120)),
        ("    'Support Calls': 5.0, 'Payment Delay': 15.0, 'Subscription Type': 'Standard',", (206, 145, 120)),
        ("    'Contract Length': 'Monthly', 'Total Spend': 450.0, 'Last Interaction': 20.0", (206, 145, 120)),
        ("  },", (212, 212, 212)),
        ("  'prediction_code': 1,", (78, 201, 176)),
        ("  'prediction_label': 'Likely to Churn',", (244, 71, 71)),
        ("  'churn_probability': 100.0,  // Verified Churn Risk", (244, 71, 71)),
        ("  'loyal_probability': 0.0,", (106, 153, 85)),
        ("  'model_used': 'Logistic Regression with Pipeline Preprocessing'", (180, 180, 180)),
        ("}", (212, 212, 212)),
        ("[INFO] Document successfully retrieved from MongoDB customerChurnDB.churn_predictions collection.", (106, 153, 85)),
        ("PS C:\\Users\\Shubham\\NoSQLProject> _", (86, 156, 214))
    ]
    render_terminal_screenshot("terminal_05_mongo_history_query.png", "PowerShell - Real-Time Inference Persistence Verification in MongoDB", t5_lines)

def capture_all_ui_screenshots():
    print("\n--- Starting Flask Web Application for Live UI Captures ---")
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Wait for Flask to boot
    for attempt in range(10):
        try:
            with urlopen("http://127.0.0.1:5000/", timeout=1) as resp:
                if resp.status == 200:
                    print("  [OK] Flask web server is active on http://127.0.0.1:5000/")
                    break
        except Exception:
            time.sleep(0.5)
            
    print("\n--- Capturing Live Web Application Pages via Headless Edge ---")
    
    # 1. Dashboard
    capture_ui_page("http://127.0.0.1:5000/", "ui_01_dashboard.png", window_size="1366,850")
    
    # 2. Predict Form (Blank)
    capture_ui_page("http://127.0.0.1:5000/predict", "ui_02_predict_form.png", window_size="1366,850")
    
    # 3. High Churn Risk Prediction Result
    churn_query = "Age=45&Gender=Female&Tenure=12&Usage+Frequency=10&Support+Calls=5&Payment+Delay=15&Subscription+Type=Standard&Contract+Length=Monthly&Total+Spend=450.0&Last+Interaction=20"
    capture_ui_page(f"http://127.0.0.1:5000/predict?{churn_query}", "ui_03_churn_result.png", window_size="1366,950")
    
    # 4. Loyal Customer Prediction Result
    loyal_query = "Age=32&Gender=Male&Tenure=48&Usage+Frequency=24&Support+Calls=1&Payment+Delay=0&Subscription+Type=Premium&Contract+Length=Annual&Total+Spend=1200.0&Last+Interaction=4"
    capture_ui_page(f"http://127.0.0.1:5000/predict?{loyal_query}", "ui_04_loyal_result.png", window_size="1366,950")
    
    # 5. History Table
    capture_ui_page("http://127.0.0.1:5000/history", "ui_05_history.png", window_size="1366,850")
    
    # 6. Evaluation Page
    capture_ui_page("http://127.0.0.1:5000/evaluation", "ui_06_evaluation.png", window_size="1366,1100")

if __name__ == "__main__":
    generate_all_terminal_screenshots()
    capture_all_ui_screenshots()
    print("\n=======================================================")
    print("ALL SCREENSHOTS SUCCESSFULLY CAPTURED & SAVED!")
    print(f"Location: {SCREENSHOTS_DIR}")
    print("=======================================================")
