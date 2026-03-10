# ══════════════════════════════════════════════════════════════
#  WEEK 5  |  DAY 4  |  DESCRIPTIVE STATISTICS
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Compute and interpret descriptive statistics with describe() and quantiles
#  2. Calculate and interpret a correlation matrix with df.corr()
#  3. Detect outliers using the IQR method
#
#  TIME:  ~30 minutes  (3 concepts × 10 min each)
#
#  YOUTUBE
#  ───────
#  Search: "pandas describe statistics mean median std quartiles"
#  Search: "Python outlier detection IQR method tutorial"
#
# ══════════════════════════════════════════════════════════════

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

hotel_path   = os.path.join(os.path.dirname(__file__), "..", "datasets", "hotel_bookings.xlsx")
titanic_path = os.path.join(os.path.dirname(__file__), "..", "datasets", "titanic_train.xlsx")

df = None
for path, name in [(hotel_path, "hotel_bookings"), (titanic_path, "titanic")]:
    try:
        df = pd.read_excel(path)
        print(f"Loaded {name}: {df.shape}")
        break
    except FileNotFoundError:
        continue

if df is None:
    print("No dataset file found. Using inline demo data.")
    np.random.seed(42)
    n = 500
    df = pd.DataFrame({
        "lead_time":       np.random.exponential(80, n).round(0).astype(int).clip(0, 500),
        "stays_in_nights": np.random.poisson(3, n).clip(1, 20),
        "adults":          np.random.choice([1, 2, 3, 4], n, p=[0.2, 0.6, 0.15, 0.05]),
        "adr":             np.abs(np.random.normal(100, 45, n)).round(2),
        "is_canceled":     np.random.choice([0, 1], n, p=[0.63, 0.37]),
        "total_guests":    np.random.choice([1, 2, 3, 4, 5], n, p=[0.15, 0.55, 0.20, 0.07, 0.03]),
        "total_of_special_requests": np.random.choice([0, 1, 2, 3, 4], n, p=[0.5, 0.3, 0.15, 0.04, 0.01]),
        "hotel": np.random.choice(["City Hotel", "Resort Hotel"], n, p=[0.6, 0.4]),
    })

print("Columns:", list(df.columns))

numeric_cols = df.select_dtypes(include="number").columns.tolist()
target_col   = "adr" if "adr" in numeric_cols else numeric_cols[0]


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — DESCRIPTIVE STATISTICS: describe(), QUARTILES
# ══════════════════════════════════════════════════════════════
#
#  df.describe() returns for each numeric column:
#    count   non-null count
#    mean    arithmetic average
#    std     standard deviation (spread around the mean)
#    min     smallest value
#    25%     Q1: 25% of data falls below this
#    50%     median (Q2)
#    75%     Q3: 75% of data falls below this
#    max     largest value
#
#  KEY INTERPRETATION:
#    mean >> median    right-skewed (a few very large values pull the mean up)
#    large std / mean  high variability relative to the average
#    large Q3-to-max gap   potential outliers at the top
#
#  Additional methods:
#    col.skew()               skewness (+: right tail, -: left tail)
#    col.quantile(0.90)       90th percentile
#    df.groupby(col).describe() statistics split by a category
#
# EXAMPLE ──────────────────────────────────────────────────────

print("\n=== DESCRIPTIVE STATISTICS ===")
print(df.describe().round(2))

col = df[target_col]
print(f"\n=== {target_col.upper()} DETAIL ===")
print(f"Mean:     {col.mean():.2f}")
print(f"Median:   {col.median():.2f}")
print(f"Std:      {col.std():.2f}")
print(f"Q1:       {col.quantile(0.25):.2f}")
print(f"Q3:       {col.quantile(0.75):.2f}")
skew = col.skew()
label = "right-skewed" if skew > 0.5 else "left-skewed" if skew < -0.5 else "approximately symmetric"
print(f"Skewness: {skew:.2f} ({label})")

# Statistics grouped by hotel type or another category
group_col = "hotel" if "hotel" in df.columns else df.select_dtypes("object").columns[0]
print(f"\n=== {target_col} by {group_col} ===")
print(df.groupby(group_col)[target_col].describe().round(2))

# Histogram + boxplot side by side
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.hist(col.dropna(), bins=40, color="steelblue", edgecolor="white", alpha=0.8)
plt.axvline(col.mean(),   color="red",    linestyle="--", label=f"Mean: {col.mean():.0f}")
plt.axvline(col.median(), color="orange", linestyle="--", label=f"Median: {col.median():.0f}")
plt.title(f"{target_col} Distribution")
plt.xlabel(target_col)
plt.legend()

plt.subplot(1, 2, 2)
plt.boxplot(col.dropna(), vert=True, patch_artist=True,
            boxprops={"facecolor": "lightsteelblue"})
plt.title(f"{target_col} Box Plot")
plt.ylabel(target_col)
plt.tight_layout()
plt.show()


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
#
#  Using df and its numeric columns:
#
#  1. Print descriptive stats for all numeric columns (df.describe()).
#
#  2. Find the column with the highest coefficient of variation.
#     CV = std / mean — measures variability relative to the average.
#     Print: "Most variable column: <name> (CV = X.XX)"
#
#  3. Print the 90th percentile of target_col.
#     Print: "90th percentile of <target_col>: X.XX"
#
#  Expected output:
#      Most variable column: <name> (CV = X.XX)
#      90th percentile of adr: X.XX
#






# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — CORRELATION: df.corr()
# ══════════════════════════════════════════════════════════════
#
#  Pearson correlation measures the LINEAR relationship between two variables.
#  Ranges from -1 to +1:
#    +1.0   perfect positive (both rise together)
#    +0.7   strong positive
#    +0.3   moderate positive
#    ~0.0   no linear relationship
#    -0.3   moderate negative
#    -1.0   perfect negative
#
#  df.corr()                    Pearson (default), numeric columns only
#  df.corr(method="spearman")   Spearman rank (better for skewed data)
#  df[a].corr(df[b])            correlation between two specific columns
#
#  IMPORTANT: correlation only detects LINEAR relationships.
#
# EXAMPLE ──────────────────────────────────────────────────────

corr_cols   = df.select_dtypes(include="number").columns[:6].tolist()
corr_matrix = df[corr_cols].corr()

print("\n=== CORRELATION MATRIX ===")
print(corr_matrix.round(3))

# Find the top 3 most-correlated pairs
corr_pairs = []
for i, col_a in enumerate(corr_cols):
    for j, col_b in enumerate(corr_cols):
        if j > i:
            r = corr_matrix.loc[col_a, col_b]
            corr_pairs.append((abs(r), r, col_a, col_b))

corr_pairs.sort(reverse=True)
print("\nTop 3 correlated pairs:")
for abs_r, r, a, b in corr_pairs[:3]:
    direction = "positive" if r > 0 else "negative"
    strength  = "strong" if abs_r > 0.5 else "moderate" if abs_r > 0.3 else "weak"
    print(f"  {a} vs {b}: r={r:.3f} ({strength} {direction})")

# Heatmap
plt.figure(figsize=(9, 7))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", vmin=-1, vmax=1,
            fmt=".2f", square=True, linewidths=0.5)
plt.title("Correlation Matrix", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.show()


# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
#
#  Using df_sales_corr below:
#
#  1. Print the full correlation matrix.
#
#  2. Find the column most correlated with "revenue" (excluding revenue itself).
#     Print: "Most correlated with revenue: <column> (r = X.XX)"
#
#  3. Create a scatter plot of that column vs revenue.
#     Add a trend line using np.polyfit(x, y, 1) and np.poly1d.
#     Title: "<column> vs Revenue"
#     Call plt.tight_layout() then plt.show()
#
#  Expected output:
#      Correlation matrix printed
#      Most correlated with revenue: <column> (r = X.XX)
#      Scatter plot with trend line
#

np.random.seed(55)
n2 = 150
exp_col    = np.random.uniform(1, 20, n2)
calls_col  = exp_col * 7 + np.random.normal(0, 10, n2)
props_col  = calls_col * 0.25 + np.random.normal(0, 5, n2)
closed_col = props_col * 0.35 + np.random.normal(0, 2, n2)
rev_col    = closed_col * 18000 + np.random.normal(0, 15000, n2)

df_sales_corr = pd.DataFrame({
    "experience_yrs":  np.abs(exp_col).round(1),
    "calls_per_month": np.abs(calls_col).round(0).astype(int),
    "proposals_sent":  np.abs(props_col).round(0).astype(int),
    "deals_closed":    np.abs(closed_col).round(0).astype(int),
    "revenue":         np.abs(rev_col).round(0).astype(int),
})


# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — OUTLIER DETECTION WITH THE IQR METHOD
# ══════════════════════════════════════════════════════════════
#
#  The IQR method detects outliers without assuming a specific distribution.
#
#  Steps:
#    1. Q1 = 25th percentile
#    2. Q3 = 75th percentile
#    3. IQR = Q3 - Q1
#    4. Lower fence = Q1 - 1.5 * IQR
#    5. Upper fence = Q3 + 1.5 * IQR
#    6. Values outside the fences are flagged as outliers
#
#  Why IQR instead of std-based methods?
#    - Robust to extreme values (std is inflated by the very outliers you seek)
#    - Does not assume normality
#    - Same logic used by matplotlib and seaborn boxplots
#
# EXAMPLE ──────────────────────────────────────────────────────

def detect_outliers_iqr(series, multiplier=1.5):
    """Return (is_outlier_mask, lower_fence, upper_fence)."""
    q1  = series.quantile(0.25)
    q3  = series.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - multiplier * iqr
    upper = q3 + multiplier * iqr
    is_outlier = (series < lower) | (series > upper)
    return is_outlier, lower, upper

col_data = df[target_col].dropna()
is_outlier, lower, upper = detect_outliers_iqr(col_data)

print(f"\n=== OUTLIER DETECTION ({target_col}) ===")
print(f"IQR fences: lower={lower:.2f}, upper={upper:.2f}")
print(f"Outliers:   {is_outlier.sum()} ({is_outlier.mean()*100:.1f}%)")

# Box plot with fence lines + histogram highlighting outliers
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].boxplot(col_data, patch_artist=True,
                boxprops={"facecolor": "lightsteelblue"},
                flierprops={"marker": "o", "color": "crimson", "alpha": 0.5, "markersize": 5})
axes[0].axhline(upper, color="crimson", linestyle="--", linewidth=1.5, label=f"Upper: {upper:.0f}")
axes[0].axhline(lower, color="crimson", linestyle="--", linewidth=1.5, label=f"Lower: {lower:.0f}")
axes[0].set_title(f"{target_col} Box Plot with Fences")
axes[0].legend()

axes[1].hist(col_data[~is_outlier], bins=30, color="steelblue", alpha=0.8, label="Normal")
axes[1].hist(col_data[is_outlier],  bins=10, color="crimson",   alpha=0.8, label="Outliers")
axes[1].axvline(upper, color="darkred", linestyle="--", linewidth=1.5)
axes[1].axvline(lower, color="darkred", linestyle="--", linewidth=1.5)
axes[1].set_title(f"{target_col} — Outlier Highlight")
axes[1].set_xlabel(target_col)
axes[1].legend()

plt.suptitle("IQR Outlier Detection", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.show()

df_clean = df[df[target_col].notna() & ~is_outlier.reindex(df.index, fill_value=False)]
print(f"\nRows after removing {target_col} outliers: {len(df_clean)} (was {len(df)})")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
#
#  Write a function called outlier_report(df, columns) that:
#    1. Accepts a DataFrame and list of column names
#    2. For each column, calls detect_outliers_iqr()
#    3. Prints a formatted table:
#         Column          | Count | Pct   | Lower  | Upper
#         lead_time       |   XX  |  X.X% | XX.XX  | XX.XX
#    4. Returns a dict: {col: {"count": n, "pct": p, "lower": l, "upper": u}}
#
#  Call it with the first 4 numeric columns in df.
#  Then print which column has the most outliers.
#
#  Expected output:
#      Column                | Count | Pct   | Lower  | Upper
#      <col1>                |    X  |  X.X% | XX.XX  | XX.XX
#      ...
#      Column with most outliers: <name>
#
