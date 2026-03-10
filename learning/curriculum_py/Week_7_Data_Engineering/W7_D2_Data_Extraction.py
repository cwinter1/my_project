# ══════════════════════════════════════════════════════════════
#  WEEK 7  |  DAY 2  |  DATA EXTRACTION
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Extract from multiple CSV files in a folder using glob and pd.concat
#  2. Extract from a SQLite database using sqlite3 and pd.read_sql
#  3. Extract from a REST API using requests with error handling
#
#  TIME:  ~30 minutes
#
#  YOUTUBE
#  ───────
#  Search: "Python glob read multiple CSV files pandas concat"
#  Search: "pandas read_sql database extraction"
#
# ══════════════════════════════════════════════════════════════

import pandas as pd
import sqlite3
import os
import glob
import io


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — EXTRACT FROM MULTIPLE CSV FILES IN A FOLDER
# ══════════════════════════════════════════════════════════════
# In production, data often arrives as daily or monthly files in a folder.
# Pattern:  sales_2024_01.csv, sales_2024_02.csv, sales_2024_03.csv, ...
# We need to read ALL matching files and combine them into one DataFrame.
#
# TOOLS:
#   glob.glob(pattern)  -- returns a list of file paths matching a pattern
#   pd.concat([df1, df2, ...])  -- stack DataFrames vertically
#   pd.read_csv(path)  -- read one file at a time
#
# GLOB PATTERNS:
#   "*.csv"             -- all CSV files in the current folder
#   "data/*.csv"        -- all CSVs in the 'data' subfolder
#   "sales_2024_*.csv"  -- files matching the naming convention

# EXAMPLE ──────────────────────────────────────────────────────

this_dir = os.path.dirname(__file__)

# First, create several small CSV files to simulate a folder of monthly data
monthly_csvs = {
    "sales_2024_01.csv": "date,rep,region,product,revenue\n2024-01-10,Alice,West,Laptop,1299.99\n2024-01-15,Bob,East,Monitor,399.99\n2024-01-20,Carol,West,Keyboard,149.99",
    "sales_2024_02.csv": "date,rep,region,product,revenue\n2024-02-05,Alice,West,Mouse,79.99\n2024-02-12,Bob,East,Headset,199.99\n2024-02-18,Dave,Central,Webcam,89.99",
    "sales_2024_03.csv": "date,rep,region,product,revenue\n2024-03-01,Carol,West,Laptop,1299.99\n2024-03-08,Bob,East,Keyboard,149.99\n2024-03-22,Eve,East,Monitor,399.99",
}

for filename, content in monthly_csvs.items():
    with open(os.path.join(this_dir, filename), "w") as f:
        f.write(content)

print("Sample CSV files created in:", this_dir)

# --- Read all matching files using glob ---
def extract_from_folder(folder_path, pattern="*.csv"):
    """
    Read all CSV files matching pattern in folder_path.
    Returns (combined_DataFrame, list_of_files_read).
    """
    search_path = os.path.join(folder_path, pattern)
    file_paths = sorted(glob.glob(search_path))

    if not file_paths:
        print(f"[EXTRACT] No files matching '{pattern}' in {folder_path}")
        return pd.DataFrame(), []

    print(f"[EXTRACT] Found {len(file_paths)} file(s):")
    dfs = []
    for path in file_paths:
        try:
            df = pd.read_csv(path)
            df["_source_file"] = os.path.basename(path)   # track which file each row came from
            dfs.append(df)
            print(f"  {os.path.basename(path)}: {len(df)} rows")
        except Exception as e:
            print(f"  ERROR reading {path}: {e}")

    combined = pd.concat(dfs, ignore_index=True)
    print(f"[EXTRACT] Combined: {len(combined)} rows total")
    return combined, file_paths

# Extract only the monthly sales files (not all CSVs in the folder)
df_combined, files = extract_from_folder(this_dir, pattern="sales_2024_*.csv")
print("\n=== Combined Sales Data ===")
print(df_combined)

# Aggregate across all files
print("\nRevenue by region (all months):")
print(df_combined.groupby("region")["revenue"].sum().round(2))


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
# Write a function called extract_with_metadata(folder_path, pattern) that:
#   1. Reads all matching CSV files using glob
#   2. Adds two metadata columns to each DataFrame:
#      "_source_file": just the filename (os.path.basename)
#      "_extract_month": the filename without path and extension
#        e.g. "sales_2024_01.csv" -> "sales_2024_01"
#   3. Returns (combined_df, extraction_summary) where extraction_summary is:
#      {"files_read": n, "total_rows": n, "columns": list_of_cols}
#
# Call it on this_dir with pattern="sales_2024_*.csv" and print the summary.
#
# Expected output:
#   {'files_read': 3, 'total_rows': 9, 'columns': ['date', 'rep', 'region',
#    'product', 'revenue', '_source_file', '_extract_month']}





# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — EXTRACT FROM A DATABASE (sqlite3 + pd.read_sql)
# ══════════════════════════════════════════════════════════════
# Extracting from a database involves:
#   1. Connecting to the database
#   2. Writing a SELECT query
#   3. Using pd.read_sql() to load results into a DataFrame
#   4. Closing the connection
#
# When extracting large tables:
#   - Use WHERE to filter (only load data you actually need)
#   - Use SELECT specific_columns (avoid SELECT *)
#   - Use LIMIT or WHERE date > 'last_run_date' for incremental extraction
#   - Use chunksize= in pd.read_sql() for very large tables

# EXAMPLE ──────────────────────────────────────────────────────

# Create an in-memory SQLite database with CRM data to extract from
conn = sqlite3.connect(":memory:")
cur = conn.cursor()

cur.executescript("""
    CREATE TABLE crm_deals (
        deal_id     INTEGER PRIMARY KEY,
        rep_name    TEXT,
        stage       TEXT,
        value       REAL,
        close_date  TEXT,
        is_won      INTEGER DEFAULT 0
    );

    INSERT INTO crm_deals VALUES (1,'Alice Ng','closed_won',45000,'2024-01-31',1);
    INSERT INTO crm_deals VALUES (2,'Bob Chen','negotiation',22000,NULL,0);
    INSERT INTO crm_deals VALUES (3,'Priya Mehta','closed_won',67000,'2024-02-28',1);
    INSERT INTO crm_deals VALUES (4,'Sara Jones','closed_won',31000,'2024-03-15',1);
    INSERT INTO crm_deals VALUES (5,'Bob Chen','prospecting',8000,NULL,0);
    INSERT INTO crm_deals VALUES (6,'Priya Mehta','negotiation',55000,NULL,0);
    INSERT INTO crm_deals VALUES (7,'Alice Ng','closed_won',89000,'2024-04-01',1);

    CREATE TABLE crm_activities (
        activity_id INTEGER PRIMARY KEY,
        deal_id     INTEGER,
        activity    TEXT,
        activity_date TEXT,
        notes       TEXT
    );

    INSERT INTO crm_activities VALUES (1,1,'call','2024-01-10','Initial discovery');
    INSERT INTO crm_activities VALUES (2,1,'demo','2024-01-17','Product demo delivered');
    INSERT INTO crm_activities VALUES (3,2,'call','2024-02-01','Follow-up call');
    INSERT INTO crm_activities VALUES (4,3,'demo','2024-02-10','Technical deep-dive');
    INSERT INTO crm_activities VALUES (5,7,'call','2024-03-15','Negotiation call');
""")
conn.commit()

def extract_from_database(connection, query, params=None):
    """
    Execute a SQL query and return the result as a DataFrame.
    """
    print(f"\n[EXTRACT DB] Running query...")
    try:
        if params:
            df = pd.read_sql(query, connection, params=params)
        else:
            df = pd.read_sql(query, connection)
        print(f"[EXTRACT DB] {len(df)} rows returned")
        return df, {"rows": len(df), "status": "ok"}
    except Exception as e:
        print(f"[EXTRACT DB] ERROR: {e}")
        return pd.DataFrame(), {"rows": 0, "status": "error", "error": str(e)}

# Extract all won deals
df_won, meta = extract_from_database(conn, "SELECT * FROM crm_deals WHERE is_won = 1")
print("\nWon deals:")
print(df_won)

# Extract with parameters
df_rep, meta = extract_from_database(
    conn,
    "SELECT * FROM crm_deals WHERE rep_name = ?",
    params=("Alice Ng",)
)
print("\nAlice's deals:")
print(df_rep)

# Multi-table extract with JOIN
df_joined, meta = extract_from_database(conn, """
    SELECT d.deal_id, d.rep_name, d.stage, d.value,
           COUNT(a.activity_id) AS activity_count
    FROM   crm_deals d
    LEFT JOIN crm_activities a ON d.deal_id = a.deal_id
    GROUP BY d.deal_id, d.rep_name, d.stage, d.value
    ORDER BY d.value DESC
""")
print("\nDeals with activity count:")
print(df_joined)


# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
# Write a function called extract_new_deals(connection, last_close_date) that:
#   1. Queries crm_deals for all closed deals with close_date > last_close_date
#   2. Prints how many new deals were found
#   3. Returns the DataFrame
#
# Call it twice:
#   extract_new_deals(conn, "2024-01-31")  -> should find 2 deals (Feb and March)
#   extract_new_deals(conn, "2024-04-01")  -> should find 0 new deals
#
# Expected output:
#   [EXTRACT DB] 3 rows returned
#   New deals since 2024-01-31: 3
#   [EXTRACT DB] 0 rows returned
#   New deals since 2024-04-01: 0





# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — EXTRACT FROM A REST API
# ══════════════════════════════════════════════════════════════
# Extracting from an API follows a consistent pattern:
#   1. Make a GET request to the endpoint
#   2. Parse the JSON response
#   3. Convert to a DataFrame
#   4. Handle pagination if the API returns data in pages
#
# JSONPLACEHOLDER: https://jsonplaceholder.typicode.com
# This is a free, public fake API perfect for learning.
# No authentication required.

# EXAMPLE ──────────────────────────────────────────────────────

def extract_from_api(url, params=None, timeout=10):
    """
    Fetch JSON data from a REST API and return as a DataFrame.
    Returns (DataFrame, metadata_dict).
    """
    try:
        import requests
        print(f"\n[EXTRACT API] GET {url}")
        response = requests.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        data = response.json()
        # Handle both list responses and nested responses
        if isinstance(data, list):
            df = pd.DataFrame(data)
        elif isinstance(data, dict):
            df = pd.DataFrame([data])
        else:
            df = pd.DataFrame()
        print(f"[EXTRACT API] {len(df)} records returned")
        return df, {"rows": len(df), "status": "ok", "url": url}
    except ImportError:
        print("[EXTRACT API] requests not installed. Run: pip install requests")
        return pd.DataFrame(), {"rows": 0, "status": "error", "error": "requests not installed"}
    except Exception as e:
        print(f"[EXTRACT API] ERROR: {e}")
        return pd.DataFrame(), {"rows": 0, "status": "error", "error": str(e)}

# Extract posts from JSONPlaceholder
df_posts, meta = extract_from_api("https://jsonplaceholder.typicode.com/posts",
                                   params={"userId": 1})
if not df_posts.empty:
    print("\nPosts for user 1:")
    print(df_posts[["id", "title"]].head(5))
    print(f"Total posts: {len(df_posts)}")

# Extract users
df_users, meta = extract_from_api("https://jsonplaceholder.typicode.com/users")
if not df_users.empty:
    print("\nUsers:")
    print(df_users[["id", "name", "email"]].head(5))


# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
# JSONPlaceholder supports a simple pagination-like filter via userId.
# Write a function called extract_posts_for_users(user_ids) that:
#   1. Loops through the list of user_ids
#   2. For each, calls extract_from_api with params={"userId": uid}
#   3. Adds a "user_id" column to each DataFrame
#   4. Combines all results into one DataFrame using pd.concat
#   5. Returns (combined_df, summary) where summary has:
#      {"total_rows": n, "users_processed": n, "users_failed": n}
#
# Call it with user_ids=[1, 2, 3, 4] and print:
#   - Total rows
#   - Users processed
#   - First 5 rows (id, userId, title columns)
#
# Expected output:
#   [EXTRACT API] GET https://jsonplaceholder.typicode.com/posts  (x4)
#   Total rows: 40
#   Users processed: 4
#   [first 5 rows]




conn.close()
