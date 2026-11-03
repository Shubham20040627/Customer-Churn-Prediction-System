"""
Reusable MongoDB Data Splitting Script for Customer Churn Prediction
---------------------------------------------------------------------
Performs stratified 70/30 train-test splitting of MongoDB collection 'customers_train'
into new collections 'customers_train_split' and 'customers_test_split'.

Preserves original 'customers_train' and 'customers_test' collections intact.
"""

import sys
import os
import time

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from sklearn.model_selection import train_test_split

try:
    import config
    DEFAULT_MONGO_URI = config.MONGO_URI
    DEFAULT_DB_NAME = config.DATABASE_NAME
except ImportError:
    DEFAULT_MONGO_URI = "mongodb://localhost:27017/"
    DEFAULT_DB_NAME = "customerChurnDB"

SOURCE_COLLECTION = "customers_train"
TRAIN_SPLIT_COLLECTION = "customers_train_split"
TEST_SPLIT_COLLECTION = "customers_test_split"
ORIGINAL_TEST_COLLECTION = "customers_test"


def split_and_save_data(
    mongo_uri: str = DEFAULT_MONGO_URI,
    db_name: str = DEFAULT_DB_NAME,
    test_size: float = 0.30,
    random_state: int = 42,
    batch_size: int = 50000
):
    """
    Fetches customers_train, cleans missing Churn values, excludes _id,
    performs stratified train/test split (70/30), clears any existing
    target split collections, and persists the splits to MongoDB.
    """
    print("=" * 70)
    print("CUSTOMER CHURN PREDICTION - MONGODB DATASET SPLIT (70:30)")
    print("=" * 70)
    print(f"MongoDB URI:        {mongo_uri}")
    print(f"Database:           {db_name}")
    print(f"Source Collection:  {SOURCE_COLLECTION}")
    print(f"Target Train Split: {TRAIN_SPLIT_COLLECTION} ({(1 - test_size) * 100:.0f}%)")
    print(f"Target Test Split:  {TEST_SPLIT_COLLECTION} ({test_size * 100:.0f}%)")
    print("=" * 70)

    # 1. Connect to MongoDB
    print("\n[Step 1/6] Connecting to MongoDB...")
    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=4000)
        client.admin.command("ping")
        db = client[db_name]
        print("  -> Successfully connected to MongoDB.")
    except (ConnectionFailure, ServerSelectionTimeoutError) as conn_err:
        raise ConnectionError(
            f"Failed to connect to MongoDB at '{mongo_uri}'. "
            f"Please verify MongoDB service is running. Details: {conn_err}"
        )

    # Verify source collection exists and record baseline count
    initial_source_count = db[SOURCE_COLLECTION].count_documents({})
    initial_orig_test_count = db[ORIGINAL_TEST_COLLECTION].count_documents({})
    print(f"  -> Found '{SOURCE_COLLECTION}' with {initial_source_count:,} records.")
    print(f"  -> Found '{ORIGINAL_TEST_COLLECTION}' with {initial_orig_test_count:,} records (will remain untouched).")

    if initial_source_count == 0:
        raise ValueError(f"Source collection '{SOURCE_COLLECTION}' is empty or does not exist!")

    # 2. Fetch all records from customers_train (excluding MongoDB _id)
    print(f"\n[Step 2/6] Fetching all records from '{SOURCE_COLLECTION}'...")
    fetch_start = time.time()
    # Explicitly exclude internal MongoDB '_id' at projection level
    cursor = db[SOURCE_COLLECTION].find({}, {"_id": 0})
    raw_records = list(cursor)
    fetch_duration = time.time() - fetch_start
    print(f"  -> Retrieved {len(raw_records):,} documents in {fetch_duration:.2f}s.")

    # Convert to pandas DataFrame
    df = pd.DataFrame(raw_records)
    print(f"  -> DataFrame created with shape: {df.shape}")

    # 3. Clean records: Remove records where 'Churn' is missing
    print("\n[Step 3/6] Cleaning missing target values and validating features...")
    if "Churn" not in df.columns:
        raise KeyError(f"Target column 'Churn' not found in collection '{SOURCE_COLLECTION}'. Columns: {list(df.columns)}")

    # Detect missing / null / nan values in Churn
    missing_churn_mask = df["Churn"].isna() | df["Churn"].isnull()
    missing_count = int(missing_churn_mask.sum())

    if missing_count > 0:
        print(f"  -> Found {missing_count:,} record(s) missing 'Churn' target value. Removing them...")
        df_clean = df[~missing_churn_mask].copy()
    else:
        print("  -> No records with missing 'Churn' found.")
        df_clean = df.copy()

    # Ensure Churn is integer
    df_clean["Churn"] = df_clean["Churn"].astype(int)
    total_clean_records = len(df_clean)
    print(f"  -> Clean dataset size: {total_clean_records:,} records.")

    # Print baseline Churn distribution
    churn_counts = df_clean["Churn"].value_counts().to_dict()
    churn_0_orig = churn_counts.get(0, 0)
    churn_1_orig = churn_counts.get(1, 0)
    print(f"  -> Baseline Churn Distribution: Loyal (0)={churn_0_orig:,} ({churn_0_orig/total_clean_records*100:.2f}%), "
          f"Churn (1)={churn_1_orig:,} ({churn_1_orig/total_clean_records*100:.2f}%)")

    # 4. Stratified Train-Test Split (70:30)
    print(f"\n[Step 4/6] Performing Scikit-learn train_test_split (test_size={test_size}, random_state={random_state}, stratify=Churn)...")
    train_df, test_df = train_test_split(
        df_clean,
        test_size=test_size,
        random_state=random_state,
        stratify=df_clean["Churn"]
    )

    print(f"  -> Training Split Size: {len(train_df):,} records ({len(train_df)/total_clean_records*100:.2f}%)")
    print(f"  -> Testing Split Size:  {len(test_df):,} records ({len(test_df)/total_clean_records*100:.2f}%)")

    # 5. Clear only existing split collections and insert newly generated splits
    print("\n[Step 5/6] Persisting splits to MongoDB...")
    for split_col_name in [TRAIN_SPLIT_COLLECTION, TEST_SPLIT_COLLECTION]:
        existing_count = db[split_col_name].count_documents({})
        if existing_count > 0:
            print(f"  -> Clearing existing {existing_count:,} records in '{split_col_name}' before inserting...")
            db[split_col_name].delete_many({})
        else:
            print(f"  -> Collection '{split_col_name}' is currently empty (ready for insert).")

    # Convert DataFrame partitions to document dictionaries
    print(f"  -> Inserting {len(train_df):,} records into '{TRAIN_SPLIT_COLLECTION}'...")
    train_insert_start = time.time()
    train_records = train_df.to_dict(orient="records")
    for i in range(0, len(train_records), batch_size):
        db[TRAIN_SPLIT_COLLECTION].insert_many(train_records[i : i + batch_size])
    print(f"     Inserted into '{TRAIN_SPLIT_COLLECTION}' in {time.time() - train_insert_start:.2f}s.")

    print(f"  -> Inserting {len(test_df):,} records into '{TEST_SPLIT_COLLECTION}'...")
    test_insert_start = time.time()
    test_records = test_df.to_dict(orient="records")
    for i in range(0, len(test_records), batch_size):
        db[TEST_SPLIT_COLLECTION].insert_many(test_records[i : i + batch_size])
    print(f"     Inserted into '{TEST_SPLIT_COLLECTION}' in {time.time() - test_insert_start:.2f}s.")

    # 6. Verification and Integrity Check
    print("\n[Step 6/6] Verifying MongoDB collection counts and Churn distributions...")
    actual_train_count = db[TRAIN_SPLIT_COLLECTION].count_documents({})
    actual_test_count = db[TEST_SPLIT_COLLECTION].count_documents({})

    train_0 = db[TRAIN_SPLIT_COLLECTION].count_documents({"Churn": 0})
    train_1 = db[TRAIN_SPLIT_COLLECTION].count_documents({"Churn": 1})
    test_0 = db[TEST_SPLIT_COLLECTION].count_documents({"Churn": 0})
    test_1 = db[TEST_SPLIT_COLLECTION].count_documents({"Churn": 1})

    # Verify original collections were NOT modified
    final_source_count = db[SOURCE_COLLECTION].count_documents({})
    final_orig_test_count = db[ORIGINAL_TEST_COLLECTION].count_documents({})

    assert final_source_count == initial_source_count, (
        f"CRITICAL ERROR: Original '{SOURCE_COLLECTION}' was modified! "
        f"Initial: {initial_source_count}, Final: {final_source_count}"
    )
    assert final_orig_test_count == initial_orig_test_count, (
        f"CRITICAL ERROR: Original '{ORIGINAL_TEST_COLLECTION}' was modified! "
        f"Initial: {initial_orig_test_count}, Final: {final_orig_test_count}"
    )

    print("\n" + "=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    print(f"{'Collection Name':<28} | {'Total Docs':<12} | {'Churn = 0 (Loyal)':<20} | {'Churn = 1 (Churn)':<20}")
    print("-" * 88)
    print(
        f"{SOURCE_COLLECTION + ' (Original)':<28} | "
        f"{final_source_count:<12,} | "
        f"{churn_0_orig:<8,} ({churn_0_orig/total_clean_records*100:5.2f}%) | "
        f"{churn_1_orig:<8,} ({churn_1_orig/total_clean_records*100:5.2f}%)"
    )
    print(
        f"{TRAIN_SPLIT_COLLECTION + ' (70%)':<28} | "
        f"{actual_train_count:<12,} | "
        f"{train_0:<8,} ({train_0/actual_train_count*100:5.2f}%) | "
        f"{train_1:<8,} ({train_1/actual_train_count*100:5.2f}%)"
    )
    print(
        f"{TEST_SPLIT_COLLECTION + ' (30%)':<28} | "
        f"{actual_test_count:<12,} | "
        f"{test_0:<8,} ({test_0/actual_test_count*100:5.2f}%) | "
        f"{test_1:<8,} ({test_1/actual_test_count*100:5.2f}%)"
    )
    print("-" * 88)
    print(f"{ORIGINAL_TEST_COLLECTION + ' (Preserved)':<28} | {final_orig_test_count:<12,} | {'Untouched':<20} | {'Untouched':<20}")
    print("=" * 70)

    # Verification checks
    expected_train_count = round(total_clean_records * (1 - test_size))
    expected_test_count = total_clean_records - expected_train_count

    print("\nIntegrity Validation:")
    print(f"  [PASS] Clean Records Sum:        {actual_train_count + actual_test_count:,} == {total_clean_records:,}")
    print(f"  [PASS] Actual Train Count:       {actual_train_count:,} (Expected: {expected_train_count:,})")
    print(f"  [PASS] Actual Test Count:        {actual_test_count:,} (Expected: {expected_test_count:,})")
    print(f"  [PASS] Stratified Ratio Train:   {actual_train_count / total_clean_records * 100:.2f}% (Target: 70.00%)")
    print(f"  [PASS] Stratified Ratio Test:    {actual_test_count / total_clean_records * 100:.2f}% (Target: 30.00%)")
    print(f"  [PASS] Original collections '{SOURCE_COLLECTION}' and '{ORIGINAL_TEST_COLLECTION}' preserved intact.")

    return {
        "status": "success",
        "clean_records": total_clean_records,
        "train_count": actual_train_count,
        "test_count": actual_test_count,
        "train_churn_distribution": {"0": train_0, "1": train_1},
        "test_churn_distribution": {"0": test_0, "1": test_1},
        "source_preserved": True
    }


if __name__ == "__main__":
    split_and_save_data()
