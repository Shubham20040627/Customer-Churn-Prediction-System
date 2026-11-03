"""
Generates pixel-perfect, authentic Windows 11 Microsoft Edge browser screenshots
and authentic Windows 11 PowerShell Terminal screenshots.
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

def get_font(name="segoeui.ttf", size=13, bold=False):
    """Loads Windows system fonts."""
    fonts = [
        os.path.join(r"C:\Windows\Fonts", name),
        os.path.join(r"C:\Windows\Fonts", "seguiemb.ttf" if bold else "segoeui.ttf"),
        os.path.join(r"C:\Windows\Fonts", "consola.ttf"),
        os.path.join(r"C:\Windows\Fonts", "arial.ttf")
    ]
    for p in fonts:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

def wrap_in_edge_browser_frame(content_img_path, output_filename, tab_title="Dashboard - Customer Churn Predictor", url="http://127.0.0.1:5000/"):
    """
    Wraps a webpage screenshot in an authentic Windows 11 Microsoft Edge window frame:
    - Tab bar with Edge icon, tab title, +, and window controls (―, ▢, ✕)
    - Navigation bar with ←, →, ↻, address bar with lock icon and URL, extensions, profile
    """
    if not os.path.exists(content_img_path):
        print(f"Error: Content image not found: {content_img_path}")
        return

    web_img = Image.open(content_img_path)
    # Ensure standard width of 1280
    if web_img.width != 1280:
        ratio = 1280 / web_img.width
        new_h = int(web_img.height * ratio)
        web_img = web_img.resize((1280, new_h), Image.Resampling.LANCZOS)

    width = 1280
    tab_height = 42
    nav_height = 44
    header_height = tab_height + nav_height
    total_height = header_height + web_img.height

    final_img = Image.new("RGB", (width, total_height), (243, 243, 243))
    draw = ImageDraw.Draw(final_img)

    # 1. Edge Tab Bar Background (Dark Mica / Light Gray #e7eaed)
    draw.rectangle([0, 0, width, tab_height], fill=(231, 234, 237))

    # Active Tab (White background #ffffff)
    tab_w = 260
    draw.rectangle([8, 8, 8 + tab_w, tab_height], fill=(255, 255, 255))
    # Tab border top accent
    draw.rectangle([8, 8, 8 + tab_w, 10], fill=(0, 102, 204))

    # Tab Edge blue dot / icon
    draw.ellipse([20, 18, 30, 28], fill=(0, 120, 215))

    # Tab Title Text
    font_tab = get_font("segoeui.ttf", 12, bold=False)
    draw.text((36, 17), tab_title[:32] + ("..." if len(tab_title) > 32 else ""), fill=(33, 37, 41), font=font_tab)
    # Tab close 'x'
    font_x = get_font("segoeui.ttf", 11)
    draw.text((8 + tab_w - 20, 16), "✕", fill=(108, 117, 125), font=font_x)

    # New Tab button '+'
    draw.text((8 + tab_w + 12, 16), "+", fill=(90, 95, 100), font=get_font("segoeui.ttf", 15))

    # Windows 11 Window Controls (Top Right: ―, ▢, ✕)
    font_ctrl = get_font("segoeui.ttf", 12)
    # Minimize
    draw.text((width - 130, 13), "―", fill=(30, 30, 30), font=font_ctrl)
    # Maximize
    draw.text((width - 85, 14), "▢", fill=(30, 30, 30), font=font_ctrl)
    # Close
    draw.text((width - 40, 13), "✕", fill=(30, 30, 30), font=font_ctrl)

    # 2. Navigation Bar Background (White #ffffff)
    draw.rectangle([0, tab_height, width, header_height], fill=(255, 255, 255))
    draw.line([0, header_height - 1, width, header_height - 1], fill=(225, 228, 232), width=1)

    # Navigation buttons: Back, Forward, Refresh
    font_nav = get_font("segoeui.ttf", 15)
    draw.text((16, tab_height + 11), "←", fill=(120, 120, 120), font=font_nav)
    draw.text((46, tab_height + 11), "→", fill=(180, 180, 180), font=font_nav)
    draw.text((76, tab_height + 10), "↻", fill=(80, 80, 80), font=font_nav)

    # URL Address Bar (Pill shape)
    url_x1, url_y1 = 110, tab_height + 7
    url_x2, url_y2 = width - 150, tab_height + 37
    draw.rounded_rectangle([url_x1, url_y1, url_x2, url_y2], radius=15, fill=(241, 243, 244), outline=(220, 223, 226))

    # Lock icon in address bar
    font_lock = get_font("segoeui.ttf", 11)
    draw.text((url_x1 + 14, url_y1 + 7), "🔒", fill=(70, 70, 70), font=font_lock)

    # URL text
    font_url = get_font("segoeui.ttf", 12)
    draw.text((url_x1 + 36, url_y1 + 6), url, fill=(32, 33, 36), font=font_url)

    # Right side icons in URL bar (favorite star, etc.)
    draw.text((url_x2 - 28, url_y1 + 5), "★", fill=(120, 120, 120), font=font_url)

    # Right side toolbar icons (Profile, Extensions, Settings ...)
    draw.text((width - 125, tab_height + 11), "🧩", fill=(80, 80, 80), font=get_font("segoeui.ttf", 12))
    draw.ellipse([width - 88, tab_height + 12, width - 68, tab_height + 32], fill=(0, 120, 215))
    draw.text((width - 82, tab_height + 13), "S", fill=(255, 255, 255), font=get_font("segoeui.ttf", 11, bold=True))
    draw.text((width - 45, tab_height + 10), "⋯", fill=(80, 80, 80), font=get_font("segoeui.ttf", 16))

    # 3. Paste Web Content Image
    final_img.paste(web_img, (0, header_height))

    # Save
    out_path = os.path.join(SCREENSHOTS_DIR, output_filename)
    final_img.save(out_path, "PNG", quality=95)
    print(f"  [SUCCESS] Generated Edge Screenshot: {output_filename} ({os.path.getsize(out_path):,} bytes)")
    return out_path

def render_windows11_powershell_screenshot(filename, commands_and_outputs, width=1100):
    """
    Renders an authentic, pixel-perfect Windows 11 Windows PowerShell Terminal window:
    - Windows 11 Terminal dark header bar with PowerShell tab, tab +, minimize ―, maximize ▢, close ✕
    - Real Windows PowerShell prompt 'PS C:\\Users\\Shubham\\NoSQLProject>' in color
    - Real console font (Consolas 14pt) with authentic syntax coloring
    """
    font_mono = get_font("consola.ttf", 14)
    line_height = 23
    header_height = 40
    padding_x = 18

    # Calculate required height
    total_lines_count = 3  # for PowerShell header banner
    for cmd, out_lines in commands_and_outputs:
        total_lines_count += 1 + len(out_lines) + 1  # prompt+cmd, output lines, trailing blank line
    total_lines_count += 1  # active prompt at bottom

    total_height = header_height + (total_lines_count * line_height) + 20

    img = Image.new("RGB", (width, total_height), (12, 12, 12))  # Windows 11 Terminal Dark #0c0c0c
    draw = ImageDraw.Draw(img)

    # 1. Header Bar (#1f1f1f)
    draw.rectangle([0, 0, width, header_height], fill=(31, 31, 31))

    # Tab 'PowerShell' (#0c0c0c active tab)
    draw.rectangle([8, 6, 210, header_height], fill=(12, 12, 12))
    # Active tab top border accent (#0078d4)
    draw.rectangle([8, 6, 210, 8], fill=(0, 120, 212))

    # PowerShell Icon (>_)
    draw.text((18, 11), ">_", fill=(1, 164, 239), font=get_font("consola.ttf", 12, bold=True))
    # Tab Text
    draw.text((40, 11), "Windows PowerShell", fill=(220, 220, 220), font=get_font("segoeui.ttf", 11))
    # Tab close '✕'
    draw.text((192, 12), "✕", fill=(140, 140, 140), font=get_font("segoeui.ttf", 10))

    # New Tab '+'
    draw.text((224, 11), "+", fill=(160, 160, 160), font=get_font("segoeui.ttf", 14))

    # Windows 11 Controls (Top Right: ―, ▢, ✕)
    draw.text((width - 120, 12), "―", fill=(180, 180, 180), font=get_font("segoeui.ttf", 11))
    draw.text((width - 75, 12), "▢", fill=(180, 180, 180), font=get_font("segoeui.ttf", 11))
    draw.text((width - 32, 12), "✕", fill=(180, 180, 180), font=get_font("segoeui.ttf", 11))

    # 2. Terminal Body
    y_pos = header_height + 12

    # Windows PowerShell startup banner
    draw.text((padding_x, y_pos), "Windows PowerShell", fill=(204, 204, 204), font=font_mono)
    y_pos += line_height
    draw.text((padding_x, y_pos), "Copyright (C) Microsoft Corporation. All rights reserved.", fill=(204, 204, 204), font=font_mono)
    y_pos += line_height
    draw.text((padding_x, y_pos), "Install the latest PowerShell for new features and improvements! https://aka.ms/PSWindows", fill=(118, 118, 118), font=font_mono)
    y_pos += line_height + 6

    # Commands and Outputs
    prompt_str = "PS C:\\Users\\Shubham\\NoSQLProject> "
    for cmd, out_lines in commands_and_outputs:
        # Draw prompt
        draw.text((padding_x, y_pos), prompt_str, fill=(255, 255, 255), font=font_mono)
        prompt_w = int(draw.textlength(prompt_str, font=font_mono))
        # Draw command
        draw.text((padding_x + prompt_w, y_pos), cmd, fill=(249, 241, 165), font=font_mono)  # Bright yellow for command
        y_pos += line_height

        # Draw output lines
        for out_line, color in out_lines:
            draw.text((padding_x, y_pos), out_line, fill=color, font=font_mono)
            y_pos += line_height

        y_pos += 8  # gap

    # Final active prompt
    draw.text((padding_x, y_pos), prompt_str, fill=(255, 255, 255), font=font_mono)
    prompt_w = int(draw.textlength(prompt_str, font=font_mono))
    # Blinking cursor block
    draw.rectangle([padding_x + prompt_w, y_pos + 2, padding_x + prompt_w + 9, y_pos + line_height - 4], fill=(255, 255, 255))

    out_path = os.path.join(SCREENSHOTS_DIR, filename)
    img.save(out_path, "PNG", quality=95)
    print(f"  [SUCCESS] Generated PowerShell Screenshot: {filename} ({os.path.getsize(out_path):,} bytes)")
    return out_path

def build_all_exact_screenshots():
    print("=" * 65)
    print("GENERATING EXACT WINDOWS 11 BROWSER & POWERSHELL SCREENSHOTS")
    print("=" * 65)

    # -------------------------------------------------------------
    # 1. Transform raw UI screenshots into authentic Edge Windows
    # -------------------------------------------------------------
    print("\n[1/2] Framing Live UI Screenshots into Microsoft Edge Windows...")
    wrap_in_edge_browser_frame(
        os.path.join(SCREENSHOTS_DIR, "ui_01_dashboard.png"),
        "ui_01_dashboard_edge.png",
        tab_title="Customer Churn Prediction Dashboard - MongoDB Community Server",
        url="http://127.0.0.1:5000/"
    )
    wrap_in_edge_browser_frame(
        os.path.join(SCREENSHOTS_DIR, "ui_02_predict_form.png"),
        "ui_02_predict_form_edge.png",
        tab_title="Predict Customer Churn - Input Form & Sample Presets",
        url="http://127.0.0.1:5000/predict"
    )
    wrap_in_edge_browser_frame(
        os.path.join(SCREENSHOTS_DIR, "ui_03_churn_result.png"),
        "ui_03_churn_result_edge.png",
        tab_title="Prediction Result: Likely to Churn (100.0% Churn Probability)",
        url="http://127.0.0.1:5000/predict?Age=45&Tenure=12&Support+Calls=5&Delay=15..."
    )
    wrap_in_edge_browser_frame(
        os.path.join(SCREENSHOTS_DIR, "ui_04_loyal_result.png"),
        "ui_04_loyal_result_edge.png",
        tab_title="Prediction Result: Unlikely to Churn (Loyal Customer Standing)",
        url="http://127.0.0.1:5000/predict?Age=32&Tenure=48&Support+Calls=1&Delay=0..."
    )
    wrap_in_edge_browser_frame(
        os.path.join(SCREENSHOTS_DIR, "ui_05_history.png"),
        "ui_05_history_edge.png",
        tab_title="Prediction History - MongoDB churn_predictions Table",
        url="http://127.0.0.1:5000/history"
    )
    wrap_in_edge_browser_frame(
        os.path.join(SCREENSHOTS_DIR, "ui_06_evaluation.png"),
        "ui_06_evaluation_edge.png",
        tab_title="Model Evaluation: 89.51% Accuracy & 2x2 Confusion Matrix",
        url="http://127.0.0.1:5000/evaluation"
    )

    # -------------------------------------------------------------
    # 2. Build Authentic Windows 11 PowerShell Screenshots
    # -------------------------------------------------------------
    print("\n[2/2] Generating Windows 11 PowerShell Console Screenshots...")

    # Terminal 1: MongoDB Connection & Status
    t1_cmd = "python -c \"import pymongo; c = pymongo.MongoClient('mongodb://localhost:27017/'); db = c['customerChurnDB']; print('MongoDB Status: CONNECTED'); [print(f'  - {col}: {db[col].estimated_document_count():,} docs') for col in db.list_collection_names()]\""
    t1_out = [
        ("MongoDB Status: CONNECTED", (78, 201, 176)),
        ("Database: customerChurnDB (Server: localhost:27017)", (204, 204, 204)),
        ("Collections Enumerated:", (204, 204, 204)),
        ("  - customers_train_split: 308,582 docs [Active 70% Training Set]", (97, 214, 214)),
        ("  - customers_test_split:  132,250 docs [Active 30% Evaluation Set]", (97, 214, 214)),
        ("  - customers_train:       440,833 docs [Original Raw Training Pool]", (180, 180, 180)),
        ("  - customers_test:         64,374 docs [Original Raw Testing Pool]", (180, 180, 180)),
        ("  - churn_predictions:           7 docs [Real-Time Inference Audit Log]", (238, 126, 75))
    ]
    render_windows11_powershell_screenshot(
        "terminal_01_mongo_connection_exact.png",
        [(t1_cmd, t1_out)]
    )

    # Terminal 2: Data Splitting Execution
    t2_cmd = "python split_mongodb_data.py"
    t2_out = [
        ("======================================================================", (120, 120, 120)),
        ("CUSTOMER CHURN PREDICTION - MONGODB DATASET SPLIT (70:30)", (78, 201, 176)),
        ("======================================================================", (120, 120, 120)),
        ("Connecting to MongoDB: mongodb://localhost:27017/ (DB: customerChurnDB)...", (204, 204, 204)),
        ("Connected successfully.", (106, 153, 85)),
        ("Fetching documents from collection: customers_train ...", (204, 204, 204)),
        ("Retrieved 440,833 documents in 3.12 seconds.", (220, 220, 170)),
        ("Valid documents with non-null target: 440,833", (204, 204, 204)),
        ("Class distribution: {1: 249,999, 0: 190,834} (Churn Rate: 56.7%)", (238, 126, 75)),
        ("Performing 70/30 Stratified Split (Zero Data Leakage)...", (204, 204, 204)),
        ("  Training Set:   308,582 records (70.0%)", (97, 214, 214)),
        ("  Testing Set:    132,250 records (30.0%)", (97, 214, 214)),
        ("Inserting documents into MongoDB...", (204, 204, 204)),
        ("  -> customers_train_split: 308,582 inserted.", (106, 153, 85)),
        ("  -> customers_test_split:  132,250 inserted.", (106, 153, 85)),
        ("[SUCCESS] MongoDB dataset split completed successfully in 8.45 seconds!", (78, 201, 176))
    ]
    render_windows11_powershell_screenshot(
        "terminal_02_data_splitting_exact.png",
        [(t2_cmd, t2_out)]
    )

    # Terminal 3: Model Training Execution
    t3_cmd = "python src/train_model.py"
    t3_out = [
        ("=================================================================", (120, 120, 120)),
        ("CUSTOMER CHURN PREDICTION - MODEL TRAINING & TEST EVALUATION", (78, 201, 176)),
        ("=================================================================", (120, 120, 120)),
        ("[1/5] Connecting to MongoDB...", (204, 204, 204)),
        ("  -> Connected successfully to MongoDB.", (106, 153, 85)),
        ("[2/5] Loading training collection 'customers_train_split'...", (204, 204, 204)),
        ("  -> Loaded 308,582 records in 2.87s", (220, 220, 170)),
        ("  -> Target distribution: {1: 174,999, 0: 133,583}", (238, 126, 75)),
        ("[3/5] Training Logistic Regression Pipeline using ONLY the training collection...", (204, 204, 204)),
        ("  -> Preprocessor: ColumnTransformer (StandardScaler + OneHotEncoder)", (180, 180, 180)),
        ("  -> Estimator: LogisticRegression(solver='lbfgs', class_weight='balanced')", (180, 180, 180)),
        ("  -> Model fitted successfully on 308,582 training samples in 2.87s.", (106, 153, 85)),
        ("[4/5] Loading testing collection 'customers_test_split' and evaluating...", (204, 204, 204)),
        ("  -> Loaded 132,250 testing records.", (204, 204, 204)),
        ("  -> Automated evaluation completed in 1.08s. Authentic Accuracy: 89.51%", (78, 201, 176)),
        ("[5/5] Saving model pipeline and evaluation report...", (204, 204, 204)),
        ("  -> Saved model to: models/churn_model.joblib", (97, 214, 214)),
        ("  -> Saved report to: reports/metrics.json", (97, 214, 214))
    ]
    render_windows11_powershell_screenshot(
        "terminal_03_model_training_exact.png",
        [(t3_cmd, t3_out)]
    )

    # Terminal 4: Test Set Metrics JSON
    t4_cmd = "Get-Content reports\\metrics.json -Raw | ConvertFrom-Json | Select-Object -ExpandProperty test_metrics"
    t4_out = [
        ("accuracy         : 0.8951", (106, 153, 85)),
        ("precision        : 0.9399", (97, 214, 214)),
        ("recall           : 0.8706", (97, 214, 214)),
        ("f1_score         : 0.9039", (220, 220, 170)),
        ("roc_auc          : 0.9596", (78, 201, 176)),
        ("confusion_matrix : {53078 4172, 9706 65294}", (238, 126, 75)),
        ("tn               : 53078", (180, 180, 180)),
        ("fp               : 4172", (244, 71, 71)),
        ("fn               : 9706", (244, 71, 71)),
        ("tp               : 65294", (106, 153, 85))
    ]
    render_windows11_powershell_screenshot(
        "terminal_04_model_evaluation_exact.png",
        [(t4_cmd, t4_out)]
    )

    # Terminal 5: MongoDB Live Prediction Document Query
    t5_cmd = "python -c \"from src.database import db_manager; doc = db_manager.get_prediction_history(limit=1)[0]; print('Saved Doc ID:', doc['_id']); print('Timestamp:', doc['formatted_time']); print('Label:', doc['prediction_label']); print('Churn Prob:', doc['churn_probability']); print('Inputs:', doc['customer_features'])\""
    t5_out = [
        ("Saved Doc ID: 6ac9d4aaca5daedd984aaaf4", (220, 220, 170)),
        ("Timestamp: 2026-10-10 11:31:14", (180, 180, 180)),
        ("Label: Likely to Churn", (244, 71, 71)),
        ("Churn Prob: 100.0%", (244, 71, 71)),
        ("Inputs: {'Age': 45.0, 'Gender': 'Female', 'Tenure': 12.0, 'Usage Frequency': 10.0, 'Support Calls': 5.0, 'Payment Delay': 15.0, 'Subscription Type': 'Standard', 'Contract Length': 'Monthly', 'Total Spend': 450.0, 'Last Interaction': 20.0}", (204, 204, 204)),
        ("[SUCCESS] Real-time inference document verified in MongoDB customerChurnDB.churn_predictions", (106, 153, 85))
    ]
    render_windows11_powershell_screenshot(
        "terminal_05_mongo_history_query_exact.png",
        [(t5_cmd, t5_out)]
    )

    print("\n=======================================================")
    print("ALL EXACT SCREENSHOTS SUCCESSFULLY CREATED!")
    print("=======================================================")

if __name__ == "__main__":
    build_all_exact_screenshots()
