# ══════════════════════════════════════════════════════════════
#  WEEK 2  |  DAY 5  |  MODULES
# ══════════════════════════════════════════════════════════════
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Import and use common standard library modules (os, datetime, math)
#  2. Understand how to create a custom module and import from it
#  3. Know how to install third-party packages and import them in your project
#
#  TIME:  ~30-35 minutes
#
#  YOUTUBE
#  ───────
#  Search: "Python import modules standard library tutorial"
#  Search: "Python pip install third party packages"
# ══════════════════════════════════════════════════════════════


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — IMPORTING STANDARD LIBRARY MODULES (os, datetime, math)
# ══════════════════════════════════════════════════════════════
# Python ships with a large standard library — hundreds of modules you can
# use without installing anything.
#
# Import styles:
#   import module_name                  -- import the whole module
#   import module_name as alias         -- import with a shorter alias
#   from module_name import specific    -- import one specific name
#   from module_name import a, b, c     -- import several names at once
#
# Common modules for data work:
#   os        -- interact with the operating system: paths, env variables
#   datetime  -- work with dates and times
#   math      -- mathematical functions and constants
#   random    -- generate random numbers (useful for sampling)
#   csv       -- read and write CSV files (Week 3)
#   json      -- parse and produce JSON (Week 3)

# EXAMPLE ──────────────────────────────────────────────────────
import os
import math
from datetime import datetime, date, timedelta

# --- os module ---
# Build platform-safe file paths (works on Windows and Mac/Linux)
base_dir = os.path.dirname(__file__)   # directory this file lives in
data_dir = os.path.join(base_dir, "data")
print("Base directory:", base_dir)
print("Data directory:", data_dir)

# Check if a path exists
print("Data dir exists:", os.path.exists(data_dir))   # False (not created yet)

# List environment variables
user = os.environ.get("USERNAME") or os.environ.get("USER") or "unknown"
print("Current user:", user)

# --- datetime module ---
today = date.today()
now = datetime.now()
print("Today:", today)                              # 2024-11-15 (example)
print("Now:", now.strftime("%Y-%m-%d %H:%M"))       # 2024-11-15 14:32

# Calculate date arithmetic — useful for report windows
week_ago = today - timedelta(days=7)
quarter_end = date(today.year, ((today.month - 1) // 3) * 3 + 3, 1)
print("7 days ago:", week_ago)

# Parse a date string into a datetime object
report_date = datetime.strptime("2024-09-30", "%Y-%m-%d")
print("Report date:", report_date.date())           # 2024-09-30

# --- math module ---
print("Pi:", round(math.pi, 4))                     # 3.1416
print("Square root of 144:", math.sqrt(144))        # 12.0
print("Log base 10 of 1000:", math.log10(1000))     # 3.0
print("Ceiling of 4.2:", math.ceil(4.2))            # 5
print("Floor of 4.9:", math.floor(4.9))             # 4


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
# A reporting system needs to label reports with useful date information.
# Using datetime and timedelta:
#
# 1. Print today's date formatted as "YYYY-MM-DD"
# 2. Print the date 30 days from now formatted as "Month DD, YYYY"
#    (example: "December 15, 2024")
# 3. Print the number of days between 2024-01-01 and 2024-12-31
#
# Expected output (dates will differ based on today's date):
#   Today: 2024-11-15
#   30 days from now: December 15, 2024
#   Days in 2024: 365




# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — CREATING AND IMPORTING A CUSTOM MODULE
# ══════════════════════════════════════════════════════════════
# Any Python file can be imported as a module.
# When you import a module, Python runs it and makes its names available.
#
# HOW IT WORKS:
#   1. You have file_a.py in the same folder as file_b.py
#   2. In file_b.py you write: import file_a
#   3. Now file_b.py can use file_a.some_function()
#
# BEST PRACTICES:
#   - Keep related utility functions in a separate file (e.g. utils.py)
#   - Use if __name__ == "__main__": to prevent code from running on import
#   - Organise larger projects into packages (folders with __init__.py)
#
# For this lesson, we simulate what a custom module looks like
# by defining functions here — in a real project these would live in
# a separate file called data_utils.py

# EXAMPLE ──────────────────────────────────────────────────────
# --- Simulating the contents of data_utils.py ---
# In production you would have: from data_utils import clean_string, calculate_margin

def clean_string(value):
    """Strip whitespace and convert to lowercase."""
    if value is None:
        return ""
    return str(value).strip().lower()

def calculate_margin(revenue, cost):
    """Return gross margin percentage. Returns None if revenue is zero."""
    if revenue == 0:
        return None
    return round((revenue - cost) / revenue * 100, 2)

def format_currency(amount, symbol="$"):
    """Format a number as a currency string with commas."""
    return f"{symbol}{amount:,.2f}"

# --- Using the 'module' functions ---
print(clean_string("  SALES DEPARTMENT  "))   # sales department
print(clean_string(None))                      # (empty string)

margin = calculate_margin(150000, 90000)
print(f"Margin: {margin}%")                    # Margin: 40.0%

print(format_currency(1250000))                # $1,250,000.00
print(format_currency(85000, symbol="EUR "))   # EUR 85,000.00

# --- What the import statement would look like if this were a real module ---
# from data_utils import clean_string, calculate_margin, format_currency
# -- or --
# import data_utils
# data_utils.clean_string("  hello  ")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
# Imagine these three functions are in your shared utils module.
# Write each function, then call all three and print the results.
#
# Function 1: get_quarter(month_number)
#   Returns the quarter as a string: "Q1", "Q2", "Q3", or "Q4"
#   Months 1-3 -> "Q1", 4-6 -> "Q2", 7-9 -> "Q3", 10-12 -> "Q4"
#
# Function 2: truncate_string(text, max_length)
#   If text is longer than max_length, return the first max_length characters
#   followed by "...". Otherwise return text unchanged.
#
# Function 3: safe_divide(a, b)
#   Returns a / b rounded to 4 decimal places, or 0.0 if b is zero.
#
# Test calls:
#   get_quarter(5)                    -> "Q2"
#   get_quarter(11)                   -> "Q4"
#   truncate_string("Annual Revenue Report 2024", 15)  -> "Annual Revenue ..."
#   truncate_string("Short", 20)      -> "Short"
#   safe_divide(355, 113)             -> 3.1416
#   safe_divide(100, 0)               -> 0.0




# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — INSTALLING AND USING THIRD-PARTY PACKAGES
# ══════════════════════════════════════════════════════════════
# Python's ecosystem includes tens of thousands of packages on PyPI
# (the Python Package Index at pypi.org).
#
# INSTALLING PACKAGES:
#   Open a terminal and run:
#     pip install package_name
#     pip install package_name==1.2.3    (pin a specific version)
#     pip install -r requirements.txt    (install from a list file)
#
# REQUIREMENTS FILE:
#   It is standard practice to list your project's dependencies in a file
#   called requirements.txt. Example contents:
#     pandas==2.1.0
#     numpy==1.26.0
#     requests==2.31.0
#     openpyxl==3.1.2
#
# KEY DATA PACKAGES YOU WILL USE IN THIS COURSE:
#   Package        | Install command           | Purpose
#   ---------------|---------------------------|---------------------------
#   pandas         | pip install pandas        | DataFrames, data analysis
#   numpy          | pip install numpy         | Numeric arrays, math
#   matplotlib     | pip install matplotlib    | Plotting charts
#   seaborn        | pip install seaborn       | Statistical visualization
#   requests       | pip install requests      | HTTP requests (APIs)
#   openpyxl       | pip install openpyxl      | Read/write Excel files
#   beautifulsoup4 | pip install beautifulsoup4| Web scraping (HTML parsing)
#   sqlalchemy     | pip install sqlalchemy    | SQL abstraction layer
#   pyodbc         | pip install pyodbc        | Connect to SQL Server
#   schedule       | pip install schedule      | Run functions on a schedule
#   boto3          | pip install boto3         | AWS SDK (S3, etc.)

# Checking what is installed: pip list  or  pip show package_name

# VIRTUAL ENVIRONMENTS:
#   Always work inside a virtual environment to isolate project dependencies.
#   Create one with:
#     python -m venv venv
#   Activate it:
#     Windows:    venv\Scripts\activate
#     Mac/Linux:  source venv/bin/activate
#   Then pip install packages inside the activated environment.

# EXAMPLE ──────────────────────────────────────────────────────
# DEMONSTRATING AN IMPORT WITH A FALLBACK:
# This pattern gracefully handles the case where a package is not yet installed.

try:
    import requests
    print("requests is installed:", requests.__version__)
except ImportError:
    print("requests is not installed. Run: pip install requests")

try:
    import pandas as pd
    print("pandas is installed:", pd.__version__)
except ImportError:
    print("pandas is not installed. Run: pip install pandas")

try:
    import numpy as np
    print("numpy is installed:", np.__version__)
except ImportError:
    print("numpy is not installed. Run: pip install numpy")

# Once installed, usage is straightforward:
# import pandas as pd
# df = pd.read_csv("sales_data.csv")
# print(df.head())


# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
# Write a function called check_packages that:
#   - Accepts a list of package names (strings)
#   - For each package, tries to import it
#   - Prints "INSTALLED: <name>" if it imports successfully
#   - Prints "MISSING:   <name>  -->  pip install <name>" if ImportError occurs
#   - Returns a dict: {package_name: True/False}
#
# Call it with:
#   packages = ["os", "math", "pandas", "numpy", "requests",
#               "nonexistent_package", "fake_library"]
#
# Expected output (will vary based on what is installed):
#   INSTALLED: os
#   INSTALLED: math
#   INSTALLED: pandas
#   INSTALLED: numpy
#   INSTALLED: requests
#   MISSING:   nonexistent_package  -->  pip install nonexistent_package
#   MISSING:   fake_library  -->  pip install fake_library


