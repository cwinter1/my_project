# ══════════════════════════════════════════════════════════════
#  WEEK 7  |  DAY 4  |  DATA LOADING
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Load data to CSV files — both full refresh and incremental append modes
#  2. Load a DataFrame to a SQLite database using to_sql with replace/append
#  3. Verify a load with row count checks, sample comparison, and logging
#
#  TIME:  ~30-35 minutes
#
#  YOUTUBE
#  ───────
#  Search: "pandas to_csv to_sql load data tutorial"
#  Search: "Python ETL load verification row count"
#
# ══════════════════════════════════════════════════════════════

import pandas as pd
import sqlite3
import os
from datetime import datetime

this_dir = os.path.dirname(__file__)

# Sample clean DataFrame (as if it just came out of the transform stage)
clean_sales = pd.DataFrame({
    "sale_id":      range(1, 11),
    "sale_date":    ["2024-01-10", "2024-01-15", "2024-01-22", "2024-02-03",
                     "2024-02-10", "2024-02-18", "2024-03-01", "2024-03-12",
                     "2024-03-22", "2024-04-05"],
    "rep_name":     ["Alice Ng", "Bob Chen", "Carol Diaz", "Alice Ng", "Dave Park",
                     "Eve Torres", "Carol Diaz", "Bob Chen", "Grace Lee", "Alice Ng"],
    "region":       ["West", "East", "West", "West", "Central",
                     "East", "West", "East", "East", "West"],
    "product":      ["Laptop", "Monitor", "Keyboard", "Headset", "Webcam",
                     "Monitor", "Laptop", "Keyboard", "Headset", "Mouse"],
    "quantity":     [1, 2, 3, 1, 4, 1, 2, 5, 1, 3],
    "net_revenue":  [1169.99, 759.98, 449.97, 169.99, 359.96,
                     399.99, 2209.98, 674.95, 169.99, 223.97],
})

print("=== CLEAN SALES DATA TO LOAD ===")
print(clean_sales)
print(f"Shape: {clean_sales.shape}")


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — LOADING TO CSV (FULL AND INCREMENTAL/APPEND)
# ══════════════════════════════════════════════════════════════
#
# FULL LOAD:
#   Write the entire DataFrame to a new file (or overwrite existing).
#   Used when you want a fresh, complete snapshot each time.
#   df.to_csv("output.csv", index=False)
#
# INCREMENTAL/APPEND LOAD:
#   Add new rows to an existing file without rewriting it.
#   Used for logs, history tables, and cumulative exports.
#   df.to_csv("output.csv", mode="a", header=False, index=False)
#
# KEY PARAMETERS:
#   index=False          -- do not write the row number as a column
#   mode="w"             -- write (overwrite) [default]
#   mode="a"             -- append to existing file
#   header=True/False    -- write column names as header row
#   encoding="utf-8"     -- consistent text encoding

# EXAMPLE ──────────────────────────────────────────────────────

def load_to_csv_full(df, output_path):
    """
    Full refresh: overwrite the CSV with the entire DataFrame.
    Returns the number of rows written.
    """
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"[LOAD CSV] Full load: {len(df)} rows -> {os.path.basename(output_path)}")
    return len(df)

def load_to_csv_append(df, output_path):
    """
    Incremental append: add new rows to an existing CSV.
    If the file does not exist, creates it with a header.
    Returns the number of rows appended.
    """
    file_exists = os.path.exists(output_path)
    df.to_csv(
        output_path,
        mode="a",
        header=not file_exists,  # write header only if file is new
        index=False,
        encoding="utf-8",
    )
    print(f"[LOAD CSV] Appended: {len(df)} rows -> {os.path.basename(output_path)}")
    return len(df)

# Full load
full_output = os.path.join(this_dir, "sales_full.csv")
rows_written = load_to_csv_full(clean_sales, full_output)

# Verify
df_verify = pd.read_csv(full_output)
print(f"Verification — rows in file: {len(df_verify)}")   # should match rows_written

# Incremental load — simulate three daily runs
daily_run_1 = clean_sales.iloc[:3].copy()
daily_run_2 = clean_sales.iloc[3:7].copy()
daily_run_3 = clean_sales.iloc[7:].copy()

incremental_output = os.path.join(this_dir, "sales_incremental.csv")

# Remove old file if it exists (for clean demo)
if os.path.exists(incremental_output):
    os.remove(incremental_output)

load_to_csv_append(daily_run_1, incremental_output)
load_to_csv_append(daily_run_2, incremental_output)
load_to_csv_append(daily_run_3, incremental_output)

# Verify cumulative rows
df_cum = pd.read_csv(incremental_output)
print(f"\nIncremental file rows after 3 runs: {len(df_cum)}")   # 10


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1 — Timestamped Export
# ══════════════════════════════════════════════════════════════
#
# Write a function called load_with_timestamp(df, output_dir, base_name) that:
#   1. Generates a timestamped filename: "<base_name>_<YYYYMMDD_HHMMSS>.csv"
#      Use datetime.now().strftime("%Y%m%d_%H%M%S")
#   2. Saves the DataFrame to that file (full load, index=False)
#   3. Prints: "Saved <rows> rows to <filename>"
#   4. Returns the full file path
#
# Call it with clean_sales, this_dir, and "sales_export"
# Print the returned path.
#
# Expected output:
#     Saved 10 rows to sales_export_20240101_120000.csv
#     Full path: c:\...\sales_export_20240101_120000.csv





# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — LOADING TO SQLite DATABASE (to_sql, if_exists)
# ══════════════════════════════════════════════════════════════
#
# pandas to_sql() writes a DataFrame directly to a SQL table.
# Works with any SQLAlchemy-compatible database (SQLite, PostgreSQL, SQL Server).
#
# Syntax:
#   df.to_sql("table_name", connection_or_engine, if_exists="replace", index=False)
#
# if_exists options:
#   "fail"    -- raise error if table exists (safe default)
#   "replace" -- drop and recreate the table (full refresh)
#   "append"  -- insert rows into existing table (incremental)
#
# IMPORTANT: to_sql() with sqlite3 connection works directly.
# For production databases (SQL Server, PostgreSQL), use SQLAlchemy engine.

# EXAMPLE ──────────────────────────────────────────────────────

db_path = os.path.join(this_dir, "sales_warehouse.db")

# Remove old DB for clean demo
if os.path.exists(db_path):
    os.remove(db_path)

# Full load to SQLite
conn = sqlite3.connect(db_path)

# First load: full replace (creates or overwrites the table)
clean_sales.to_sql("fact_sales", conn, if_exists="replace", index=False)
print(f"\n[LOAD DB] Full load: {len(clean_sales)} rows to fact_sales")

# Verify
df_db = pd.read_sql("SELECT COUNT(*) AS row_count FROM fact_sales", conn)
print(f"DB row count: {df_db['row_count'].iloc[0]}")

# Append: simulate loading next day's new records
new_records = pd.DataFrame({
    "sale_id":     [11, 12],
    "sale_date":   ["2024-04-10", "2024-04-11"],
    "rep_name":    ["Bob Chen", "Eve Torres"],
    "region":      ["East", "East"],
    "product":     ["Laptop", "Webcam"],
    "quantity":    [1, 2],
    "net_revenue": [1169.99, 161.99],
})

new_records.to_sql("fact_sales", conn, if_exists="append", index=False)
print(f"[LOAD DB] Appended: {len(new_records)} rows to fact_sales")

# Verify append
df_after = pd.read_sql("SELECT COUNT(*) AS row_count FROM fact_sales", conn)
print(f"DB row count after append: {df_after['row_count'].iloc[0]}")   # should be 12

# Create a dimension table
dim_products = pd.DataFrame({
    "product":    ["Laptop", "Monitor", "Keyboard", "Headset", "Webcam", "Mouse"],
    "category":   ["Electronics", "Electronics", "Accessories", "Accessories", "Peripherals", "Accessories"],
    "unit_price": [1299.99, 399.99, 149.99, 199.99, 89.99, 79.99],
})
dim_products.to_sql("dim_products", conn, if_exists="replace", index=False)
print(f"[LOAD DB] dim_products: {len(dim_products)} rows")

conn.close()
print("Database saved to:", db_path)


# ══════════════════════════════════════════════════════════════
#  EXERCISE 2 — Upsert Pattern
# ══════════════════════════════════════════════════════════════
#
# In production, you often want to "upsert" data: insert new rows and
# update existing rows (replace if duplicate key).
# SQLite does not have MERGE, but we can simulate it.
#
# Write a function called upsert_to_sqlite(df, db_path, table_name, key_col) that:
#   1. Opens a connection to db_path
#   2. Tries to read the existing table into a DataFrame (or starts with empty)
#   3. Concatenates the new df with the existing data
#   4. Drops duplicates based on key_col, keeping the LAST occurrence (new data wins)
#   5. Writes the result back with if_exists="replace"
#   6. Returns the final row count
#
# Call it with clean_sales, db_path, "fact_sales", "sale_id"
# Then call it again with updated_records (some existing, some new)
# Print row counts before and after.
#
# Expected output:
#     After initial load: 12 rows
#     After upsert: 13 rows (1 new + 1 updated, no duplicates)

# --- starting data ---
updated_records = pd.DataFrame({
    "sale_id":     [5, 13],       # sale_id=5 is an update, sale_id=13 is new
    "sale_date":   ["2024-02-10", "2024-04-15"],
    "rep_name":    ["Dave Park", "Alice Ng"],
    "region":      ["Central", "West"],
    "product":     ["Webcam", "Laptop"],
    "quantity":    [6, 2],        # sale_id=5 quantity changed from 4 to 6
    "net_revenue": [539.94, 2339.98],
})





# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — LOAD VERIFICATION: ROW COUNTS, SAMPLES, LOGGING
# ══════════════════════════════════════════════════════════════
#
# After every load, verify that:
#   1. The row count in the destination matches what was loaded
#   2. A sample of the data looks correct (spot check)
#   3. The load is logged with timestamp, row counts, and status
#
# This protects against silent failures (partial loads, truncations, etc.)

# EXAMPLE ──────────────────────────────────────────────────────

def verify_csv_load(source_df, output_path):
    """
    Verify a CSV load was successful.
    Returns a dict with verification results.
    """
    result = {
        "output_path": output_path,
        "expected_rows": len(source_df),
        "actual_rows": None,
        "row_count_match": False,
        "sample_match": False,
        "status": "unknown",
    }

    try:
        df_loaded = pd.read_csv(output_path)
        result["actual_rows"] = len(df_loaded)
        result["row_count_match"] = (result["actual_rows"] == result["expected_rows"])

        # Sample check: compare first and last row values
        if len(df_loaded) > 0 and len(source_df) > 0:
            first_match = (source_df.iloc[0].tolist() == df_loaded.iloc[0].tolist())
            last_match  = (source_df.iloc[-1].tolist() == df_loaded.iloc[-1].tolist())
            result["sample_match"] = first_match and last_match

        result["status"] = "pass" if (result["row_count_match"] and result["sample_match"]) else "fail"
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)

    return result

def log_pipeline_run(pipeline_name, rows_extracted, rows_loaded, status, log_path):
    """
    Append a run record to a pipeline log CSV.
    """
    run_record = pd.DataFrame([{
        "timestamp":       datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "pipeline":        pipeline_name,
        "rows_extracted":  rows_extracted,
        "rows_loaded":     rows_loaded,
        "status":          status,
    }])
    file_exists = os.path.exists(log_path)
    run_record.to_csv(log_path, mode="a", header=not file_exists, index=False)
    print(f"[LOG] Run recorded: {status}")

# Verify the full CSV load
print("\n=== LOAD VERIFICATION ===")
verify_result = verify_csv_load(clean_sales, full_output)
for key, value in verify_result.items():
    print(f"  {key:<20}: {value}")

# Log the run
log_path = os.path.join(this_dir, "pipeline_run_log.csv")
log_pipeline_run("daily_sales_etl", len(clean_sales), len(clean_sales), "success", log_path)
log_pipeline_run("daily_sales_etl", 15, 15, "success", log_path)

# Read log back
df_log = pd.read_csv(log_path)
print("\n=== PIPELINE RUN LOG ===")
print(df_log)


# ══════════════════════════════════════════════════════════════
#  EXERCISE 3 — Full Load Verification Suite
# ══════════════════════════════════════════════════════════════
#
# Write a function called run_load_verification(source_df, db_path, table_name) that:
#   1. Connects to the SQLite database
#   2. Counts rows in the table: SELECT COUNT(*) FROM <table_name>
#   3. Checks that the count matches len(source_df)
#   4. Reads a sample of 3 rows from the DB and prints them
#   5. Checks that all column names in source_df exist in the DB table
#   6. Returns a dict: {"row_count_match": bool, "columns_match": bool,
#                       "db_row_count": int, "expected": int, "status": "pass"/"fail"}
#
# Call it for the "fact_sales" table in sales_warehouse.db.
# (row count will be 12 since we appended 2 extra records earlier)
#
# Expected output:
#     Row count match: True  (DB=12, Expected=10 -- False, since we appended extras)
#     Columns match: True
#     Status: fail (or pass if you adjusted expected count)
#
# Note: The "row_count_match" will be False because we appended extra rows.
# The function should still run and report accurately.




