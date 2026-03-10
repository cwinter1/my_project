# ══════════════════════════════════════════════════════════════
#  WEEK 4  |  DAY 6  |  WEEKLY PROJECT — TITANIC ANALYSIS
# ══════════════════════════════════════════════════════════════
#
#  PROJECT GOAL
#  ────────────
#  Analyze the Titanic passenger dataset to answer five business
#  questions about survival rates, fare differences, and
#  demographic patterns.
#
#  SKILLS PRACTICED
#  ─────────────────
#  - Loading Excel files with pd.read_excel
#  - DataFrame exploration: shape, dtypes, isnull
#  - Cleaning: fillna with median, dropna
#  - Boolean filtering and conditional logic
#  - groupby and aggregation (mean, value_counts)
#  - Creating new columns from existing data
#  - Formatted print output
#
#  TIME:  ~45-60 minutes
#
# ══════════════════════════════════════════════════════════════


# ── SETUP — provided by teacher, do not change ────────────────

import pandas as pd
import numpy as np
import os

this_file   = os.path.dirname(__file__)
titanic_path = os.path.join(this_file, "..", "datasets", "titanic_train.xlsx")

try:
    df_raw = pd.read_excel(titanic_path)
    print("Titanic dataset loaded:", df_raw.shape)
except FileNotFoundError:
    print("titanic_train.xlsx not found — generating inline demo data.")
    np.random.seed(42)
    n = 891
    df_raw = pd.DataFrame({
        "PassengerId": range(1, n + 1),
        "Survived":    np.random.choice([0, 1], n, p=[0.616, 0.384]),
        "Pclass":      np.random.choice([1, 2, 3], n, p=[0.242, 0.206, 0.552]),
        "Name":        ["Passenger_" + str(i) for i in range(1, n + 1)],
        "Sex":         np.random.choice(["male", "female"], n, p=[0.647, 0.353]),
        "Age":         np.where(np.random.rand(n) < 0.20, np.nan,
                                np.random.normal(29.7, 14.5, n).clip(1, 80).round(1)),
        "SibSp":       np.random.choice([0, 1, 2, 3, 4], n, p=[0.68, 0.23, 0.06, 0.02, 0.01]),
        "Parch":       np.random.choice([0, 1, 2, 3], n, p=[0.76, 0.13, 0.09, 0.02]),
        "Ticket":      ["T" + str(i) for i in range(1, n + 1)],
        "Fare":        np.where(np.random.rand(n) < 0.01, np.nan,
                                np.random.exponential(32, n).clip(5, 512).round(4)),
        "Cabin":       np.where(np.random.rand(n) < 0.77, np.nan, "C" + np.random.choice(
                                [str(i) for i in range(10, 150)], n).astype(str)),
        "Embarked":    np.random.choice(["S", "C", "Q", np.nan], n, p=[0.722, 0.188, 0.086, 0.004]),
    })


# ══════════════════════════════════════════════════════════════
#  TASK 1 — Explore the Dataset
# ══════════════════════════════════════════════════════════════
#  Print the following, each on a labelled line:
#    - Shape of the DataFrame (rows, columns)
#    - Column names and their dtypes
#    - Number of null values in each column (only show columns
#      that have at least 1 null)
#
#  Expected output (approximate with real data):
#    Shape: (891, 12)
#    Dtypes:
#    PassengerId      int64
#    Survived         int64
#    ...
#    Columns with nulls:
#    Age        177
#    Cabin      687
#    Embarked     2
#




# ══════════════════════════════════════════════════════════════
#  TASK 2 — Clean the Data
# ══════════════════════════════════════════════════════════════
#  Start with df = df_raw.copy().
#  Apply these cleaning steps in order:
#    1. Fill null values in the "Age" column with the median age
#    2. Drop any rows where "Fare" is null
#  Print the shape before and after cleaning.
#
#  Expected output (approximate):
#    Before cleaning: (891, 12)
#    After cleaning : (889, 12)
#




# ══════════════════════════════════════════════════════════════
#  TASK 3 — Survival Rates
# ══════════════════════════════════════════════════════════════
#  Use the cleaned df from Task 2 for all remaining tasks.
#
#  Calculate:
#    - The overall survival rate (mean of Survived, as a percentage)
#    - The survival rate broken down by Pclass (groupby + mean)
#
#  Print results rounded to 1 decimal place.
#
#  Expected output (approximate with real data):
#    Overall survival rate: 38.4%
#    Survival rate by class:
#    Pclass
#    1    62.9%
#    2    47.3%
#    3    24.2%
#




# ══════════════════════════════════════════════════════════════
#  TASK 4 — Gender and Survival
# ══════════════════════════════════════════════════════════════
#  Calculate the survival rate for male passengers and for female
#  passengers separately using groupby on "Sex".
#  Print the results rounded to 1 decimal place.
#
#  Expected output (approximate with real data):
#    Survival rate by gender:
#    Sex
#    female    74.2%
#    male      18.9%
#




# ══════════════════════════════════════════════════════════════
#  TASK 5 — Average Fare: Survivors vs Non-Survivors
# ══════════════════════════════════════════════════════════════
#  Group df by Survived and compute the mean of Fare.
#  Print each group's average fare rounded to 2 decimal places.
#  Label 0 as "Did not survive" and 1 as "Survived".
#
#  Expected output (approximate with real data):
#    Average fare — Did not survive: $22.12
#    Average fare — Survived       : $48.40
#




# ══════════════════════════════════════════════════════════════
#  TASK 6 — Survival Rate by Age Group
# ══════════════════════════════════════════════════════════════
#  Create a new column called "age_group" in df using these rules:
#    Age < 18            -> "child"
#    18 <= Age <= 60     -> "adult"
#    Age > 60            -> "senior"
#
#  Use pd.cut or a custom function — your choice.
#  Group by age_group and compute the mean survival rate.
#  Print results sorted from highest to lowest survival rate,
#  rounded to 1 decimal place.
#
#  Expected output (approximate with real data):
#    Survival rate by age group:
#    age_group
#    child     53.9%
#    adult     37.0%
#    senior    22.7%
#  (Order determined by survival rate, highest first.)
#


