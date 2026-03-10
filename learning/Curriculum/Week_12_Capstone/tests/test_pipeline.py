"""
W12 Capstone Pipeline — Integration tests (simulation mode).

Run with:
    PIPELINE_MODE=simulation MOCK_LLM=true
    pytest Week_12_Capstone/tests/test_pipeline.py -v

What is tested:
  Stage 1 — Extract:    raw records returned as a list of dicts
  Stage 2 — Transform:  clean DataFrame has 0 nulls in key columns
  Stage 3 — Load:       SQLite row count matches DataFrame length
  Stage 4 — Report:     pipeline_report.json is written and is valid JSON
"""

import json
import os
import sqlite3
import tempfile

import pandas as pd
import pytest


# ── Pipeline stage implementations (simulation mode) ──────────────────────────

def stage1_extract():
    """
    Stage 1 — Extract: simulate fetching from data.gov.il public transit API.
    Returns raw records as a list of dicts (Bronze layer input).
    """
    return [
        {"bus_line": "1",  "city": "Tel Aviv",   "passengers": 1200, "date": "2025-07-01"},
        {"bus_line": "2",  "city": "Haifa",       "passengers":  850, "date": "2025-07-01"},
        {"bus_line": "3",  "city": "Jerusalem",   "passengers": 1450, "date": "2025-07-01"},
        {"bus_line": "4",  "city": "Tel Aviv",   "passengers":  980, "date": "2025-07-01"},
        {"bus_line": "5",  "city": "Beer Sheva",  "passengers":  620, "date": "2025-07-01"},
        {"bus_line": "6",  "city": "Haifa",       "passengers": None, "date": "2025-07-01"},
    ]


def stage2_transform(records):
    """
    Stage 2 — Transform: clean and standardize raw records.
    Drops rows with null in key columns, normalizes city names.
    Returns a clean DataFrame (Silver layer).
    """
    df = pd.DataFrame(records)
    df["city"] = df["city"].str.strip().str.title()
    df = df.dropna(subset=["bus_line", "city", "passengers", "date"])
    df["passengers"] = df["passengers"].astype(int)
    return df


def stage3_load(df, db_path):
    """
    Stage 3 — Load: write clean DataFrame to SQLite (simulates PostgreSQL).
    Returns the number of rows written.
    """
    conn = sqlite3.connect(db_path)
    df.to_sql("ridership", conn, if_exists="replace", index=False)
    count = conn.execute("SELECT COUNT(*) FROM ridership").fetchone()[0]
    conn.close()
    return count


def stage4_report(df, report_path):
    """
    Stage 4 — Report: write a JSON summary of the pipeline run.
    Returns the report dict.
    """
    report = {
        "row_count":         len(df),
        "cities":            sorted(df["city"].unique().tolist()),
        "total_passengers":  int(df["passengers"].sum()),
        "status":            "success",
    }
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    return report


# ── Stage 1 — Extract ─────────────────────────────────────────────────────────

def test_stage1_extract_returns_records():
    records = stage1_extract()
    assert isinstance(records, list)
    assert len(records) > 0


def test_stage1_extract_has_required_keys():
    records = stage1_extract()
    required = {"bus_line", "city", "passengers", "date"}
    assert required <= records[0].keys(), (
        f"Missing keys: {required - records[0].keys()}"
    )


# ── Stage 2 — Transform ───────────────────────────────────────────────────────

def test_stage2_transform_no_nulls_in_key_columns():
    """Clean DataFrame must have 0 nulls in key columns."""
    records = stage1_extract()
    df = stage2_transform(records)
    for col in ["bus_line", "city", "passengers", "date"]:
        null_count = df[col].isnull().sum()
        assert null_count == 0, f"Column '{col}' has {null_count} null(s) after transform"


def test_stage2_transform_drops_incomplete_rows():
    """Row with null passengers must be dropped."""
    records = stage1_extract()
    df = stage2_transform(records)
    # Raw data has 6 records, 1 with null passengers -> expect 5 after clean
    assert len(df) < len(records)
    assert len(df) > 0


# ── Stage 3 — Load ────────────────────────────────────────────────────────────

def test_stage3_load_row_count_matches_dataframe():
    """SQLite row count must equal the number of rows in the clean DataFrame."""
    records = stage1_extract()
    df = stage2_transform(records)
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name
    try:
        count = stage3_load(df, db_path)
        assert count == len(df), (
            f"DB row count {count} != DataFrame length {len(df)}"
        )
    finally:
        os.unlink(db_path)


# ── Stage 4 — Report ──────────────────────────────────────────────────────────

def test_stage4_report_written():
    """pipeline_report.json must be written to disk."""
    records = stage1_extract()
    df = stage2_transform(records)
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as f:
        report_path = f.name
    try:
        stage4_report(df, report_path)
        assert os.path.exists(report_path)
    finally:
        os.unlink(report_path)


def test_stage4_report_is_valid_json():
    """Report file must be valid JSON with required fields."""
    records = stage1_extract()
    df = stage2_transform(records)
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as f:
        report_path = f.name
    try:
        stage4_report(df, report_path)
        with open(report_path) as f:
            report = json.load(f)
        assert "row_count" in report
        assert "status" in report
        assert report["status"] == "success"
        assert isinstance(report["row_count"], int)
        assert report["row_count"] == len(df)
    finally:
        os.unlink(report_path)
