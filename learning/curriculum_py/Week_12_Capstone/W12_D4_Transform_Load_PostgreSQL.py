# ══════════════════════════════════════════════════════════════
#  WEEK 12  |  DAY 4  |  TRANSFORM AND LOAD — SILVER LAYER
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Apply Silver layer transformations to raw records
#  2. Load cleaned records into SQLite (same SQL as PostgreSQL)
#  3. Query results using SELECT, COUNT, GROUP BY, ORDER BY
#
#  PIPELINE CONTEXT
#  ─────────────────
#  This is Stage 4 of the capstone pipeline:
#    Day 1: Docker + Kafka setup (simulation)
#    Day 2: Extract data from API, produce to Kafka
#    Day 3: Store raw records in Bronze layer (MinIO)
#    Day 4: Transform and load to PostgreSQL (Silver) <-- today
#    Day 5: Orchestrate the full pipeline with logging
#
#  TIME:  ~45 minutes
#
# ══════════════════════════════════════════════════════════════


import sqlite3
import os
from datetime import datetime


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — SILVER LAYER TRANSFORMATION
# ══════════════════════════════════════════════════════════════
#
#  The Silver layer converts raw Bronze data into clean,
#  consistent records that are safe to load into a database.
#
#  Standard Silver transformations:
#
#    1. Strip whitespace from string fields
#       raw:     "  Tel Aviv  "  ->  "Tel Aviv"
#
#    2. Replace empty strings with None
#       raw:     ""  ->  None (becomes NULL in SQL)
#
#    3. Rename columns to snake_case
#       raw:     "DistrictName"  ->  "district_name"
#
#    4. Add a loaded_at timestamp
#       Every row gets a loaded_at field set to the current time.
#       This lets you audit when each record was processed and
#       makes it easy to find "records loaded in the last hour".
#
#    5. Cast numeric strings to int or float
#       raw:     "42"  ->  42
#
#  The transformation function takes a list of raw dicts and
#  returns a new list of cleaned dicts.  It never modifies the
#  original list — this preserves the Bronze record unchanged.
#
# EXAMPLE ──────────────────────────────────────────────────────

def transform_demo(record):
    """Apply basic Silver transformations to one record dict."""
    cleaned = {}
    for key, value in record.items():
        # Strip whitespace from strings, replace empty with None.
        if isinstance(value, str):
            value = value.strip()
            if value == "":
                value = None
        cleaned[key] = value
    # Add loaded_at timestamp.
    cleaned["loaded_at"] = datetime.now().isoformat()
    return cleaned

raw_demo = {"district": "  North  ", "year": 2022, "note": ""}
cleaned_demo = transform_demo(raw_demo)

print("Raw record    :", raw_demo)
print("Cleaned record:", cleaned_demo)
print(f"  'note' is now: {repr(cleaned_demo['note'])} (None = SQL NULL)")
print(f"  'district' stripped: '{cleaned_demo['district']}'")
print(f"  loaded_at added: {cleaned_demo['loaded_at'][:19]}")


# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — LOADING TO SQLite (SAME SQL AS PostgreSQL)
# ══════════════════════════════════════════════════════════════
#
#  SQLite is a file-based relational database built into Python.
#  It uses standard SQL, so the INSERT, SELECT, GROUP BY, and
#  ORDER BY statements you write here work identically in
#  PostgreSQL (just the connection setup differs).
#
#  Key steps to load records:
#
#    1. Connect: sqlite3.connect("mydb.db") returns a Connection.
#       Pass ":memory:" to create a temporary in-memory database.
#
#    2. Get a cursor: conn.cursor() returns a Cursor object.
#       All SQL is executed through the cursor.
#
#    3. CREATE TABLE: define column names and types.
#       Use IF NOT EXISTS so re-running the script does not error.
#
#    4. INSERT with executemany: pass a list of tuples.
#       executemany is much faster than calling execute() in a loop.
#
#    5. Commit: conn.commit() writes the changes to disk.
#
#    6. Close: conn.close() releases the file lock.
#
# EXAMPLE ──────────────────────────────────────────────────────

conn = sqlite3.connect(":memory:")   # in-memory database
cursor = conn.cursor()

# Create a simple table.
cursor.execute("""
    CREATE TABLE IF NOT EXISTS demo_records (
        id          INTEGER,
        district    TEXT,
        accidents   INTEGER,
        year        INTEGER,
        loaded_at   TEXT
    )
""")

# Insert 3 rows using executemany.
demo_rows = [
    (1, "North",  42, 2022, datetime.now().isoformat()),
    (2, "South",  31, 2022, datetime.now().isoformat()),
    (3, "Center", 78, 2023, datetime.now().isoformat()),
]
cursor.executemany(
    "INSERT INTO demo_records VALUES (?, ?, ?, ?, ?)",
    demo_rows,
)
conn.commit()

# Verify the count.
cursor.execute("SELECT COUNT(*) FROM demo_records")
count = cursor.fetchone()[0]
print(f"\nInserted rows: {count}")
conn.close()

# REAL MODE (requires PostgreSQL + psycopg2) ───────────────────
# import psycopg2
#
# conn = psycopg2.connect(
#     host="localhost", port=5432,
#     dbname="pipeline_db", user="postgres", password="postgres"
# )
# cursor = conn.cursor()
# cursor.execute("CREATE TABLE IF NOT EXISTS pipeline_data (...)")
# cursor.executemany("INSERT INTO pipeline_data VALUES (%s, %s, %s, %s, %s)", rows)
# conn.commit()
# cursor.close()
# conn.close()
# ──────────────────────────────────────────────────────────────


# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — QUERYING RESULTS
# ══════════════════════════════════════════════════════════════
#
#  After loading, we run SQL queries to verify and summarize
#  the data.  Three standard verification queries:
#
#    1. Total count:  SELECT COUNT(*) FROM table_name
#       Confirms the expected number of rows were loaded.
#
#    2. Top N rows:   SELECT * FROM table_name ORDER BY col DESC LIMIT 5
#       Shows the rows with the highest value in a numeric column.
#
#    3. Group by:     SELECT col, COUNT(*) FROM table_name GROUP BY col
#       Counts rows per unique value of a categorical column.
#       Shows how the data is distributed across categories.
#
#  cursor.fetchall() returns a list of tuples.
#  cursor.fetchone() returns one tuple (or None).
#
# EXAMPLE ──────────────────────────────────────────────────────

conn2 = sqlite3.connect(":memory:")
c2 = conn2.cursor()

c2.execute("""
    CREATE TABLE IF NOT EXISTS traffic (
        id INTEGER, district TEXT, accidents INTEGER, year INTEGER
    )
""")
c2.executemany(
    "INSERT INTO traffic VALUES (?, ?, ?, ?)",
    [
        (1, "North",    42, 2022),
        (2, "South",    31, 2022),
        (3, "Center",   78, 2022),
        (4, "North",    39, 2023),
        (5, "Center",   65, 2023),
        (6, "South",    50, 2023),
    ],
)
conn2.commit()

# Query 1: total count.
c2.execute("SELECT COUNT(*) FROM traffic")
print(f"\nTotal rows in traffic table: {c2.fetchone()[0]}")

# Query 2: top 3 rows by accidents (highest first).
c2.execute("SELECT district, year, accidents FROM traffic ORDER BY accidents DESC LIMIT 3")
print("Top 3 by accidents:")
for row in c2.fetchall():
    print(f"  {row[0]:8s} {row[1]}  {row[2]} accidents")

# Query 3: count per district.
c2.execute("SELECT district, COUNT(*) AS row_count FROM traffic GROUP BY district ORDER BY row_count DESC")
print("Rows per district:")
for row in c2.fetchall():
    print(f"  {row[0]:8s} : {row[1]} rows")

conn2.close()


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
#
#  Write a function transform_records(raw_records)
#  that cleans a list of raw record dicts and returns a new
#  list of cleaned dicts.
#
#  For each record the function must:
#    1. Strip leading/trailing whitespace from all string values
#    2. Replace any empty string value with None
#    3. Add a key "loaded_at" with value datetime.now().isoformat()
#
#  The function must return a NEW list — do not modify the
#  original raw_records list.
#
#  After calling the function, print the count of cleaned records
#  and show the first record to confirm loaded_at was added.
#
#  Expected output:
#    Transformed 5 records
#    First cleaned record:
#      {'_id': 1, 'district': 'North', 'accidents': 42, 'year': 2022, 'notes': None, 'loaded_at': '...'}

# --- starting data ---
raw_records = [
    {"_id": 1, "district": "North  ",  "accidents": 42, "year": 2022, "notes": ""},
    {"_id": 2, "district": "  South",  "accidents": 31, "year": 2022, "notes": "partial"},
    {"_id": 3, "district": "Center",   "accidents": 78, "year": 2022, "notes": ""},
    {"_id": 4, "district": " Haifa ",  "accidents": 55, "year": 2023, "notes": ""},
    {"_id": 5, "district": "Tel Aviv", "accidents": 91, "year": 2023, "notes": "verified"},
]




# (write your code here)




# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
#
#  Write a function load_to_db(records, db_path)
#  that loads cleaned records into SQLite and returns the row
#  count in the table after loading.
#
#  Rules:
#    - Connect to db_path (use ":memory:" to keep it in RAM)
#    - CREATE TABLE IF NOT EXISTS pipeline_data with columns:
#        record_id INTEGER, district TEXT, accidents INTEGER,
#        year INTEGER, notes TEXT, loaded_at TEXT
#    - Use executemany to insert all records
#    - Commit and then run SELECT COUNT(*) to get the row count
#    - Close the connection and return the row count
#
#  Use the cleaned records returned by transform_records
#  in Exercise 1 as input.
#
#  Expected output:
#    Loaded 5 rows into pipeline_data

# --- starting data ---
# Use cleaned_records from Exercise 1 above
db_path = ":memory:"




# (write your code here)




# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
#
#  Connect to a new in-memory SQLite database and insert the
#  records below. Then write and execute three SQL query strings:
#
#    query_total   : SELECT COUNT(*) FROM pipeline_data
#    query_top5    : top 5 rows ordered by accidents DESC
#    query_by_year : count of rows per year, ordered by year ASC
#
#  Print the results of each query.
#
#  Expected output:
#    Total rows: 8
#    Top 5 by accidents:
#      Center 2023 91 accidents
#      North  2023 88 accidents
#      Center 2022 78 accidents
#      South  2023 71 accidents
#      Haifa  2022 65 accidents
#    Rows per year:
#      2022 : 4 rows
#      2023 : 4 rows

# --- starting data ---
analysis_records = [
    (1, "North",  42, 2022, "2024-01-15T10:00:00"),
    (2, "South",  31, 2022, "2024-01-15T10:00:00"),
    (3, "Center", 78, 2022, "2024-01-15T10:00:00"),
    (4, "Haifa",  65, 2022, "2024-01-15T10:00:00"),
    (5, "North",  88, 2023, "2024-01-15T10:00:00"),
    (6, "South",  71, 2023, "2024-01-15T10:00:00"),
    (7, "Center", 91, 2023, "2024-01-15T10:00:00"),
    (8, "Haifa",  60, 2023, "2024-01-15T10:00:00"),
]

query_total    = "SELECT COUNT(*) FROM pipeline_data"
query_top5     = "SELECT district, year, accidents FROM pipeline_data ORDER BY accidents DESC LIMIT 5"
query_by_year  = "SELECT year, COUNT(*) FROM pipeline_data GROUP BY year ORDER BY year ASC"




# (write your code here)




