# ══════════════════════════════════════════════════════════════
#  WEEK 5  |  DAY 5  |  PROJECT: SALES ANALYSIS
# ══════════════════════════════════════════════════════════════
#  LEARNING OBJECTIVES
#  ───────────────────
#  This mini-project combines everything from Weeks 4 and 5:
#  load -> clean -> filter -> group -> pivot -> visualize
#
#  TIME:  ~30-35 minutes
#
#  YOUTUBE
#  ───────
#  Search: "pandas end to end data analysis project"
#  Search: "matplotlib seaborn visualization project"
# ══════════════════════════════════════════════════════════════

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set_theme(style="whitegrid", palette="muted")

# ══════════════════════════════════════════════════════════════
#  SETUP — Load hotel_bookings.xlsx
# ══════════════════════════════════════════════════════════════
this_file = os.path.dirname(__file__)
hotel_path = os.path.join(this_file, "..", "datasets", "hotel_bookings.xlsx")

try:
    df_raw = pd.read_excel(hotel_path)
    print("Hotel bookings loaded:", df_raw.shape)
except FileNotFoundError:
    print("hotel_bookings.xlsx not found. Generating inline demo data.")
    np.random.seed(99)
    n = 1000
    months_list = ["January","February","March","April","May","June",
                   "July","August","September","October","November","December"]
    month_order = {m: i+1 for i, m in enumerate(months_list)}

    df_raw = pd.DataFrame({
        "hotel":               np.random.choice(["City Hotel","Resort Hotel"], n, p=[0.6,0.4]),
        "is_canceled":         np.random.choice([0, 1], n, p=[0.63, 0.37]),
        "lead_time":           np.random.exponential(80, n).round(0).astype(int).clip(0, 500),
        "arrival_date_year":   np.random.choice([2015, 2016, 2017], n, p=[0.2, 0.4, 0.4]),
        "arrival_date_month":  np.random.choice(months_list, n),
        "stays_in_weekend_nights": np.random.choice([0,1,2,3], n, p=[0.3,0.4,0.2,0.1]),
        "stays_in_week_nights":    np.random.choice([0,1,2,3,4,5], n, p=[0.1,0.2,0.3,0.2,0.15,0.05]),
        "adults":              np.random.choice([1,2,3,4], n, p=[0.2,0.6,0.15,0.05]),
        "children":            np.random.choice([0,1,2], n, p=[0.85,0.12,0.03]),
        "adr":                 np.abs(np.random.normal(100, 45, n)).round(2),
        "customer_type":       np.random.choice(["Transient","Contract","Group","Transient-Party"], n,
                                                p=[0.75, 0.10, 0.07, 0.08]),
        "distribution_channel": np.random.choice(["TA/TO","Direct","Corporate","GDS","Undefined"], n,
                                                  p=[0.47, 0.30, 0.14, 0.08, 0.01]),
        "market_segment":      np.random.choice(["Online TA","Offline TA/TO","Direct","Corporate",
                                                  "Groups","Complementary"], n,
                                                 p=[0.30, 0.20, 0.25, 0.15, 0.08, 0.02]),
        "total_of_special_requests": np.random.choice([0,1,2,3,4,5], n, p=[0.5,0.3,0.12,0.05,0.02,0.01]),
        "reserved_room_type":  np.random.choice(["A","B","C","D","E","F"], n,
                                                 p=[0.5,0.1,0.1,0.15,0.1,0.05]),
        "previous_cancellations": np.random.choice([0,1,2], n, p=[0.87, 0.10, 0.03]),
    })

print("\nFirst 5 rows:")
print(df_raw.head())
print("\nColumn names:")
print(list(df_raw.columns))


# ══════════════════════════════════════════════════════════════
#  STEP 1 — CHECK NULLS AND BASIC QUALITY (demonstrated for you)
# ══════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("STEP 1: Data Quality Check")
print("="*60)

print("Shape:", df_raw.shape)
print("\nNull counts:")
null_counts = df_raw.isnull().sum()
print(null_counts[null_counts > 0])

print("\nData types (numeric only):")
print(df_raw.select_dtypes(include="number").dtypes)

# Check the adr (average daily rate) column
if "adr" in df_raw.columns:
    print(f"\nADR stats: min={df_raw['adr'].min():.2f}, "
          f"mean={df_raw['adr'].mean():.2f}, "
          f"max={df_raw['adr'].max():.2f}")


# ══════════════════════════════════════════════════════════════
#  TASK 1 — CLEAN THE DATA
# ══════════════════════════════════════════════════════════════
# Complete the cleaning steps below.
# All instructions are in the comments.

print("\n" + "="*60)
print("TASK 1: Data Cleaning")
print("="*60)

# Start with a copy
df = df_raw.copy()

# 1a. Fill nulls in "children" with 0 if it exists
# 1b. Fill nulls in "adr" with the median if it exists
# 1c. Remove rows where adr <= 0 (those are complimentary / data errors)
# 1d. Remove rows where adults == 0 (invalid bookings)
# 1e. Print the shape after cleaning




# ══════════════════════════════════════════════════════════════
#  STEP 2 — FEATURE ENGINEERING (demonstrated for you)
# ══════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("STEP 2: Feature Engineering")
print("="*60)

# Ensure df is defined even if Task 1 was skipped
if "df" not in dir() or df is None:
    df = df_raw.copy()

# Calculate total stay length (weekend + weekday nights)
if "stays_in_weekend_nights" in df.columns and "stays_in_week_nights" in df.columns:
    df["total_nights"] = df["stays_in_weekend_nights"] + df["stays_in_week_nights"]

# Calculate estimated revenue per booking
if "adr" in df.columns and "total_nights" in df.columns:
    df["estimated_revenue"] = (df["adr"] * df["total_nights"]).round(2)

# Convert month name to month number for sorting
month_order_map = {
    "January":1,"February":2,"March":3,"April":4,"May":5,"June":6,
    "July":7,"August":8,"September":9,"October":10,"November":11,"December":12
}
if "arrival_date_month" in df.columns:
    df["arrival_month_num"] = df["arrival_date_month"].map(month_order_map)

print("New columns added:")
print([c for c in df.columns if c not in df_raw.columns])


# ══════════════════════════════════════════════════════════════
#  TASK 2 — FILTER AND AGGREGATION ANALYSIS
# ══════════════════════════════════════════════════════════════
# Complete the analysis below. Instructions are in the comments.

print("\n" + "="*60)
print("TASK 2: Analysis")
print("="*60)

# 2a. Filter to non-canceled bookings only (is_canceled == 0)
#     Store as df_active

# 2b. Using df_active, calculate cancellation rate by hotel type:
#     group by "hotel", count total bookings and sum is_canceled from df (all rows)
#     Print: "City Hotel cancellation rate: X.X%"
#            "Resort Hotel cancellation rate: X.X%"

# 2c. Using df_active, find the top 3 market segments by estimated_revenue (total sum)
#     Print them sorted descending

# 2d. Using df_active, calculate average adr by:
#     - hotel type
#     - customer_type
#     (Group by both columns, find mean of adr, round to 2)
#     Print the result




# ══════════════════════════════════════════════════════════════
#  STEP 3 — PIVOT TABLE (demonstrated for you)
# ══════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("STEP 3: Pivot Table — Bookings by Hotel and Month")
print("="*60)

# Ensure df_active exists
df_active = df[df["is_canceled"] == 0].copy() if "is_canceled" in df.columns else df.copy()

if "arrival_date_month" in df_active.columns and "hotel" in df_active.columns:
    # Sort months correctly
    month_order_list = ["January","February","March","April","May","June",
                        "July","August","September","October","November","December"]
    available_months = [m for m in month_order_list if m in df_active["arrival_date_month"].unique()]

    pivot = pd.pivot_table(
        df_active,
        values="adr",
        index="hotel",
        columns="arrival_date_month",
        aggfunc="mean",
        fill_value=0,
    )
    # Reorder columns to calendar order if possible
    pivot = pivot.reindex(columns=[m for m in month_order_list if m in pivot.columns])
    print(pivot.round(2).to_string())


# ══════════════════════════════════════════════════════════════
#  TASK 3 — CREATE 3 VISUALIZATIONS
# ══════════════════════════════════════════════════════════════
# Create three charts, each saved to a separate PNG file.

print("\n" + "="*60)
print("TASK 3: Visualizations")
print("="*60)

# Chart 1: Bar chart — Average ADR by hotel type
# Use df_active, group by "hotel", compute mean of "adr"
# Colors: ["steelblue", "darkorange"]
# Title: "Average Daily Rate by Hotel Type"
# Save as: "project_chart1_adr.png"




# Chart 2: Line chart — Monthly booking trend
# Use df_active, group by arrival_month_num, count rows
# Sort by month number so January is first
# Title: "Monthly Booking Volume"
# X label: "Month Number", Y label: "Number of Bookings"
# Save as: "project_chart2_monthly.png"




# Chart 3: Box plot — ADR distribution by customer type
# Use seaborn: sns.boxplot(data=df_active, x="customer_type", y="adr")
# Rotate x-axis labels 20 degrees
# Title: "ADR Distribution by Customer Type"
# Save as: "project_chart3_customer.png"




# ══════════════════════════════════════════════════════════════
#  TASK 4 — GENERATE A SUMMARY REPORT DICT
# ══════════════════════════════════════════════════════════════
# Create a dict called report_summary with the following keys and values.
# All values should be computed from df_active (non-canceled bookings).

print("\n" + "="*60)
print("TASK 4: Summary Report")
print("="*60)

# Keys to populate:
#   "total_bookings"        : number of rows in df_active
#   "average_adr"           : mean of adr, rounded to 2
#   "average_nights"        : mean of total_nights, rounded to 2 (or 0 if column missing)
#   "total_estimated_revenue": sum of estimated_revenue, rounded to 0 (or 0 if missing)
#   "top_hotel_by_bookings" : hotel type with the most bookings (value_counts().idxmax())
#   "top_market_segment"    : market segment with the most bookings




# ══════════════════════════════════════════════════════════════
#  FINAL OUTPUT — Print the report summary
# ══════════════════════════════════════════════════════════════
# After completing all tasks, uncomment and run this block to see your results.

# print("\n" + "="*60)
# print("FINAL REPORT SUMMARY")
# print("="*60)
# for key, value in report_summary.items():
#     print(f"  {key:<35}: {value}")
