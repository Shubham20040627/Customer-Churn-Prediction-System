"""
Data Exploration and Inspection Module
Connects to MongoDB, loads collections into DataFrames, and displays dataset shape,
column names, data types, missing values, and descriptive statistics.
"""

import sys
import os

# Add parent directory to path so config can be imported directly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
try:
    import config
    from src.database import db_manager
except ImportError:
    from .. import config
    from .database import db_manager


def inspect_dataset(df, name="Dataset"):
    """
    Performs full exploratory analysis on a DataFrame and returns a structured summary.
    """
    print(f"\n{'='*30} {name.upper()} EXPLORATION {'='*30}")
    
    if df.empty:
        print(f"Warning: {name} is empty!")
        return {"shape": (0, 0), "empty": True}

    shape = df.shape
    columns = df.columns.tolist()
    dtypes = {col: str(dtype) for col, dtype in df.dtypes.items()}
    missing_values = df.isnull().sum().to_dict()
    total_missing = sum(missing_values.values())

    print(f"1. Dataset Shape: {shape[0]:,} rows x {shape[1]} columns")
    print(f"2. Total Missing Values: {total_missing:,}")
    
    print("\n3. Column Types and Null Counts:")
    info_table = []
    for col in columns:
        null_cnt = missing_values[col]
        null_pct = (null_cnt / shape[0]) * 100 if shape[0] > 0 else 0
        info_table.append({
            "Column": col,
            "Type": dtypes[col],
            "Null Count": null_cnt,
            "Null %": f"{null_pct:.2f}%"
        })
    info_df = pd.DataFrame(info_table)
    print(info_df.to_string(index=False))

    # Identify features
    numerical_cols = [c for c in config.NUMERICAL_FEATURES if c in df.columns]
    categorical_cols = [c for c in config.CATEGORICAL_FEATURES if c in df.columns]

    print(f"\n4. Identified Numerical Features ({len(numerical_cols)}): {numerical_cols}")
    print(f"5. Identified Categorical Features ({len(categorical_cols)}): {categorical_cols}")

    if config.TARGET_COLUMN in df.columns:
        print(f"\n6. Target Column '{config.TARGET_COLUMN}' Value Distribution:")
        val_counts = df[config.TARGET_COLUMN].value_counts(dropna=False)
        val_pcts = df[config.TARGET_COLUMN].value_counts(normalize=True, dropna=False) * 100
        target_summary = pd.DataFrame({
            "Count": val_counts,
            "Percentage (%)": val_pcts.round(2)
        })
        print(target_summary)

    if numerical_cols:
        print("\n7. Numerical Features Descriptive Statistics:")
        stats = df[numerical_cols].describe().T[["mean", "std", "min", "25%", "50%", "75%", "max"]]
        print(stats.round(2))
    else:
        stats = pd.DataFrame()

    if categorical_cols:
        print("\n8. Categorical Features Unique Values:")
        for col in categorical_cols:
            unique_vals = df[col].unique().tolist()
            print(f"   - {col}: {unique_vals}")

    print(f"{'='*75}\n")

    return {
        "name": name,
        "shape": shape,
        "columns": columns,
        "dtypes": dtypes,
        "missing_values": missing_values,
        "numerical_cols": numerical_cols,
        "categorical_cols": categorical_cols,
        "stats": stats.to_dict() if not stats.empty else {}
    }


def run_exploration():
    """Fetches records from MongoDB and prints exploration reports for both train and test collections."""
    print("Connecting to MongoDB customerChurnDB...")
    connected, msg = db_manager.test_connection()
    if not connected:
        print(f"Error: {msg}")
        return

    print("Fetching training data from MongoDB collection 'customers_train'...")
    # Fetch a representative sample for fast terminal exploration, or full set
    train_df = db_manager.get_train_dataframe(limit=50000)
    inspect_dataset(train_df, name="customers_train (Sample of 50,000 records)")

    print("Fetching test data from MongoDB collection 'customers_test'...")
    test_df = db_manager.get_test_dataframe(limit=10000)
    inspect_dataset(test_df, name="customers_test (Sample of 10,000 records)")


if __name__ == "__main__":
    run_exploration()
