# ══════════════════════════════════════════════════════════════
#  WEEK 9  |  DAY 3  |  CLASSIFICATION
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Understand when to use classification (vs regression)
#  2. Train a Logistic Regression classifier
#  3. Train a Decision Tree classifier
#  4. Compare the two models on the same data
#
#  TIME:  ~40 minutes
#
#  YOUTUBE
#  ───────
#  Search: "logistic regression Python scikit-learn explained"
#  Search: "decision tree classifier Python scikit-learn"
#
#  DATASET: Curriculum/datasets/titanic_train.xlsx
#
# ══════════════════════════════════════════════════════════════

import os
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — CLASSIFICATION VS REGRESSION
# ══════════════════════════════════════════════════════════════
#
# Regression  -> predict a NUMBER      (salary, price, temperature)
# Classification -> predict a CATEGORY (yes/no, spam/not spam, survived/died)
#
# The output in classification is a CLASS LABEL:
#   Binary:      2 classes    -> survived: 0 or 1
#   Multi-class: 3+ classes   -> product category: A, B, or C
#
# ALGORITHMS we use today:
#   Logistic Regression -> good starting point, fast, interpretable
#   Decision Tree       -> easy to understand, works well with mixed data types

# EXAMPLE ──────────────────────────────────────────────────────

print("=" * 55)
print("CONCEPT 1: Prepare Classification Data")
print("=" * 55)

dataset_path = os.path.join(os.path.dirname(__file__), "..", "datasets", "titanic_train.xlsx")
df = pd.read_excel(dataset_path)

# Keep relevant columns, drop rows with nulls
df_model = df[["Survived", "Pclass", "Age", "SibSp", "Fare"]].dropna()

print(f"Rows available: {len(df_model)}")
print(f"Survived breakdown:\n{df_model['Survived'].value_counts()}")
print()

X = df_model[["Pclass", "Age", "SibSp", "Fare"]]
y = df_model["Survived"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"Train: {len(X_train)} rows  |  Test: {len(X_test)} rows")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
# Before modeling, always understand what you are predicting.
# Using df_model:
#   1. Print the percentage of survivors (Survived == 1) -- round to 1 decimal
#   2. Print the average Age of survivors vs non-survivors
#      Hint: df_model.groupby("Survived")["Age"].mean()
#
# Expected output (approximate):
#   Survival rate: 40.6%
#   Average age by survival:
#   Survived
#   0    30.x
#   1    28.x





# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — LOGISTIC REGRESSION
# ══════════════════════════════════════════════════════════════
#
# Despite the name, Logistic Regression is a CLASSIFIER, not a regressor.
# It predicts the PROBABILITY of belonging to a class (0 or 1).
#
# How it works:
#   - Outputs a probability between 0 and 1
#   - If probability >= 0.5 -> class 1 (survived)
#   - If probability < 0.5  -> class 0 (did not survive)
#
# When to use:
#   - Binary classification (yes/no)
#   - You need a probability, not just a label
#   - Fast and interpretable

# EXAMPLE ──────────────────────────────────────────────────────

print()
print("=" * 55)
print("CONCEPT 2: Logistic Regression")
print("=" * 55)

lr_model = LogisticRegression(max_iter=1000)
lr_model.fit(X_train, y_train)
y_pred_lr = lr_model.predict(X_test)

acc_lr = accuracy_score(y_test, y_pred_lr)
print(f"Logistic Regression Accuracy: {acc_lr:.1%}")
print()
print("Detailed report:")
print(classification_report(y_test, y_pred_lr, target_names=["Died", "Survived"]))

# Predict probabilities for first 5 test rows
proba = lr_model.predict_proba(X_test.head())
print("Survival probabilities for first 5 test rows:")
for i, (died, survived) in enumerate(proba):
    print(f"  Row {i+1}: Died={died:.2f}  Survived={survived:.2f}")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
# Predict whether a NEW passenger would survive, using the Logistic Regression model.
# Create a DataFrame for this passenger and predict.
#
# Passenger details:
#   Pclass = 1, Age = 35, SibSp = 0, Fare = 100.0
#
# Steps:
#   1. Create a DataFrame with one row using these values
#   2. Use lr_model.predict() to get the prediction (0 or 1)
#   3. Use lr_model.predict_proba() to get the probability
#   4. Print: "Prediction: Survived/Died  (confidence: xx%)"
#
# Expected output:
#   Prediction: Survived or Died  (confidence: xx%)





# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — DECISION TREE
# ══════════════════════════════════════════════════════════════
#
# A Decision Tree splits the data into branches based on conditions,
# like a flowchart of questions.
#
# Example (simplified):
#   Is Pclass == 1?
#     Yes -> Did you pay Fare > 50?
#             Yes -> Survived
#             No  -> Died
#     No  -> Age < 15?
#             Yes -> Survived
#             No  -> Died
#
# Advantages: very interpretable -- you can literally read the decision rules.
# Risk: can "memorize" training data (overfitting) if tree is too deep.

# EXAMPLE ──────────────────────────────────────────────────────

print()
print("=" * 55)
print("CONCEPT 3: Decision Tree")
print("=" * 55)

dt_model = DecisionTreeClassifier(max_depth=4, random_state=42)
# max_depth limits the tree size -- prevents memorizing training data
dt_model.fit(X_train, y_train)
y_pred_dt = dt_model.predict(X_test)

acc_dt = accuracy_score(y_test, y_pred_dt)
print(f"Decision Tree Accuracy: {acc_dt:.1%}")
print()
print("Feature importances (how much each feature contributed):")
for feature, importance in zip(X.columns, dt_model.feature_importances_):
    bar = "=" * int(importance * 40)
    print(f"  {feature:10}: {importance:.3f}  {bar}")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
# Train a Decision Tree with max_depth=2 and another with max_depth=6.
# Compare both to the Logistic Regression from Concept 2.
#
# For each model print:
#   Model name      Accuracy
#   Logistic Reg    xx.x%
#   Tree depth=2    xx.x%
#   Tree depth=6    xx.x%
#
# Then as a comment:
#   - Which performs best on the test set?
#   - Why might depth=6 score LOWER than depth=4 on the test set?
#     (Hint: think about overfitting)
#
# Expected output:
#   Logistic Reg    xx.x%
#   Tree depth=2    xx.x%
#   Tree depth=6    xx.x%




