# ══════════════════════════════════════════════════════════════
#  WEEK 8  |  DAY 3  |  DATA QUALITY
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Define the four core data quality dimensions
#  2. Write reusable quality check functions in Python
#  3. Build a quality report that runs all checks and summarizes results
#
#  TIME:  ~30 minutes
#
#  YOUTUBE
#  ───────
#  Search: "data quality checks Python pandas tutorial"
#  Search: "data quality framework completeness accuracy"
#
# ══════════════════════════════════════════════════════════════

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Sample dataset -- realistic sales pipeline output with intentional quality issues
np.random.seed(42)
n = 200

records = {
    "sale_id":      list(range(1, 201)),
    "sale_date":    pd.date_range("2024-01-01", periods=n, freq="1D").strftime("%Y-%m-%d").tolist(),
    "rep_name":     np.random.choice(["Alice", "Bob", "Carol", "Dave", "Eve", None], n, p=[0.25,0.25,0.20,0.15,0.10,0.05]).tolist(),
    "region":       np.random.choice(["West", "East", "Central", "INVALID_REGION", None], n, p=[0.35,0.30,0.25,0.07,0.03]).tolist(),
    "product":      np.random.choice(["Laptop", "Monitor", "Keyboard", "Headset", "Mouse"], n).tolist(),
    "quantity":     (np.random.randint(1, 20, n) * np.random.choice([1, 1, 1, -1], n, p=[0.9,0.05,0.02,0.03])).tolist(),
    "unit_price":   np.round(np.abs(np.random.normal(300, 200, n)), 2).tolist(),
    "revenue":      None,   # will be computed below (with some intentional errors)
}

df = pd.DataFrame(records)

# Compute revenue with some errors
df["revenue"] = df["quantity"] * df["unit_price"]
# Inject some missing revenues
df.loc[np.random.choice(df.index, 8, replace=False), "revenue"] = np.nan
# Inject some extreme outliers
df.loc[np.random.choice(df.index, 3, replace=False), "revenue"] = 9999999

# Inject duplicate sale_ids
df.loc[195:197, "sale_id"] = [10, 20, 30]

print("=== DATASET WITH QUALITY ISSUES ===")
print(df.head(10))
print(f"\nShape: {df.shape}")


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — DATA QUALITY DIMENSIONS
# ══════════════════════════════════════════════════════════════
# The four core data quality dimensions explain WHAT can go wrong with data:
#
# 1. COMPLETENESS:
#    Are all required values present?
#    Measure: % of non-null values per required column
#    Bad data: NULL, empty string, "N/A", -9999 (missing value placeholders)
#
# 2. ACCURACY:
#    Are values within valid ranges and correct domains?
#    Measure: % of values within expected bounds or matching an allowed set
#    Bad data: negative quantities, future dates, unknown category codes
#
# 3. CONSISTENCY:
#    Does the data agree with itself?
#    Measure: % of records where computed values match stored values
#    Bad data: revenue != quantity * unit_price, duplicate primary keys
#
# 4. TIMELINESS:
#    Is the data fresh enough to be useful?
#    Measure: time since most recent record vs expected freshness threshold
#    Bad data: a "daily" table that has not been updated in 3 days

# EXAMPLE ──────────────────────────────────────────────────────

print("\n=== DATA QUALITY DIMENSIONS ===")
dimensions = [
    ("Completeness", "Are all required fields populated?",
     "NULL/missing values in required columns"),
    ("Accuracy",     "Are values in valid ranges and domains?",
     "Negative prices, unknown region codes, future dates"),
    ("Consistency",  "Does data agree with itself?",
     "revenue != qty * price, duplicate IDs"),
    ("Timeliness",   "Is the data current enough?",
     "Table not updated within expected window"),
]
for dim, question, example_issue in dimensions:
    print(f"\n  {dim}")
    print(f"    Question: {question}")
    print(f"    Example issue: {example_issue}")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
# Write a function called check_completeness(df, required_cols) that:
#   1. For each column in required_cols:
#      - Count null values
#      - Count empty string values (for string columns)
#      - Compute completeness_pct = (non-missing / total) * 100
#   2. Returns a dict: {col_name: {"missing": n, "completeness_pct": x}}
#
# Call it with df and required_cols = ["sale_id", "rep_name", "region", "revenue"]
# Print each column's completeness percentage.
#
# Expected output:
#   sale_id    : 200/200 (100.0% complete)
#   rep_name   : ~190/200 (~95.0% complete, 10 missing)
#   region     : ~194/200 (~97.0% complete, 6 missing)
#   revenue    : ~192/200 (~96.0% complete, 8 missing)





# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — WRITING QUALITY CHECK FUNCTIONS
# ══════════════════════════════════════════════════════════════
# Each quality check should be a standalone function that:
#   - Accepts a DataFrame (and optional config parameters)
#   - Returns a check_result dict with: passed (bool), failing_count, details
#   - Does NOT modify the DataFrame
#
# This design allows you to run any combination of checks and aggregate results.

# EXAMPLE ──────────────────────────────────────────────────────

def check_null_pct(df, column, max_null_pct=5.0):
    """Check that null percentage in a column does not exceed threshold."""
    null_count = df[column].isnull().sum()
    null_pct   = null_count / len(df) * 100
    passed     = null_pct <= max_null_pct
    return {
        "check":          f"null_pct_{column}",
        "passed":         passed,
        "failing_count":  int(null_count),
        "metric":         round(null_pct, 2),
        "threshold":      max_null_pct,
        "detail":         f"{null_pct:.1f}% nulls (limit: {max_null_pct}%)",
    }

def check_value_range(df, column, min_val=None, max_val=None):
    """Check that all numeric values fall within [min_val, max_val]."""
    col = pd.to_numeric(df[column], errors="coerce")
    mask = pd.Series([True] * len(df), index=df.index)
    if min_val is not None:
        mask &= (col >= min_val)
    if max_val is not None:
        mask &= (col <= max_val)
    failing = (~mask & col.notna()).sum()
    return {
        "check":         f"range_{column}",
        "passed":        failing == 0,
        "failing_count": int(failing),
        "detail":        f"{failing} values outside [{min_val}, {max_val}]",
    }

def check_unique(df, column):
    """Check that a column has no duplicate values."""
    dup_count = df[column].duplicated().sum()
    return {
        "check":         f"unique_{column}",
        "passed":        dup_count == 0,
        "failing_count": int(dup_count),
        "detail":        f"{dup_count} duplicate values in '{column}'",
    }

def check_allowed_values(df, column, allowed_set):
    """Check that all non-null values in a column are in the allowed set."""
    non_null   = df[column].dropna()
    invalid    = non_null[~non_null.isin(allowed_set)]
    return {
        "check":         f"allowed_values_{column}",
        "passed":        len(invalid) == 0,
        "failing_count": len(invalid),
        "detail":        f"{len(invalid)} values not in allowed set. Examples: {invalid.unique()[:3].tolist()}",
    }

def check_consistency(df, result_col, factor_a, factor_b, tolerance=0.01):
    """Check that result_col = factor_a * factor_b within tolerance."""
    expected  = df[factor_a] * df[factor_b]
    actual    = pd.to_numeric(df[result_col], errors="coerce")
    diff      = (actual - expected).abs()
    failing   = (diff > tolerance).sum()
    return {
        "check":         f"consistency_{result_col}={factor_a}*{factor_b}",
        "passed":        failing == 0,
        "failing_count": int(failing),
        "detail":        f"{failing} rows where {result_col} != {factor_a} * {factor_b}",
    }

# Run individual checks
print("\n=== INDIVIDUAL QUALITY CHECKS ===")

results = [
    check_null_pct(df, "rep_name",  max_null_pct=2.0),
    check_null_pct(df, "revenue",   max_null_pct=1.0),
    check_value_range(df, "quantity",  min_val=0),
    check_value_range(df, "unit_price", min_val=1.0, max_val=10000.0),
    check_value_range(df, "revenue",   max_val=500000.0),
    check_unique(df, "sale_id"),
    check_allowed_values(df, "region", {"West", "East", "Central"}),
    check_consistency(df, "revenue", "quantity", "unit_price"),
]

for r in results:
    status = "PASS" if r["passed"] else "FAIL"
    print(f"  [{status}] {r['check']:<50} | {r['detail']}")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
# Write two more check functions and add them to the results list.
#
# Function 1: check_timeliness(df, date_column, max_days_old=2)
#   - Parses the date column
#   - Finds the most recent date in the column
#   - Checks that it is no more than max_days_old days before today
#   - Returns the standard check_result dict
#   - For this exercise, use today = datetime(2024, 7, 20)
#     (the data ends around day 200 = July 18, 2024)
#
# Function 2: check_no_future_dates(df, date_column, reference_date)
#   - Parses the date column
#   - Counts how many dates are AFTER reference_date
#   - Returns the standard check_result dict
#   - Use reference_date = datetime(2024, 7, 20)
#
# Run both and print the results.
#
# Expected output:
#   [PASS or FAIL] timeliness_sale_date ...
#   [PASS] no_future_dates_sale_date ...





# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — BUILDING A QUALITY REPORT
# ══════════════════════════════════════════════════════════════
# A quality report aggregates all checks into a single summary dict.
# It is produced at the end of every pipeline run and stored in a log.
#
# The report includes:
#   - Overall pass/fail status
#   - Per-check results
#   - Key metrics (total checks, passed, failed, overall score)

# EXAMPLE ──────────────────────────────────────────────────────

def run_quality_checks(df, checks_config):
    """
    Run a list of check functions and produce a quality report.
    checks_config: list of (function, kwargs) tuples
    Returns a report dict.
    """
    report = {
        "run_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "row_count":     len(df),
        "checks":        [],
        "total_checks":  0,
        "passed":        0,
        "failed":        0,
        "quality_score": 0.0,
        "overall_status": "pending",
    }

    for check_func, kwargs in checks_config:
        result = check_func(df, **kwargs)
        report["checks"].append(result)
        report["total_checks"] += 1
        if result["passed"]:
            report["passed"] += 1
        else:
            report["failed"] += 1

    total = report["total_checks"]
    report["quality_score"] = round(report["passed"] / total * 100, 1) if total > 0 else 0.0
    report["overall_status"] = "PASS" if report["failed"] == 0 else "FAIL"

    return report

# Define all checks to run
checks_config = [
    (check_null_pct,       {"column": "rep_name",    "max_null_pct": 10.0}),
    (check_null_pct,       {"column": "revenue",     "max_null_pct": 5.0}),
    (check_value_range,    {"column": "quantity",    "min_val": 0}),
    (check_value_range,    {"column": "unit_price",  "min_val": 1.0, "max_val": 10000.0}),
    (check_value_range,    {"column": "revenue",     "max_val": 500000.0}),
    (check_unique,         {"column": "sale_id"}),
    (check_allowed_values, {"column": "region", "allowed_set": {"West", "East", "Central"}}),
    (check_consistency,    {"result_col": "revenue", "factor_a": "quantity", "factor_b": "unit_price"}),
]

report = run_quality_checks(df, checks_config)

print("\n=== QUALITY REPORT ===")
print(f"Run timestamp:  {report['run_timestamp']}")
print(f"Row count:      {report['row_count']}")
print(f"Total checks:   {report['total_checks']}")
print(f"Passed:         {report['passed']}")
print(f"Failed:         {report['failed']}")
print(f"Quality score:  {report['quality_score']}%")
print(f"Overall status: {report['overall_status']}")

print("\nCheck details:")
for check in report["checks"]:
    status = "PASS" if check["passed"] else "FAIL"
    print(f"  [{status}] {check['check']:<50} | {check['detail']}")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
# A quality gate is a threshold: if quality score falls below it,
# the pipeline should STOP rather than load bad data.
#
# Write a function called quality_gate(report, min_score=90.0, critical_checks=None)
# where:
#   - min_score: minimum quality score percentage to pass the gate
#   - critical_checks: list of check names that MUST pass regardless of score
#
# The function should:
#   1. Check if report["quality_score"] >= min_score
#   2. Check if all critical_checks are in the PASSED set
#   3. Return {"gate_passed": bool, "reason": str}
#      If gate fails, reason explains WHY it failed.
#
# Test with:
#   quality_gate(report, min_score=70.0,
#                critical_checks=["unique_sale_id", "range_quantity"])
#
# Then test with a stricter gate:
#   quality_gate(report, min_score=99.0)  # should fail
#
# Expected output (first call):
#   Gate result: {'gate_passed': True/False, 'reason': '...'}
#
# Expected output (second call):
#   Gate result: {'gate_passed': False, 'reason': 'Quality score X% below minimum 99.0%'}




