# ══════════════════════════════════════════════════════════════
#  WEEK 7  |  DAY 1  |  ETL PIPELINES
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Understand the ETL (Extract, Transform, Load) architecture as a code pattern
#  2. Build an Extract function that reads from a CSV source
#  3. Build Transform and Load functions and chain them into a complete pipeline
#
#  TIME:  ~30 minutes
#
#  YOUTUBE
#  ───────
#  Search: "ETL pipeline Python tutorial extract transform load"
#  Search: "Python data pipeline architecture functions"
#
# ══════════════════════════════════════════════════════════════

import pandas as pd
import io
import os

# We use io.StringIO to embed CSV data directly in memory --
# no files on disk required, so the lesson works anywhere.


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — ETL ARCHITECTURE: EXTRACT, TRANSFORM, LOAD AS A PATTERN
# ══════════════════════════════════════════════════════════════
# ETL stands for Extract, Transform, Load -- the three stages of moving data
# from a source system into a destination like a data warehouse or database.
#
# EXTRACT:  Pull raw data from source systems (CSV, DB, API, Excel)
# TRANSFORM: Clean, validate, enrich, and reshape the data
# LOAD:     Write the transformed data to a destination
#
# WHY STRUCTURE CODE THIS WAY?
#   - Each stage is testable in isolation
#   - Failures are easier to pinpoint (did extract fail? or transform?)
#   - Stages can be swapped independently (change the source without touching transform)
#   - Makes pipelines readable and maintainable
#
# A simple ETL pipeline in Python looks like this:
#
#   def extract(source):    ...  return raw_df
#   def transform(raw_df):  ...  return clean_df
#   def load(clean_df, dest): ...
#
#   def run_pipeline():
#       raw    = extract("sales_2024.csv")
#       clean  = transform(raw)
#       load(clean, "warehouse.db")

# EXAMPLE ──────────────────────────────────────────────────────

# ETL METADATA: track what happened during a run
pipeline_metadata = {
    "pipeline_name":    "daily_sales_etl",
    "version":          "1.0.0",
    "rows_extracted":   0,
    "rows_transformed": 0,
    "rows_loaded":      0,
    "errors":           [],
    "status":           "not_started",
}

# Embedded CSV -- simulates a real daily sales file received from a source system
RAW_CSV = """sale_id,sale_date,rep_name,region,product,quantity,unit_price,discount_pct
1,2024-01-10,Alice Ng,West,Laptop,1,1299.99,0
2,2024-01-10,Bob Chen,East,Monitor,2,399.99,10
3,2024-01-11,Carol Diaz,West,Keyboard,3,149.99,0
4,2024-01-11,Alice Ng,West,Mouse,5,79.99,5
5,2024-01-12,INVALID,UNKNOWN,,0,-50,
6,2024-01-12,Bob Chen,East,Headset,1,199.99,0
7,2024-01-13,Carol Diaz,West,Laptop,2,1299.99,15
8,2024-01-14,Dave Park,Central,USB Hub,10,49.99,0
9,,Alice Ng,West,Mouse,2,79.99,0
10,2024-01-15,Eve Torres,East,Webcam,3,89.99,20
"""

print("=== ETL Pipeline Architecture Demo ===")
print("Source: embedded CSV (io.StringIO)")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
# Without writing any real transformation logic yet, write a function called
# pipeline_skeleton() that:
#   1. Prints "EXTRACT: Reading from source..."
#   2. Prints "TRANSFORM: Cleaning and validating..."
#   3. Prints "LOAD: Writing to destination..."
#   4. Returns a dict with keys "extract", "transform", "load"
#      each having value "complete"
#
# Call the function and print the returned dict.
#
# Expected output:
#   EXTRACT: Reading from source...
#   TRANSFORM: Cleaning and validating...
#   LOAD: Writing to destination...
#   {'extract': 'complete', 'transform': 'complete', 'load': 'complete'}





# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — BUILDING AN EXTRACT FUNCTION (FROM CSV FILE)
# ══════════════════════════════════════════════════════════════
# The extract function is responsible for:
#   - Reading raw data from the source
#   - Returning it as a pandas DataFrame (unchanged)
#   - Handling read errors (file not found, network failure, etc.)
#   - NOT transforming anything -- extraction is purely about reading
#
# Return the raw data and a metadata dict describing what was read.

# EXAMPLE ──────────────────────────────────────────────────────

def extract_from_csv_string(csv_string, source_name="inline_csv"):
    """
    Read CSV data from a string (simulates reading from a file or API).
    Returns (DataFrame, metadata_dict).
    """
    print(f"\n[EXTRACT] Reading from: {source_name}")
    try:
        df = pd.read_csv(io.StringIO(csv_string))
        rows = len(df)
        cols = len(df.columns)
        print(f"[EXTRACT] Read {rows} rows x {cols} columns")
        return df, {"rows": rows, "columns": cols, "source": source_name, "status": "ok"}
    except Exception as e:
        print(f"[EXTRACT] ERROR: {e}")
        return pd.DataFrame(), {"rows": 0, "columns": 0, "source": source_name,
                                 "status": "error", "error_message": str(e)}

def extract_from_file(filepath):
    """
    Read CSV data from a real file path.
    Returns (DataFrame, metadata_dict).
    """
    print(f"\n[EXTRACT] Reading file: {filepath}")
    try:
        df = pd.read_csv(filepath)
        print(f"[EXTRACT] Read {len(df)} rows from {os.path.basename(filepath)}")
        return df, {"rows": len(df), "source": filepath, "status": "ok"}
    except FileNotFoundError:
        print(f"[EXTRACT] ERROR: File not found: {filepath}")
        return pd.DataFrame(), {"rows": 0, "source": filepath, "status": "error",
                                 "error_message": "File not found"}

# Run the extract
raw_df, extract_meta = extract_from_csv_string(RAW_CSV, "daily_sales_feed")
pipeline_metadata["rows_extracted"] = extract_meta["rows"]

print("\n=== Raw Data (first 5 rows) ===")
print(raw_df.head())
print("\nData types:")
print(raw_df.dtypes)
print("\nNull counts:")
print(raw_df.isnull().sum())


# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
# Write a function called extract_all_sources(sources) that:
#   1. Accepts a list of (source_name, csv_string) tuples
#   2. Calls extract_from_csv_string for each one
#   3. Concatenates all resulting DataFrames into one combined DataFrame
#      using pd.concat() with ignore_index=True
#   4. Returns (combined_df, summary_dict) where summary_dict has:
#      {"total_rows": n, "sources": [list of source names], "status": "ok"}
#
# Call it with the two CSV strings defined below and print:
#   - The shape of the combined DataFrame
#   - The sources in the summary
#
# Expected output:
#   [EXTRACT] Reading from: region_west
#   [EXTRACT] Read 3 rows x 4 columns
#   [EXTRACT] Reading from: region_east
#   [EXTRACT] Read 3 rows x 4 columns
#   Combined shape: (6, 4)
#   Sources: ['region_west', 'region_east']
# --- starting data ---
west_csv = "rep,product,qty,revenue\nAlice,Laptop,1,1299.99\nAlice,Mouse,2,159.98\nCarol,Keyboard,3,449.97"
east_csv = "rep,product,qty,revenue\nBob,Monitor,2,799.98\nBob,Headset,1,199.99\nEve,Webcam,3,269.97"





# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — TRANSFORM AND LOAD FUNCTIONS, CHAINING INTO A PIPELINE
# ══════════════════════════════════════════════════════════════
# The transform function:
#   - Cleans data (handle nulls, fix types, remove invalid rows)
#   - Validates data (check ranges, required fields)
#   - Enriches data (add calculated columns, lookups)
#   - Returns a clean DataFrame
#
# The load function:
#   - Writes the clean DataFrame to a destination
#   - Handles the "if_exists" logic (replace vs append)
#   - Returns a count of rows written

# EXAMPLE ──────────────────────────────────────────────────────

def transform_sales(df):
    """
    Clean and enrich the raw sales DataFrame.
    Returns (clean_df, metadata_dict).
    """
    print("\n[TRANSFORM] Starting transformation...")
    errors = []
    df_clean = df.copy()

    # Fix column names: strip whitespace and lowercase
    df_clean.columns = [c.strip().lower() for c in df_clean.columns]

    # Parse dates -- invalid dates become NaT
    df_clean["sale_date"] = pd.to_datetime(df_clean["sale_date"], errors="coerce")

    # Drop rows with null sale_date or null product (required fields)
    before = len(df_clean)
    df_clean = df_clean.dropna(subset=["sale_date", "product"])
    dropped = before - len(df_clean)
    if dropped > 0:
        errors.append(f"Dropped {dropped} rows with missing sale_date or product")
        print(f"[TRANSFORM] Dropped {dropped} invalid rows")

    # Convert numeric columns, coerce errors to NaN
    df_clean["quantity"]     = pd.to_numeric(df_clean["quantity"],   errors="coerce").fillna(0).astype(int)
    df_clean["unit_price"]   = pd.to_numeric(df_clean["unit_price"], errors="coerce").fillna(0.0)
    df_clean["discount_pct"] = pd.to_numeric(df_clean["discount_pct"], errors="coerce").fillna(0.0)

    # Remove rows with invalid data
    df_clean = df_clean[df_clean["quantity"] > 0]
    df_clean = df_clean[df_clean["unit_price"] > 0]

    # Add calculated columns
    df_clean["discount_amount"] = (df_clean["unit_price"] * df_clean["discount_pct"] / 100).round(2)
    df_clean["final_price"]     = (df_clean["unit_price"] - df_clean["discount_amount"]).round(2)
    df_clean["line_revenue"]    = (df_clean["quantity"] * df_clean["final_price"]).round(2)

    # Standardize region
    df_clean["region"] = df_clean["region"].str.strip().str.title()

    rows_out = len(df_clean)
    print(f"[TRANSFORM] Output: {rows_out} clean rows")
    return df_clean, {"rows_in": before, "rows_out": rows_out, "errors": errors, "status": "ok"}

def load_to_csv(df, output_path):
    """Write the DataFrame to a CSV file. Returns rows written."""
    print(f"\n[LOAD] Writing {len(df)} rows to: {output_path}")
    df.to_csv(output_path, index=False)
    print(f"[LOAD] Complete.")
    return len(df)

def run_pipeline(csv_data, output_path):
    """Run the full ETL pipeline and return a summary dict."""
    meta = {"pipeline": "daily_sales_etl", "errors": []}

    # Extract
    raw, extract_info = extract_from_csv_string(csv_data, "daily_sales_feed")
    meta["rows_extracted"] = extract_info["rows"]

    if extract_info["status"] != "ok":
        meta["status"] = "failed_at_extract"
        return meta

    # Transform
    clean, transform_info = transform_sales(raw)
    meta["rows_transformed"] = transform_info["rows_out"]
    meta["errors"].extend(transform_info["errors"])

    # Load
    rows_loaded = load_to_csv(clean, output_path)
    meta["rows_loaded"] = rows_loaded
    meta["status"] = "success"

    return meta

# Run the complete pipeline
output_path = os.path.join(os.path.dirname(__file__), "pipeline_output.csv")
summary = run_pipeline(RAW_CSV, output_path)

print("\n=== PIPELINE RUN SUMMARY ===")
for key, value in summary.items():
    print(f"  {key:<20}: {value}")

# Verify the output
df_loaded = pd.read_csv(output_path)
print(f"\nOutput file shape: {df_loaded.shape}")
print(df_loaded[["sale_date", "rep_name", "product", "quantity", "line_revenue"]].head())


# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
# Extend the pipeline by writing a function called validate_sales(df) that
# runs between transform and load.
# The function should check 3 rules and return a validation report:
#
# Rule 1: All sale_date values must be non-null
# Rule 2: All unit_price values must be > 0
# Rule 3: All region values must be in ["West", "East", "Central", "North", "South"]
#
# For each rule, the report should say how many rows pass and fail.
# If any rule has failures, print a WARNING but do NOT stop the pipeline.
#
# Returns: (is_valid: bool, report: dict)
# is_valid = True only if ALL rules pass (0 failures)
#
# Use the clean DataFrame from transform_sales(raw_df) as input.
#
# Expected output:
#   [VALIDATE] Rule: sale_date not null     | Pass: 8 | Fail: 0
#   [VALIDATE] Rule: unit_price > 0        | Pass: 8 | Fail: 0
#   [VALIDATE] Rule: region in allowed set | Pass: 7 | Fail: 1
#   WARNING: 1 validation failure(s) detected
#   is_valid: False
# --- starting data ---
raw_df_exercise, _ = extract_from_csv_string(RAW_CSV)
clean_df_exercise, _ = transform_sales(raw_df_exercise)




