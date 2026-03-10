# ══════════════════════════════════════════════════════════════
#  WEEK 10  |  DAY 2  |  PROMPT ENGINEERING
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Write clear, effective prompts that get reliable results
#  2. Use few-shot prompting (give examples in the prompt)
#  3. Ask for structured output (JSON, CSV, tables)
#  4. Chain prompts — use one LLM response as input to the next
#
#  TIME:  ~35 minutes
#
#  YOUTUBE
#  ───────
#  Search: "prompt engineering tutorial Python LLM"
#  Search: "few shot prompting explained examples"
#  Search: "ChatGPT prompt engineering best practices"
#
#  NOTE: You need an API key from Day 1 to run the live examples.
#        If you don't have one yet, read the concepts and do Exercise 1
#        (which doesn't require an API call).
#
# ══════════════════════════════════════════════════════════════

import os
import json


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — WHAT MAKES A GOOD PROMPT?
# ══════════════════════════════════════════════════════════════
#
# A good prompt is:
#   1. SPECIFIC about the task
#   2. SPECIFIC about the output format
#   3. SPECIFIC about what to do when unsure
#
# BAD prompt:
#   "Analyze this data."
#
# GOOD prompt:
#   "You are a data analyst. Given the following CSV data, identify the top 3
#    products by revenue. Respond ONLY with a JSON array like:
#    [{'product': '...', 'revenue': ...}]
#    If data is missing or unclear, return an empty array []."
#
# THE THREE ROLES:
#   system   — persona and rules for the model ("You are a...")
#   user     — the actual request
#   assistant— what the model responds (used in multi-turn conversations)

# EXAMPLE ──────────────────────────────────────────────────────
print("=" * 55)
print("CONCEPT 1: Good vs Bad Prompts")
print("=" * 55)
print()
print("BAD:")
bad_prompt = "Tell me about the data."
print(f"  User: {bad_prompt}")
print("  Problem: What data? What format? What level of detail?")
print()
print("GOOD:")
good_prompt = """
You are a data analyst. Given this sales summary:
  Product A: revenue=50000, units=200
  Product B: revenue=30000, units=350
  Product C: revenue=80000, units=100

List the products ranked by revenue (highest first).
Respond ONLY with a JSON array:
[{"rank": 1, "product": "...", "revenue": ...}, ...]
"""
print(f"  User: {good_prompt.strip()}")
print("  Better: specific role, specific data, specific format")

# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
# Rewrite each bad prompt as a good one. Write your answers as comments.
#
# Bad prompt 1:
#   "Summarize this text."
#   Rewrite it for a data engineer who needs a 2-sentence summary of a technical doc.
#
# Bad prompt 2:
#   "Is this customer happy?"
#   Rewrite it to classify sentiment as positive/negative/neutral and return JSON.
#
# Bad prompt 3:
#   "Fix my code."
#   Rewrite it so the model explains WHAT was wrong before giving the fix.
#
# Expected output:
#     3 well-written prompts with specific roles, formats, and edge-case handling





# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — FEW-SHOT PROMPTING
# ══════════════════════════════════════════════════════════════
#
# Few-shot = give the model 2-3 examples of the input/output you want.
# The model learns the pattern from your examples and applies it to new input.
# Very useful when you need a specific format or style.

# EXAMPLE ──────────────────────────────────────────────────────
print()
print("=" * 55)
print("CONCEPT 2: Few-Shot Prompt Template")
print("=" * 55)

few_shot_prompt = """
You classify customer support tickets into categories.

Examples:
  Input:  "My payment was declined twice."
  Output: billing

  Input:  "The app crashes when I open the settings menu."
  Output: technical

  Input:  "I never received my order from last week."
  Output: shipping

Now classify this ticket:
  Input:  "I was charged twice for the same subscription."
  Output:
"""

print(few_shot_prompt)
print("Expected answer: billing")
print()
print("The model learns the pattern: input → single lowercase category word")

# To run with an API (uncomment once you have a key):
# from openai import OpenAI
# client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
# response = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[{"role": "user", "content": few_shot_prompt}],
#     max_tokens=10
# )
# print("API answer:", response.choices[0].message.content.strip())

# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
# Build a few-shot prompt that extracts structured data from messy text.
# Provide 2 examples, then test with a new input.
#
# Task: extract "city" and "population" from a sentence.
#
# Example inputs/outputs:
#   Input:  "Tel Aviv has a population of about 460,000 people."
#   Output: {"city": "Tel Aviv", "population": 460000}
#
#   Input:  "Jerusalem, with 970,000 residents, is the largest city."
#   Output: {"city": "Jerusalem", "population": 970000}
#
# New input to classify:
#   "Haifa is home to around 285,000 inhabitants."
#
# Write the full few-shot prompt string (no API call needed — just the prompt).
# As a comment, write what you expect the model to output.
#
# Expected output:
#     A prompt string with 2 examples and 1 new input
#     Comment: {"city": "Haifa", "population": 285000}





# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — PROMPT CHAINING
# ══════════════════════════════════════════════════════════════
#
# Chaining = use the output of one LLM call as the input to the next.
# Good for complex tasks that are too hard to do in one step.
#
# Example pipeline:
#   Step 1: Extract raw facts from a long document  → bullet points
#   Step 2: Turn bullet points into a SQL INSERT statement
#   Step 3: Validate the SQL for correctness

# EXAMPLE ──────────────────────────────────────────────────────
print()
print("=" * 55)
print("CONCEPT 3: Prompt Chaining Template")
print("=" * 55)

def call_llm(prompt, system="You are a helpful assistant.", model="gpt-4o-mini"):
    """Template function — replace with real API call."""
    # from openai import OpenAI
    # client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    # response = client.chat.completions.create(
    #     model=model,
    #     messages=[
    #         {"role": "system", "content": system},
    #         {"role": "user",   "content": prompt}
    #     ],
    #     max_tokens=300
    # )
    # return response.choices[0].message.content.strip()
    return "[API response would appear here]"   # placeholder

# Chain example:
raw_text = """
  Meeting notes - Q3 Review - July 2025
  Sales: 2.4M, up 12% vs Q2. Top product: Laptop Pro (35% of revenue).
  Concerns: logistics delays causing 8% return rate.
  Next steps: hire 2 logistics managers, launch Laptop Pro 2 in September.
"""

# Step 1: Extract key facts
step1_prompt  = f"Extract 4 key facts from these meeting notes as bullet points:\n{raw_text}"
facts         = call_llm(step1_prompt, system="You are a concise note-taker.")
print("Step 1 output (key facts):")
print(facts)

# Step 2: Turn facts into an action plan
step2_prompt  = f"Turn these facts into a prioritized action plan with 3 items:\n{facts}"
action_plan   = call_llm(step2_prompt, system="You are a project manager.")
print("\nStep 2 output (action plan):")
print(action_plan)

# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
# Build a prompt chain that does the following:
#   Step 1: Given a raw CSV row as text, extract the fields as JSON
#   Step 2: Given the JSON, write a Python print statement that displays the data nicely
#
# Raw input:
#   "Alice Cohen,30,Data Engineer,Tel Aviv,75000"
#
# Expected Step 1 output (JSON):
#   {"name": "Alice Cohen", "age": 30, "role": "Data Engineer",
#    "city": "Tel Aviv", "salary": 75000}
#
# Expected Step 2 output (Python code):
#   print(f"Name: Alice Cohen | Role: Data Engineer | City: Tel Aviv | Salary: 75,000")
#
# Write the two prompts as strings (call_llm() will return a placeholder for now).
# When you have an API key, replace the call_llm() function body with a real call.

raw_csv_row = "Alice Cohen,30,Data Engineer,Tel Aviv,75000"




