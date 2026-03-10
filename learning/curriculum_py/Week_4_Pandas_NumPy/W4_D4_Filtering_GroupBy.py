# ══════════════════════════════════════════════════════════════
#  WEEK 4  |  DAY 4  |  FILTERING AND GROUPBY
# ══════════════════════════════════════════════════════════════
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Filter rows using boolean conditions, including multi-condition filtering
#  2. Group data by one column and apply a single aggregation
#  3. Apply multiple aggregations with groupby().agg() and clean the result
#
#  TIME:  ~30-35 minutes
#
#  YOUTUBE
#  ───────
#  Search: "pandas boolean filtering multiple conditions"
#  Search: "pandas groupby agg tutorial"
# ══════════════════════════════════════════════════════════════

import pandas as pd
import numpy as np
import os

# Load the police dataset (police.xlsx from datasets folder)
this_file = os.path.dirname(__file__)
police_path = os.path.join(this_file, "..", "datasets", "police.xlsx")

try:
    df = pd.read_excel(police_path)
    print("Police dataset loaded:", df.shape)
    print("Columns:", list(df.columns))
    print(df.head(3))
except FileNotFoundError:
    print(f"police.xlsx not found at: {police_path}")
    print("Using inline demo DataFrame for this lesson.")
    # Inline fallback dataset — realistic traffic stop data
    np.random.seed(42)
    n = 200
    df = pd.DataFrame({
        "stop_date":     pd.date_range("2015-01-01", periods=n, freq="3D").strftime("%Y-%m-%d"),
        "driver_gender": np.random.choice(["M", "F"], n),
        "driver_age":    np.random.randint(16, 75, n),
        "driver_race":   np.random.choice(["White", "Black", "Hispanic", "Asian"], n, p=[0.5,0.25,0.15,0.10]),
        "violation":     np.random.choice(["Speeding", "Equipment", "Moving violation",
                                           "Registration/plates", "Other"], n),
        "search_conducted": np.random.choice([True, False], n, p=[0.15, 0.85]),
        "stop_outcome":  np.random.choice(["Citation", "Warning", "Arrest", "No action"], n,
                                          p=[0.55, 0.30, 0.10, 0.05]),
        "is_arrested":   np.random.choice([True, False], n, p=[0.10, 0.90]),
        "stop_duration": np.random.choice(["0-15 Min", "16-30 Min", "30+ Min"], n,
                                          p=[0.60, 0.30, 0.10]),
        "drugs_related_stop": np.random.choice([True, False], n, p=[0.05, 0.95]),
    })

print("\nDataset preview:")
print(df.head())


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — BOOLEAN FILTERING
# ══════════════════════════════════════════════════════════════
# Boolean filtering works by creating a True/False mask and applying it to the DataFrame.
#
# Single condition:
#   df[df["col"] == "value"]
#   df[df["col"] > 100]
#
# Multiple conditions — MUST use & (AND), | (OR), ~ (NOT):
#   df[(df["age"] > 30) & (df["gender"] == "F")]
#   df[(df["status"] == "A") | (df["status"] == "B")]
#
# IMPORTANT: Always wrap each condition in parentheses when combining.
# Python's 'and'/'or' do NOT work on boolean arrays — use & and | instead.
#
# Other useful filter methods:
#   df[df["col"].isin(["A", "B"])]      -- match any value in a list
#   df[df["col"].str.contains("text")]  -- string contains (case-sensitive by default)
#   df[df["col"].between(10, 20)]       -- inclusive range filter

# EXAMPLE ──────────────────────────────────────────────────────
# Single condition: filter to Speeding violations only
speeding = df[df["violation"] == "Speeding"]
print("\n=== Single Condition Filter ===")
print(f"Speeding stops: {len(speeding)}")

# Single condition: filter to stops that resulted in an arrest
arrested = df[df["is_arrested"] == True]
print(f"Arrests: {len(arrested)}")

# Multiple conditions: female drivers, arrested
female_arrests = df[(df["driver_gender"] == "F") & (df["is_arrested"] == True)]
print(f"\nFemale arrests: {len(female_arrests)}")

# Multiple conditions with OR: Citation OR Warning outcome
non_arrest_outcomes = df[(df["stop_outcome"] == "Citation") | (df["stop_outcome"] == "Warning")]
print(f"Citations or Warnings: {len(non_arrest_outcomes)}")

# Using isin for multiple value matching (cleaner than multiple OR conditions)
minor_outcomes = df[df["stop_outcome"].isin(["Warning", "No action"])]
print(f"Minor outcomes (Warning or No action): {len(minor_outcomes)}")

# Negate with ~
not_speeding = df[~(df["violation"] == "Speeding")]
print(f"Non-speeding stops: {len(not_speeding)}")

# Age range filter
young_drivers = df[df["driver_age"].between(16, 25)]
print(f"Drivers aged 16-25: {len(young_drivers)}")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
# Using the police/demo DataFrame df:
#
# Task A: Filter to male drivers who were searched (search_conducted == True)
#         Print how many rows match
#
# Task B: Filter to speeding stops where the driver was NOT arrested
#         Print how many rows match
#
# Task C: Filter to stops with stop_duration == "30+ Min" AND
#         (stop_outcome == "Arrest" OR is_arrested == True)
#         Print the first 5 matching rows
#
# Expected output will depend on whether real or demo data is used.
# Print counts for A and B, and head(5) for C.




# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — groupby() WITH SINGLE AGGREGATION
# ══════════════════════════════════════════════════════════════
# groupby() splits the DataFrame into groups by one or more column values.
# You then apply an aggregation function to each group.
#
# Syntax:
#   df.groupby("column")["value_column"].agg_function()
#
# Common aggregation functions:
#   .count()    -- number of non-null values
#   .sum()      -- total
#   .mean()     -- average
#   .median()   -- median
#   .min()      -- minimum
#   .max()      -- maximum
#   .std()      -- standard deviation
#   .nunique()  -- count of distinct values
#
# The result is a Series (or DataFrame) with the group labels as index.
# Use .reset_index() to convert the index back to a regular column.

# EXAMPLE ──────────────────────────────────────────────────────
# Count of stops by violation type
stops_by_violation = df.groupby("violation")["violation"].count()
print("\n=== Stops by Violation ===")
print(stops_by_violation.sort_values(ascending=False))

# Arrest rate by gender (mean of boolean is_arrested gives the proportion)
arrest_rate = df.groupby("driver_gender")["is_arrested"].mean().round(3) * 100
print("\n=== Arrest Rate by Gender (%) ===")
print(arrest_rate)

# Average driver age by violation
avg_age = df.groupby("violation")["driver_age"].mean().round(1)
print("\n=== Average Driver Age by Violation ===")
print(avg_age)

# Count stops per race using reset_index() to get a clean DataFrame
stops_by_race = (
    df.groupby("driver_race")["driver_race"]
    .count()
    .reset_index(name="stop_count")
    .sort_values("stop_count", ascending=False)
)
print("\n=== Stops by Race (as DataFrame) ===")
print(stops_by_race)


# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
# Using df:
#
# Task A: Count the number of stops per stop_outcome.
#         Sort from most to least common. Print the result.
#
# Task B: Calculate the search rate (mean of search_conducted) by violation type.
#         Round to 3 decimal places. Sort by rate descending.
#         Print as a clean DataFrame with columns: violation, search_rate
#
# Task C: Find the stop_duration type with the highest arrest rate.
#         Print: "<duration> has the highest arrest rate: X.X%"
#
# Expected output format:
#   Stop counts by outcome:
#   Citation      ...
#   Warning       ...
#   ...
#
#   Search rate by violation:
#   ...
#
#   30+ Min has the highest arrest rate: X.X%




# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — groupby() WITH MULTIPLE AGGREGATIONS (agg dict), reset_index()
# ══════════════════════════════════════════════════════════════
# Use .agg() with a dict to apply DIFFERENT aggregations to DIFFERENT columns.
#
# Syntax:
#   df.groupby("group_col").agg({
#       "col_a": "sum",
#       "col_b": "mean",
#       "col_c": ["min", "max"],   # multiple functions for one column
#   })
#
# This returns a DataFrame.
# When you use a list of functions, the column headers become a MultiIndex.
# Use .reset_index() to flatten the index.
# Use .columns = [...] or .rename() to give readable column names.

# EXAMPLE ──────────────────────────────────────────────────────
# Comprehensive summary: group by violation
summary = df.groupby("violation").agg(
    total_stops=("violation", "count"),
    arrests=("is_arrested", "sum"),
    searches=("search_conducted", "sum"),
    avg_age=("driver_age", "mean"),
    search_rate=("search_conducted", "mean"),
    arrest_rate=("is_arrested", "mean"),
).round(3).reset_index()

# Convert rates to percentages
summary["search_rate"] = (summary["search_rate"] * 100).round(1)
summary["arrest_rate"] = (summary["arrest_rate"] * 100).round(1)

print("\n=== Violation Summary ===")
print(summary.to_string(index=False))

# Multiple agg functions per column — results in MultiIndex columns
age_stats = df.groupby("driver_gender")["driver_age"].agg(["mean", "min", "max", "std"])
age_stats = age_stats.round(1).reset_index()
age_stats.columns = ["gender", "avg_age", "min_age", "max_age", "std_age"]
print("\n=== Driver Age Stats by Gender ===")
print(age_stats)

# Two-level groupby: violation AND gender
dual_group = (
    df.groupby(["violation", "driver_gender"])
    .agg(
        stops=("violation", "count"),
        arrests=("is_arrested", "sum"),
    )
    .reset_index()
)
print("\n=== Stops and Arrests by Violation and Gender ===")
print(dual_group)


# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
# Using df, build a comprehensive report grouped by driver_race.
# Use .agg() to calculate in ONE groupby call:
#   - total_stops:    count of stops
#   - total_arrests:  sum of is_arrested
#   - total_searches: sum of search_conducted
#   - avg_age:        mean of driver_age (round to 1)
#   - arrest_pct:     mean of is_arrested * 100 (round to 2)
#   - search_pct:     mean of search_conducted * 100 (round to 2)
#
# Sort the result by total_stops descending.
# Print the final DataFrame with these column names exactly.
#
# Then print:
#   "Race with highest search rate: <race> (<pct>%)"
#
# Expected output format:
#   driver_race   total_stops  total_arrests  ...  search_pct
#   White         ...
#   Black         ...
#   ...
#
#   Race with highest search rate: <race> (<value>%)


