# ══════════════════════════════════════════════════════════════
#  WEEK 8  |  DAY 7  |  AUTOMATED QA AND FILE VERIFICATION
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Read files programmatically and extract patterns using regex
#  2. Build a check function that returns a structured list of issues
#  3. Walk a directory tree and apply checks to every file
#
#  TIME:  ~35 minutes  (3 concepts × 10-12 min each)
#
#  YOUTUBE
#  ───────
#  Search: "Python os.walk directory files tutorial"
#  Search: "Python regex re.search re.findall explained"
#  Search: "Python ast.parse syntax checking"
#
#  REAL-WORLD CONTEXT
#  ──────────────────
#  Data pipelines produce files constantly: CSVs, JSON exports, reports.
#  Instead of opening each one manually, a QA script checks all of them
#  automatically and tells you exactly what is wrong and where.
#  This is how data teams maintain quality at scale.
#
# ══════════════════════════════════════════════════════════════


import os
import re
import ast


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — READING A FILE AND SEARCHING FOR PATTERNS
# ══════════════════════════════════════════════════════════════
#
#  open() reads a file into a string.
#  re.search() looks for ONE match anywhere in the string.
#  re.findall() returns a list of ALL matches.
#  in operator does a simple substring check (no regex needed).
#
#  Pattern: read → search → report
#
# EXAMPLE ──────────────────────────────────────────────────────

report_text = """
Date: 2024-01-15
Region: North
Total Sales: 48200
Status: COMPLETE
"""

# Simple substring check
if "COMPLETE" in report_text:
    print("Status check: PASS")
else:
    print("Status check: FAIL — missing COMPLETE marker")

# Regex: find a date pattern YYYY-MM-DD
date_match = re.search(r"\d{4}-\d{2}-\d{2}", report_text)
if date_match:
    print(f"Date found: {date_match.group()}")

# Regex: find all numbers in the text
numbers = re.findall(r"\d+", report_text)
print(f"Numbers found: {numbers}")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
#  You receive a pipeline log as a string.
#  Write checks that print PASS or FAIL for each rule.
#
#  Rules to check:
#    - Must contain the word "SUCCESS"
#    - Must contain an email address (pattern: word@word.word)
#    - Must NOT contain the word "ERROR"
#
#  Expected output:
#    Status check: PASS
#    Email check: PASS — found david@pipeline.com
#    Error check: PASS — no errors found
#
# --- starting data ---
pipeline_log = """
Job: daily_sales_extract
Run: 2024-03-10 06:00:01
Operator: david@pipeline.com
Records loaded: 12450
Result: SUCCESS
"""




# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — A CHECK FUNCTION THAT RETURNS A LIST OF ISSUES
# ══════════════════════════════════════════════════════════════
#
#  A well-designed checker returns a LIST of issues, not just True/False.
#  Empty list = file is clean.
#  Non-empty list = file has problems — each item describes one problem.
#
#  This pattern is used in pytest, data validators, linters, and
#  schema checks (Great Expectations, Pydantic, etc.).
#
# EXAMPLE ──────────────────────────────────────────────────────

def check_sales_csv_row(row: dict) -> list:
    """
    Check one row from a sales CSV.
    Returns a list of issue strings. Empty list = row is valid.
    """
    issues = []

    if "amount" not in row:
        issues.append("missing 'amount' column")
    elif not isinstance(row["amount"], (int, float)):
        issues.append(f"'amount' must be a number, got: {row['amount']}")
    elif row["amount"] < 0:
        issues.append(f"'amount' is negative: {row['amount']}")

    if "region" not in row:
        issues.append("missing 'region' column")
    elif row["region"] not in ("North", "South", "East", "West"):
        issues.append(f"unknown region: {row['region']}")

    return issues


# Test it
rows = [
    {"amount": 1500, "region": "North"},
    {"amount": -200, "region": "East"},
    {"amount": 800,  "region": "Unknown"},
    {"region": "South"},
]

for i, row in enumerate(rows):
    issues = check_sales_csv_row(row)
    if issues:
        print(f"Row {i}: FAIL — {', '.join(issues)}")
    else:
        print(f"Row {i}: PASS")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
#  Write a function check_employee_record(record) that takes a dict
#  and returns a list of issues based on these rules:
#    - Must have keys: "name", "age", "department"
#    - "age" must be a number between 18 and 70
#    - "department" must be one of: "Sales", "Tech", "HR", "Finance"
#
#  Expected output:
#    Record 0: PASS
#    Record 1: FAIL — age out of range: 15
#    Record 2: FAIL — unknown department: Marketing
#    Record 3: FAIL — missing 'age' column, unknown department: ?
#
# --- starting data ---
employee_records = [
    {"name": "Sarah Levi",   "age": 34, "department": "Tech"},
    {"name": "Omer Ben-David","age": 15, "department": "Sales"},
    {"name": "Dana Cohen",   "age": 29, "department": "Marketing"},
    {"name": "Yoav Mizrahi", "department": "?"},
]




# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — WALKING A DIRECTORY AND CHECKING EVERY FILE
# ══════════════════════════════════════════════════════════════
#
#  os.walk(folder) yields (root, subdirs, files) for every subfolder.
#  Combined with a check function, you can verify an entire directory
#  of files in one pass and print a structured report.
#
#  This is the same pattern used by linters (flake8, pylint),
#  test runners (pytest), and data quality platforms.
#
# EXAMPLE ──────────────────────────────────────────────────────

def check_csv_file(filepath: str) -> list:
    """Check that a CSV file is non-empty and has a header row."""
    issues = []
    try:
        with open(filepath, encoding="utf-8") as f:
            lines = f.readlines()
        if len(lines) == 0:
            issues.append("file is empty")
        elif len(lines) == 1:
            issues.append("only a header row — no data")
    except Exception as e:
        issues.append(f"could not read file: {e}")
    return issues


def run_folder_qa(folder: str):
    """Walk a folder and run check_csv_file on every .csv file."""
    total = 0
    passing = 0

    for root, dirs, files in os.walk(folder):
        dirs.sort()
        for filename in sorted(files):
            if not filename.endswith(".csv"):
                continue
            filepath = os.path.join(root, filename)
            rel = os.path.relpath(filepath, folder)
            issues = check_csv_file(filepath)
            total += 1
            if issues:
                print(f"  FAIL  {rel}")
                for issue in issues:
                    print(f"        - {issue}")
            else:
                print(f"  PASS  {rel}")
                passing += 1

    print(f"\n  {passing}/{total} files passing")


# To use: run_folder_qa("path/to/your/csv/folder")
# Example (runs only if a 'sample_data' folder exists here):
sample_folder = os.path.join(os.path.dirname(__file__), "sample_data")
if os.path.isdir(sample_folder):
    run_folder_qa(sample_folder)
else:
    print("(run_folder_qa demo — point it at a real folder to see output)")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
#  Write a function run_log_qa(folder) that walks a folder,
#  reads every .log file, and checks each one for these rules:
#    - Must contain "SUCCESS" or "COMPLETE"
#    - Must NOT contain "CRITICAL"
#    - Must contain at least one date pattern YYYY-MM-DD
#
#  Print a PASS / FAIL report like the example above.
#  At the end print: "X/Y log files passing"
#
#  You do not need real .log files to write the function.
#  Write and test the logic — you can call it with any folder path.
#
#  Expected output format:
#    PASS  pipeline/daily_extract.log
#    FAIL  pipeline/nightly_load.log
#          - missing SUCCESS or COMPLETE marker
#    FAIL  pipeline/archive/old_job.log
#          - contains CRITICAL error
#          - no date pattern found
#
#    2/3 log files passing
#




