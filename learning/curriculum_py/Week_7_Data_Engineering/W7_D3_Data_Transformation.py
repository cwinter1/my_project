# ══════════════════════════════════════════════════════════════
#  WEEK 7  |  DAY 3  |  DATA TRANSFORMATION
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Standardize column names for clean, consistent DataFrames
#  2. Validate data by checking for nulls, value ranges, and data types
#  3. Apply business rules: calculate derived columns and map categories
#
#  TIME:  ~30 minutes
#
#  YOUTUBE
#  ───────
#  Search: "pandas data transformation cleaning tutorial"
#  Search: "Python data validation pipeline business rules"
#
# ══════════════════════════════════════════════════════════════

import pandas as pd
import numpy as np

# Sample dirty DataFrame that represents raw data from an ERP system import
raw_data = pd.DataFrame({
    "Employee ID":     ["E001", "E002", "E003", "E004", "E005", "E006", "E007"],
    "Full Name":       ["Alice Ng", "Bob Chen", "carol diaz", "Dave  Park", "", "FRANK WU", "Grace Lee"],
    "Department Code": ["ENG", "SLS", "FIN", "ENG", "SLS", "XYZ", None],
    "  Salary  ":      [95000, 72000, 81000, 88000, -500, 1200000, 105000],
    "Start Date":      ["2021-03-15", "2019-07-01", "2020-11-20", "2022/01/10",
                        "2023-05-30", "NotADate", "2018-04-22"],
    "Status ":         ["Active", "ACTIVE", "inactive", "Active", "active", "Active", "Terminated"],
    "Performance Score": [4.5, 3.2, 4.8, None, 2.1, 3.9, 4.2],
    " Manager?":       ["Yes", "No", "No", "Yes", "No", "no", "Yes"],
})

print("=== RAW DATA ===")
print(raw_data)
print("\nColumn names (note spaces and mixed casing):")
print(list(raw_data.columns))


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — STANDARDIZING COLUMN NAMES
# ══════════════════════════════════════════════════════════════
# Inconsistent column names cause errors and make code hard to write.
# The standard in data engineering is:
#   - All lowercase
#   - Words separated by underscores
#   - No leading or trailing spaces
#   - No special characters
#
# This is called "snake_case" naming.
#
# TECHNIQUES:
#   df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
#   df.rename(columns={"Old Name": "new_name"}) -- rename specific columns
#   df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# EXAMPLE ──────────────────────────────────────────────────────

def standardize_column_names(df):
    """
    Strip whitespace, lowercase, and replace spaces with underscores.
    Returns a new DataFrame with clean column names.
    """
    new_cols = []
    for col in df.columns:
        clean = col.strip()                          # remove leading/trailing spaces
        clean = clean.lower()                        # lowercase
        clean = clean.replace(" ", "_")              # spaces to underscores
        clean = clean.replace("?", "")               # remove punctuation
        clean = clean.replace("(", "").replace(")", "")
        new_cols.append(clean)
    df_clean = df.copy()
    df_clean.columns = new_cols
    return df_clean

df = standardize_column_names(raw_data)
print("\n=== AFTER COLUMN NAME STANDARDIZATION ===")
print(list(df.columns))
# ['employee_id', 'full_name', 'department_code', 'salary', 'start_date',
#  'status', 'performance_score', 'manager']


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
# The messy_cols DataFrame below has poorly named columns.
# Apply standardize_column_names() to it and also:
#   1. Rename "emp_id" to "employee_id" using df.rename(columns={...})
#   2. Rename "dept" to "department"
#   3. Print the final column names
#
# Expected output:
#   ['employee_id', 'department', 'annual_salary', 'hire_year', 'is_full_time']
# --- starting data ---
messy_cols = pd.DataFrame({
    "  EMP ID":          [1, 2, 3],
    "  DEPT":            ["ENG", "SLS", "FIN"],
    "Annual Salary (USD)": [95000, 72000, 81000],
    "HIRE YEAR":         [2021, 2019, 2020],
    "Full Time? ":       [True, True, False],
})





# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — DATA VALIDATION
# ══════════════════════════════════════════════════════════════
# Data validation checks that the data meets expected quality standards BEFORE
# it enters a database or report. Catching bad data early prevents downstream errors.
#
# COMMON VALIDATION CHECKS:
#   1. Null check:       required columns have no NaN values
#   2. Range check:      numeric values are within acceptable bounds
#   3. Type check:       columns have the right data type
#   4. Domain check:     categorical values come from an allowed set
#   5. Uniqueness check: key columns have no duplicates
#   6. Format check:     strings match expected patterns (dates, IDs)
#
# A validation function should:
#   - Return True/False for each rule
#   - Collect ALL failures before stopping (so you fix all at once)
#   - Log which rows violated each rule

# EXAMPLE ──────────────────────────────────────────────────────

def validate_employees(df):
    """
    Run validation checks on the employees DataFrame.
    Returns a validation report dict.
    """
    report = {"checks": [], "total_failures": 0, "is_valid": True}

    def add_check(rule_name, failing_count, detail=""):
        status = "PASS" if failing_count == 0 else "FAIL"
        report["checks"].append({
            "rule": rule_name,
            "status": status,
            "failures": failing_count,
            "detail": detail,
        })
        if failing_count > 0:
            report["total_failures"] += failing_count
            report["is_valid"] = False

    # Check 1: Required columns not null
    required_cols = ["employee_id", "full_name", "department_code", "salary"]
    for col in required_cols:
        if col in df.columns:
            nulls = df[col].isnull().sum() + (df[col] == "").sum()
            add_check(f"no_null_{col}", nulls, f"{nulls} null/empty values")

    # Check 2: Salary range
    if "salary" in df.columns:
        sal = pd.to_numeric(df["salary"], errors="coerce")
        below_min = (sal < 20000).sum()
        above_max = (sal > 500000).sum()
        add_check("salary_min_20000", below_min,
                  df.loc[sal < 20000, "employee_id"].tolist() if below_min else "")
        add_check("salary_max_500000", above_max,
                  df.loc[sal > 500000, "employee_id"].tolist() if above_max else "")

    # Check 3: Valid department codes
    valid_depts = {"ENG", "SLS", "FIN", "OPS", "HR"}
    if "department_code" in df.columns:
        invalid_depts = df[~df["department_code"].isin(valid_depts) & df["department_code"].notna()]
        add_check("valid_department_code", len(invalid_depts),
                  invalid_depts["employee_id"].tolist() if len(invalid_depts) else "")

    # Check 4: Performance score 0-5
    if "performance_score" in df.columns:
        score = pd.to_numeric(df["performance_score"], errors="coerce")
        out_of_range = ((score < 0) | (score > 5)).sum()
        add_check("performance_score_0_to_5", out_of_range)

    return report

validation_result = validate_employees(df)

print("\n=== VALIDATION REPORT ===")
for check in validation_result["checks"]:
    status_str = "PASS" if check["status"] == "PASS" else "FAIL"
    print(f"  [{status_str}] {check['rule']:<35} | Failures: {check['failures']:>3}  {check['detail']}")

print(f"\nTotal failures: {validation_result['total_failures']}")
print(f"Is valid: {validation_result['is_valid']}")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
# The pipeline_runs DataFrame below simulates ETL job logs.
# Write a function called validate_pipeline_runs(df) that checks:
#
#   Rule 1: "run_id" must be unique (no duplicates)
#   Rule 2: "status" must be in ["success", "failure", "running", "skipped"]
#   Rule 3: "rows_processed" must be >= 0
#   Rule 4: "duration_sec" must be > 0 and < 7200 (2 hours)
#   Rule 5: "pipeline_name" must not be null
#
# Return the same report structure as validate_employees.
# Print the report in the same format.
#
# Expected output:
#   [PASS] unique_run_id          | Failures:   0
#   [FAIL] valid_status           | Failures:   1  ['RUN-004']
#   [FAIL] rows_processed >= 0    | Failures:   1  ['RUN-002']
#   [PASS] duration_0_to_7200     | Failures:   0
#   [PASS] pipeline_name_not_null | Failures:   0
# --- starting data ---
pipeline_runs = pd.DataFrame({
    "run_id":         ["RUN-001", "RUN-002", "RUN-003", "RUN-004", "RUN-005"],
    "pipeline_name":  ["daily_sales", "inventory_sync", "daily_sales", "crm_export", "daily_sales"],
    "status":         ["success", "failure", "success", "crashed", "success"],
    "rows_processed": [15000, -100, 8500, 0, 22000],
    "duration_sec":   [42.7, 5.3, 38.1, 120.5, 55.8],
})





# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — BUSINESS RULES TRANSFORMATION
# ══════════════════════════════════════════════════════════════
# Business rules transform raw data into business-meaningful values.
# These are domain-specific calculations and mappings your organization defines.
#
# COMMON PATTERNS:
#   1. Derived columns: calculate new columns from existing ones
#      e.g. revenue = quantity * unit_price
#      e.g. tenure_years = (today - hire_date).days / 365
#
#   2. Category mapping: convert codes to human-readable labels
#      e.g. dept_code "ENG" -> "Engineering"
#
#   3. Bucketing/binning: group continuous values into categories
#      e.g. salary < 60k = "Junior", 60k-90k = "Mid", 90k+ = "Senior"
#
#   4. Flag creation: create boolean indicators
#      e.g. is_high_performer = performance_score >= 4.0

# EXAMPLE ──────────────────────────────────────────────────────

def apply_business_rules(df):
    """
    Apply business logic transformations to the employees DataFrame.
    Returns transformed DataFrame.
    """
    df = df.copy()

    # 1. Parse and standardize the start_date
    df["start_date"] = pd.to_datetime(df["start_date"], errors="coerce")

    # 2. Calculate tenure in years (rounded to 1 decimal)
    today = pd.Timestamp("2024-12-31")   # use fixed date for reproducibility
    df["tenure_years"] = ((today - df["start_date"]).dt.days / 365.25).round(1)
    df["tenure_years"] = df["tenure_years"].clip(lower=0)   # no negative tenure

    # 3. Standardize full_name
    df["full_name"] = df["full_name"].str.strip().str.title()

    # 4. Standardize status
    df["status"] = df["status"].str.strip().str.lower().str.capitalize()

    # 5. Map department code to full name
    dept_map = {
        "ENG": "Engineering",
        "SLS": "Sales",
        "FIN": "Finance",
        "OPS": "Operations",
        "HR":  "Human Resources",
    }
    df["department"] = df["department_code"].map(dept_map).fillna("Unknown")

    # 6. Salary band bucketing
    salary_col = pd.to_numeric(df["salary"], errors="coerce")
    df["salary_band"] = pd.cut(
        salary_col,
        bins=[0, 60000, 90000, 120000, float("inf")],
        labels=["Junior", "Mid", "Senior", "Executive"],
        right=True,
    )

    # 7. Boolean flags
    df["is_manager"]      = df["manager"].str.lower().str.strip().isin(["yes"]) if "manager" in df.columns else False
    df["is_high_performer"] = pd.to_numeric(df["performance_score"], errors="coerce") >= 4.0
    df["is_active"]       = df["status"].str.lower() == "active"

    # 8. Performance tier
    score = pd.to_numeric(df["performance_score"], errors="coerce")
    df["performance_tier"] = pd.cut(
        score,
        bins=[0, 2.5, 3.5, 4.5, 5.0],
        labels=["Needs Improvement", "Meets Expectations", "Exceeds", "Outstanding"],
        right=True,
    )

    return df

df_transformed = apply_business_rules(df)
print("\n=== AFTER BUSINESS RULES ===")
cols_to_show = ["employee_id", "full_name", "department", "salary", "salary_band",
                "tenure_years", "is_manager", "performance_tier"]
print(df_transformed[[c for c in cols_to_show if c in df_transformed.columns]])


# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
# Apply business rules to the raw_sales DataFrame below.
# Write a function called transform_sales_rules(df) that:
#
#   Rule 1: Calculate "net_revenue" = quantity * unit_price * (1 - discount_pct/100)
#   Rule 2: Calculate "commission" = net_revenue * commission_rate
#           where commission_rate is looked up from this dict:
#           {"West": 0.08, "East": 0.09, "Central": 0.07} (default 0.07 if not found)
#   Rule 3: Categorize each deal:
#           net_revenue < 1000: "Small Deal"
#           1000-4999: "Medium Deal"
#           5000+: "Large Deal"
#           Store as "deal_size"
#   Rule 4: Flag high-value reps:
#           is_top_rep = True if net_revenue >= 2000, else False
#
# Print the transformed DataFrame (all columns).
#
# Expected output:
#   [DataFrame with net_revenue, commission, deal_size, is_top_rep columns]
# --- starting data ---
raw_sales = pd.DataFrame({
    "rep":          ["Alice", "Bob", "Carol", "Dave", "Eve"],
    "region":       ["West", "East", "Central", "West", "East"],
    "product":      ["Laptop", "Monitor", "Keyboard", "Headset", "Laptop"],
    "quantity":     [2, 3, 5, 1, 4],
    "unit_price":   [1299.99, 399.99, 149.99, 199.99, 1299.99],
    "discount_pct": [10, 5, 0, 15, 20],
})




