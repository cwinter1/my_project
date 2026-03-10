# ══════════════════════════════════════════════════════════════
#  WEEK 5  |  DAY 3  |  TIME SERIES ANALYSIS
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Parse and index datetime data using pd.to_datetime and DatetimeIndex
#  2. Resample time series to different frequencies with .resample("ME")
#  3. Smooth noisy data with rolling averages using .rolling().mean()
#
#  TIME:  ~30 minutes  (3 concepts × 10 min each)
#
#  YOUTUBE
#  ───────
#  Search: "pandas time series datetime index resample"
#  Search: "pandas rolling window moving average tutorial"
#
# ══════════════════════════════════════════════════════════════

# All data is generated inline with pd.date_range — no external file needed.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
date_range = pd.date_range(start="2022-01-01", end="2023-12-31", freq="D")
n = len(date_range)

# Simulate seasonal + trending + noisy daily sales
seasonal = np.sin(np.linspace(0, 4 * np.pi, n)) * 800 + 3000
trend    = np.linspace(0, 500, n)
noise    = np.random.normal(0, 300, n)
sales    = (seasonal + trend + noise).clip(0)

df_raw = pd.DataFrame({
    "date":    date_range,
    "sales":   sales.round(2),
    "orders":  (sales / 35).round(0).astype(int),
    "returns": (sales * 0.03 + np.random.normal(0, 10, n)).clip(0).round(0).astype(int),
})
print("Raw shape:", df_raw.shape)
print(df_raw.head(3))


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — pd.to_datetime AND DatetimeIndex
# ══════════════════════════════════════════════════════════════
#
#  Time series analysis requires a proper datetime index.
#  pandas stores dates as datetime64 — a fast, sortable numeric type.
#
#  pd.to_datetime(series)             convert strings to datetime
#  pd.date_range(start, end, freq)    generate a sequence of dates
#    freq options: "D" daily, "W" weekly, "ME" month-end,
#                  "QE" quarter-end, "YE" year-end, "h" hourly
#  df.set_index("date_col")           promote a column to the index
#
#  After setting a DatetimeIndex you can slice by string:
#    df.loc["2022-01"]          entire January 2022
#    df.loc["2022-01":"2022-03"] January through March 2022
#
#  Datetime properties available on a DatetimeIndex:
#    .year, .month, .day
#    .day_name()    "Monday", "Tuesday", etc.
#    .quarter       1, 2, 3, or 4
#
# EXAMPLE ──────────────────────────────────────────────────────

# Convert the date column and set as index
df = df_raw.copy()
df["date"] = pd.to_datetime(df["date"])
df = df.set_index("date")

print("\nDatetimeIndex dtype:", df.index.dtype)     # datetime64[ns]
print("January 2022 rows:", len(df.loc["2022-01"]))  # 31
print("Q1 2022 rows:", len(df.loc["2022-01-01":"2022-03-31"]))  # 90

# Extract date parts as columns for grouping
df["month"]       = df.index.month
df["year"]        = df.index.year
df["day_of_week"] = df.index.day_name()
df["quarter"]     = df.index.quarter

print("\nWith date parts extracted:")
print(df.head(3))

# Plot the raw daily series
plt.figure(figsize=(14, 4))
plt.plot(df.index, df["sales"], color="steelblue", linewidth=0.8, alpha=0.7)
plt.title("Daily Sales 2022-2023", fontsize=13, fontweight="bold")
plt.xlabel("Date")
plt.ylabel("Sales (USD)")
plt.tight_layout()
plt.show()


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
#
#  Using df (already has a DatetimeIndex):
#
#  1. Filter to all rows in Q4 2022 using df.loc["2022-10":"2022-12"].
#     Print how many rows are in Q4 2022.
#
#  2. Calculate and print the total Q4 2022 sales (round to 0).
#
#  3. Using the "day_of_week" column, find the day of the week with
#     the highest average sales. Group by day_of_week, take mean of sales,
#     then call .idxmax(). Print: "Best sales day: <day>"
#
#  Expected output:
#      Q4 2022 rows: 92
#      Q4 2022 total sales: <value around 275000>
#      Best sales day: <varies by seed, likely Wednesday or Thursday>
#






# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — RESAMPLING WITH .resample()
# ══════════════════════════════════════════════════════════════
#
#  Resampling changes the frequency of a time series.
#
#  Downsampling (fewer rows, aggregated):
#    df.resample("ME").sum()    monthly totals  (ME = month-end)
#    df.resample("W").mean()    weekly averages
#    df.resample("QE").sum()    quarterly totals
#    df.resample("YE").sum()    annual totals
#
#  resample() requires a DatetimeIndex.
#  Older pandas code used "M", "Q", "Y" — newer pandas uses "ME", "QE", "YE".
#  After resampling, call .to_period("M") to get readable labels like 2022-01.
#
# EXAMPLE ──────────────────────────────────────────────────────

df_ts = df[["sales", "orders", "returns"]].copy()

# Monthly totals
monthly = df_ts.resample("ME").sum()
monthly.index = monthly.index.to_period("M")
print("\n=== Monthly Totals (first 6) ===")
print(monthly.head(6))

# Monthly average daily sales
monthly_avg = df_ts["sales"].resample("ME").mean().round(2)
print("\n=== Monthly Average Daily Sales (first 6) ===")
print(monthly_avg.head(6))

# Year-over-year growth
annual = df_ts.resample("YE").sum()
yoy = ((annual["sales"].iloc[1] / annual["sales"].iloc[0]) - 1) * 100
print(f"\nYear-over-year sales growth: {yoy:.1f}%")

# Monthly comparison bar chart
monthly_2022 = df_ts["sales"].loc["2022"].resample("ME").sum()
monthly_2023 = df_ts["sales"].loc["2023"].resample("ME").sum()

plt.figure(figsize=(12, 5))
x = np.arange(12)
plt.bar(x - 0.2, monthly_2022.values, width=0.35, label="2022", color="steelblue", alpha=0.8)
plt.bar(x + 0.2, monthly_2023.values, width=0.35, label="2023", color="darkorange", alpha=0.8)
plt.xticks(x, ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])
plt.title("Monthly Revenue: 2022 vs 2023", fontsize=13, fontweight="bold")
plt.xlabel("Month")
plt.ylabel("Total Sales (USD)")
plt.legend()
plt.tight_layout()
plt.show()


# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
#
#  Using df_ts (DatetimeIndex, columns: sales, orders, returns):
#
#  1. Resample to weekly with "W" and sum. Print the first 4 rows.
#
#  2. Calculate monthly return rate:
#       monthly_returns = df_ts["returns"].resample("ME").sum()
#       monthly_orders  = df_ts["orders"].resample("ME").sum()
#       return_rate = (monthly_returns / monthly_orders * 100).round(2)
#     Print the 2022 monthly return rate.
#
#  3. Find the month with the highest total sales across both years.
#     Print: "Best month: <period> with $<amount> total sales"
#
#  Expected output:
#      Weekly data (first 4 rows): [4 rows]
#      Monthly return rate 2022: [series]
#      Best month: <period> with $<amount> total sales
#


# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — ROLLING WINDOW WITH .rolling().mean()
# ══════════════════════════════════════════════════════════════
#
#  Raw daily data is noisy. A moving average smooths out short-term variation
#  to reveal the underlying trend.
#
#  .rolling(window=7).mean()    7-day moving average
#  .rolling(window=30).mean()   30-day moving average
#  .rolling(7).sum()            7-day rolling sum
#  .rolling(7).std()            7-day rolling standard deviation
#
#  The first (window - 1) values are NaN because there is not enough history.
#  Use rolling(7, min_periods=1) to allow fewer than 7 periods at the start.
#
#  Anomaly detection pattern:
#    upper = ma_30 + 2 * rolling_std
#    lower = ma_30 - 2 * rolling_std
#    anomalies = df[(df["sales"] > upper) | (df["sales"] < lower)]
#
# EXAMPLE ──────────────────────────────────────────────────────

df_ts["ma_7"]  = df_ts["sales"].rolling(window=7).mean()
df_ts["ma_30"] = df_ts["sales"].rolling(window=30).mean()
df_ts["ma_90"] = df_ts["sales"].rolling(window=90).mean()

print("\n=== Rolling Averages (first 10 rows) ===")
print(df_ts[["sales", "ma_7", "ma_30"]].head(10))
# First 6 rows of ma_7 will be NaN, first 29 rows of ma_30 will be NaN

# Plot raw data with three moving averages
plt.figure(figsize=(14, 6))
plt.plot(df_ts.index, df_ts["sales"],  color="lightsteelblue", linewidth=0.6, alpha=0.8, label="Daily Sales")
plt.plot(df_ts.index, df_ts["ma_7"],   color="steelblue",  linewidth=1.5, label="7-Day MA")
plt.plot(df_ts.index, df_ts["ma_30"],  color="darkorange", linewidth=2,   label="30-Day MA")
plt.plot(df_ts.index, df_ts["ma_90"],  color="crimson",    linewidth=2.5, label="90-Day MA")
plt.title("Daily Sales with Moving Averages", fontsize=13, fontweight="bold")
plt.xlabel("Date")
plt.ylabel("Sales (USD)")
plt.legend(loc="upper left")
plt.tight_layout()
plt.show()

# Anomaly detection: days more than 2 std from the 30-day mean
df_ts["rolling_std"] = df_ts["sales"].rolling(window=30).std()
upper = df_ts["ma_30"] + 2 * df_ts["rolling_std"]
lower = df_ts["ma_30"] - 2 * df_ts["rolling_std"]
anomalies = df_ts[(df_ts["sales"] > upper) | (df_ts["sales"] < lower)]
print(f"\nAnomaly days (>2 std from 30-day mean): {len(anomalies)}")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
#
#  Using df_ts:
#
#  1. Calculate a 14-day rolling mean of sales, stored as "ma_14".
#  2. Calculate a 14-day rolling min and max, stored as "roll_min" and "roll_max".
#
#  3. Create a plot of 2023 data only (df_ts.loc["2023"]) showing:
#       - The 14-day MA as a solid blue line (label="14-Day MA")
#       - A shaded band between roll_min and roll_max using plt.fill_between()
#         (alpha=0.2, color="steelblue", label="Min/Max Band")
#     Title: "2023 Sales: 14-Day Rolling Window"
#     Call plt.legend(), plt.tight_layout(), plt.show()
#
#  4. Print the date in 2023 where the 14-day MA reached its peak value.
#     Print: "Peak MA date: <date>"
#
#  Expected output:
#      Chart with a trend line surrounded by a light shaded band
#      Peak MA date: <date in 2023>
#
