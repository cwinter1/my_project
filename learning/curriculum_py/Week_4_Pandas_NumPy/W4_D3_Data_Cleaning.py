# ══════════════════════════════════════════════════════════════
#  WEEK 4  |  DAY 3  |  DATA CLEANING
# ══════════════════════════════════════════════════════════════
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Detect and handle missing (null) values using isnull, dropna, and fillna
#  2. Find and remove duplicate rows using duplicated and drop_duplicates
#  3. Convert column data types using astype, pd.to_datetime, and pd.to_numeric
#
#  TIME:  ~30-35 minutes
#
#  YOUTUBE
#  ───────
#  Search: "pandas data cleaning missing values tutorial"
#  Search: "pandas dropna fillna duplicates astype"
# ══════════════════════════════════════════════════════════════

import pandas as pd
import numpy as np
import os

# Load the Titanic dataset — it has real nulls to practice on
this_file = os.path.dirname(__file__)
titanic_path = os.path.join(this_file, "..", "datasets", "titanic_train.xlsx")

try:
    df = pd.read_excel(titanic_path)
    print("Titanic loaded:", df.shape)
except FileNotFoundError:
    print("titanic_train.xlsx not found. Using inline demo data.")
    # Inline fallback so the lesson works without the file
    df = pd.DataFrame({
        "PassengerId": range(1, 11),
        "Survived": [0, 1, 1, 1, 0, 0, 0, 1, 1, 0],
        "Pclass":   [3, 1, 3, 1, 3, 3, 1, 3, 2, 2],
        "Name":     ["Braund, Mr. Owen", "Cumings, Mrs. John", "Heikkinen, Miss. Laina",
                     "Futrelle, Mrs. Jacques", "Allen, Mr. William",
                     "Moran, Mr. James", "McCarthy, Mr. Timothy",
                     "Palsson, Master. Gosta", "Johnson, Mrs. Oscar", "Nasser, Mrs. Nicholas"],
        "Sex":      ["male","female","female","female","male","male","male","male","female","female"],
        "Age":      [22.0, 38.0, 26.0, 35.0, np.nan, np.nan, 54.0, 2.0, 27.0, 14.0],
        "Fare":     [7.25, 71.28, 7.93, 53.10, 8.05, 8.46, 51.86, 21.07, 11.13, 30.07],
        "Cabin":    [np.nan, "C85", np.nan, "C123", np.nan, np.nan, "E46", np.nan, np.nan, np.nan],
        "Embarked": ["S", "C", "S", "S", "S", "Q", "S", "S", "S", np.nan],
    })


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — FINDING AND HANDLING NULL VALUES (isnull, dropna, fillna)
# ══════════════════════════════════════════════════════════════
# NULL values (NaN in pandas) appear whenever data is missing.
# They break calculations: sum, mean, etc. silently skip them.
# You must decide: drop the row, fill with a value, or leave it as-is.
#
# DETECTION:
#   df.isnull()              -- True/False mask for every cell
#   df.isnull().sum()        -- count of nulls per column
#   df.isnull().sum() / len(df) * 100  -- null percentage per column
#   df.notnull()             -- opposite of isnull
#
# HANDLING:
#   df.dropna()              -- drop rows with ANY null
#   df.dropna(subset=["Age"]) -- drop rows where Age is null only
#   df.dropna(how="all")     -- drop rows where ALL values are null
#   df.fillna(0)             -- replace all nulls with 0
#   df.fillna({"Age": df["Age"].mean()}) -- fill each column differently
#   df["col"].fillna(method="ffill") -- forward-fill (carry last known value)

# EXAMPLE ──────────────────────────────────────────────────────
print("\n=== NULL VALUE ANALYSIS ===")
print("Null count per column:")
print(df.isnull().sum())

print("\nNull percentage per column:")
null_pct = (df.isnull().sum() / len(df) * 100).round(1)
print(null_pct)

# Which columns have more than 10% nulls?
high_null_cols = null_pct[null_pct > 10].index.tolist()
print(f"\nColumns with >10% nulls: {high_null_cols}")

# Strategy 1: Fill Age with the median (more robust than mean for skewed data)
median_age = df["Age"].median()
df_filled = df.copy()
df_filled["Age"] = df_filled["Age"].fillna(median_age)
print(f"\nMedian age used for fill: {median_age}")
print(f"Age nulls after fill: {df_filled['Age'].isnull().sum()}")   # 0

# Strategy 2: Fill Embarked (categorical) with the most common value (mode)
most_common_port = df["Embarked"].mode()[0]
df_filled["Embarked"] = df_filled["Embarked"].fillna(most_common_port)
print(f"Embarked filled with: {most_common_port}")

# Strategy 3: Drop rows where the key target column is null
df_dropped = df.dropna(subset=["Survived"])
print(f"\nRows after dropna on Survived: {len(df_dropped)} (was {len(df)})")

# Strategy 4: Drop an entire column that is mostly null (Cabin is ~77% null)
if "Cabin" in df_filled.columns and null_pct.get("Cabin", 0) > 50:
    df_no_cabin = df_filled.drop(columns=["Cabin"])
    print(f"Dropped 'Cabin' column. Remaining columns: {len(df_no_cabin.columns)}")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
# Use the original df (with nulls).
# Create a new DataFrame df_clean by:
#   1. Filling null Ages with the MEAN age (round the mean to 1 decimal)
#   2. Dropping any rows where Embarked is null
#   3. Print how many rows were removed (before vs after)
#   4. Print the null count per column to confirm no nulls remain
#      (except Cabin which you are allowed to leave as-is)
#
# Expected output:
#   Original rows: 891
#   After cleaning: 889
#   Null counts after cleaning:
#   ... (only Cabin should remain > 0 if present)




# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — FINDING AND REMOVING DUPLICATES (duplicated, drop_duplicates)
# ══════════════════════════════════════════════════════════════
# Duplicate rows cause inflated counts and incorrect aggregations.
# pandas makes it easy to detect and remove them.
#
#   df.duplicated()                -- True for every row that is a duplicate of a previous row
#   df.duplicated(subset=["col"]) -- duplicates based on one column only
#   df.duplicated().sum()          -- count of duplicate rows
#   df.drop_duplicates()           -- return DataFrame with duplicates removed
#   df.drop_duplicates(subset=["col"], keep="last") -- keep last occurrence

# EXAMPLE ──────────────────────────────────────────────────────
# Create a DataFrame with intentional duplicates to demonstrate
orders_data = {
    "order_id":    ["ORD-001", "ORD-002", "ORD-003", "ORD-001", "ORD-004", "ORD-002"],
    "customer":    ["Acme",    "Beta",    "Gamma",   "Acme",    "Delta",   "Beta"],
    "product":     ["Widget",  "Gadget",  "Widget",  "Widget",  "Gadget",  "Gadget"],
    "amount":      [1200,      850,       700,       1200,      950,       850],
}

df_orders = pd.DataFrame(orders_data)
print("\n=== DUPLICATES ===")
print("Orders with duplicates:")
print(df_orders)

# Check for duplicates
print(f"\nDuplicate rows: {df_orders.duplicated().sum()}")   # 2

# See which rows are duplicates
print("\nDuplicate mask:")
print(df_orders[df_orders.duplicated(keep=False)])   # show ALL copies

# Remove complete duplicates
df_no_dups = df_orders.drop_duplicates()
print(f"\nAfter drop_duplicates: {len(df_no_dups)} rows (was {len(df_orders)})")
print(df_no_dups)

# Check duplicates on a single column (order_id should be unique)
dup_ids = df_orders[df_orders.duplicated(subset=["order_id"])]["order_id"]
print(f"\nDuplicate order IDs: {dup_ids.tolist()}")

# Keep the last occurrence when there are conflicting duplicates
df_keep_last = df_orders.drop_duplicates(subset=["order_id"], keep="last")
print("\nAfter dedup on order_id (keep last):")
print(df_keep_last)


# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
# The CRM export below has duplicate contact records.
# Some contacts appear multiple times with slightly different entry dates.
#
# Tasks:
#   1. Count how many rows are full duplicates
#   2. Count how many unique email addresses exist
#   3. Remove duplicates keeping only the FIRST occurrence per email
#   4. Print the cleaned DataFrame
#
# Expected output:
#   Full duplicate rows: 1
#   Unique emails: 4
#   Cleaned contacts (4 rows):
#   [cleaned data]

contacts = pd.DataFrame({
    "email":      ["alice@corp.com", "bob@corp.com", "carol@corp.com",
                   "bob@corp.com",   "dave@corp.com","alice@corp.com"],
    "name":       ["Alice Ng",       "Bob Chen",     "Carol Diaz",
                   "Bob Chen",       "Dave Park",    "Alice Ng"],
    "created":    ["2024-01-10",     "2024-01-12",   "2024-01-15",
                   "2024-01-12",     "2024-01-18",   "2024-01-10"],
})




# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — CONVERTING DATA TYPES (astype, pd.to_datetime, pd.to_numeric)
# ══════════════════════════════════════════════════════════════
# When pandas reads data from Excel or CSV, it sometimes assigns the wrong type.
# Common issues:
#   - Numbers stored as strings (e.g. "1,500" instead of 1500)
#   - Dates stored as strings ("2024-01-15" instead of datetime)
#   - Booleans stored as "True"/"False" strings
#
# CONVERSION TOOLS:
#   df["col"].astype(int)          -- convert to integer (fails on nulls/non-numeric)
#   df["col"].astype(float)        -- convert to float
#   df["col"].astype(str)          -- convert to string
#   pd.to_numeric(df["col"])       -- smart conversion, errors="coerce" turns bad values to NaN
#   pd.to_datetime(df["col"])      -- parse strings into datetime objects
#   df["col"].astype("category")   -- memory-efficient for low-cardinality string columns

# EXAMPLE ──────────────────────────────────────────────────────
# Create a messy import to demonstrate
raw_data = pd.DataFrame({
    "sale_date":  ["2024-01-15", "2024-02-22", "2024-03-08", "2024-04-01"],
    "amount":     ["1500",       "2,300",       "850",         "4100"],
    "qty":        ["10",         "15",          "7",           "22"],
    "is_online":  ["True",       "False",       "True",        "True"],
    "region":     ["West",       "East",        "West",        "Central"],
})

print("\n=== RAW DATA TYPES ===")
print(raw_data.dtypes)
# All columns are "object" (string) because they were read from a dirty source

# Convert sale_date to datetime
raw_data["sale_date"] = pd.to_datetime(raw_data["sale_date"])

# Convert amount: strip the comma first, then to numeric
raw_data["amount"] = pd.to_numeric(raw_data["amount"].str.replace(",", ""))

# Convert qty to integer
raw_data["qty"] = raw_data["qty"].astype(int)

# Convert is_online to boolean
raw_data["is_online"] = raw_data["is_online"].map({"True": True, "False": False})

# Convert region to category (saves memory when there are many repeated values)
raw_data["region"] = raw_data["region"].astype("category")

print("\n=== CLEANED DATA TYPES ===")
print(raw_data.dtypes)
print()
print(raw_data)

# Demonstrate pd.to_numeric with errors="coerce"
messy_amounts = pd.Series(["1500", "2300", "N/A", "850", "unknown", "4100"])
clean_amounts = pd.to_numeric(messy_amounts, errors="coerce")  # bad values become NaN
print("\nCleaned amounts (coerce):", clean_amounts.tolist())
# [1500.0, 2300.0, NaN, 850.0, NaN, 4100.0]

# Extract date parts after converting to datetime
raw_data["month"] = raw_data["sale_date"].dt.month
raw_data["year"]  = raw_data["sale_date"].dt.year
raw_data["day_name"] = raw_data["sale_date"].dt.day_name()
print("\nWith date parts extracted:")
print(raw_data[["sale_date", "month", "year", "day_name"]])


# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
# The DataFrame below arrived from an HR system export with bad data types.
# Fix all of them so the final dtypes are correct.
#
# Required final types:
#   hire_date   -> datetime64
#   salary      -> float64 (strip "$" and "," first)
#   years_exp   -> int64 (strip " yrs")
#   is_manager  -> bool (map "Yes"/"No" to True/False)
#   department  -> category
#
# After fixing, print:
#   1. The dtypes
#   2. The average salary by is_manager group
#
# Expected output:
#   hire_date      datetime64[ns]
#   salary         float64
#   years_exp      int64
#   is_manager     bool
#   department     category
#
#   Average salary:
#   is_manager
#   False    76500.0
#   True     98000.0

hr_export = pd.DataFrame({
    "hire_date":  ["2020-03-15", "2018-07-01", "2022-11-20", "2019-05-08"],
    "salary":     ["$95,000",    "$72,000",    "$81,000",    "$88,000"],
    "years_exp":  ["8 yrs",      "12 yrs",     "3 yrs",      "7 yrs"],
    "is_manager": ["Yes",        "No",         "No",         "No"],
    "department": ["Engineering","Sales",      "Finance",    "Engineering"],
})


