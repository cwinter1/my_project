# ══════════════════════════════════════════════════════════════
#  WEEK 3  |  DAY 2  |  CSV DATA
# ══════════════════════════════════════════════════════════════
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Read a CSV file row by row using Python's csv module
#  2. Write and append CSV data using csv.writer and csv.DictWriter
#  3. Load a CSV directly into a pandas DataFrame with pd.read_csv()
#
#  TIME:  ~30-35 minutes
#
#  YOUTUBE
#  ───────
#  Search: "Python csv module read write tutorial"
#  Search: "Python pandas read_csv DataFrame tutorial"
# ══════════════════════════════════════════════════════════════

import csv
import os
import io

# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — READING CSV WITH THE csv MODULE
# ══════════════════════════════════════════════════════════════
# CSV (Comma-Separated Values) is the most common format for tabular data.
# Python's built-in csv module handles quoting, escaping, and delimiters.
#
# Two main readers:
#   csv.reader(f)       -- returns rows as lists: ["Alice", "Sales", "85000"]
#   csv.DictReader(f)   -- returns rows as dicts: {"name": "Alice", "dept": "Sales"}
#
# DictReader is usually preferred because column names are explicit.
#
# Important parameters:
#   delimiter=","       -- the separator character (default is comma)
#   quotechar='"'       -- the character used to wrap fields that contain the delimiter

# EXAMPLE ──────────────────────────────────────────────────────
# Create a sample CSV file to work with
this_dir = os.path.dirname(__file__)
employees_csv = os.path.join(this_dir, "employees.csv")

sample_data = """name,department,salary,start_date
Alice Ng,Engineering,95000,2021-03-15
Bob Chen,Sales,72000,2019-07-01
Carol Diaz,Finance,81000,2020-11-20
Dave Park,Engineering,88000,2022-01-10
Eve Torres,Sales,67500,2023-05-30
Frank Wu,Finance,79000,2021-08-14
"""

with open(employees_csv, "w", newline="") as f:
    f.write(sample_data)

# --- Reading with csv.reader (rows as lists) ---
print("=== csv.reader ===")
with open(employees_csv, "r", newline="") as f:
    reader = csv.reader(f)
    header = next(reader)     # consume and store the header row
    print("Columns:", header)
    for row in reader:
        name, dept, salary, start = row
        print(f"  {name:<15} | {dept:<15} | ${int(salary):>7,}")

# --- Reading with csv.DictReader (rows as dicts) ---
print("\n=== csv.DictReader ===")
total_salary = 0
engineering_employees = []

with open(employees_csv, "r", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        total_salary += int(row["salary"])
        if row["department"] == "Engineering":
            engineering_employees.append(row["name"])

print(f"Total payroll: ${total_salary:,}")      # $482,500
print(f"Engineering team: {engineering_employees}")
# ['Alice Ng', 'Dave Park']


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
# Using csv.DictReader and the employees.csv file created above,
# calculate the average salary by department.
#
# Steps:
#   1. Read every row and group salaries by department
#   2. Calculate the average salary for each department (round to 2 decimal places)
#   3. Print each department and its average salary, sorted alphabetically by dept
#
# Expected output:
#   Engineering : $91,500.00
#   Finance     : $80,000.00
#   Sales       : $69,750.00




# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — WRITING CSV WITH THE csv MODULE
# ══════════════════════════════════════════════════════════════
# csv.writer(f)        -- write rows as lists
# csv.DictWriter(f)    -- write rows as dicts using a fieldnames list
#
# Always open write files with:
#   newline=""  -- prevents csv module from adding extra blank lines on Windows
#   encoding="utf-8"  -- consistent text encoding
#
# DictWriter requires you to specify fieldnames (the column order).
# Call writeheader() to write the header row first.

# EXAMPLE ──────────────────────────────────────────────────────
# --- Writing with csv.writer ---
summary_csv = os.path.join(this_dir, "department_summary.csv")

dept_data = [
    ["Department", "Headcount", "Total Payroll", "Avg Salary"],
    ["Engineering", 2, 183000, 91500.0],
    ["Finance",     2, 160000, 80000.0],
    ["Sales",       2, 139500, 69750.0],
]

with open(summary_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(dept_data)   # write all rows at once

print(f"Summary written: {summary_csv}")

# --- Writing with csv.DictWriter ---
deals_csv = os.path.join(this_dir, "pipeline_deals.csv")

deals = [
    {"deal_id": "D-001", "account": "Acme Ltd",   "stage": "closed_won",  "value": 45000},
    {"deal_id": "D-002", "account": "Beta Corp",  "stage": "negotiation", "value": 22000},
    {"deal_id": "D-003", "account": "Gamma Inc",  "stage": "closed_won",  "value": 67000},
    {"deal_id": "D-004", "account": "Delta LLC",  "stage": "prospecting", "value": 8000},
]

fieldnames = ["deal_id", "account", "stage", "value"]

with open(deals_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(deals)

print(f"Deals written: {deals_csv}")

# --- Appending to an existing CSV ---
new_deal = {"deal_id": "D-005", "account": "Epsilon SA", "stage": "closed_won", "value": 31000}

with open(deals_csv, "a", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writerow(new_deal)   # append without writing header again

print("New deal appended.")

# Verify by reading back
with open(deals_csv, "r", newline="") as f:
    for row in csv.DictReader(f):
        print(f"  {row['deal_id']} | {row['account']:<12} | {row['stage']:<15} | ${int(row['value']):,}")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
# Using the deals list defined above (or read from deals_csv):
# Write a function called export_closed_deals(deals, output_path) that:
#   1. Filters the deals list to only include stage == "closed_won"
#   2. Adds a "commission" field to each deal: value * 0.05 (rounded to 2)
#   3. Writes the filtered + enhanced data to output_path as a CSV
#      Columns: deal_id, account, value, commission
#
# Call the function and write to "closed_deals.csv" in the same folder.
# Then read it back and print each row.
#
# Expected output:
#   deal_id | account     | value  | commission
#   D-001   | Acme Ltd    | 45000  | 2250.0
#   D-003   | Gamma Inc   | 67000  | 3350.0
#   D-005   | Epsilon SA  | 31000  | 1550.0




# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — READING CSV WITH PANDAS (PREVIEW OF WEEK 4)
# ══════════════════════════════════════════════════════════════
# While the csv module is powerful, pandas makes CSV handling much faster
# for data analysis work.
#
# pd.read_csv() reads a CSV into a DataFrame — a table-like object
# with rows and columns you can filter, group, and analyze easily.
#
# Key parameters:
#   pd.read_csv("file.csv")
#   pd.read_csv("file.csv", sep=";")          -- semicolon-delimited
#   pd.read_csv("file.csv", usecols=["a","b"])-- load specific columns only
#   pd.read_csv("file.csv", dtype={"id": str})-- specify column types
#   pd.read_csv("file.csv", nrows=100)         -- read only first 100 rows
#
# You will go deep on pandas in Week 4. This is just a taste.

# EXAMPLE ──────────────────────────────────────────────────────
try:
    import pandas as pd

    # Read the employees CSV we already created
    df = pd.read_csv(employees_csv)

    print("\n=== pandas read_csv ===")
    print(df)
    print()
    print("Shape:", df.shape)          # (6, 4)  -> 6 rows, 4 columns
    print("Columns:", list(df.columns))
    print()

    # Instant aggregation — no loops needed
    print("Average salary by department:")
    print(df.groupby("department")["salary"].mean().round(2))
    # department
    # Engineering    91500.0
    # Finance        80000.0
    # Sales          69750.0

    # Filter rows where salary > 80000
    high_earners = df[df["salary"] > 80000]
    print("\nEmployees earning over $80,000:")
    print(high_earners[["name", "department", "salary"]])

    # Read from a StringIO object (CSV data in memory — useful for testing)
    csv_string = "product,units,revenue\nWidgets,500,25000\nGadgets,300,45000\n"
    df2 = pd.read_csv(io.StringIO(csv_string))
    print("\nIn-memory CSV:")
    print(df2)

except ImportError:
    print("pandas not installed. Run: pip install pandas")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
# Using pandas, read the deals_csv file created earlier.
# Perform the following three operations and print the results:
#
# 1. Print the total number of deals (len or df.shape[0])
# 2. Print the sum of the "value" column for stage == "closed_won" deals
# 3. Print the number of deals in each stage (use value_counts())
#
# Expected output:
#   Total deals: 5
#   Closed-won revenue: $143,000
#   Stage counts:
#   closed_won     3
#   negotiation    1
#   prospecting    1


