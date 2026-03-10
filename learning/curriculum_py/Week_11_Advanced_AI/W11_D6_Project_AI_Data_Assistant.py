# ══════════════════════════════════════════════════════════════
#  WEEK 11  |  DAY 6  |  PROJECT — AI DATA ASSISTANT
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Load a real dataset and compute descriptive statistics
#  2. Build a structured prompt that summarizes data for an LLM
#  3. Understand how an AI assistant integrates data context
#  4. Format and print a complete AI-powered analysis report
#
#  TIME:  ~45 minutes
#
# ══════════════════════════════════════════════════════════════


import os
import pandas as pd


# ══════════════════════════════════════════════════════════════
#  TASK 1 — LOAD THE DATASET AND COMPUTE STATISTICS
# ══════════════════════════════════════════════════════════════
#
#  The Titanic dataset contains information about passengers:
#  who survived, their age, ticket class, sex, and fare.
#
#  We load the Excel file using pandas, then compute four
#  key statistics that will be passed to the AI assistant:
#
#    total_passengers  — total number of rows
#    survival_rate     — percentage who survived (Survived == 1)
#    average_age       — mean of the Age column (drop NaN)
#    class_distribution — value_counts() of the Pclass column
#
#  These numbers give the assistant the context it needs to
#  make meaningful observations about the data.
#
# EXAMPLE ──────────────────────────────────────────────────────

dataset_path = os.path.join(os.path.dirname(__file__), "..", "datasets", "titanic_train.xlsx")
df = pd.read_excel(dataset_path)

total_passengers   = len(df)
survival_rate      = round(df["Survived"].mean() * 100, 1)
average_age        = round(df["Age"].dropna().mean(), 1)
class_distribution = df["Pclass"].value_counts().sort_index()

print("Dataset loaded.")
print(f"  Total passengers  : {total_passengers}")
print(f"  Survival rate     : {survival_rate}%")
print(f"  Average age       : {average_age}")
print("  Class distribution:")
for pclass, count in class_distribution.items():
    print(f"    Class {pclass}: {count} passengers")


# ══════════════════════════════════════════════════════════════
#  TASK 2 — BUILD A STRUCTURED PROMPT
# ══════════════════════════════════════════════════════════════
#
#  A structured prompt is a text string that gives the LLM
#  both the context (the data) and the instruction (what to do).
#
#  Good prompts for data analysis include:
#    - A role assignment ("You are a data analyst...")
#    - The statistics in plain language
#    - A clear, specific question
#
#  We use an f-string to embed the computed statistics so the
#  prompt changes automatically if the data changes.
#
# EXAMPLE ──────────────────────────────────────────────────────

class_3_count = int(class_distribution.get(3, 0))
class_2_count = int(class_distribution.get(2, 0))
class_1_count = int(class_distribution.get(1, 0))

prompt = f"""You are a data analyst reviewing the Titanic passenger dataset.

Here are the key statistics:
  - Total passengers   : {total_passengers}
  - Survival rate      : {survival_rate}%
  - Average age        : {average_age} years
  - Class 1 passengers : {class_1_count}
  - Class 2 passengers : {class_2_count}
  - Class 3 passengers : {class_3_count}

Question: What patterns do you see in this data that might explain
why some passengers survived and others did not?"""

print("\nPrompt built successfully.")
print(f"  Prompt length: {len(prompt)} characters")


# ══════════════════════════════════════════════════════════════
#  TASK 3 — SIMULATE AN LLM RESPONSE
# ══════════════════════════════════════════════════════════════
#
#  In a real application you would send the prompt to an API
#  (OpenAI, Anthropic, etc.) and receive a response.
#
#  Here we use a hardcoded string that represents a realistic
#  AI response. This lets you build and test the full pipeline
#  without API keys or network access.
#
#  In production you would replace this string with:
#    response = openai_client.chat.completions.create(...)
#    simulated_response = response.choices[0].message.content
#
# EXAMPLE ──────────────────────────────────────────────────────

simulated_response = """Based on the Titanic statistics provided, several patterns stand out:

1. Survival rate of 38.4% indicates that most passengers did not survive.
   This aligns with historical records — there were not enough lifeboats
   for everyone on board.

2. Class distribution reveals a heavy skew toward third-class passengers.
   Historical data shows survival rates were strongly correlated with
   ticket class: first-class passengers had priority access to lifeboats.
   A survival rate below 50% suggests third-class passengers faced
   significantly worse odds.

3. The average age of approximately 29-30 years suggests a relatively
   young passenger population. Children were given priority in lifeboat
   loading ("women and children first"), so age would be an important
   predictor of survival.

4. Recommendations for deeper analysis:
   - Compare survival rate by Pclass (expect Class 1 > Class 2 > Class 3)
   - Analyze survival by Sex (women had much higher survival rates)
   - Check survival rate for passengers under 16 years old
   - Examine fare distribution as a proxy for socioeconomic status"""

print("\nLLM response received (simulated).")


# ══════════════════════════════════════════════════════════════
#  TASK 4 — PRINT THE FULL ASSISTANT REPORT
# ══════════════════════════════════════════════════════════════
#
#  The final report combines all three components into a
#  readable document:
#    Section 1: Data statistics (what we computed)
#    Section 2: The prompt (what we asked the AI)
#    Section 3: The AI response (what the AI answered)
#
#  Formatting guidelines:
#    - Use separator lines to divide sections clearly
#    - Label each section so a reader knows what they are seeing
#    - Round all numbers to 1 decimal place
#
# EXAMPLE ──────────────────────────────────────────────────────

separator = "=" * 60

print("\n")
print(separator)
print("  AI DATA ASSISTANT REPORT — TITANIC DATASET")
print(separator)

print("\n--- SECTION 1: DATA STATISTICS ---\n")
print(f"  Total passengers   : {total_passengers}")
print(f"  Survival rate      : {survival_rate}%")
print(f"  Average age        : {average_age} years")
print(f"  Class 1 passengers : {class_1_count}")
print(f"  Class 2 passengers : {class_2_count}")
print(f"  Class 3 passengers : {class_3_count}")

print("\n--- SECTION 2: PROMPT SENT TO AI ---\n")
print(prompt)

print("\n--- SECTION 3: AI RESPONSE ---\n")
print(simulated_response)

print("\n" + separator)
print("  END OF REPORT")
print(separator)


# ══════════════════════════════════════════════════════════════
#  YOUR TASKS
# ══════════════════════════════════════════════════════════════
#
#  The four tasks above are already complete as working examples.
#  Your job is to extend the assistant with the steps below.
#
# ──────────────────────────────────────────────────────────────
#  TASK 1 (your turn)
# ──────────────────────────────────────────────────────────────
#  Extend the statistics section.
#  Compute two more stats from the dataset:
#    - pct_female : percentage of passengers who were female
#    - pct_child  : percentage of passengers under age 16
#      (use df["Age"].dropna() and count those < 16)
#
#  Print both values in the format:
#    Female passengers  : 35.2%
#    Passengers under 16: 8.5%
#
#  Expected output (values depend on the real dataset):
#    Female passengers  : 35.2%
#    Passengers under 16: 8.5%

# --- starting data ---
# df is already loaded above


# (write your code here)




# ──────────────────────────────────────────────────────────────
#  TASK 2 (your turn)
# ──────────────────────────────────────────────────────────────
#  Rebuild the prompt to include the two new statistics
#  (pct_female and pct_child) from Task 1 above.
#  Add a second question at the end:
#    "Which passenger group would you predict had the highest
#     survival rate, and why?"
#
#  Print only the first 200 characters of the new prompt
#  followed by "..." to confirm it was built correctly.
#
#  Expected output:
#    Extended prompt preview (200 chars):
#    You are a data analyst reviewing the Titanic passenger dataset.
#    ...

# --- starting data ---
# pct_female and pct_child computed in Task 1


# (write your code here)




# ──────────────────────────────────────────────────────────────
#  TASK 3 (your turn)
# ──────────────────────────────────────────────────────────────
#  Write a second simulated LLM response that specifically
#  addresses the two new statistics (female percentage and
#  children percentage).
#
#  The response must be a multi-line string (at least 4 lines)
#  assigned to a variable called extended_response.
#  It should mention both "women" and "children" in the text.
#
#  Print the first line of extended_response.
#
#  Expected output (first line only):
#    Based on the additional gender and age statistics provided:

# --- starting data ---
# No variables needed — write the string from scratch


# (write your code here)




# ──────────────────────────────────────────────────────────────
#  TASK 4 (your turn)
# ──────────────────────────────────────────────────────────────
#  Print a final summary report that combines ALL six statistics
#  (the original four plus pct_female and pct_child).
#
#  Format the output as a table with two columns:
#    Statistic              Value
#    ──────────────────     ──────
#    Total passengers       891
#    Survival rate          38.4%
#    Average age            29.7 years
#    Female passengers      35.2%
#    Passengers under 16    8.5%
#    Class 1 / 2 / 3        216 / 184 / 491
#
#  Print the extended_response from Task 3 after the table.
#
#  Expected output:
#    FULL REPORT
#    ══════════════════════════════════════════════════════════════
#    Statistic              Value
#    ──────────────────     ──────
#    Total passengers       891
#    ...

# --- starting data ---
# All variables from Tasks 1-3 are available above


# (write your code here)




