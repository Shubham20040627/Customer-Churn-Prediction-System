"""
Customer Churn Prediction System
Flask Web Application Entry Point
Connects the user interface to MongoDB customerChurnDB and machine learning prediction logic.
"""

import sys
import os

# Add root folder to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, flash, redirect, url_for
import config
from src.database import db_manager
from src.predict import predictor
from src.evaluation import get_evaluation_data


def create_app():
    """Initializes and configures the Flask application."""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = config.FLASK_SECRET_KEY

    # Attempt to pre-load model into memory if already trained
    if predictor.is_model_trained():
        try:
            predictor.get_model()
            print("Model pre-loaded successfully on application startup.")
        except Exception as err:
            print(f"Warning: Could not pre-load model at startup: {err}")

    # ---------------------------------------------------------
    # Route 1: Home / Dashboard
    # ---------------------------------------------------------
    @app.route("/")
    def index():
        counts = db_manager.get_dashboard_counts()
        model_trained = predictor.is_model_trained()

        if not counts["connected"]:
            flash(f"MongoDB Notice: {counts['error']}", "warning")

        return render_template(
            "index.html",
            active_page="home",
            stats=counts,
            model_trained=model_trained
        )

    # ---------------------------------------------------------
    # Route 2: Predict Customer Churn (Form & Result)
    # ---------------------------------------------------------
    @app.route("/predict", methods=["GET", "POST"])
    def predict_page():
        model_trained = predictor.is_model_trained()
        if not model_trained:
            flash(
                "The machine learning model has not been trained yet. "
                "Please run 'python src/train_model.py' before making predictions.",
                "warning"
            )

        result = None
        form_data = None

        req_data = request.form.to_dict() if request.method == "POST" else (request.args.to_dict() if request.args else None)

        if req_data:
            if not model_trained:
                flash("Cannot predict without a trained model. Run 'python src/train_model.py' first.", "danger")
                return redirect(url_for("predict_page"))

            try:
                # Capture form data
                form_data = req_data

                # Run inference and persist to MongoDB
                result = predictor.predict(form_data, save_to_db=True)

                flash(
                    f"Prediction completed! Result: {result['prediction_label']} ({result['churn_probability']}% probability). Saved in MongoDB.",
                    "success"
                )
            except ValueError as val_err:
                flash(f"Input Validation Error: {str(val_err)}", "danger")
            except Exception as err:
                flash(f"Prediction Error: {str(err)}", "danger")

        return render_template(
            "predict.html",
            active_page="predict",
            result=result,
            form_data=form_data,
            model_trained=model_trained
        )

    # ---------------------------------------------------------
    # Route 3: Prediction History
    # ---------------------------------------------------------
    @app.route("/history")
    def history_page():
        # Retrieve recent predictions from MongoDB churn_predictions collection
        predictions = db_manager.get_prediction_history(limit=100)
        return render_template(
            "history.html",
            active_page="history",
            predictions=predictions
        )

    # ---------------------------------------------------------
    # Route 4: Model Evaluation
    # ---------------------------------------------------------
    @app.route("/evaluation")
    def evaluation_page():
        eval_data = get_evaluation_data()
        return render_template(
            "evaluation.html",
            active_page="evaluation",
            evaluation=eval_data
        )

    # ---------------------------------------------------------
    # Error Handlers
    # ---------------------------------------------------------
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template(
            "error.html",
            error_title="404 - Page Not Found",
            error_message="The requested page does not exist on this Customer Churn Prediction portal.",
            active_page=""
        ), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template(
            "error.html",
            error_title="500 - Server Error",
            error_message="An internal server error occurred.",
            error_details=str(e),
            active_page=""
        ), 500

    return app


if __name__ == "__main__":
    app = create_app()
    print("\n" + "="*65)
    print("CUSTOMER CHURN PREDICTION WEB APPLICATION")
    print(f"MongoDB Target: {config.MONGO_URI} (Database: {config.DATABASE_NAME})")
    print(f"Server URL:     http://{config.FLASK_HOST}:{config.FLASK_PORT}/")
    print("="*65 + "\n")
    app.run(
        host=config.FLASK_HOST,
        port=config.FLASK_PORT,
        debug=config.FLASK_DEBUG
    )
