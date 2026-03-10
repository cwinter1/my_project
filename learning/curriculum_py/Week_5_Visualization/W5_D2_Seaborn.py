# ══════════════════════════════════════════════════════════════
#  WEEK 5  |  DAY 2  |  SEABORN: STATISTICAL VISUALIZATION
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Create bar and histogram plots with seaborn's high-level API
#  2. Create box plots and scatter plots to explore distributions
#  3. Build a correlation heatmap and apply seaborn themes
#
#  TIME:  ~30 minutes  (3 concepts × 10 min each)
#
#  YOUTUBE
#  ───────
#  Search: "seaborn tutorial Python barplot histplot"
#  Search: "seaborn heatmap correlation matrix tutorial"
#
# ══════════════════════════════════════════════════════════════

# Install if needed:  pip install seaborn matplotlib pandas openpyxl

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

titanic_path = os.path.join(os.path.dirname(__file__), "..", "datasets", "titanic_train.xlsx")

try:
    df = pd.read_excel(titanic_path)
    print("Titanic loaded:", df.shape)
except FileNotFoundError:
    print("titanic_train.xlsx not found. Using inline demo data.")
    np.random.seed(42)
    n = 300
    df = pd.DataFrame({
        "Survived": np.random.choice([0, 1], n, p=[0.62, 0.38]),
        "Pclass":   np.random.choice([1, 2, 3], n, p=[0.24, 0.21, 0.55]),
        "Sex":      np.random.choice(["male", "female"], n, p=[0.65, 0.35]),
        "Age":      np.abs(np.random.normal(29, 14, n)).clip(1, 75).round(1),
        "SibSp":    np.random.choice(range(0, 6), n, p=[0.68, 0.23, 0.05, 0.02, 0.01, 0.01]),
        "Fare":     np.abs(np.random.exponential(32, n)).round(2),
        "Embarked": np.random.choice(["S", "C", "Q"], n, p=[0.72, 0.19, 0.09]),
    })
    df.insert(0, "PassengerId", range(1, n + 1))


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — sns.barplot AND sns.histplot
# ══════════════════════════════════════════════════════════════
#
#  Seaborn builds on matplotlib and integrates directly with DataFrames.
#  It produces polished charts with less code.
#
#  sns.barplot(data=df, x="category", y="value")
#    computes the MEAN of y for each category
#    automatically adds 95% confidence interval error bars
#
#  sns.histplot(data=df, x="column", bins=20)
#    histogram of a continuous variable
#    kde=True overlays a smoothed density curve
#
#  Parameters common to most seaborn functions:
#    data=df        the DataFrame to use
#    x=, y=         which columns to plot
#    hue=           split by a third variable (adds color)
#    palette=       color scheme: "viridis", "Set2", "muted", etc.
#    ax=            the matplotlib axes object to draw on
#
# EXAMPLE ──────────────────────────────────────────────────────

sns.set_theme(style="whitegrid", palette="muted")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Barplot: mean survival rate by passenger class, split by sex
sns.barplot(
    data=df, x="Pclass", y="Survived", hue="Sex",
    palette="Set2", ax=axes[0], capsize=0.05,
)
axes[0].set_title("Survival Rate by Class and Gender", fontsize=13, fontweight="bold")
axes[0].set_xlabel("Passenger Class")
axes[0].set_ylabel("Survival Rate (mean)")
axes[0].set_ylim(0, 1)
axes[0].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.0%}"))

# Histplot: age distribution split by survival
sns.histplot(
    data=df, x="Age", hue="Survived", bins=25,
    kde=True, palette=["crimson", "steelblue"], alpha=0.6, ax=axes[1],
)
axes[1].set_title("Age Distribution by Survival", fontsize=13, fontweight="bold")
axes[1].set_xlabel("Age")
axes[1].set_ylabel("Count")
legend = axes[1].get_legend()
if legend:
    legend.set_title("Survived")

plt.tight_layout()
plt.show()


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
#
#  Create a 1x2 figure using plt.subplots(1, 2, figsize=(14, 5)).
#
#  Left panel: sns.barplot showing average Fare by Pclass.
#    Use order=[1, 2, 3].
#    Title: "Average Fare by Class"
#
#  Right panel: sns.histplot showing Fare distribution for each Pclass.
#    Use hue="Pclass", kde=True, bins=30.
#    Title: "Fare Distribution by Class"
#
#  Call plt.tight_layout() then plt.show().
#
#  Expected output:
#      Two-panel seaborn chart showing fare patterns by passenger class
#






# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — sns.boxplot AND sns.scatterplot
# ══════════════════════════════════════════════════════════════
#
#  Box plots show the distribution of a numeric variable:
#    Median      center line inside the box
#    IQR box     Q1 to Q3 (middle 50% of data)
#    Whiskers    extend to 1.5 * IQR from box edges
#    Outliers    individual dots beyond the whiskers
#
#  sns.scatterplot supports hue, size, and style for multi-dimensional display.
#
#  sns.boxplot(data=df, x="category", y="value", hue="group")
#  sns.scatterplot(data=df, x="col_a", y="col_b", hue="label", alpha=0.6)
#
# EXAMPLE ──────────────────────────────────────────────────────

# Boxplot: fare distribution by class and sex
plt.figure(figsize=(10, 6))
sns.boxplot(
    data=df, x="Pclass", y="Fare", hue="Sex", palette="pastel",
    flierprops={"marker": "o", "markersize": 4, "alpha": 0.5},
)
plt.title("Fare Distribution by Class and Gender", fontsize=13, fontweight="bold")
plt.xlabel("Passenger Class")
plt.ylabel("Fare (GBP)")
plt.legend(title="Sex")
plt.tight_layout()
plt.show()

# Scatterplot: age vs fare colored by survival outcome
df_scatter = df[["Age", "Fare", "Survived", "Pclass"]].dropna().copy()
df_scatter["Survived_Label"] = df_scatter["Survived"].map(
    {0: "Did not survive", 1: "Survived"}
)

plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=df_scatter, x="Age", y="Fare",
    hue="Survived_Label", style="Pclass",
    palette=["crimson", "steelblue"], alpha=0.6, s=60,
)
plt.title("Age vs Fare: Survival Outcome by Class", fontsize=13, fontweight="bold")
plt.xlabel("Age (years)")
plt.ylabel("Fare (GBP)")
plt.legend(title="Outcome / Class", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()
plt.show()


# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
#
#  Create a 1x2 figure using plt.subplots(1, 2, figsize=(14, 5)).
#
#  Left panel: sns.boxplot of Age by Pclass.
#    Use hue="Survived", palette="Set3".
#    Title: "Age by Class and Survival"
#
#  Right panel: sns.scatterplot of Age vs SibSp (siblings/spouses aboard).
#    Use hue="Survived", palette=["crimson", "steelblue"], alpha=0.5.
#    Title: "Age vs Siblings by Survival"
#
#  Call plt.tight_layout() then plt.show().
#
#  Expected output:
#      Two-panel figure showing age patterns across class and family groups
#


# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — sns.heatmap FOR CORRELATION, set_theme()
# ══════════════════════════════════════════════════════════════
#
#  A correlation matrix shows pairwise linear correlations.
#  Values range from -1 (perfect negative) to +1 (perfect positive).
#  Near 0 means little linear relationship.
#
#  df.corr()   computes Pearson correlation between all numeric columns
#
#  sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1)
#    annot=True    show the value inside each cell
#    cmap          color map: "coolwarm" (red=positive, blue=negative)
#    fmt=".2f"     format cell numbers to 2 decimal places
#    square=True   make cells square
#    linewidths    spacing between cells
#
#  sns.set_theme() controls the global look of all seaborn plots:
#    style=   "whitegrid", "darkgrid", "white", "dark", "ticks"
#    palette= "deep", "muted", "pastel", "bright", "colorblind"
#    context= "paper", "notebook", "talk", "poster"
#
# EXAMPLE ──────────────────────────────────────────────────────

numeric_cols  = ["Survived", "Pclass", "Age", "SibSp", "Fare"]
df_numeric    = df[numeric_cols].dropna()
corr_matrix   = df_numeric.corr()

print("\n=== Correlation Matrix ===")
print(corr_matrix.round(2))

plt.figure(figsize=(8, 6))
sns.heatmap(
    corr_matrix, annot=True, cmap="coolwarm",
    vmin=-1, vmax=1, square=True, fmt=".2f",
    linewidths=0.5, cbar_kws={"shrink": 0.8},
)
plt.title("Titanic Dataset — Correlation Matrix", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.show()

# Interpretation notes printed for reference:
print("Pclass vs Fare:     strong negative (~-0.55) — lower class = lower fare")
print("Pclass vs Survived: negative (~-0.34) — higher class number = less likely to survive")
print("Age vs Survived:    slight negative (~-0.07) — weak relationship")

# Show a different theme for comparison
sns.set_theme(style="darkgrid", context="talk", palette="colorblind")
plt.figure(figsize=(10, 5))
sns.histplot(data=df, x="Age", bins=20, kde=True, color="steelblue")
plt.title("Age Distribution (darkgrid theme, talk context)")
plt.tight_layout()
plt.show()

# Reset to neutral theme
sns.set_theme(style="whitegrid")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
#
#  Using df_sales below:
#    1. Compute the correlation matrix with df_sales.corr()
#    2. Plot a heatmap with annot=True, cmap="YlOrRd", vmin=0, vmax=1
#    3. Title: "Sales Metrics — Correlation Matrix"
#    4. Call plt.tight_layout() then plt.show()
#    5. Print two observations about what the correlations tell you
#
#  Expected output:
#      Heatmap showing strong positive correlations across the sales funnel
#

np.random.seed(12)
n = 100
experience  = np.random.uniform(1, 15, n)
calls_made  = experience * 8 + np.random.normal(0, 15, n)
meetings    = calls_made * 0.2 + np.random.normal(0, 5, n)
deals       = meetings * 0.3 + np.random.normal(0, 2, n)
revenue_col = deals * 15000 + np.random.normal(0, 20000, n)

df_sales = pd.DataFrame({
    "experience_yrs": experience.round(1),
    "calls_made":     np.abs(calls_made).round(0).astype(int),
    "meetings":       np.abs(meetings).round(0).astype(int),
    "deals_closed":   np.abs(deals).round(0).astype(int),
    "revenue":        np.abs(revenue_col).round(0).astype(int),
})
