# ══════════════════════════════════════════════════════════════
#  WEEK 7  |  DAY 6  |  WEEKLY PROJECT — TESTED ETL PIPELINE
# ══════════════════════════════════════════════════════════════
#
#  PROJECT GOAL
#  ────────────
#  Build a production-quality ETL pipeline that extracts employee
#  data from CSV, cleans and transforms it, loads it into SQLite,
#  and verifies correctness with a suite of test functions.
#
#  SKILLS PRACTICED
#  ─────────────────
#  - Writing ETL functions (extract, transform, load)
#  - Logging with the logging module (console + file)
#  - Data cleaning: nulls, duplicates, type conversion
#  - Writing test functions with assertions
#  - Running and reporting a full pipeline
#
#  TIME:  ~45-60 minutes
#
# ══════════════════════════════════════════════════════════════


# ── SETUP — provided by teacher, do not change ────────────────

import logging
import sqlite3
import pandas as pd
import io
import os
from datetime import datetime

# ── Logging configuration ──────────────────────────────────────
# Writes to both the console and a log file in the same folder.

this_dir = os.path.dirname(os.path.abspath(__file__))
log_path  = os.path.join(this_dir, "etl_pipeline.log")

logger = logging.getLogger("etl_pipeline")
logger.setLevel(logging.INFO)

if not logger.handlers:
    _fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    _console = logging.StreamHandler()
    _console.setFormatter(_fmt)
    logger.addHandler(_console)

    _file = logging.FileHandler(log_path, encoding="utf-8")
    _file.setFormatter(_fmt)
    logger.addHandler(_file)

# ── Sample CSV data ───────────────────────────────────────────
# Contains nulls in rows 6 and 9, and a duplicate of row 1.

EMPLOYEE_CSV = """employee_id,name,department,salary,hire_date
1,Alice Cohen,Engineering,85000,2021-03-15
2,Bob Levi,Marketing,72000,2020-07-22
3,Charlie Mizrahi,Engineering,91000,2019-11-01
4,Diana Shapiro,HR,68000,2022-01-10
5,Eve Goldstein,Marketing,75000,2021-09-30
6,Frank Alon,Engineering,,2020-04-18
7,Gal Peretz,HR,64000,2023-02-28
8,Hadas Katz,Marketing,71000,2021-06-14
9,,Engineering,88000,2020-08-05
10,Iris Ben-David,HR,66000,2022-11-20
1,Alice Cohen,Engineering,85000,2021-03-15
"""

# ── Helper: path for the SQLite database ─────────────────────
DB_PATH = os.path.join(this_dir, "employees.db")


# ══════════════════════════════════════════════════════════════
#  TASK 1 — EXTRACT
# ══════════════════════════════════════════════════════════════
#  Write a function called extract(csv_string) that:
#    - Reads the CSV string into a pandas DataFrame using io.StringIO
#    - Logs: "Extracted N rows from source"  (where N is the row count)
#    - Returns the DataFrame
#
#  After defining the function, call it with EMPLOYEE_CSV and
#  store the result in a variable called raw_df.
#  Print the shape of raw_df.
#
#  Expected output:
#      2025-01-01 00:00:00 | INFO     | Extracted 11 rows from source
#      Raw shape: (11, 5)
#




def extract(csv_string):
    pass   # replace with your code




# ══════════════════════════════════════════════════════════════
#  TASK 2 — TRANSFORM
# ══════════════════════════════════════════════════════════════
#  Write a function called transform(df) that:
#    - Works on a copy of df (use df.copy())
#    - Drops rows where name is null — log: "Dropped N rows with null name"
#    - Fills null salary values with the median salary — log: "Filled N null salaries with median"
#    - Removes duplicate rows — log: "Removed N duplicate rows"
#    - Converts hire_date column to datetime (pd.to_datetime)
#    - Adds a column "years_employed": integer years from hire_date to today
#      (use datetime.now().year minus hire_date.dt.year)
#    - Logs: "Transform complete. Output: N rows"
#    - Returns the cleaned DataFrame
#
#  After defining the function, call it with raw_df and store
#  the result in a variable called clean_df.
#  Print clean_df[["name","salary","years_employed"]].
#
#  Expected output (values approximate — years depend on run date):
#      2025-01-01 00:00:00 | INFO     | Dropped 1 rows with null name
#      2025-01-01 00:00:00 | INFO     | Filled 1 null salaries with median
#      2025-01-01 00:00:00 | INFO     | Removed 1 duplicate rows
#      2025-01-01 00:00:00 | INFO     | Transform complete. Output: 9 rows
#                name  salary  years_employed
#      0   Alice Cohen   85000               4
#      ...




def transform(df):
    pass   # replace with your code




# ══════════════════════════════════════════════════════════════
#  TASK 3 — LOAD
# ══════════════════════════════════════════════════════════════
#  Write a function called load(df, db_path) that:
#    - Opens a sqlite3 connection to db_path
#    - Writes df to a SQLite table named "employees"
#      (use df.to_sql with if_exists="replace", index=False)
#    - Logs: "Loaded N rows to employees table"
#    - Closes the connection
#    - Returns the number of rows loaded
#
#  After defining the function, call it with clean_df and DB_PATH.
#  Store the return value in rows_loaded.
#  Print: "Rows in database:", rows_loaded
#
#  Expected output:
#      2025-01-01 00:00:00 | INFO     | Loaded 9 rows to employees table
#      Rows in database: 9
#




def load(df, db_path):
    pass   # replace with your code




# ══════════════════════════════════════════════════════════════
#  TASK 4 — WRITE TESTS
# ══════════════════════════════════════════════════════════════
#  Write three test functions. Each function should run its own
#  logic, assert the condition, and print "PASS: <test name>"
#  or "FAIL: <test name> — <reason>" using try/except AssertionError.
#
#  test_extract():
#    - Calls extract(EMPLOYEE_CSV)
#    - Asserts the returned DataFrame has exactly these columns:
#      ["employee_id","name","department","salary","hire_date"]
#    - Asserts the row count is 11
#
#  test_transform():
#    - Calls extract(EMPLOYEE_CSV) then transform(result)
#    - Asserts no nulls exist in any column (df.isnull().sum().sum() == 0)
#    - Asserts "years_employed" is in the columns
#    - Asserts all values in years_employed are positive integers
#
#  test_load():
#    - Calls load(clean_df, DB_PATH)   (use the clean_df from Task 2)
#    - Opens a sqlite3 connection and queries: SELECT COUNT(*) FROM employees
#    - Asserts the count equals len(clean_df)
#
#  Do NOT call the test functions yet — that is Task 5.
#
#  Expected output when called: (see Task 5)
#




def test_extract():
    pass   # replace with your code


def test_transform():
    pass   # replace with your code


def test_load():
    pass   # replace with your code




# ══════════════════════════════════════════════════════════════
#  TASK 5 — RUN THE PIPELINE AND ALL TESTS
# ══════════════════════════════════════════════════════════════
#  Write a function called run_pipeline() that:
#    - Calls extract(EMPLOYEE_CSV)  → raw_df
#    - Calls transform(raw_df)      → clean_df
#    - Calls load(clean_df, DB_PATH)
#    - Returns a dict:
#        {"rows_extracted": N, "rows_after_clean": N, "rows_loaded": N}
#
#  After defining run_pipeline, call it and store the result.
#  Then call test_extract(), test_transform(), and test_load()
#  in sequence. Store whether all three printed PASS (you can
#  count manually or track with a list).
#
#  Expected output:
#      2025-01-01 00:00:00 | INFO     | Extracted 11 rows from source
#      2025-01-01 00:00:00 | INFO     | Dropped 1 rows with null name
#      2025-01-01 00:00:00 | INFO     | Filled 1 null salaries with median
#      2025-01-01 00:00:00 | INFO     | Removed 1 duplicate rows
#      2025-01-01 00:00:00 | INFO     | Transform complete. Output: 9 rows
#      2025-01-01 00:00:00 | INFO     | Loaded 9 rows to employees table
#      PASS: test_extract
#      PASS: test_transform
#      PASS: test_load
#




def run_pipeline():
    pass   # replace with your code




# ══════════════════════════════════════════════════════════════
#  TASK 6 — PIPELINE RUN REPORT
# ══════════════════════════════════════════════════════════════
#  Using the results from Task 5, print a formatted run report.
#  The report must include:
#    - Rows extracted from source
#    - Rows after cleaning
#    - Rows loaded to database
#    - Number of tests passed (e.g. "3 / 3")
#    - Pipeline status: "SUCCESS" if all 3 tests passed, else "NEEDS REVIEW"
#
#  Expected output:
#      ══════════════════════════════════
#       ETL PIPELINE RUN REPORT
#      ══════════════════════════════════
#       Rows extracted   : 11
#       Rows after clean : 9
#       Rows loaded      : 9
#       Tests passed     : 3 / 3
#       Status           : SUCCESS
#      ══════════════════════════════════
#




