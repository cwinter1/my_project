"""
W9 Machine Learning — ML pipeline contract tests.

Run with:
    pytest Week_9_Machine_Learning/tests/test_ml.py -v

What is tested:
  - mlflow.active_run() is not None inside a training run
  - R² score meets minimum threshold (>= 0.70)
  - Confusion matrix sums to len(test set)
  - At least one MLflow run is persisted after training
"""

import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
import pytest
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import confusion_matrix, r2_score
from sklearn.model_selection import train_test_split


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def regression_data():
    """Salary prediction: years_of_experience -> salary (strong linear signal)."""
    np.random.seed(42)
    n = 150
    years = np.random.uniform(1, 20, n)
    salary = 40000 + 3000 * years + np.random.normal(0, 1500, n)
    df = pd.DataFrame({"years_exp": years, "salary": salary})
    return train_test_split(df[["years_exp"]], df["salary"], test_size=0.2, random_state=42)


@pytest.fixture
def classification_data():
    """Pass/fail prediction: score -> passed (1 if score >= 60)."""
    np.random.seed(42)
    n = 300
    scores = np.random.uniform(20, 100, n)
    labels = (scores >= 60).astype(int)
    df = pd.DataFrame({"score": scores, "passed": labels})
    return train_test_split(df[["score"]], df["passed"], test_size=0.2, random_state=42)


# ── 1. MLflow run is active during training ───────────────────────────────────

def test_mlflow_run_active_during_training(regression_data):
    X_train, X_test, y_train, y_test = regression_data
    with mlflow.start_run() as run:
        model = LinearRegression()
        model.fit(X_train, y_train)
        mlflow.log_param("model", "LinearRegression")
        assert mlflow.active_run() is not None, (
            "mlflow.active_run() must not be None inside start_run()"
        )
        run_id = run.info.run_id
    assert run_id is not None


# ── 2. R² meets minimum threshold ────────────────────────────────────────────

def test_r2_meets_threshold(regression_data):
    X_train, X_test, y_train, y_test = regression_data
    model = LinearRegression()
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    r2 = r2_score(y_test, preds)
    assert r2 >= 0.70, (
        f"R² = {r2:.3f} is below the minimum acceptable threshold of 0.70"
    )


# ── 3. Confusion matrix sums to test set size ─────────────────────────────────

def test_confusion_matrix_sums_to_test_size(classification_data):
    X_train, X_test, y_train, y_test = classification_data
    model = LogisticRegression(random_state=42, max_iter=300)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    cm = confusion_matrix(y_test, preds)
    assert cm.sum() == len(y_test), (
        f"Confusion matrix sum {cm.sum()} != test set size {len(y_test)}"
    )


# ── 4. MLflow run is persisted after training ─────────────────────────────────

def test_mlflow_run_persisted(regression_data):
    X_train, X_test, y_train, y_test = regression_data
    with mlflow.start_run():
        model = LinearRegression()
        model.fit(X_train, y_train)
        r2 = r2_score(y_test, model.predict(X_test))
        mlflow.log_metric("r2", r2)
        mlflow.log_param("test_size", 0.2)
    runs = mlflow.search_runs(search_all_experiments=True)
    assert len(runs) > 0, "At least one MLflow run must exist after training"
