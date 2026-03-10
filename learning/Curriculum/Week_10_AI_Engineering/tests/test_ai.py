"""
W10 AI Engineering — Contract tests.

Run with:
    MOCK_LLM=true pytest Week_10_AI_Engineering/tests/test_ai.py -v

What is tested:
  1. Pydantic output model validates known-good JSON
  2. Pydantic output model rejects known-bad JSON (raises ValidationError)
  3. Golden output regression: snapshot has required fields and correct types
"""

import json
from pathlib import Path

import pytest
from pydantic import BaseModel, ValidationError


# ── Models used in W10 lessons ─────────────────────────────────────────────────

class ProductReview(BaseModel):
    product:   str
    sentiment: str    # "positive", "negative", "neutral"
    score:     int    # 1-5
    reason:    str


class SalesRecord(BaseModel):
    employee_name: str
    city:          str
    sales_amount:  int
    quarter:       str
    above_target:  bool


# ── 1. Pydantic validates known-good JSON ──────────────────────────────────────

def test_product_review_valid():
    good = {
        "product":   "Laptop Pro",
        "sentiment": "positive",
        "score":     4,
        "reason":    "Fast and reliable",
    }
    review = ProductReview(**good)
    assert review.product == "Laptop Pro"
    assert review.score == 4
    assert isinstance(review.sentiment, str)


def test_sales_record_valid():
    good = {
        "employee_name": "Dana Levi",
        "city":          "Tel Aviv",
        "sales_amount":  67000,
        "quarter":       "Q3",
        "above_target":  True,
    }
    record = SalesRecord(**good)
    assert record.employee_name == "Dana Levi"
    assert record.above_target is True


# ── 2. Pydantic rejects known-bad JSON ─────────────────────────────────────────

def test_product_review_bad_score_type():
    """score must be int — string should raise ValidationError."""
    bad = {
        "product":   "Keyboard",
        "sentiment": "positive",
        "score":     "not-a-number",
        "reason":    "ok",
    }
    with pytest.raises(ValidationError):
        ProductReview(**bad)


def test_sales_record_missing_quarter():
    """quarter is required — omitting it must raise ValidationError."""
    bad = {
        "employee_name": "Ron Ben",
        "city":          "Haifa",
        "sales_amount":  43000,
        "above_target":  False,
    }
    with pytest.raises(ValidationError):
        SalesRecord(**bad)


# ── 3. Golden output regression ────────────────────────────────────────────────

SNAPSHOT = Path(__file__).parent / "snapshots" / "golden_output.json"


def test_golden_snapshot_exists():
    assert SNAPSHOT.exists(), f"Golden snapshot missing: {SNAPSHOT}"


def test_golden_snapshot_parses_as_product_review():
    """Snapshot must be a valid ProductReview — same schema as production output."""
    with open(SNAPSHOT) as f:
        data = json.load(f)
    review = ProductReview(**data)
    assert 1 <= review.score <= 5, "score must be between 1 and 5"
    assert review.sentiment in ("positive", "negative", "neutral"), (
        f"sentiment '{review.sentiment}' is not one of the allowed values"
    )


def test_golden_snapshot_fields_unchanged():
    """All required fields must be present and have the correct types.

    This test fails if a schema change removes or renames a field,
    protecting downstream code that depends on the LLM output contract.
    """
    with open(SNAPSHOT) as f:
        data = json.load(f)

    required = {"product", "sentiment", "score", "reason"}
    missing = required - data.keys()
    assert not missing, f"Snapshot is missing fields: {missing}"

    assert isinstance(data["score"], int),     "score must be int in snapshot"
    assert isinstance(data["sentiment"], str), "sentiment must be str in snapshot"
    assert isinstance(data["product"], str),   "product must be str in snapshot"
    assert isinstance(data["reason"], str),    "reason must be str in snapshot"
