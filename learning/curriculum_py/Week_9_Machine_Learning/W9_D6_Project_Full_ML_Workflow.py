# ══════════════════════════════════════════════════════════════
#  WEEK 9  |  DAY 6  |  PROJECT — FULL ML WORKFLOW
# ══════════════════════════════════════════════════════════════
#
#  PROJECT GOAL
#  ────────────
#  Build a complete machine learning pipeline on the Titanic dataset:
#  load and clean the data, engineer features, train a classifier
#  inside a scikit-learn Pipeline, evaluate it, and save/reload the model.
#
#  SKILLS USED
#  ───────────
#  - pandas: read_excel, fillna, drop, get_dummies
#  - scikit-learn Pipeline with SimpleImputer and StandardScaler
#  - train_test_split, RandomForestClassifier
#  - accuracy_score, confusion_matrix, classification_report
#  - joblib: dump and load for model persistence
#
#  TIME:  ~45-60 minutes
#
# ══════════════════════════════════════════════════════════════

import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib


# ══════════════════════════════════════════════════════════════
#  PART 1 — LOAD AND INSPECT THE DATA
# ══════════════════════════════════════════════════════════════
# The Titanic dataset has one row per passenger.
# The target column is "Survived" (0 = did not survive, 1 = survived).
# We load it from Excel using pandas, then inspect shape and nulls.
#
# EXAMPLE ──────────────────────────────────────────────────────

dataset_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "datasets", "titanic_train.xlsx")
df = pd.read_excel(dataset_path)

print("Shape:", df.shape)
print("\nColumn names:")
print(df.columns.tolist())
print("\nMissing values per column:")
print(df.isnull().sum())
print("\nFirst 3 rows:")
print(df.head(3))


# ══════════════════════════════════════════════════════════════
#  PART 2 — CLEAN AND PREPARE FEATURES
# ══════════════════════════════════════════════════════════════
# We select a subset of columns that are useful for prediction.
# Text columns like Name, Ticket, Cabin are dropped.
# "Sex" is encoded as a binary integer (male=1, female=0).
# "Embarked" gets one-hot encoding.
# Missing Age values are left for the Pipeline to impute.
#
# EXAMPLE ──────────────────────────────────────────────────────

# Keep only these columns for the model
features = ["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare", "Embarked"]
target   = "Survived"

df_model = df[features + [target]].copy()

# Encode Sex as integer
df_model["Sex"] = df_model["Sex"].map({"male": 1, "female": 0})

# One-hot encode Embarked (drop_first avoids dummy variable trap)
df_model = pd.get_dummies(df_model, columns=["Embarked"], drop_first=True)

print("\nPrepared feature columns:")
print(df_model.columns.tolist())
print("\nNull counts after encoding:")
print(df_model.isnull().sum())


# ══════════════════════════════════════════════════════════════
#  TASK 1 — SPLIT THE DATA
# ══════════════════════════════════════════════════════════════
# Split df_model into training and test sets.
# Use 80% for training and 20% for testing.
# Set random_state=42 so results are reproducible.
# The target column is "Survived".
#
# Expected output (approximate, depends on dataset size):
#   Training rows: 712
#   Test rows:     179
#
# --- starting data ---
X = df_model.drop(columns=[target])
y = df_model[target]




# X_train, X_test, y_train, y_test = ...




# ══════════════════════════════════════════════════════════════
#  PART 3 — BUILD A PIPELINE AND TRAIN
# ══════════════════════════════════════════════════════════════
# A scikit-learn Pipeline chains preprocessing steps with a model.
# Step 1: SimpleImputer fills missing Age/Fare values with the median.
# Step 2: StandardScaler normalizes numeric features to zero mean.
# Step 3: RandomForestClassifier is the model.
# Calling pipeline.fit() runs all steps in order on the training data.
#
# EXAMPLE ──────────────────────────────────────────────────────

pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler",  StandardScaler()),
    ("model",   RandomForestClassifier(n_estimators=100, random_state=42)),
])

# Assumes Task 1 was completed and X_train / y_train exist
try:
    pipeline.fit(X_train, y_train)
    print("\nModel training complete.")
except NameError:
    print("\nSkipping fit — complete Task 1 first to define X_train and y_train.")


# ══════════════════════════════════════════════════════════════
#  TASK 2 — EVALUATE THE MODEL
# ══════════════════════════════════════════════════════════════
# Use the trained pipeline to predict on X_test.
# Then print:
#   - Accuracy score (rounded to 4 decimal places)
#   - Confusion matrix
#   - Full classification report
#
# Expected output (approximate):
#   Accuracy: 0.8212
#
#   Confusion matrix:
#   [[94 15]
#    [17 53]]
#
#   Classification report:
#                 precision    recall  f1-score   support
#              0       0.85      0.86      0.85       109
#              1       0.78      0.76      0.77        70
#
# --- starting data ---
# Use: pipeline, X_test, y_test




# y_pred = ...




# ══════════════════════════════════════════════════════════════
#  PART 4 — FEATURE IMPORTANCE
# ══════════════════════════════════════════════════════════════
# Random Forest exposes feature importances — how much each
# feature contributed to splitting decisions across all trees.
# Higher = more important.  We access the fitted model via
# pipeline.named_steps["model"].
#
# EXAMPLE ──────────────────────────────────────────────────────

try:
    rf_model      = pipeline.named_steps["model"]
    feature_names = X_train.columns.tolist()
    importances   = rf_model.feature_importances_

    importance_df = pd.DataFrame({
        "feature":    feature_names,
        "importance": importances,
    }).sort_values("importance", ascending=False)

    print("\nFeature importances:")
    print(importance_df.to_string(index=False))
except Exception:
    print("\nSkipping feature importance — complete Tasks 1 and 2 first.")


# ══════════════════════════════════════════════════════════════
#  TASK 3 — SAVE AND RELOAD THE MODEL
# ══════════════════════════════════════════════════════════════
# Save the trained pipeline to a file named "titanic_pipeline.pkl"
# in the same folder as this script using joblib.dump().
# Then reload it with joblib.load() and run one prediction on X_test
# to confirm the reloaded model gives the same result as the original.
#
# Expected output (approximate):
#   Model saved to: ...titanic_pipeline.pkl
#   Reloaded model accuracy: 0.8212
#   Predictions match: True
#
# --- starting data ---
model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "titanic_pipeline.pkl")




# joblib.dump(...)
# reloaded = joblib.load(...)




# ══════════════════════════════════════════════════════════════
#  PART 5 — PREDICT ON A NEW PASSENGER
# ══════════════════════════════════════════════════════════════
# Once a model is saved, we can load it and predict survival for
# a passenger we invent.  We must build a DataFrame with the same
# column names as the training data.
# Missing columns (like Embarked dummies) are filled with 0.
#
# EXAMPLE ──────────────────────────────────────────────────────

# A new passenger: 3rd class, male, age 22, travelling alone, paid 7.25
new_passenger_data = {
    "Pclass": [3],
    "Sex":    [1],
    "Age":    [22.0],
    "SibSp":  [0],
    "Parch":  [0],
    "Fare":   [7.25],
}

try:
    # Add any dummy columns that training data had, defaulting to 0
    new_passenger = pd.DataFrame(new_passenger_data)
    for col in X_train.columns:
        if col not in new_passenger.columns:
            new_passenger[col] = 0
    new_passenger = new_passenger[X_train.columns]

    prediction = pipeline.predict(new_passenger)[0]
    probability = pipeline.predict_proba(new_passenger)[0]

    print("\nNew passenger prediction:")
    print(f"  Survived: {prediction}  (0 = No, 1 = Yes)")
    print(f"  Probability of survival: {probability[1]:.2%}")
except Exception:
    print("\nSkipping prediction — complete previous tasks first.")

print("\nProject complete.")
