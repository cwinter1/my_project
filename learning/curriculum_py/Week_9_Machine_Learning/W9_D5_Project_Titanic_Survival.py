# ══════════════════════════════════════════════════════════════
#  WEEK 9  |  DAY 5  |  PROJECT: TITANIC SURVIVAL PREDICTION
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  This project combines everything from Week 9:
#  1. Load and explore real data
#  2. Clean and prepare features
#  3. Train and compare multiple models
#  4. Evaluate and select the best model
#  5. Document your findings (as comments)
#
#  TIME:  ~45 minutes
#
#  YOUTUBE
#  ───────
#  Search: "Titanic machine learning project Python scikit-learn"
#
#  DATASET: Curriculum/datasets/titanic_train.xlsx
#
#  GOAL:
#  Build the best possible model to predict Titanic survival.
#  You will go through the full ML workflow from raw data to final evaluation.
#
# ══════════════════════════════════════════════════════════════

import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report


dataset_path = os.path.join(os.path.dirname(__file__), "..", "datasets", "titanic_train.xlsx")
df = pd.read_excel(dataset_path)


# ══════════════════════════════════════════════════════════════
#  STEP 1 — EXPLORE THE DATA
# ══════════════════════════════════════════════════════════════

print("=" * 55)
print("STEP 1: Explore the Data")
print("=" * 55)

print(df.shape)                  # rows, columns
print(df.dtypes)                 # column types
print()
print("Missing values:")
print(df.isnull().sum())
print()
print("Survival rate:")
print(df["Survived"].value_counts(normalize=True).round(3))


# ══════════════════════════════════════════════════════════════
#  TASK 1 — EXPLORE AVERAGES BY SURVIVAL
# ══════════════════════════════════════════════════════════════
# Print the average Fare and Age for survivors vs non-survivors.
# Use groupby("Survived")[column].mean()
#
# What do you notice? Write 1-2 observations as comments.
#
# Expected output:
#   Average Fare by survival:
#   Survived
#   0    xx.xx
#   1    xx.xx
#   Average Age by survival:
#   Survived
#   0    xx.xx
#   1    xx.xx





# ══════════════════════════════════════════════════════════════
#  STEP 2 — FEATURE ENGINEERING
# ══════════════════════════════════════════════════════════════
#
# Raw data often needs preparation before modeling:
#   - Drop columns that do not help predictions (names, ticket numbers, etc.)
#   - Handle missing values (fill or drop)
#   - Convert text to numbers (Male/Female -> 0/1)

print()
print("=" * 55)
print("STEP 2: Feature Engineering")
print("=" * 55)

df_ml = df.copy()

# Convert Sex to numeric: male=0, female=1
df_ml["Sex_num"] = (df_ml["Sex"] == "female").astype(int)

# Fill missing Age with median
df_ml["Age"] = df_ml["Age"].fillna(df_ml["Age"].median())

# Select features
features = ["Pclass", "Age", "SibSp", "Parch", "Fare", "Sex_num"]
df_ml = df_ml[features + ["Survived"]].dropna()

print(f"Rows ready for modeling: {len(df_ml)}")
print(df_ml.head())


# ══════════════════════════════════════════════════════════════
#  TASK 2 — ADD A NEW FEATURE
# ══════════════════════════════════════════════════════════════
# Add one more engineered feature:
#   "family_size" = SibSp + Parch + 1  (total people including the passenger)
#
# Add it to df_ml and add "family_size" to the features list.
# Print the first 5 rows showing the new column.
#
# Expected output:
#   (first 5 rows of df_ml with a family_size column)





# ══════════════════════════════════════════════════════════════
#  STEP 3 — TRAIN / TEST SPLIT
# ══════════════════════════════════════════════════════════════

print()
print("=" * 55)
print("STEP 3: Train / Test Split")
print("=" * 55)

X = df_ml[features]
y = df_ml["Survived"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"Training rows: {len(X_train)}  |  Test rows: {len(X_test)}")


# ══════════════════════════════════════════════════════════════
#  STEP 4 — TRAIN AND COMPARE MODELS
# ══════════════════════════════════════════════════════════════

print()
print("=" * 55)
print("STEP 4: Train and Compare Models")
print("=" * 55)

models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Decision Tree d=3":   DecisionTreeClassifier(max_depth=3, random_state=42),
    "Decision Tree d=5":   DecisionTreeClassifier(max_depth=5, random_state=42),
}

results = {}
for name, m in models.items():
    m.fit(X_train, y_train)
    test_acc = accuracy_score(y_test, m.predict(X_test))
    cv_acc   = cross_val_score(m, X, y, cv=5).mean()
    results[name] = {"test_acc": test_acc, "cv_acc": cv_acc, "model": m}
    print(f"  {name:25}: Test={test_acc:.3f}  CV={cv_acc:.3f}")


# ══════════════════════════════════════════════════════════════
#  TASK 3 — ADD A FOURTH MODEL
# ══════════════════════════════════════════════════════════════
# The code above trains 3 models. Add a 4th model to the "models" dict:
#   "Decision Tree d=8": DecisionTreeClassifier(max_depth=8, random_state=42)
#
# Re-run the loop and observe: does deeper = better on the test set?
# Write your observation as a comment.
#
# Expected output:
#   Decision Tree d=8   : Test=x.xxx  CV=x.xxx





# ══════════════════════════════════════════════════════════════
#  STEP 5 — EVALUATE THE BEST MODEL
# ══════════════════════════════════════════════════════════════

print()
print("=" * 55)
print("STEP 5: Final Evaluation")
print("=" * 55)

# Select best model by CV accuracy
best_name = max(results, key=lambda k: results[k]["cv_acc"])
best_model = results[best_name]["model"]
print(f"Best model: {best_name}")
print()
print(classification_report(y_test, best_model.predict(X_test),
                             target_names=["Died", "Survived"]))


# ══════════════════════════════════════════════════════════════
#  TASK 4 — FINAL REFLECTION
# ══════════════════════════════════════════════════════════════
# Answer these as comments:
#
#   1. Which model performed best by CV accuracy?
#   2. What was the accuracy on the test set?
#   3. For the Survived class -- what was the Precision and Recall?
#   4. If this were a real rescue operation, would you prioritize Precision or Recall?
#      Explain why.
#   5. What additional features (not in this dataset) could improve the model?
#
# Expected output:
#   (Your answers written as comments below)




