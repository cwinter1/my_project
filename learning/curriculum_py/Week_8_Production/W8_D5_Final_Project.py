# ══════════════════════════════════════════════════════════════
#  WEEK 8  |  DAY 5  |  FINAL PROJECT: END-TO-END DATA ENGINEERING PIPELINE
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  This project integrates everything from Weeks 2-8:
#  extract -> transform -> validate -> load -> query -> quality check -> report
#
#  TIME:  ~30 minutes
#
#  YOUTUBE
#  ───────
#  Search: "Python end to end data pipeline project"
#  Search: "ETL pipeline sqlite pandas complete project"
#
# ══════════════════════════════════════════════════════════════

import pandas as pd
import numpy as np
import sqlite3
import csv
import os
import io
import logging
from datetime import datetime

this_dir = os.path.dirname(__file__)

# Set up pipeline logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("final_project")

print("=" * 70)
print("FINAL PROJECT: END-TO-END DATA ENGINEERING PIPELINE")
print("=" * 70)


# ══════════════════════════════════════════════════════════════
#  STEP 1 — GENERATE SOURCE CSV FILES
# ══════════════════════════════════════════════════════════════
# In production these would already exist on disk or S3.
# We generate them programmatically for a self-contained project.

# EXAMPLE ──────────────────────────────────────────────────────

np.random.seed(42)

def generate_region_csv(region, num_rows, seed_offset):
    """Generate a sales CSV string for one region."""
    np.random.seed(42 + seed_offset)
    products = ["Laptop", "Monitor", "Keyboard", "Mouse", "Headset", "Webcam"]
    reps = {
        "West":    ["Alice Ng",   "Lena Kim",   "Beth Morris"],
        "East":    ["Bob Chen",   "Priya Mehta", "Omar Nasser"],
        "Central": ["Carol Diaz", "Sara Jones",  "Mike Brown"],
    }
    region_reps = reps.get(region, ["Rep A", "Rep B"])

    rows = []
    for i in range(num_rows):
        qty   = np.random.randint(1, 10)
        price = round(float(np.random.choice([899.99, 349.99, 89.99, 39.99, 149.99, 69.99])), 2)
        # Introduce some intentional quality issues
        if i % 20 == 0:
            qty = -1          # invalid: negative quantity
        if i % 30 == 0:
            price = None      # missing price
        rows.append({
            "sale_id":   (seed_offset * 1000) + i + 1,
            "sale_date": (pd.Timestamp("2024-01-01") + pd.Timedelta(days=i % 90)).strftime("%Y-%m-%d"),
            "region":    region,
            "rep_name":  np.random.choice(region_reps),
            "product":   np.random.choice(products),
            "quantity":  qty,
            "unit_price": price,
        })
    df = pd.DataFrame(rows)
    return df.to_csv(index=False)

# Create three regional CSV files
source_files = {}
for region, offset, count in [("West", 1, 150), ("East", 2, 180), ("Central", 3, 120)]:
    filename = f"sales_{region.lower()}_2024.csv"
    filepath = os.path.join(this_dir, filename)
    csv_content = generate_region_csv(region, count, offset)
    with open(filepath, "w") as f:
        f.write(csv_content)
    source_files[region] = filepath
    logger.info(f"Generated: {filename} ({count} rows)")

print(f"\nGenerated {len(source_files)} source files.")


# ══════════════════════════════════════════════════════════════
#  TASK 1 — EXTRACT: READ ALL THREE CSV FILES AND COMBINE THEM
# ══════════════════════════════════════════════════════════════
# Instructions:
#   1. Read each file in source_files.values() using pd.read_csv()
#   2. Add a "_source_file" column to each (os.path.basename of the path)
#   3. Combine with pd.concat(ignore_index=True)
#   4. Store as df_raw
#   5. Print: "Extracted <n> rows from <k> files"
#
# Expected output:
#   Extracted 450 rows from 3 files

logger.info("TASK 1: Extract")
print("\n" + "="*70)
print("TASK 1: EXTRACT")
print("="*70)





# ══════════════════════════════════════════════════════════════
#  STEP 2 — INSPECT RAW DATA (demonstrated for you)
# ══════════════════════════════════════════════════════════════
# This block runs automatically to show you what the raw data looks like.

# EXAMPLE ──────────────────────────────────────────────────────

try:
    print("\nRaw data preview:")
    print(df_raw.head(5))
    print(f"\nShape: {df_raw.shape}")
    print(f"Nulls per column:\n{df_raw.isnull().sum()}")
    print(f"\nQuantity stats:\n{df_raw['quantity'].describe()}")
except NameError:
    print("Note: df_raw not yet defined. Complete Task 1 first.")
    # Create a fallback so later steps have data to work with
    df_raw = pd.read_csv(list(source_files.values())[0])
    for path in list(source_files.values())[1:]:
        df_raw = pd.concat([df_raw, pd.read_csv(path)], ignore_index=True)


# ══════════════════════════════════════════════════════════════
#  TASK 2 — TRANSFORM: CLEAN AND ENRICH THE DATA
# ══════════════════════════════════════════════════════════════
# Instructions:
#   1. Start with df_raw.copy() -> df_clean
#   2. Convert sale_date to datetime (pd.to_datetime, errors="coerce")
#   3. Convert quantity and unit_price to numeric (pd.to_numeric, errors="coerce")
#   4. Drop rows where quantity <= 0 or unit_price is null/NaN
#   5. Calculate "revenue" = quantity * unit_price (round to 2)
#   6. Add "quarter" column: "Q1" for months 1-3, "Q2" for 4-6, etc.
#      (use df_clean["sale_date"].dt.quarter.map({1:"Q1",2:"Q2",3:"Q3",4:"Q4"}))
#   7. Add "deal_size" column:
#      revenue < 200 -> "Small", 200-999 -> "Medium", 1000+ -> "Large"
#      (use pd.cut with bins=[0, 200, 999, float("inf")], labels=["Small","Medium","Large"])
#   8. Standardize rep_name: .str.strip().str.title()
#   9. Print: "Transformed: <n> rows remain after cleaning"
#
# Expected output:
#   Transformed: ~420 rows remain after cleaning

logger.info("TASK 2: Transform")
print("\n" + "="*70)
print("TASK 2: TRANSFORM")
print("="*70)





# ══════════════════════════════════════════════════════════════
#  TASK 3 — LOAD: WRITE TO SQLite DATABASE
# ══════════════════════════════════════════════════════════════
# Instructions:
#   1. Create an in-memory SQLite database: conn = sqlite3.connect(":memory:")
#   2. Write df_clean to a table called "fact_sales" using to_sql()
#      with if_exists="replace" and index=False
#   3. Create a summary view by running SQL and storing in df_summary:
#      SELECT region, quarter, COUNT(*) as sales_count,
#             SUM(revenue) as total_revenue,
#             AVG(revenue) as avg_revenue
#      FROM fact_sales
#      GROUP BY region, quarter
#      ORDER BY region, quarter
#   4. Print the df_summary table
#
# Expected output:
#   Loaded <n> rows to fact_sales
#   Regional quarterly summary:
#   [table with region, quarter, sales_count, total_revenue, avg_revenue]

logger.info("TASK 3: Load")
print("\n" + "="*70)
print("TASK 3: LOAD TO DATABASE")
print("="*70)





# ══════════════════════════════════════════════════════════════
#  STEP 4 — ANALYTICAL QUERIES (demonstrated for you)
# ══════════════════════════════════════════════════════════════
# These run after Task 3. They will only work if conn is defined.

# EXAMPLE ──────────────────────────────────────────────────────

print("\n" + "="*70)
print("STEP 4: ANALYTICAL QUERIES")
print("="*70)

try:
    # Query 1: Top 5 products by revenue
    df_products = pd.read_sql("""
        SELECT product,
               SUM(quantity)  AS units_sold,
               ROUND(SUM(revenue), 2) AS total_revenue
        FROM   fact_sales
        GROUP BY product
        ORDER BY total_revenue DESC
        LIMIT 5
    """, conn)
    print("\nTop 5 Products by Revenue:")
    print(df_products.to_string(index=False))

    # Query 2: Rep performance
    df_reps = pd.read_sql("""
        SELECT rep_name,
               region,
               COUNT(*)               AS deals,
               ROUND(SUM(revenue), 2) AS total_revenue,
               ROUND(AVG(revenue), 2) AS avg_deal
        FROM   fact_sales
        GROUP BY rep_name, region
        ORDER BY total_revenue DESC
        LIMIT 8
    """, conn)
    print("\nTop Rep Performance:")
    print(df_reps.to_string(index=False))

    # Query 3: Deal size distribution
    df_deals = pd.read_sql("""
        SELECT deal_size,
               COUNT(*) AS count,
               ROUND(SUM(revenue), 2) AS total_revenue
        FROM   fact_sales
        GROUP BY deal_size
        ORDER BY total_revenue DESC
    """, conn)
    print("\nDeal Size Distribution:")
    print(df_deals.to_string(index=False))

except Exception as e:
    print(f"Query error: {e}")
    print("Make sure Task 3 is complete and 'conn' is defined.")


# ══════════════════════════════════════════════════════════════
#  TASK 4 — QUALITY CHECK AND PIPELINE REPORT
# ══════════════════════════════════════════════════════════════
# Instructions (two parts):
#
# PART A -- Quality Checks:
# Using df_clean, check:
#   1. No null values in required cols: sale_id, rep_name, product, revenue
#   2. All revenue values > 0
#   3. sale_id is unique
#   4. All regions in {"West", "East", "Central"}
# Print each check as [PASS] or [FAIL] with the failure count.
#
# PART B -- Pipeline Run Report:
# Create a dict called pipeline_report with these keys:
#   "run_timestamp"        : datetime.now().isoformat()
#   "source_files"         : list(source_files.keys())
#   "rows_extracted"       : len(df_raw)
#   "rows_after_transform" : len(df_clean)
#   "rows_loaded"          : len(df_clean)
#   "quality_checks_passed": number of checks that passed
#   "quality_checks_total" : 4
#   "total_revenue"        : df_clean["revenue"].sum().round(2)
#   "regions_covered"      : df_clean["region"].nunique()
#   "date_range"           : str(df_clean["sale_date"].min().date()) + " to " + str(df_clean["sale_date"].max().date())
#   "pipeline_status"      : "SUCCESS" if all quality checks pass, else "WARNING"
#
# Print the report at the end.

logger.info("TASK 4: Quality Check and Report")
print("\n" + "="*70)
print("TASK 4: QUALITY CHECK AND PIPELINE REPORT")
print("="*70)





# ══════════════════════════════════════════════════════════════
#  FINAL OUTPUT — PRINT REPORT SUMMARY
# ══════════════════════════════════════════════════════════════
print("\n" + "="*70)
print("PIPELINE RUN COMPLETE")
print("="*70)

try:
    for key, value in pipeline_report.items():
        print(f"  {key:<30}: {value}")
except NameError:
    print("Note: pipeline_report not yet defined. Complete Task 4 first.")

# Save report to JSON
import json
try:
    report_path = os.path.join(this_dir, "pipeline_run_report.json")
    # Convert any non-serializable types
    serializable_report = {}
    for k, v in pipeline_report.items():
        if isinstance(v, (pd.Timestamp, datetime)):
            serializable_report[k] = str(v)
        elif hasattr(v, "item"):   # numpy scalar
            serializable_report[k] = v.item()
        else:
            serializable_report[k] = v

    with open(report_path, "w") as f:
        json.dump(serializable_report, f, indent=2)
    logger.info(f"Report saved: {report_path}")
    print(f"\nReport saved to: {report_path}")
except NameError:
    print("Report not saved -- pipeline_report not defined yet.")
except Exception as e:
    print(f"Could not save report: {e}")

# Close connection if open
try:
    conn.close()
    logger.info("Database connection closed.")
except Exception:
    pass

print("\n" + "="*70)
print("PROJECT COMPLETE -- You have built a production-grade ETL pipeline!")
print("="*70)
