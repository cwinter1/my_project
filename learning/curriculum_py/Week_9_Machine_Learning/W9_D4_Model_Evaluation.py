# ══════════════════════════════════════════════════════════════
#  WEEK 9  |  DAY 4  |  MODEL EVALUATION
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Understand accuracy, precision, recall, and F1 -- and when each matters
#  2. Read and interpret a confusion matrix
#  3. Detect overfitting by comparing train vs test scores
#  4. Use cross-validation for a more reliable evaluation
#
#  TIME:  ~35 minutes
#
#  YOUTUBE
#  ───────
#  Search: "precision recall F1 score explained simply"
#  Search: "confusion matrix Python scikit-learn"
#  Search: "cross validation explained Python"
#
#  DATASET: Curriculum/datasets/titanic_train.xlsx
#
# ══════════════════════════════════════════════════════════════

import os
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (accuracy_score, confusion_matrix,
                             classification_report, ConfusionMatrixDisplay)
import matplotlib.pyplot as plt

dataset_path = os.path.join(os.path.dirname(__file__), "..", "datasets", "titanic_train.xlsx")
df = pd.read_excel(dataset_path)
df_model = df[["Survived", "Pclass", "Age", "SibSp", "Fare"]].dropna()

X = df_model[["Pclass", "Age", "SibSp", "Fare"]]
y = df_model["Survived"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — CONFUSION MATRIX
# ══════════════════════════════════════════════════════════════
#
# A confusion matrix shows WHERE the model is making mistakes.
#
#                    Predicted: Died   Predicted: Survived
# Actual: Died           TN                  FP
# Actual: Survived       FN                  TP
#
#   TN = True Negative   -> predicted Died, actually Died       (correct)
#   TP = True Positive   -> predicted Survived, actually Survived (correct)
#   FP = False Positive  -> predicted Survived, actually Died    (false alarm)
#   FN = False Negative  -> predicted Died, actually Survived    (missed it)

# EXAMPLE ──────────────────────────────────────────────────────

print("=" * 55)
print("CONCEPT 1: Confusion Matrix")
print("=" * 55)

model = DecisionTreeClassifier(max_depth=4, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

cm = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(cm)
print()
tn, fp, fn, tp = cm.ravel()
print(f"  True Negatives  (correctly predicted Died):     {tn}")
print(f"  True Positives  (correctly predicted Survived): {tp}")
print(f"  False Positives (predicted Survived, was Died): {fp}")
print(f"  False Negatives (predicted Died, was Survived): {fn}")

# Visualise -- comment out if matplotlib not available
# ConfusionMatrixDisplay(cm, display_labels=["Died","Survived"]).plot()
# plt.title("Decision Tree -- Confusion Matrix")
# plt.show()


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
# Using the variables tn, fp, fn, tp calculated above, compute:
#   1. Total test rows                        (tn + fp + fn + tp)
#   2. Total correctly predicted              (tn + tp)
#   3. Overall accuracy as a percentage       (correct / total * 100)
#   4. Of all passengers that actually survived, what % did the model catch?
#      This is called RECALL = tp / (tp + fn)
#
# Print each result.
#
# Expected output:
#   Total test rows: xxx
#   Correctly predicted: xxx
#   Accuracy: xx.x%
#   Recall (survived): xx.x%





# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — PRECISION, RECALL, F1
# ══════════════════════════════════════════════════════════════
#
# Accuracy alone can be misleading.
# Example: if 95% of emails are NOT spam, a model that always says "not spam"
#          gets 95% accuracy -- but catches zero spam. Useless!
#
# Precision -- "of everything I predicted as positive, how many were right?"
#              Precision = TP / (TP + FP)
#              Use when false positives are costly  (e.g., spam filter)
#
# Recall    -- "of all actual positives, how many did I catch?"
#              Recall = TP / (TP + FN)
#              Use when false negatives are costly  (e.g., disease detection)
#
# F1 Score  -- harmonic mean of precision and recall
#              F1 = 2 * (Precision * Recall) / (Precision + Recall)
#              Use when you need a balance between both

# EXAMPLE ──────────────────────────────────────────────────────

print()
print("=" * 55)
print("CONCEPT 2: Precision, Recall, F1")
print("=" * 55)

print(classification_report(y_test, y_pred, target_names=["Died", "Survived"]))

# Manual calculation for the "Survived" class:
precision = tp / (tp + fp)
recall    = tp / (tp + fn)
f1        = 2 * (precision * recall) / (precision + recall)
print(f"Manual calculation for Survived class:")
print(f"  Precision: {precision:.3f}")
print(f"  Recall:    {recall:.3f}")
print(f"  F1:        {f1:.3f}")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
# Answer as comments for these scenarios:
#
# Scenario A: You build a model to detect FRAUD in transactions.
#   - What is more costly: FP (flagging a legit transaction) or FN (missing fraud)?
#   - Should you optimize for Precision or Recall? Why?
#
# Scenario B: You build a cancer screening model.
#   - What is more costly: FP (unnecessary follow-up tests) or FN (missing cancer)?
#   - Should you optimize for Precision or Recall? Why?
#
# Scenario C: You build a churn prediction model.
#   - You want to offer retention discounts to likely churners.
#   - Is it worse to offer a discount to a loyal customer (FP) or miss a churner (FN)?
#   - Which metric would you focus on?
#
# Expected output:
#   (Your answers written as comments below)





# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — OVERFITTING AND CROSS-VALIDATION
# ══════════════════════════════════════════════════════════════
#
# Overfitting = model memorizes training data but fails on new data.
# Sign: very high train score, much lower test score.
#
# Cross-Validation (CV) = split data into K folds, train K times,
#                         each time a different fold is the test set.
#                         Average the K scores -> more reliable estimate.

# EXAMPLE ──────────────────────────────────────────────────────

print()
print("=" * 55)
print("CONCEPT 3: Overfitting & Cross-Validation")
print("=" * 55)

for depth in [2, 4, 8, None]:
    m = DecisionTreeClassifier(max_depth=depth, random_state=42)
    m.fit(X_train, y_train)
    train_acc = accuracy_score(y_train, m.predict(X_train))
    test_acc  = accuracy_score(y_test,  m.predict(X_test))
    label = str(depth) if depth else "unlimited"
    print(f"  depth={label:10}: train={train_acc:.3f}  test={test_acc:.3f}  "
          f"{'OVERFIT' if train_acc - test_acc > 0.05 else 'OK'}")

print()
# Cross-validation on the best model (depth=4)
best_model = DecisionTreeClassifier(max_depth=4, random_state=42)
cv_scores = cross_val_score(best_model, X, y, cv=5, scoring="accuracy")
print(f"5-Fold CV scores: {cv_scores.round(3)}")
print(f"Mean CV accuracy: {cv_scores.mean():.3f} (+/- {cv_scores.std():.3f})")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
# Run 5-fold cross-validation on a LogisticRegression(max_iter=1000).
# Print all 5 fold scores and the mean.
#
# Then compare:
#   Decision Tree  CV mean: (from above)
#   Logistic Reg   CV mean: (yours)
#
# As a comment: which model would you choose and why?
#
# Expected output:
#   Logistic Reg CV scores: [x.xxx, x.xxx, x.xxx, x.xxx, x.xxx]
#   Logistic Reg CV mean:   x.xxx
#   Decision Tree CV mean:  x.xxx
#   Logistic Reg  CV mean:  x.xxx




