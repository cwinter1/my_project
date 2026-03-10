# ══════════════════════════════════════════════════════════════
#  WEEK 9  |  DAY 1  |  MACHINE LEARNING CONCEPTS & SCIKIT-LEARN
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Explain what Machine Learning is in plain terms
#  2. Understand the difference between supervised and unsupervised learning
#  3. Set up a scikit-learn workflow: load data → split → train → predict
#  4. Understand what "features" and "labels" mean
#
#  TIME:  ~35 minutes
#
#  YOUTUBE
#  ───────
#  Search: "Machine learning explained simply 3Blue1Brown"
#  Search: "scikit-learn tutorial beginners Python"
#  Search: "supervised vs unsupervised learning explained"
#
#  INSTALL (if needed):
#    pip install scikit-learn pandas numpy
#
# ══════════════════════════════════════════════════════════════


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — WHAT IS MACHINE LEARNING?
# ══════════════════════════════════════════════════════════════
#
# Machine Learning (ML) = teaching a computer to find patterns in data
#                         so it can make predictions on NEW data.
#
# Traditional programming:
#   Rules + Data → Answer
#   (you write the rules yourself)
#
# Machine Learning:
#   Data + Answers → Rules  (the model learns the rules from examples)
#   Then: New Data + Rules → Prediction
#
# TWO MAIN TYPES:
#
# Supervised Learning   → you provide data WITH the correct answers (labels)
#                         the model learns to predict the answer for new data
#                         Examples: predicting salary, classifying spam email
#
# Unsupervised Learning → data WITHOUT answers — model finds hidden patterns
#                         Examples: customer segmentation, anomaly detection
#
# KEY TERMS:
#   Features (X)  → the input columns  (age, experience, city...)
#   Label   (y)   → the column to predict  (salary, churn, price...)
#   Training set  → data the model LEARNS from
#   Test set      → data the model is EVALUATED on (it has never seen this)
#
# EXAMPLE ──────────────────────────────────────────────────────
print("=" * 55)
print("Machine Learning Concepts")
print("=" * 55)
print()
print("Goal: predict an employee's salary based on experience")
print()
print("Features (X): years_experience, education_level, city")
print("Label    (y): salary")
print()
print("Step 1: Collect historical data (employees we already know)")
print("Step 2: Train a model on that data")
print("Step 3: Give the model a NEW employee's features")
print("Step 4: Model predicts the salary")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
# For each scenario below, decide:
#   a) What are the FEATURES (inputs)?
#   b) What is the LABEL (what we want to predict)?
#
# Write your answers as comments.
#
# Scenario 1: Predict if a customer will cancel their subscription (churn)
#   Available columns: age, monthly_spend, num_complaints, plan_type, region
#
# Scenario 2: Predict a house price
#   Available columns: num_rooms, area_sqm, city, floor, age_years, price
#
# Scenario 3: Predict if an email is spam
#   Available columns: has_link, word_count, sender_domain, has_attachment, is_spam
#
# Expected answers (as comments):
#   Scenario 1:  Features: age, monthly_spend, num_complaints, plan_type, region
#                Label: churn (whether they cancel)
#   Scenario 2:  Features: num_rooms, area_sqm, city, floor, age_years
#                Label: price
#   Scenario 3:  Features: has_link, word_count, sender_domain, has_attachment
#                Label: is_spam




# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — THE SCIKIT-LEARN WORKFLOW
# ══════════════════════════════════════════════════════════════
#
# Every ML project follows this pattern:
#
#   1. Load & explore data
#   2. Prepare features (X) and label (y)
#   3. Split into train and test sets
#   4. Train (fit) the model on training data
#   5. Predict on test data
#   6. Evaluate — how good are the predictions?
#
# EXAMPLE ──────────────────────────────────────────────────────
print()
print("=" * 55)
print("SHOWCASE: Predict Salary from Experience")
print("=" * 55)

# Step 1: Create sample data
data = {
    "years_experience": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                         1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5],
    "salary":           [45000, 50000, 58000, 62000, 70000, 76000, 82000, 88000, 94000, 100000,
                         47000, 54000, 60000, 65000, 73000, 79000, 85000, 91000]
}
df = pd.DataFrame(data)
print("Sample data:")
print(df.head())
print()

# Step 2: Define X (features) and y (label)
X = df[["years_experience"]]   # 2D — always double brackets for features
y = df["salary"]               # 1D — single bracket for label

# Step 3: Split into train (80%) and test (20%)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"Training rows: {len(X_train)}  |  Test rows: {len(X_test)}")

# Step 4: Train the model
model = LinearRegression()
model.fit(X_train, y_train)    # model learns from training data
print("Model trained.")

# Step 5: Predict on test data
y_pred = model.predict(X_test)

# Step 6: Evaluate
mae = mean_absolute_error(y_test, y_pred)
print(f"Mean Absolute Error: ${mae:,.0f}")
print("(On average, predictions are off by this amount)")

# Show predictions vs actual
print()
print("Predictions vs Actual:")
for actual, predicted in zip(y_test, y_pred):
    print(f"  Actual: {actual:>8,.0f}  |  Predicted: {predicted:>8,.0f}")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
# Using the trained model above, predict the salary for:
#   - A person with 3 years of experience
#   - A person with 7 years of experience
#   - A person with 12 years of experience
#
# Use: model.predict([[value]])  -- note the double brackets
#
# Print each prediction formatted as: "X years → $salary"
#
# Expected output (approximate):
#   3 years → $58,xxx
#   7 years → $82,xxx
#   12 years → $109,xxx




# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — TRAIN / TEST SPLIT — WHY IT MATTERS
# ══════════════════════════════════════════════════════════════
#
# If you train AND test on the same data, the model looks great but is useless.
# (Like giving students the exam answers during study — they'll score 100%
#  but won't actually know the material.)
#
# Test set = data the model has NEVER seen during training.
# This gives you an honest measure of how well the model generalizes.
#
# train_test_split parameters:
#   test_size=0.2   → 20% goes to test, 80% to train
#   random_state=42 → ensures you get the same split every time (reproducible)
#
# EXAMPLE ──────────────────────────────────────────────────────
print()
print("=" * 55)
print("Train vs Test scores")
print("=" * 55)

# Score on training data (optimistic — model has seen this)
train_score = model.score(X_train, y_train)
# Score on test data (realistic — model has NOT seen this)
test_score  = model.score(X_test, y_test)

print(f"Train R² score: {train_score:.3f}")
print(f"Test  R² score: {test_score:.3f}")
print("(R² of 1.0 = perfect, 0 = no better than guessing the average)")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
# Re-run the salary model but change test_size to 0.4 (40% test).
# Compare the test R² score to the original (0.2 split).
#
# Steps:
#   1. Split data again with test_size=0.4
#   2. Train a new model (LinearRegression)
#   3. Print the test R² score
#   4. As a comment, write: is the score better or worse than the 0.2 split? Why?
#
# Note: with small datasets, more test data = fewer training samples = lower score.




