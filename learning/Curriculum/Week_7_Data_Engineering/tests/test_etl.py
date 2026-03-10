"""
W7 Data Engineering — ETL pipeline contract tests.

Run with:
    pytest Week_7_Data_Engineering/tests/test_etl.py -v

What is tested:
  - Stage 1 (Extract): returns non-empty list of records with required keys
  - Stage 2 (Transform): drops nulls, adds derived column
  - Stage 3 (Load): SQLite row count matches DataFrame length
  - Stage 4 (Report): JSON file written and is valid
"""

import json
import os
import sqlite3
import tempfile

import pandas as pd
import pytest


# ── ETL stage functions ────────────────────────────────────────────────────────

def extract_raw_data():
    """Stage 1: return raw employee records (simulates file/API extraction)."""
    return [
        {"id": 1, "name": "Alice", "dept": "Engineering", "salary": 95000.0},
        {"id": 2, "name": "Bob",   "dept": "Sales",       "salary": 72000.0},
        {"id": 3, "name": "Carol", "dept": "Finance",     "salary": None},
        {"id": 4, "name": "Dave",  "dept": "Engineering", "salary": 88000.0},
        {"id": 5, "name": "Eve",   "dept": "Sales",       "salary": 65000.0},
    ]


def transform(records):
    """Stage 2: drop nulls in salary, add salary_band column."""
    df = pd.DataFrame(records)
    df = df.dropna(subset=["salary"])
    df["salary_band"] = df["salary"].apply(
        lambda s: "high" if s >= 90000 else "mid" if s >= 75000 else "standard"
    )
    return df


def load(df, db_path):
    """Stage 3: write clean DataFrame to SQLite, return row count."""
    conn = sqlite3.connect(db_path)
    df.to_sql("employees", conn, if_exists="replace", index=False)
    count = conn.execute("SELECT COUNT(*) FROM employees").fetchone()[0]
    conn.close()
    return count


def write_report(df, report_path):
    """Stage 4: write a summary JSON report."""
    report = {
        "row_count":   len(df),
        "departments": sorted(df["dept"].unique().tolist()),
        "avg_salary":  round(float(df["salary"].mean()), 2),
    }
    with open(report_path, "w") as f:
        json.dump(report, f)
    return report


# ── Tests ──────────────────────────────────────────────────────────────────────

def test_extract_returns_records():
    records = extract_raw_data()
    assert isinstance(records, list)
    assert len(records) > 0
    required = {"id", "name", "dept", "salary"}
    assert required <= records[0].keys(), f"Missing keys: {required - records[0].keys()}"


def test_extract_has_expected_count():
    assert len(extract_raw_data()) == 5


def test_transform_drops_nulls():
    df = transform(extract_raw_data())
    assert df["salary"].isnull().sum() == 0, "transform must remove rows with null salary"


def test_transform_adds_salary_band():
    df = transform(extract_raw_data())
    assert "salary_band" in df.columns
    assert set(df["salary_band"]).issubset({"high", "mid", "standard"})


def test_load_row_count_matches_dataframe():
    df = transform(extract_raw_data())
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name
    try:
        count = load(df, db_path)
        assert count == len(df), f"DB row count {count} != DataFrame length {len(df)}"
    finally:
        os.unlink(db_path)


def test_report_written_and_valid_json():
    df = transform(extract_raw_data())
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as f:
        report_path = f.name
    try:
        write_report(df, report_path)
        with open(report_path) as f:
            report = json.load(f)
        assert "row_count" in report
        assert "avg_salary" in report
        assert isinstance(report["row_count"], int)
        assert report["row_count"] == len(df)
    finally:
        os.unlink(report_path)
