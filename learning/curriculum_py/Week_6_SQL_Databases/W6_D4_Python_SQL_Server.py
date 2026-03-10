# ══════════════════════════════════════════════════════════════
#  WEEK 6  |  DAY 4  |  PYTHON AND SQL SERVER
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Understand pyodbc and how to build a SQL Server connection string
#  2. Read SQL Server data into a pandas DataFrame using pd.read_sql()
#  3. Write a DataFrame to SQL Server using the Py_MSSql custom module
#
#  TIME:  ~30 minutes
#
#  YOUTUBE
#  ───────
#  Search: "Python pyodbc SQL Server connection tutorial"
#  Search: "pandas read_sql write to SQL Server"
#
# ══════════════════════════════════════════════════════════════

# NOTE: Most code in this file is shown as COMMENTED TEMPLATES.
# Connecting to SQL Server requires an actual SQL Server instance,
# valid credentials, and the correct ODBC driver installed.
# The patterns shown here are production-ready -- just swap in real values.
#
# To install the required packages:
#   pip install pyodbc
#   pip install pandas sqlalchemy
#
# To find installed ODBC drivers:
#   import pyodbc
#   print(pyodbc.drivers())

# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — WHAT IS pyodbc, CONNECTION STRING, CONNECTING
# ══════════════════════════════════════════════════════════════
# pyodbc is a Python library that uses ODBC (Open Database Connectivity)
# to connect to databases including SQL Server, Oracle, MySQL, and others.
#
# It requires:
#   1. pyodbc installed (pip install pyodbc)
#   2. An ODBC driver installed on the machine
#      (Microsoft ODBC Driver 17 or 18 for SQL Server is most common)
#
# CONNECTION STRING FORMATS:
#
# Option A -- SQL Server Authentication (username + password):
#   DRIVER={ODBC Driver 17 for SQL Server};
#   SERVER=your_server_name_or_ip;
#   DATABASE=your_database_name;
#   UID=your_username;
#   PWD=your_password;
#
# Option B -- Windows Authentication (uses your Windows login):
#   DRIVER={ODBC Driver 17 for SQL Server};
#   SERVER=your_server_name;
#   DATABASE=your_database_name;
#   Trusted_Connection=yes;
#
# Option C -- Azure SQL Database:
#   DRIVER={ODBC Driver 18 for SQL Server};
#   SERVER=yourserver.database.windows.net;
#   DATABASE=your_database;
#   UID=your_username;
#   PWD=your_password;
#   Encrypt=yes;
#   TrustServerCertificate=no;

# EXAMPLE ──────────────────────────────────────────────────────

# TEMPLATE -- Do not run this block without real credentials
"""
import pyodbc

CONNECTION_STRING = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=your_server_name;"
    "DATABASE=your_database;"
    "UID=your_username;"
    "PWD=your_password;"
)

# Connect
conn = pyodbc.connect(CONNECTION_STRING)
cursor = conn.cursor()

# Test the connection
cursor.execute("SELECT @@VERSION")
row = cursor.fetchone()
print("SQL Server version:", row[0][:50])

# Execute a query
cursor.execute("SELECT TOP 5 * FROM dbo.sales")
columns = [col[0] for col in cursor.description]
for row in cursor.fetchall():
    print(dict(zip(columns, row)))

cursor.close()
conn.close()
"""

# Working example with sqlite3 (always available, same SQL patterns)
import sqlite3
import pandas as pd

conn_demo = sqlite3.connect(":memory:")
cur_demo = conn_demo.cursor()

# Simulate a SQL Server table for demonstration
cur_demo.executescript("""
    CREATE TABLE dbo_sales (
        sale_id    INTEGER PRIMARY KEY,
        sale_date  TEXT,
        rep_name   TEXT,
        region     TEXT,
        product    TEXT,
        revenue    REAL
    );
    INSERT INTO dbo_sales VALUES (1, '2024-01-10', 'Alice Ng',   'West',    'Laptop',  4499.95);
    INSERT INTO dbo_sales VALUES (2, '2024-01-15', 'Bob Chen',   'East',    'Monitor', 1749.95);
    INSERT INTO dbo_sales VALUES (3, '2024-01-22', 'Carol Diaz', 'West',    'Laptop',  899.99);
    INSERT INTO dbo_sales VALUES (4, '2024-02-01', 'Alice Ng',   'West',    'Headset', 449.97);
    INSERT INTO dbo_sales VALUES (5, '2024-02-14', 'Bob Chen',   'East',    'Laptop',  1799.98);
    INSERT INTO dbo_sales VALUES (6, '2024-02-28', 'Dave Park',  'Central', 'Monitor', 349.99);
""")

print("Demo database populated.")
print("The code patterns below mirror real SQL Server usage.")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
# Write a function called get_connection(server, database, use_windows_auth=True)
# that:
#   1. Builds a connection string using the templates above
#   2. If use_windows_auth is True, uses Trusted_Connection=yes
#   3. If use_windows_auth is False, also accepts uid and pwd keyword args
#      and uses SQL Server Authentication
#   4. Returns the connection string (as a string, do NOT call pyodbc.connect)
#
# Call it twice and print the resulting connection strings:
#   get_connection("PROD-DB-01", "SalesDB")
#   get_connection("PROD-DB-01", "SalesDB", use_windows_auth=False,
#                  uid="sa", pwd="P@ssw0rd")
#
# Expected output:
#   DRIVER={ODBC Driver 17 for SQL Server};SERVER=PROD-DB-01;DATABASE=SalesDB;Trusted_Connection=yes;
#   DRIVER={ODBC Driver 17 for SQL Server};SERVER=PROD-DB-01;DATABASE=SalesDB;UID=sa;PWD=P@ssw0rd;





# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — READING DATA INTO A pandas DATAFRAME USING pd.read_sql()
# ══════════════════════════════════════════════════════════════
# pd.read_sql() is the standard way to move SQL query results into pandas.
# It works with any DBAPI2-compatible connection (pyodbc, sqlite3, sqlalchemy).
#
# Syntax:
#   df = pd.read_sql("SELECT ...", conn)
#   df = pd.read_sql("SELECT ... WHERE col = ?", conn, params=("value",))
#
# Advantages over manual cursor loops:
#   - Automatically reads column names as DataFrame column headers
#   - Handles NULL -> NaN conversion
#   - Returns a fully functional DataFrame ready for analysis
#   - Supports chunking large result sets with chunksize parameter

# EXAMPLE ──────────────────────────────────────────────────────

# Using our sqlite3 demo connection as a stand-in for SQL Server
print("\n=== pd.read_sql() Demo ===")

# Basic query
df_sales = pd.read_sql("SELECT * FROM dbo_sales", conn_demo)
print("Shape:", df_sales.shape)
print(df_sales.head())

# Parameterized query (prevents SQL injection)
region = "West"
df_west = pd.read_sql(
    "SELECT * FROM dbo_sales WHERE region = ?",
    conn_demo,
    params=(region,),
)
print(f"\nWest region sales ({len(df_west)} rows):")
print(df_west)

# Aggregation query
df_summary = pd.read_sql("""
    SELECT
        region,
        COUNT(*)            AS sales_count,
        ROUND(SUM(revenue),2) AS total_revenue,
        ROUND(AVG(revenue),2) AS avg_sale
    FROM dbo_sales
    GROUP BY region
    ORDER BY total_revenue DESC
""", conn_demo)
print("\nRegional summary:")
print(df_summary)

# TEMPLATE -- real SQL Server usage:
"""
import pyodbc
import pandas as pd

conn = pyodbc.connect(CONNECTION_STRING)

# Read a large table in chunks to avoid memory issues
chunk_list = []
for chunk in pd.read_sql("SELECT * FROM dbo.large_sales_table", conn, chunksize=10000):
    # Process each chunk
    chunk_list.append(chunk)

df_full = pd.concat(chunk_list, ignore_index=True)
print(f"Loaded {len(df_full):,} rows from SQL Server")

conn.close()
"""


# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
# Using pd.read_sql() with conn_demo:
#
# Task A: Read all sales data and calculate:
#   1. Total revenue by rep_name (sorted descending)
#   2. Average revenue per sale by region
# Print both results.
#
# Task B: Write a pd.read_sql() call with a parameterized query to get all
# sales with revenue > a threshold. Use threshold=1000.
# Print the matching rows.
#
# Expected output:
#   Revenue by rep:
#   Alice Ng    | $4,949.92
#   Bob Chen    | $3,549.93
#   ...
#
#   Avg revenue by region:
#   West | $1,949.97
#   ...
#
#   Sales over $1000:
#   [rows where revenue > 1000]





# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — WRITING A DATAFRAME TO SQL SERVER USING Py_MSSql
# ══════════════════════════════════════════════════════════════
# The custom Py_MSSql module (located at ../../G-Lesson_6/Modules/Py_MSSql.py)
# wraps pyodbc with helper methods for common data engineering tasks.
#
# REFERENCE PATH:
#   import sys
#   sys.path.append("../../G-Lesson_6/Modules")
#   from Py_MSSql import MSSqlConnection
#
# TYPICAL CLASS METHODS (check Py_MSSql.py for exact signatures):
#   conn = MSSqlConnection(server, database, trusted=True)
#   conn.connect()
#   df = conn.read_sql("SELECT * FROM table")
#   conn.write_df(df, table_name="dbo.my_table", if_exists="replace")
#   conn.execute_sql("TRUNCATE TABLE dbo.staging_table")
#   conn.close()
#
# PANDAS to_sql() -- ALTERNATIVE APPROACH with SQLAlchemy:
#   from sqlalchemy import create_engine
#   engine = create_engine(
#       "mssql+pyodbc://username:password@server/database?driver=ODBC+Driver+17+for+SQL+Server"
#   )
#   df.to_sql("table_name", engine, if_exists="replace", index=False)
#
# if_exists options:
#   "fail"    -- raise error if table exists
#   "replace" -- drop and recreate the table
#   "append"  -- insert rows into existing table

# EXAMPLE ──────────────────────────────────────────────────────

# TEMPLATE -- Full workflow with Py_MSSql (commented out, requires real connection)
"""
import sys
sys.path.append("../../G-Lesson_6/Modules")
from Py_MSSql import MSSqlConnection
import pandas as pd

# Step 1: Build your DataFrame
df_output = pd.DataFrame({
    "run_date":        ["2024-01-15"],
    "pipeline_name":   ["daily_sales_etl"],
    "rows_processed":  [15000],
    "status":          ["success"],
    "duration_sec":    [42.7],
})

# Step 2: Connect
db = MSSqlConnection(server="PROD-DB-01", database="DataWarehouse", trusted=True)
db.connect()

# Step 3: Write DataFrame to a staging table
db.write_df(
    df=df_output,
    table_name="dbo.etl_run_log",
    if_exists="append",    # do not overwrite existing history
)
print(f"Wrote {len(df_output)} rows to dbo.etl_run_log")

# Step 4: Verify
df_verify = db.read_sql("SELECT TOP 5 * FROM dbo.etl_run_log ORDER BY run_date DESC")
print(df_verify)

# Step 5: Always close
db.close()
"""

# Working demo using sqlite3 to_sql (same pandas API, different backend)
print("\n=== DataFrame to SQLite (mirrors SQL Server pattern) ===")

df_pipeline_log = pd.DataFrame({
    "run_date":       ["2024-01-15", "2024-01-16", "2024-01-17"],
    "pipeline_name":  ["daily_sales_etl"] * 3,
    "rows_processed": [15000, 14987, 16200],
    "status":         ["success", "success", "success"],
    "duration_sec":   [42.7, 38.1, 45.3],
})

# pandas to_sql writes a DataFrame to any SQL database
from sqlalchemy import create_engine
try:
    engine = create_engine("sqlite:///:memory:")
    df_pipeline_log.to_sql("etl_run_log", engine, if_exists="replace", index=False)

    # Read it back to verify
    df_verify = pd.read_sql("SELECT * FROM etl_run_log", engine)
    print("Written and read back:")
    print(df_verify)
except Exception as e:
    print(f"SQLAlchemy demo: {e}")
    print("Run: pip install sqlalchemy")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
# Using sqlite3 (not SQL Server -- same pattern, always works):
#
# Step 1: Read all sales from dbo_sales using pd.read_sql()
# Step 2: Transform in pandas:
#   - Add a "quarter" column: "Q1" for months 01-03, "Q2" for 04-06, etc.
#     (use pd.to_datetime and .dt.quarter)
#   - Add a "commission" column: revenue * 0.05, rounded to 2
# Step 3: Write the transformed DataFrame to a new table "dbo_sales_enriched"
#         using pd.DataFrame.to_sql() or a manual INSERT loop
# Step 4: Read back the enriched table and print it
#
# Expected output (enriched table):
#   sale_id | sale_date  | rep_name  | region | product | revenue | quarter | commission
#   1       | 2024-01-10 | Alice Ng  | West   | Laptop  | 4499.95 | Q1      | 225.0
#   ...





conn_demo.close()
print("\nDemo connection closed.")
