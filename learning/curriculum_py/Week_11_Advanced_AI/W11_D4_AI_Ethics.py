# ══════════════════════════════════════════════════════════════
#  WEEK 11  |  DAY 4  |  AI ETHICS & RESPONSIBLE AI
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Identify the main ethical risks in AI systems
#  2. Detect and mitigate bias in ML models and data
#  3. Apply fairness checks to a trained model
#  4. Write responsible AI documentation (model cards)
#
#  TIME:  ~35 minutes
#
#  YOUTUBE
#  ───────
#  Search: "AI ethics explained simply 2025"
#  Search: "bias in machine learning examples"
#  Search: "AI fairness metrics Python tutorial"
#
#  NOTE: This lesson is heavier on reading and analysis than coding.
#        The exercises focus on critical thinking + applying checks in Python.
#
# ══════════════════════════════════════════════════════════════

import os
import pandas as pd
import numpy as np


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — THE MAIN ETHICAL RISKS IN AI
# ══════════════════════════════════════════════════════════════
#
# 1. BIAS
#    The model learns unfair patterns from biased historical data.
#    Example: a hiring model trained on past data where women were less hired
#             will predict men as better candidates — even for equal qualifications.
#
# 2. LACK OF TRANSPARENCY ("Black Box")
#    Users don't know why the model made a decision.
#    Example: a loan denial with no explanation violates EU law (GDPR Article 22).
#
# 3. PRIVACY
#    Models trained on personal data can "memorize" and leak it.
#    Example: a chatbot trained on private emails might reveal someone's address.
#
# 4. HALLUCINATION
#    LLMs confidently state false information as fact.
#    Example: an AI legal assistant cites a court case that doesn't exist.
#
# 5. MISUSE
#    AI can be weaponized: deepfakes, spam generation, targeted manipulation.
#
# 6. UNINTENDED HARM
#    A model optimized for a metric causes real-world damage.
#    Example: a recommendation algorithm maximizes engagement, spreads misinformation.

# EXAMPLE ──────────────────────────────────────────────────────

print("=" * 55)
print("CONCEPT 1: AI Risk Categories")
print("=" * 55)

risks = {
    "Bias":             "Unfair treatment of groups due to biased training data",
    "Opacity":          "No explanation for model decisions",
    "Privacy":          "Personal data leakage or misuse",
    "Hallucination":    "Confident false outputs (LLMs especially)",
    "Misuse":           "Intentional harmful applications",
    "Unintended harm":  "Optimization for wrong objective causes damage",
}

for risk, description in risks.items():
    print(f"  {risk:20}: {description}")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1 — Spot the Risk
# ══════════════════════════════════════════════════════════════
#
# For each scenario, identify which risk category applies and explain why.
# Write answers as comments.
#
# Scenario A:
#   A bank's AI model approves loans for applicants from certain zip codes
#   at a much higher rate. Those zip codes correlate with ethnicity.
#   Risk category: ?  Explanation: ?
#
# Scenario B:
#   An AI customer service bot tells a customer that "your warranty covers this repair"
#   when actually it doesn't. The company has no log of what the bot said.
#   Risk category: ?  Explanation: ?
#
# Scenario C:
#   An HR system was trained on employee data including salaries, performance reviews,
#   and personal details. A researcher discovers the model can be queried to reveal
#   individual employees' salaries.
#   Risk category: ?  Explanation: ?
#
# Scenario D:
#   A content recommendation algorithm increases user watch time by 40%,
#   but users report feeling anxious and polarized after using the platform.
#   Risk category: ?  Explanation: ?
#
# Expected output:
#     (comment-based answers for all 4 scenarios)





# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — DETECTING BIAS IN ML MODELS
# ══════════════════════════════════════════════════════════════
#
# Key fairness metrics for classification:
#
#   Demographic Parity     — Does the model approve/predict the same % for all groups?
#   Equal Opportunity      — For positive cases only: does the model catch the same % per group?
#   Predictive Parity      — When the model says "yes", is it right at the same rate per group?

# EXAMPLE ──────────────────────────────────────────────────────

print()
print("=" * 55)
print("CONCEPT 2: Fairness Check")
print("=" * 55)

# Simulate a loan approval dataset with model predictions
np.random.seed(42)
n = 200

data = pd.DataFrame({
    "gender":   np.random.choice(["Male", "Female"], n, p=[0.5, 0.5]),
    "income":   np.random.randint(30000, 150000, n),
    "approved": np.random.choice([0, 1], n, p=[0.35, 0.65]),   # actual outcomes
})

# Simulate biased model predictions (approves males more often)
data["predicted"] = data.apply(
    lambda row: 1 if (row["income"] > 70000 or (row["gender"] == "Male" and row["income"] > 50000)) else 0,
    axis=1
)

print("Dataset sample:")
print(data.head(8))
print()

# Fairness check: approval rate by gender
print("Approval rate by gender (model predictions):")
approval_by_gender = data.groupby("gender")["predicted"].mean()
for gender, rate in approval_by_gender.items():
    print(f"  {gender}: {rate:.1%}")

print()
gap = abs(approval_by_gender["Male"] - approval_by_gender["Female"])
print(f"Approval rate gap: {gap:.1%}")
if gap > 0.05:
    print("WARNING: Gap > 5% — potential gender bias detected!")
else:
    print("OK: Gap within acceptable range.")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 2 — Fairness Check for Age Groups
# ══════════════════════════════════════════════════════════════
#
# Add an "age" column to the dataset and check fairness for age groups:
#   young  = age < 35
#   middle = 35 <= age < 55
#   senior = age >= 55
#
# Steps:
#   1. Add age column: np.random.randint(22, 70, n)
#   2. Create an "age_group" column based on the ranges above
#   3. Calculate model approval rate per age group
#   4. Print the rates
#   5. Flag if any group has approval rate 10%+ below the highest group
#
# Expected output:
#     Approval rate by age group:
#       young:  XX%
#       middle: XX%
#       senior: XX%
#     WARNING: ... (if gap > 10%)   OR   OK: All groups within range.





# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — MODEL CARDS (RESPONSIBLE DOCUMENTATION)
# ══════════════════════════════════════════════════════════════
#
# A Model Card documents:
#   - What the model does and who it's for
#   - What data it was trained on
#   - Performance metrics (overall AND per subgroup)
#   - Known limitations and biases
#   - Intended and prohibited uses
#
# Google, Anthropic, and OpenAI publish model cards for their models.
# For internal models, a model card protects the company legally
# and helps other teams use the model correctly.

# EXAMPLE ──────────────────────────────────────────────────────

print()
print("=" * 55)
print("CONCEPT 3: Model Card")
print("=" * 55)

model_card = {
    "model_name": "Loan Approval Classifier v1.2",
    "purpose": "Predict loan approval probability for retail banking customers",
    "training_data": {
        "source": "Internal loan applications 2018-2023",
        "rows": 45000,
        "features": ["income", "credit_score", "employment_years", "loan_amount"],
        "known_issues": "Historical data may reflect past discriminatory lending practices"
    },
    "performance": {
        "overall_accuracy": "82%",
        "male_approval_rate": "71%",
        "female_approval_rate": "68%",
        "age_under35_approval_rate": "65%",
        "age_35_to_55_approval_rate": "73%",
    },
    "intended_uses": "Initial screening only — final decisions require human review",
    "prohibited_uses": "Sole basis for loan denial without human oversight",
    "last_reviewed": "2025-01-15",
    "contact": "data-ethics@company.com"
}

for section, content in model_card.items():
    if isinstance(content, dict):
        print(f"\n{section.upper()}:")
        for k, v in content.items():
            print(f"  {k}: {v}")
    else:
        print(f"\n{section.upper()}: {content}")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 3 — Write a Model Card for the Titanic Model
# ══════════════════════════════════════════════════════════════
#
# Write a model card for the DecisionTree classifier you built in Week 9, Day 3.
# Create a dictionary called "titanic_model_card" with these sections:
#
#   model_name, purpose, training_data (source, rows, features),
#   performance (accuracy, survival recall, death recall),
#   known_limitations, intended_use, prohibited_use
#
# For known_limitations, think about:
#   - Is the Titanic data representative of real survival scenarios today?
#   - Are there demographic biases in the dataset?
#   - What features are missing that would improve the model?
#
# Print each section of your model card.
#
# Expected output:
#     MODEL_NAME: Titanic Survival Classifier v1.0
#     PURPOSE: Predict passenger survival on the Titanic
#     TRAINING_DATA:
#       source: titanic_train.xlsx
#       ...
#     KNOWN_LIMITATIONS: ...




