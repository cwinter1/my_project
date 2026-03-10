# ══════════════════════════════════════════════════════════════
#  WEEK 9  |  DAY 2  |  LINEAR REGRESSION
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Understand what linear regression does and when to use it
#  2. Train a model with multiple features (not just one)
#  3. Interpret the model's coefficients (what each feature contributes)
#  4. Evaluate with R² score and Mean Absolute Error (MAE)
#
#  TIME:  ~35 minutes
#
#  YOUTUBE
#  ───────
#  Search: "Linear regression Python scikit-learn tutorial"
#  Search: "how to interpret linear regression coefficients"
#
#  DATASET: Curriculum/datasets/titanic_train.xlsx  (uses Age, Fare columns)
#
# ══════════════════════════════════════════════════════════════

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — WHAT IS LINEAR REGRESSION?
# ══════════════════════════════════════════════════════════════
#
# Linear Regression predicts a NUMERIC value (price, salary, temperature...).
# It finds the best straight line through your data points.
#
# Formula:   y = a + b1*x1 + b2*x2 + ...
#   y   = what we predict (e.g., salary)
#   x1, x2... = features (e.g., experience, education)
#   b1, b2... = coefficients (how much each feature contributes)
#   a         = intercept (base value when all features = 0)
#
# When to use it:
#   - The output is a NUMBER (not a category)
#   - You expect a roughly linear relationship between features and output
#
# EXAMPLE ──────────────────────────────────────────────────────
print("=" * 55)
print("CONCEPT 1: Simple Linear Regression")
print("=" * 55)

# Dataset: experience → salary
experience = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
salary     = [45000, 50000, 58000, 62000, 70000, 76000, 82000, 88000, 94000, 100000]

df = pd.DataFrame({"experience": experience, "salary": salary})

X = df[["experience"]]
y = df["salary"]

model = LinearRegression()
model.fit(X, y)

print(f"Intercept (base salary): ${model.intercept_:,.0f}")
print(f"Coefficient (per year):  ${model.coef_[0]:,.0f}")
print()
print("Interpretation:")
print(f"  Starting salary = ${model.intercept_:,.0f}")
print(f"  Each extra year of experience adds ${model.coef_[0]:,.0f}")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
# Using the model trained above, answer these questions AS COMMENTS:
#
#   1. According to the model, what is the predicted salary for 0 years experience?
#      (hint: that's the intercept)
#
#   2. How much does salary increase per year of experience?
#      (hint: that's the coefficient)
#
#   3. What salary would the model predict for 15 years of experience?
#      Calculate it manually using the formula: intercept + coefficient * years
#      Then verify using model.predict([[15]])




# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — MULTIPLE FEATURES
# ══════════════════════════════════════════════════════════════
#
# In reality, predictions depend on MORE than one column.
# Linear Regression handles multiple features easily — just add more columns to X.
#
# EXAMPLE ──────────────────────────────────────────────────────
print()
print("=" * 55)
print("CONCEPT 2: Multiple Features — Titanic Data")
print("=" * 55)

import os
dataset_path = os.path.join(os.path.dirname(__file__), "..", "datasets", "titanic_train.xlsx")
df_titanic = pd.read_excel(dataset_path)

# Keep only rows where Age and Fare are not null
df_clean = df_titanic[["Age", "Pclass", "Fare"]].dropna()
print(f"Rows after removing nulls: {len(df_clean)}")
print(df_clean.head())
print()

X = df_clean[["Age", "Pclass"]]   # 2 features
y = df_clean["Fare"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model_multi = LinearRegression()
model_multi.fit(X_train, y_train)

y_pred = model_multi.predict(X_test)

print("Model with 2 features (Age + Pclass):")
print(f"  R² score:  {r2_score(y_test, y_pred):.3f}")
print(f"  MAE:       ${mean_absolute_error(y_test, y_pred):,.2f}")
print()
print("Coefficients:")
for feature, coef in zip(["Age", "Pclass"], model_multi.coef_):
    print(f"  {feature:10}: {coef:+.2f}")
print(f"  Intercept : {model_multi.intercept_:.2f}")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
# The model above uses Age and Pclass. Add "SibSp" (siblings/spouses aboard)
# as a third feature and see if the R² score improves.
#
# Steps:
#   1. Create a new X with columns: ["Age", "Pclass", "SibSp"]  (drop nulls)
#   2. Split, train, predict, evaluate
#   3. Print the R² and MAE
#   4. As a comment: did adding SibSp improve the model?




# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — EVALUATING THE MODEL
# ══════════════════════════════════════════════════════════════
#
# Two main metrics for regression:
#
# R² (R-squared) — "how much of the variation does the model explain?"
#   - Range: 0 to 1  (1 = perfect, 0 = no better than guessing the mean)
#   - 0.7 is decent, 0.9+ is strong, but depends on the domain
#
# MAE (Mean Absolute Error) — "on average, how many units off is each prediction?"
#   - In dollars: MAE = 500 means predictions are off by $500 on average
#   - Easier to interpret than R² for business communication
#
# EXAMPLE ──────────────────────────────────────────────────────
print()
print("=" * 55)
print("CONCEPT 3: Evaluation Metrics")
print("=" * 55)

y_actual   = [100, 200, 300, 400, 500]
y_predicted = [110, 190, 320, 380, 510]

mae    = mean_absolute_error(y_actual, y_predicted)
r2     = r2_score(y_actual, y_predicted)

print(f"MAE (average error): {mae:.1f}")
print(f"R² score:            {r2:.3f}")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
# Train two models on the Titanic data and compare their metrics:
#   Model A: only Pclass as feature
#   Model B: Age + Pclass + SibSp as features
#
# For each model print:
#   Model A — R²: x.xxx  MAE: $xx.xx
#   Model B — R²: x.xxx  MAE: $xx.xx
#
# Then as a comment: which is better and why?




