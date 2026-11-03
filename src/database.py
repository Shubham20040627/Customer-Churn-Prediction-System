"""
MongoDB Database Connection and Data Access Layer
Handles PyMongo connections, data loading into DataFrames, and prediction persistence.
"""

import sys
import os
from datetime import datetime, timezone

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

try:
    import config
except ImportError:
    from .. import config



class DatabaseManager:
    """Singleton-style database manager for MongoDB operations."""

    def __init__(self, uri=None, db_name=None):
        self.uri = uri or config.MONGO_URI
        self.db_name = db_name or config.DATABASE_NAME
        self._client = None

    def get_client(self):
        """Creates or returns an active PyMongo client."""
        if self._client is None:
            self._client = MongoClient(
                self.uri,
                serverSelectionTimeoutMS=4000,
                connectTimeoutMS=4000
            )
        return self._client

    def get_db(self):
        """Returns the customerChurnDB database instance."""
        client = self.get_client()
        return client[self.db_name]

    def test_connection(self):
        """
        Verifies that MongoDB is reachable.
        Returns a tuple (is_connected: bool, message: str).
        """
        try:
            client = self.get_client()
            # The ping command is cheap and does not require auth
            client.admin.command('ping')
            return True, "Successfully connected to MongoDB."
        except (ConnectionFailure, ServerSelectionTimeoutError) as err:
            return False, f"Could not connect to MongoDB at {self.uri}. Details: {str(err)}"
        except Exception as err:
            return False, f"Unexpected database error: {str(err)}"

    def get_dashboard_counts(self):
        """
        Fetches dynamic counts for dashboard statistics.
        Returns a dictionary with train, test, and saved prediction counts.
        """
        connected, msg = self.test_connection()
        if not connected:
            return {
                "connected": False,
                "error": msg,
                "train_count": 0,
                "test_count": 0,
                "predictions_count": 0
            }

        try:
            db = self.get_db()
            train_count = db[config.COLLECTIONS.get("raw_train", "customers_train")].estimated_document_count()
            test_count = db[config.COLLECTIONS.get("raw_test", "customers_test")].estimated_document_count()
            predictions_count = db[config.COLLECTIONS["predictions"]].count_documents({})
            train_split_count = db[config.COLLECTIONS.get("train", "customers_train_split")].estimated_document_count()
            test_split_count = db[config.COLLECTIONS.get("test", "customers_test_split")].estimated_document_count()

            return {
                "connected": True,
                "error": None,
                "train_count": train_count,
                "test_count": test_count,
                "predictions_count": predictions_count,
                "train_split_count": train_split_count,
                "test_split_count": test_split_count
            }
        except Exception as err:
            return {
                "connected": False,
                "error": f"Error querying collection counts: {str(err)}",
                "train_count": 0,
                "test_count": 0,
                "predictions_count": 0
            }

    def load_collection_as_dataframe(self, collection_name, limit=None, drop_missing_target=True):
        """
        Loads records from a MongoDB collection into a Pandas DataFrame.
        Safely excludes MongoDB '_id' and handles missing data.
        """
        connected, msg = self.test_connection()
        if not connected:
            raise ConnectionError(msg)

        db = self.get_db()
        col = db[collection_name]

        query = {}
        if drop_missing_target:
            # Exclude corrupt or blank records where the target Churn is null
            query[config.TARGET_COLUMN] = {"$ne": None}

        # Project out the internal MongoDB _id field to keep data clean
        projection = {"_id": 0}

        cursor = col.find(query, projection)
        if limit and limit > 0:
            cursor = cursor.limit(limit)

        data = list(cursor)
        if not data:
            return pd.DataFrame()

        df = pd.DataFrame(data)
        return df

    def get_train_dataframe(self, collection_name=None, limit=None):
        """Fetches the training dataset from customers_train_split."""
        target_collection = collection_name or config.COLLECTIONS.get("train", "customers_train_split")
        return self.load_collection_as_dataframe(
            target_collection,
            limit=limit,
            drop_missing_target=True
        )

    def get_test_dataframe(self, collection_name=None, limit=None):
        """Fetches the testing dataset from customers_test_split."""
        target_collection = collection_name or config.COLLECTIONS.get("test", "customers_test_split")
        return self.load_collection_as_dataframe(
            target_collection,
            limit=limit,
            drop_missing_target=False
        )

    def save_prediction(self, customer_input, prediction_code, prediction_label, probability):
        """
        Saves a new customer prediction result to the churn_predictions collection in MongoDB.
        
        Parameters:
            customer_input (dict): The feature values provided by the user
            prediction_code (int): 0 for Loyal / 1 for Churn
            prediction_label (str): "Unlikely to Churn" or "Likely to Churn"
            probability (dict): Churn probability breakdown {"churn": float, "loyal": float}
        
        Returns:
            str: Inserted document ID as string
        """
        connected, msg = self.test_connection()
        if not connected:
            raise ConnectionError(f"Cannot save prediction: {msg}")

        db = self.get_db()
        col = db[config.COLLECTIONS["predictions"]]

        doc = {
            "timestamp": datetime.now(timezone.utc),
            "formatted_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "customer_features": customer_input,
            "prediction_code": int(prediction_code),
            "prediction_label": prediction_label,
            "churn_probability": float(probability.get("churn", 0.0)),
            "loyal_probability": float(probability.get("loyal", 0.0)),
            "model_used": "Logistic Regression with Pipeline Preprocessing"
        }

        result = col.insert_one(doc)
        return str(result.inserted_id)

    def get_prediction_history(self, limit=100):
        """
        Retrieves saved prediction records from churn_predictions,
        sorted in descending order by timestamp (most recent first).
        """
        connected, msg = self.test_connection()
        if not connected:
            return []

        try:
            db = self.get_db()
            col = db[config.COLLECTIONS["predictions"]]
            cursor = col.find().sort("timestamp", -1).limit(limit)
            records = []
            for doc in cursor:
                doc["_id"] = str(doc["_id"])
                records.append(doc)
            return records
        except Exception as err:
            print(f"Error fetching prediction history: {err}")
            return []


# Global instance for easy import across modules
db_manager = DatabaseManager()
