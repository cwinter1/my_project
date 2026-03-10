# ══════════════════════════════════════════════════════════════
#  WEEK 4  |  DAY 2  |  PANDAS BASICS
# ══════════════════════════════════════════════════════════════
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Create a DataFrame from a dictionary or list of dicts
#  2. Select columns, rows (loc/iloc), and individual cells
#  3. Read real data from an Excel file using pd.read_excel()
#
#  TIME:  ~30-35 minutes
#
#  YOUTUBE
#  ───────
#  Search: "Python pandas DataFrame tutorial beginner"
#  Search: "pandas loc iloc selecting rows columns"
# ══════════════════════════════════════════════════════════════

# Install if needed:
#   pip install pandas openpyxl

import pandas as pd
import numpy as np
import os

# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — CREATING A DATAFRAME (FROM DICT, FROM LIST OF DICTS)
# ══════════════════════════════════════════════════════════════
# A DataFrame is a 2D table with labeled rows (index) and columns.
# It is the core data structure in pandas and works like a spreadsheet in code.
#
# TWO COMMON CREATION PATTERNS:
#
# 1. From a dict of lists (each key is a column name, each list is the column data)
#    pd.DataFrame({"col_a": [...], "col_b": [...]})
#
# 2. From a list of dicts (each dict is one row)
#    pd.DataFrame([{"col_a": v1, "col_b": v2}, {...}])
#
# The second pattern maps directly to how JSON API responses look.

# EXAMPLE ──────────────────────────────────────────────────────
# --- Method 1: dict of lists ---
employees_dict = {
    "emp_id":     ["E001", "E002", "E003", "E004", "E005"],
    "name":       ["Alice Ng", "Bob Chen", "Carol Diaz", "Dave Park", "Eve Torres"],
    "department": ["Engineering", "Sales", "Finance", "Engineering", "Sales"],
    "salary":     [95000, 72000, 81000, 88000, 67500],
    "start_year": [2021, 2019, 2020, 2022, 2023],
}

df_emp = pd.DataFrame(employees_dict)
print("=== Employee DataFrame ===")
print(df_emp)
print()
print("Shape:", df_emp.shape)              # (5, 5)  -> 5 rows, 5 columns
print("Columns:", list(df_emp.columns))
print("Index:", list(df_emp.index))        # [0, 1, 2, 3, 4]
print()

# Set a meaningful index (instead of 0, 1, 2 ...)
df_emp = df_emp.set_index("emp_id")
print("With emp_id as index:")
print(df_emp)

# --- Method 2: list of dicts (common from API responses) ---
deals_list = [
    {"deal_id": "D-001", "account": "Acme Ltd",   "stage": "closed_won",  "value": 45000},
    {"deal_id": "D-002", "account": "Beta Corp",  "stage": "negotiation", "value": 22000},
    {"deal_id": "D-003", "account": "Gamma Inc",  "stage": "closed_won",  "value": 67000},
    {"deal_id": "D-004", "account": "Delta LLC",  "stage": "prospecting", "value": 8000},
    {"deal_id": "D-005", "account": "Epsilon SA", "stage": "closed_won",  "value": 31000},
]

df_deals = pd.DataFrame(deals_list)
print("\n=== Deals DataFrame ===")
print(df_deals)
print()
print("Data types:")
print(df_deals.dtypes)

# Basic summary info
print("\nDataFrame info:")
df_deals.info()


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
# Create a DataFrame using the LIST OF DICTS method with the data below.
# Then:
#   1. Print the first 3 rows using .head(3)
#   2. Print the total value of all deals
#   3. Print the number of deals per stage using value_counts()
#
# Data:
#   [{"rep": "Tom Reyes",   "stage": "closed_won",  "value": 85000, "region": "West"},
#    {"rep": "Priya Mehta", "stage": "closed_won",  "value": 120000,"region": "East"},
#    {"rep": "Sara Jones",  "stage": "negotiation", "value": 45000, "region": "Central"},
#    {"rep": "Omar Nasser", "stage": "prospecting", "value": 15000, "region": "East"},
#    {"rep": "Lena Kim",    "stage": "closed_won",  "value": 72000, "region": "West"},
#    {"rep": "Tom Reyes",   "stage": "negotiation", "value": 38000, "region": "West"}]
#
# Expected output (value_counts):
#   closed_won     3
#   negotiation    2
#   prospecting    1
#   Total pipeline value: $375,000




# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — SELECTING COLUMNS, ROWS (loc, iloc), AND CELLS
# ══════════════════════════════════════════════════════════════
# COLUMN SELECTION:
#   df["column"]               -- one column as a Series
#   df[["col_a", "col_b"]]     -- multiple columns as a DataFrame
#
# ROW SELECTION:
#   df.loc[label]              -- by label (index value or slice)
#   df.loc[label, "col"]       -- label-based: row + column
#   df.iloc[integer]           -- by integer position (0-based)
#   df.iloc[0:3]               -- first 3 rows by position
#   df.iloc[0:3, 1:3]          -- rows 0-2, columns 1-2 by position
#
# DIFFERENCE:
#   loc  uses the actual index LABELS
#   iloc uses integer POSITIONS (like Python list indexing)

# EXAMPLE ──────────────────────────────────────────────────────
# Working with the employee DataFrame (emp_id as index)
print("=== Column Selection ===")
print("Names column:")
print(df_emp["name"])

print("\nName and salary:")
print(df_emp[["name", "salary"]])

# loc — use the actual label (emp_id in our case)
print("\n=== loc (label-based) ===")
print("Row E003:")
print(df_emp.loc["E003"])

print("\nE002 salary:", df_emp.loc["E002", "salary"])    # 72000

# Slice with loc (includes the endpoint)
print("\nE001 through E003:")
print(df_emp.loc["E001":"E003"])

# iloc — use integer position
print("\n=== iloc (position-based) ===")
print("First row (position 0):")
print(df_emp.iloc[0])

print("\nLast row:")
print(df_emp.iloc[-1])

print("\nRows 1-3, columns 0-1:")
print(df_emp.iloc[1:4, 0:2])

# Useful properties
print("\nFirst 2 rows:")
print(df_emp.head(2))

print("\nLast 2 rows:")
print(df_emp.tail(2))

# Reset to numeric index for simpler demos
df_emp_reset = df_emp.reset_index()
print("\nWith reset index:")
print(df_emp_reset[["emp_id", "name", "salary"]])


# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
# Using df_emp (the employee DataFrame with emp_id as index), complete:
#
# Task A: Select only name and department columns and print
# Task B: Use loc to get Carol Diaz's row (emp_id = E003)
# Task C: Use iloc to get the salary of the 4th employee (position 3)
# Task D: Use iloc to get a sub-DataFrame of rows 0-2, columns "name" and "salary"
#         (Tip: pass column names to loc, or integer column positions to iloc)
# Task E: Find the employee with the highest salary using .idxmax()
#         on the salary column. Print their full row.
#
# Expected output (Task E):
#   Highest earner:
#   name          Alice Ng
#   department    Engineering
#   salary           95000
#   start_year        2021




# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — READING FROM EXCEL FILE USING pd.read_excel()
# ══════════════════════════════════════════════════════════════
# pd.read_excel() reads one or more sheets from an Excel file into a DataFrame.
# Requires: pip install openpyxl
#
# Key parameters:
#   pd.read_excel("file.xlsx")                    -- reads the first sheet
#   pd.read_excel("file.xlsx", sheet_name="Sheet2")
#   pd.read_excel("file.xlsx", header=0)          -- row 0 is the header
#   pd.read_excel("file.xlsx", usecols="A:D")     -- read columns A through D
#   pd.read_excel("file.xlsx", nrows=100)         -- read first 100 data rows
#
# Always build the path using os.path so the script works on any machine.

# EXAMPLE ──────────────────────────────────────────────────────
this_file = os.path.dirname(__file__)
titanic_path = os.path.join(this_file, "..", "datasets", "titanic_train.xlsx")

try:
    df_titanic = pd.read_excel(titanic_path)

    print("\n=== Titanic Dataset ===")
    print("Shape:", df_titanic.shape)
    print("\nFirst 5 rows:")
    print(df_titanic.head())

    print("\nColumn names:")
    print(list(df_titanic.columns))

    print("\nData types:")
    print(df_titanic.dtypes)

    print("\nBasic statistics:")
    print(df_titanic.describe())

    # Quick explorations
    print("\nSurvival rate:")
    print(df_titanic["Survived"].value_counts())

    print("\nPassenger class distribution:")
    print(df_titanic["Pclass"].value_counts().sort_index())

    # Select a meaningful subset
    subset = df_titanic[["Name", "Sex", "Age", "Pclass", "Survived"]].head(10)
    print("\nFirst 10 passengers (key columns):")
    print(subset)

except FileNotFoundError:
    print(f"\ntitanic_train.xlsx not found at: {titanic_path}")
    print("Make sure the datasets folder contains titanic_train.xlsx")
    # Demonstrate the API with a small inline DataFrame instead
    demo = pd.DataFrame({
        "Name": ["Alice", "Bob", "Carol"],
        "Age":  [29, 45, 31],
        "Survived": [1, 0, 1]
    })
    print("\nDemo DataFrame (substitute):")
    print(demo)


# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
# Load titanic_train.xlsx (path already defined above as titanic_path).
# Answer the following questions using pandas selection:
#
# 1. How many passengers are in the dataset? (use len or .shape[0])
# 2. What is the average age of passengers? (round to 1 decimal)
# 3. How many passengers survived? (Survived == 1)
# 4. Select all columns for passengers in First Class (Pclass == 1)
#    and print the first 5 rows
# 5. Use iloc to print the 10th passenger's Name and Age
#
# Expected output:
#   Total passengers: 891
#   Average age: 29.7
#   Survivors: 342
#   First Class passengers (first 5):
#   [first 5 rows of Pclass==1 passengers]
#   Passenger 10: <Name>, Age: <Age>


