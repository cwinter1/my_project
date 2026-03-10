# ══════════════════════════════════════════════════════════════
#  WEEK 11  |  DAY 5  |  AI-POWERED DATA ASSISTANT
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Build a data analysis module that answers questions about a dataset
#  2. Train a churn prediction model and run fairness checks
#  3. Classify support tickets and answer policy questions
#  4. Combine all modules into a single assistant router
#
#  TIME:  ~60 minutes
#
#  YOUTUBE
#  ───────
#  Search: "Python build AI assistant tutorial"
#  Search: "customer churn prediction scikit-learn"
#
#  NOTE: This lesson combines skills from Weeks 9, 10, and 11:
#        ML model (Week 9), LLM API + RAG (Week 10), NLP + Ethics (Week 11)
#
# ══════════════════════════════════════════════════════════════

import os
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — DATA ANALYSIS MODULE
# ══════════════════════════════════════════════════════════════
#
# The first component of any data assistant is the ability to answer
# questions about a dataset using pandas. This module takes a customer
# DataFrame and prints key metrics: totals, averages, and breakdowns
# by category (city, churn status, etc.).

# EXAMPLE ──────────────────────────────────────────────────────

print("=" * 60)
print("CONCEPT 1: Data Analysis Module")
print("=" * 60)
print()

# Generate synthetic retail dataset
np.random.seed(42)
n = 500

customers = pd.DataFrame({
    "customer_id":      range(1001, 1001 + n),
    "age":              np.random.randint(18, 70, n),
    "gender":           np.random.choice(["Male", "Female"], n),
    "city":             np.random.choice(["Tel Aviv", "Jerusalem", "Haifa", "Beer Sheva"], n),
    "monthly_spend":    np.round(np.random.uniform(100, 5000, n), 2),
    "num_orders":       np.random.randint(1, 50, n),
    "num_complaints":   np.random.randint(0, 10, n),
    "months_active":    np.random.randint(1, 60, n),
    "churned":          np.random.choice([0, 1], n, p=[0.7, 0.3]),
})

print(f"Dataset: {customers.shape[0]} customers, {customers.shape[1]} columns")
print(customers.head())

def analyze_customers(df):
    """Basic customer analysis."""
    print(f"\nTotal customers:       {len(df):,}")
    print(f"Average monthly spend: ${df['monthly_spend'].mean():,.2f}")
    print(f"Churn rate:            {df['churned'].mean():.1%}")
    print()
    print("Average spend by city:")
    print(df.groupby("city")["monthly_spend"].mean().sort_values(ascending=False).round(2))
    print()
    print("Churn rate by city:")
    print(df.groupby("city")["churned"].mean().sort_values(ascending=False).map("{:.1%}".format))

analyze_customers(customers)


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1 — Extended Customer Analysis
# ══════════════════════════════════════════════════════════════
#
# Add to the analysis:
#   1. Average number of complaints for churned vs non-churned customers
#      (churned customers likely complain more — verify this)
#   2. The city with the highest churn rate
#   3. Customers who are "high risk": num_complaints > 5 AND months_active < 12
#      Print how many high-risk customers there are
#
# Expected output:
#     Avg complaints (churned):     X.X
#     Avg complaints (not churned): X.X
#     City with highest churn: <city_name>
#     High-risk customers: XX





# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — CHURN PREDICTION MODEL
# ══════════════════════════════════════════════════════════════
#
# A DecisionTree classifier predicts whether a customer will churn
# based on their behavior features. After training, we wrap it in a
# function that accepts a single customer dict and returns a risk level.

# EXAMPLE ──────────────────────────────────────────────────────

print()
print("=" * 60)
print("CONCEPT 2: Churn Prediction Model")
print("=" * 60)

features = ["age", "monthly_spend", "num_orders", "num_complaints", "months_active"]
X = customers[features]
y = customers["churned"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

churn_model = DecisionTreeClassifier(max_depth=4, random_state=42)
churn_model.fit(X_train, y_train)
acc = accuracy_score(y_test, churn_model.predict(X_test))
print(f"Churn model accuracy: {acc:.1%}")

def predict_churn(customer_data):
    """Predict churn risk for a single customer."""
    df = pd.DataFrame([customer_data])[features]
    proba = churn_model.predict_proba(df)[0]
    return {
        "churn_risk":    "HIGH" if proba[1] > 0.6 else "MEDIUM" if proba[1] > 0.3 else "LOW",
        "churn_proba":   f"{proba[1]:.1%}",
        "stay_proba":    f"{proba[0]:.1%}",
    }

# Test the prediction function
new_customer = {
    "age": 35, "monthly_spend": 800, "num_orders": 5,
    "num_complaints": 8, "months_active": 6
}
print()
print("Prediction for test customer:")
print(f"  Input: {new_customer}")
print(f"  Result: {predict_churn(new_customer)}")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 2 — Churn Predictions and Fairness Check
# ══════════════════════════════════════════════════════════════
#
# 1. Run predict_churn() on 5 different customers with varying profiles:
#    - A loyal customer (high orders, low complaints, long active)
#    - A new unhappy customer (low orders, high complaints, short active)
#    - Print the risk and probability for each
#
# 2. Fairness check: does the model predict churn at different rates
#    for males vs females?
#    Use customers.groupby("gender") to calculate average predicted
#    churn probability. Flag if gap > 5%.
#
# Expected output:
#     Customer 1 (loyal):   LOW  - churn probability: X%
#     Customer 2 (unhappy): HIGH - churn probability: X%
#     ...
#     Gender fairness check:
#       Male avg churn prob:   XX%
#       Female avg churn prob: XX%
#       Gap: X% — OK / WARNING





# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — SUPPORT TICKETS & KNOWLEDGE BASE Q&A
# ══════════════════════════════════════════════════════════════
#
# Two more assistant capabilities:
#   1. Classify support tickets into categories (billing, technical, etc.)
#   2. Answer policy questions from a knowledge base (simple RAG pattern)
#
# In production, both would use an LLM. Here we use rule-based fallbacks
# that work without an API key.

# EXAMPLE ──────────────────────────────────────────────────────

print()
print("=" * 60)
print("CONCEPT 3: Support Tickets & Knowledge Base")
print("=" * 60)

# --- Ticket classifier ---
tickets = [
    "I was charged twice this month for my subscription.",
    "The app crashes every time I try to open my account.",
    "My order from 2 weeks ago still hasn't arrived.",
    "How do I change my password?",
    "I received a damaged product in my delivery.",
]

def classify_ticket(ticket_text):
    """
    Classify a support ticket into a category.
    Categories: billing | technical | shipping | account | other
    """
    t = ticket_text.lower()
    if any(w in t for w in ["charged", "payment", "subscription", "invoice", "refund"]):
        return "billing"
    if any(w in t for w in ["crash", "error", "bug", "app", "login", "slow"]):
        return "technical"
    if any(w in t for w in ["delivery", "shipped", "arrived", "order", "package"]):
        return "shipping"
    if any(w in t for w in ["password", "account", "email", "username"]):
        return "account"
    return "other"

print()
print(f"{'Ticket':55} {'Category'}")
print("-" * 70)
for ticket in tickets:
    category = classify_ticket(ticket)
    print(f"{ticket[:55]:55} {category}")

# --- Knowledge base Q&A ---
policies = {
    "refund_001":  "Customers can request a full refund within 30 days of purchase. "
                   "Refund requests must be submitted through the app or by email.",
    "shipping_001":"Standard delivery takes 3-5 business days. Express delivery (1-2 days) "
                   "is available for an additional fee. Free shipping on orders over 200 NIS.",
    "account_001": "Passwords must be at least 8 characters and include a number. "
                   "Accounts are locked after 5 failed login attempts. "
                   "To unlock, use 'forgot password' or contact support.",
    "warranty_001":"Products carry a 12-month manufacturer warranty. "
                   "Warranty covers manufacturing defects but not physical damage.",
}

def answer_policy_question(question):
    """Simple keyword-based policy retrieval (replace with ChromaDB for production)."""
    question_lower = question.lower()
    best_match = None
    for policy_id, text in policies.items():
        if any(word in text.lower() for word in question_lower.split()):
            best_match = text
            break
    if best_match:
        return best_match
    return "I don't have information about that. Please contact support@company.com"

print()
policy_questions = [
    "How long do I have to return a product?",
    "What is the password policy?",
    "How long does delivery take?",
]

for q in policy_questions:
    answer = answer_policy_question(q)
    print(f"Q: {q}")
    print(f"A: {answer[:120]}...")
    print()


# ══════════════════════════════════════════════════════════════
#  EXERCISE 3 — Build the Complete Assistant Router
# ══════════════════════════════════════════════════════════════
#
# Write a function called data_assistant(user_input) that:
#   1. Detects the type of request from the user_input text:
#        "churn" / "predict"              -> call predict_churn() with sample data
#        "ticket" / "support"             -> call classify_ticket()
#        "policy" / "shipping" / "refund" -> call answer_policy_question()
#        "stats" / "analysis"             -> call analyze_customers()
#        else -> "I can help with: churn prediction, ticket classification,
#                 policy questions, data analysis"
#
#   2. Routes the request to the right function
#   3. Returns a helpful response string
#
# Test with:
#   data_assistant("Can you predict if this customer will churn?")
#   data_assistant("Classify this support ticket: I was charged twice")
#   data_assistant("What is the refund policy?")
#   data_assistant("Show me customer statistics")
#   data_assistant("What is the weather today?")
#
# Expected output:
#     Request: "Can you predict if this customer will churn?"
#     Response: churn_risk=HIGH, churn_proba=65% ...
#
#     Request: "What is the weather today?"
#     Response: I can help with: churn prediction, ticket classification, ...




