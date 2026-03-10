# ══════════════════════════════════════════════════════════════
#  WEEK 8  |  DAY 4  |  BIG DATA AND SPARK
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Understand when Spark is needed vs when pandas is sufficient
#  2. Learn PySpark DataFrame basics: create, select, filter, groupBy
#  3. Compare Spark and pandas for common operations
#
#  TIME:  ~30 minutes
#
#  YOUTUBE
#  ───────
#  Search: "PySpark tutorial beginners DataFrame"
#  Search: "PySpark vs pandas when to use each"
#
# ══════════════════════════════════════════════════════════════

# NOTE: PySpark code in Concepts 2 and 3 is COMMENTED OUT because PySpark
# requires Java 8+ and a Spark installation.
#
# To install:
#   pip install pyspark
#   (also requires Java: https://www.java.com/en/download/)
#
# For quick cloud-based PySpark practice without local installation:
#   - Databricks Community Edition (free): https://community.cloud.databricks.com
#   - Google Colab: !pip install pyspark in a notebook cell
#   - AWS Glue Studio / EMR Notebooks

import pandas as pd
import numpy as np


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — WHEN TO USE SPARK (DATA SIZE > MEMORY)
# ══════════════════════════════════════════════════════════════
# The rule of thumb: if your data fits in memory on one machine, use pandas.
# When data exceeds memory -- or when you need to parallelize across a cluster --
# use Spark.
#
# DATA SIZE GUIDELINES:
#   < 1 GB    -- pandas is almost always the right choice
#   1-10 GB   -- pandas with chunking OR polars (fast single-machine library)
#   10-100 GB -- Spark on a small cluster (4-8 nodes), or use Dask
#   100 GB+   -- Spark with a proper cluster (cloud: EMR, Dataproc, Databricks)
#   > 1 TB    -- Spark is effectively mandatory
#
# OTHER REASONS TO USE SPARK:
#   - Data is already distributed across a Hadoop/S3 cluster
#   - You need streaming data processing (Spark Streaming)
#   - Complex ML pipelines on big data (MLlib)
#   - SQL queries on files (Spark SQL against Parquet/Delta Lake)
#
# REASONS TO STICK WITH PANDAS:
#   - Data is small enough to fit in memory
#   - Simpler code and faster development time
#   - No cluster to manage (no infra cost)
#   - Rich ecosystem (seaborn, statsmodels, sklearn all expect pandas)

# EXAMPLE ──────────────────────────────────────────────────────

print("=== WHEN TO USE SPARK ===")

print(f"\n{'Dimension':<18} | {'Small -> pandas':<35} | {'Large -> Spark':<15}")
print("-" * 75)
print(f"{'Dataset size':<18} | < 500 MB: pandas, 500 MB-50 GB: chunking   | > 50 GB: Spark")
print(f"{'Infrastructure':<18} | Laptop or single VM: pandas             | Cluster: Spark")
print(f"{'Real-time':<18} | Scheduled batch: pandas                 | Streaming: Spark Streaming")
print(f"{'Cost':<18} | Free (local)                            | Cluster cost ($$/hr)")

# Demonstrate a pandas chunked approach for medium-sized data
print("\n=== PANDAS CHUNKED PROCESSING (for medium-sized files) ===")

def process_large_csv_in_chunks(filepath_or_data, chunk_size=1000):
    """
    Process a large CSV file in chunks to avoid loading it all into memory.
    In production, filepath_or_data would be a real file path.
    """
    import io
    # Generate sample data to simulate a large file
    np.random.seed(42)
    n_total = 5000
    sample_csv = pd.DataFrame({
        "sale_id": range(1, n_total + 1),
        "region":  np.random.choice(["West", "East", "Central"], n_total),
        "revenue": np.random.normal(1000, 300, n_total).round(2),
    }).to_csv(index=False)

    chunk_results = []
    for chunk in pd.read_csv(io.StringIO(sample_csv), chunksize=chunk_size):
        # Process each chunk independently
        agg = chunk.groupby("region")["revenue"].agg(["sum", "count"])
        chunk_results.append(agg)

    # Combine chunk aggregations
    combined = pd.concat(chunk_results).groupby(level=0).sum()
    combined["avg"] = combined["sum"] / combined["count"]
    return combined.round(2)

result = process_large_csv_in_chunks(None)
print("Revenue summary (processed in 1000-row chunks):")
print(result)


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
# Write a function called count_rows_by_value(csv_string, column, chunk_size=500)
# that:
#   1. Reads the CSV string in chunks of chunk_size using pd.read_csv + chunksize
#   2. For each chunk, uses value_counts() on the given column
#   3. Combines all chunk counts into one final Series
#   4. Returns the combined Series sorted descending
#
# Test with the large_csv below and column="category".
# Print the total count per category.
#
# Expected output:
#   Electronics    ~500
#   Accessories    ~500
#   Peripherals    ~500
#   Office         ~500
# --- starting data ---
np.random.seed(7)
import io as _io
large_csv_str = pd.DataFrame({
    "id": range(1, 2001),
    "category": np.random.choice(["Electronics","Accessories","Peripherals","Office"], 2000),
    "amount": np.random.normal(200, 50, 2000).round(2),
}).to_csv(index=False)





# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — PYSPARK DATAFRAME BASICS (COMMENTED TEMPLATE)
# ══════════════════════════════════════════════════════════════
# PySpark DataFrames look similar to pandas but run distributed across a cluster.
# The key difference: PySpark operations are LAZY -- they do not execute until
# you call an action (.show(), .count(), .collect(), .write.csv()).

# EXAMPLE ──────────────────────────────────────────────────────

# TEMPLATE (requires: pip install pyspark + Java 8+)
"""
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# Create a Spark session -- this is the entry point to all Spark functionality
spark = SparkSession.builder \
    .appName("SalesAnalysis") \
    .getOrCreate()

# Create a DataFrame from a list of dicts (small example)
data = [
    {"sale_id": 1, "rep": "Alice", "region": "West",    "revenue": 1299.99},
    {"sale_id": 2, "rep": "Bob",   "region": "East",    "revenue": 799.98},
    {"sale_id": 3, "rep": "Carol", "region": "West",    "revenue": 449.97},
    {"sale_id": 4, "rep": "Dave",  "region": "Central", "revenue": 149.99},
    {"sale_id": 5, "rep": "Alice", "region": "West",    "revenue": 2399.97},
]

df_spark = spark.createDataFrame(data)

# Show the first 5 rows (triggers execution)
df_spark.show(5)

# Print the schema (column names and types)
df_spark.printSchema()

# Select specific columns
df_spark.select("rep", "region", "revenue").show()

# Filter rows
df_spark.filter(F.col("region") == "West").show()
df_spark.filter(F.col("revenue") > 500).show()

# Add a derived column
df_spark = df_spark.withColumn("commission", F.round(F.col("revenue") * 0.08, 2))
df_spark.show()

# GroupBy with aggregation
summary = df_spark.groupBy("region").agg(
    F.count("sale_id").alias("num_sales"),
    F.sum("revenue").alias("total_revenue"),
    F.avg("revenue").alias("avg_revenue"),
)
summary.orderBy(F.desc("total_revenue")).show()

# Read from a large CSV file on S3
df_s3 = spark.read.csv("s3://my-bucket/sales/*.csv", header=True, inferSchema=True)
print(f"Rows: {df_s3.count()}")

# Write back to S3 as Parquet (more efficient for analytics)
df_s3.write.mode("overwrite").parquet("s3://my-bucket/processed/sales_clean/")

# Stop the Spark session when done
spark.stop()
"""

print("\n=== PySpark CODE TEMPLATE ===")
print("See commented code above for PySpark DataFrame basics.")
print()
print("KEY PySpark OPERATIONS:")
pyspark_ops = [
    ("spark.createDataFrame(data)",         "Create DataFrame from Python list"),
    ("spark.read.csv('path', header=True)", "Read CSV file(s) from disk or S3"),
    ("df.show(n)",                          "Print first n rows (action -- triggers execution)"),
    ("df.printSchema()",                    "Show column names and data types"),
    ("df.select('col1', 'col2')",           "Select specific columns"),
    ("df.filter(F.col('col') > value)",     "Filter rows by condition"),
    ("df.withColumn('new', expression)",    "Add or replace a column"),
    ("df.groupBy('col').agg(...)",          "Group and aggregate"),
    ("df.orderBy(F.desc('col'))",           "Sort by column descending"),
    ("df.write.parquet('path')",            "Write to Parquet format (action)"),
    ("df.count()",                          "Count rows (action -- triggers full scan)"),
]
for op, desc in pyspark_ops:
    print(f"  {op:<45} | {desc}")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
# The pandas code below performs a sales analysis.
# Write the equivalent PySpark code as COMMENTS (it would not run locally,
# but understanding the translation is the goal).
#
# pandas code:
#   df_sales = pd.read_csv("sales.csv")
#   df_west = df_sales[df_sales["region"] == "West"]
#   df_west["commission"] = df_west["revenue"] * 0.08
#   summary = df_west.groupby("rep")["revenue"].agg(["sum", "mean", "count"])
#   summary.columns = ["total_revenue", "avg_revenue", "num_deals"]
#   summary = summary.sort_values("total_revenue", ascending=False)
#   print(summary.head(5))
#
# Write the PySpark equivalent as comments below.
# Think about: SparkSession, read.csv, filter, withColumn, groupBy, agg, orderBy, show
#
# Expected output:
#   (PySpark comments showing the equivalent operations)





# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — SPARK VS PANDAS: WHEN EACH IS APPROPRIATE
# ══════════════════════════════════════════════════════════════
# A side-by-side comparison of the same operations in pandas vs PySpark.
# The pandas version runs on your laptop. The Spark version runs on a cluster.

# EXAMPLE ──────────────────────────────────────────────────────

print("\n=== SPARK VS PANDAS COMPARISON ===")

comparisons = [
    {
        "operation":  "Read CSV",
        "pandas":     "pd.read_csv('file.csv')",
        "pyspark":    "spark.read.csv('file.csv', header=True, inferSchema=True)",
    },
    {
        "operation":  "Filter rows",
        "pandas":     "df[df['col'] > 100]",
        "pyspark":    "df.filter(F.col('col') > 100)",
    },
    {
        "operation":  "Add column",
        "pandas":     "df['new'] = df['a'] * df['b']",
        "pyspark":    "df.withColumn('new', F.col('a') * F.col('b'))",
    },
    {
        "operation":  "GroupBy sum",
        "pandas":     "df.groupby('dept')['revenue'].sum()",
        "pyspark":    "df.groupBy('dept').agg(F.sum('revenue'))",
    },
    {
        "operation":  "Sort desc",
        "pandas":     "df.sort_values('revenue', ascending=False)",
        "pyspark":    "df.orderBy(F.desc('revenue'))",
    },
    {
        "operation":  "Count rows",
        "pandas":     "len(df)  or  df.shape[0]",
        "pyspark":    "df.count()",
    },
    {
        "operation":  "Write CSV",
        "pandas":     "df.to_csv('output.csv', index=False)",
        "pyspark":    "df.write.mode('overwrite').csv('output_folder/')",
    },
    {
        "operation":  "Write Parquet",
        "pandas":     "df.to_parquet('output.parquet')",
        "pyspark":    "df.write.mode('overwrite').parquet('output_folder/')",
    },
    {
        "operation":  "Null handling",
        "pandas":     "df.fillna(0)  /  df.dropna()",
        "pyspark":    "df.fillna(0)  /  df.dropna()",
    },
    {
        "operation":  "Distinct rows",
        "pandas":     "df.drop_duplicates()",
        "pyspark":    "df.distinct()",
    },
]

print(f"\n{'Operation':<20} | {'pandas':<45} | {'PySpark'}")
print("-" * 110)
for c in comparisons:
    print(f"{c['operation']:<20} | {c['pandas']:<45} | {c['pyspark']}")

# Key differences to remember
print("\nKEY DIFFERENCES:")
print("  1. pandas is EAGER (runs immediately); Spark is LAZY (builds a query plan)")
print("  2. pandas runs on ONE machine; Spark runs on a CLUSTER")
print("  3. pandas uses Python objects natively; Spark has its own type system")
print("  4. Writing to Spark creates a FOLDER of part files, not a single file")
print("  5. pandas .loc/.iloc do not exist in Spark (no row labels concept)")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
# Write a function called estimate_processing_time(rows, cols, operation) that
# estimates whether pandas or Spark is more appropriate, and why.
#
# Rules:
#   rows > 50_000_000 (50M):  always recommend "Spark"
#   rows > 5_000_000 (5M):    recommend "Spark" if operation in ["groupby", "join", "sort"]
#                              else recommend "pandas (chunked)"
#   rows <= 5_000_000:        recommend "pandas"
#
# Print: "Rows: X, Cols: Y, Op: Z => Use: <tool> | Reason: <reason>"
#
# Test with:
#   estimate_processing_time(100, 10, "filter")
#   estimate_processing_time(8_000_000, 5, "groupby")
#   estimate_processing_time(200_000_000, 50, "join")
#
# Expected output:
#   Rows: 100, Cols: 10, Op: filter  => Use: pandas | Reason: Small dataset, fits in memory easily
#   Rows: 8000000, Cols: 5, Op: groupby => Use: Spark | Reason: Large dataset with heavy operation
#   Rows: 200000000, Cols: 50, Op: join => Use: Spark | Reason: Dataset exceeds single-machine memory




