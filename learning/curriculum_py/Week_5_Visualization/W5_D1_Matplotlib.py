# ══════════════════════════════════════════════════════════════
#  WEEK 5  |  DAY 1  |  MATPLOTLIB: PLOTS, CHARTS, FORMATTING
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Create line plots and bar charts using plt.plot and plt.bar
#  2. Create histograms and scatter plots using plt.hist and plt.scatter
#  3. Format charts with titles, labels, legends, figsize, and subplots
#
#  TIME:  ~30 minutes  (3 concepts × 10 min each)
#
#  YOUTUBE
#  ───────
#  Search: "matplotlib tutorial Python line plot bar chart"
#  Search: "matplotlib formatting labels title legend figsize"
#
# ══════════════════════════════════════════════════════════════

# Install if needed:  pip install matplotlib numpy

import matplotlib.pyplot as plt
import numpy as np

# All data is defined inline — no file needed.

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

revenue_2023 = [82000, 78000, 91000, 95000, 88000, 102000,
                115000, 109000, 121000, 118000, 130000, 145000]
revenue_2024 = [91000, 85000, 98000, 107000, 102000, 118000,
                128000, 122000, 139000, 142000, 155000, 168000]
expenses_2024 = [65000, 63000, 71000, 75000, 72000, 80000,
                 88000, 85000, 91000, 92000, 98000, 104000]

departments = ["Sales", "Engineering", "Finance", "Operations", "HR"]
headcount   = [18, 25, 8, 12, 5]


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — LINE PLOT AND BAR CHART (plt.plot, plt.bar)
# ══════════════════════════════════════════════════════════════
#
#  Line plots show trends over time.
#  Bar charts compare values across categories.
#
#  plt.plot(x, y)             line plot
#  plt.bar(x, height)         vertical bar chart
#  plt.barh(y, width)         horizontal bar chart
#
#  Common style parameters:
#    color="steelblue"        fill or line color
#    linewidth=2              line thickness (plot only)
#    edgecolor="black"        bar outline color
#    alpha=0.8                transparency (0 = invisible, 1 = solid)
#    label="Series A"         used by plt.legend()
#    marker="o"               dot marker on line plots
#    linestyle="--"           dashed line
#
# EXAMPLE ──────────────────────────────────────────────────────

# Line plot: two-year revenue trend
plt.figure(figsize=(12, 5))
plt.plot(months, revenue_2023, color="steelblue", linewidth=2, marker="o",
         label="2023 Revenue")
plt.plot(months, revenue_2024, color="darkorange", linewidth=2, marker="s",
         label="2024 Revenue")
plt.plot(months, expenses_2024, color="crimson", linewidth=1.5, linestyle="--",
         marker="^", label="2024 Expenses", alpha=0.8)
plt.title("Monthly Revenue and Expenses 2023-2024", fontsize=14, fontweight="bold")
plt.xlabel("Month")
plt.ylabel("Amount (USD)")
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()

# Bar chart: headcount by department with value labels
plt.figure(figsize=(10, 6))
colors = ["steelblue", "darkorange", "seagreen", "crimson", "purple"]
bars = plt.bar(departments, headcount, color=colors, edgecolor="white", width=0.6)
for bar, value in zip(bars, headcount):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
             str(value), ha="center", va="bottom", fontsize=11, fontweight="bold")
plt.title("Headcount by Department", fontsize=14, fontweight="bold")
plt.xlabel("Department")
plt.ylabel("Number of Employees")
plt.ylim(0, max(headcount) * 1.2)
plt.tight_layout()
plt.show()


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
#
#  Create a grouped bar chart comparing Q1 vs Q2 revenue for 5 regions.
#  Each region should show two bars side by side.
#
#  Use np.arange to compute bar positions, then offset each group:
#    x = np.arange(len(regions))
#    plt.bar(x - 0.2, q1, width=0.35, label="Q1", color="steelblue")
#    plt.bar(x + 0.2, q2, width=0.35, label="Q2", color="darkorange")
#    plt.xticks(x, regions)
#
#  Add: title "Q1 vs Q2 Revenue by Region", x/y labels, legend,
#       grid on y-axis, tight_layout, and plt.show().
#
#  Expected output:
#      Grouped bar chart with 10 bars (2 per region), legend showing Q1/Q2
#

q1      = [142000, 185000, 98000, 115000, 77000]
q2      = [155000, 211000, 107000, 128000, 89000]
regions = ["West", "East", "Central", "North", "South"]




# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — HISTOGRAM AND SCATTER PLOT (plt.hist, plt.scatter)
# ══════════════════════════════════════════════════════════════
#
#  Histograms show the distribution of one numeric variable.
#  Scatter plots show the relationship between two numeric variables.
#
#  plt.hist(data, bins=20)
#    bins     controls how many bars are drawn
#    density  if True, normalizes area to 1 (shows probability)
#
#  plt.scatter(x, y, s=60, c="steelblue", alpha=0.6)
#    s        marker size
#    c        color (can be a list of values mapped to a colormap)
#
#  plt.axvline(x_val)    draw a vertical line at a specific x value
#    useful for marking mean or median on a histogram
#
#  np.polyfit(x, y, 1)  fit a linear trend line
#  np.poly1d(z)(x_line) evaluate the trend line at new x points
#
# EXAMPLE ──────────────────────────────────────────────────────

np.random.seed(42)

# Simulated employee salaries from three seniority groups
salaries = np.concatenate([
    np.random.normal(72000, 8000, 80),    # junior
    np.random.normal(95000, 12000, 50),   # mid-level
    np.random.normal(130000, 15000, 20),  # senior
])

# Sales rep experience vs revenue
experience_years = np.random.uniform(1, 15, 40)
revenue = experience_years * 18000 + np.random.normal(0, 25000, 40) + 60000

# Histogram: salary distribution with mean and median lines
plt.figure(figsize=(10, 5))
plt.hist(salaries, bins=25, color="steelblue", edgecolor="white", alpha=0.8)
plt.axvline(np.mean(salaries), color="red", linestyle="--", linewidth=2,
            label=f"Mean: ${np.mean(salaries):,.0f}")
plt.axvline(np.median(salaries), color="orange", linestyle="--", linewidth=2,
            label=f"Median: ${np.median(salaries):,.0f}")
plt.title("Employee Salary Distribution", fontsize=14, fontweight="bold")
plt.xlabel("Annual Salary (USD)")
plt.ylabel("Number of Employees")
plt.legend()
plt.tight_layout()
plt.show()

# Scatter plot: experience vs revenue with a trend line
plt.figure(figsize=(10, 6))
plt.scatter(experience_years, revenue, color="steelblue", alpha=0.7,
            s=80, edgecolors="white", linewidth=0.5)
z = np.polyfit(experience_years, revenue, 1)
p = np.poly1d(z)
x_line = np.linspace(experience_years.min(), experience_years.max(), 100)
plt.plot(x_line, p(x_line), color="crimson", linewidth=2, linestyle="--", label="Trend")
plt.title("Sales Rep Experience vs Annual Revenue", fontsize=14, fontweight="bold")
plt.xlabel("Years of Experience")
plt.ylabel("Annual Revenue (USD)")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()


# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
#
#  Create a two-panel figure using plt.subplots(1, 2, figsize=(14, 5)).
#
#  Left panel (ax1): Histogram of deal_values with 15 bins, color seagreen.
#    Add axvline for mean and median.
#    Title: "Deal Value Distribution"
#
#  Right panel (ax2): Scatter of days_in_pipeline vs deal_value.
#    color="darkorange", alpha=0.6
#    Title: "Pipeline Duration vs Deal Value"
#    X label: "Days in Pipeline", Y label: "Deal Value ($)"
#
#  Call plt.tight_layout() then plt.show().
#
#  Expected output:
#      Two-panel figure: histogram on left, scatter on right
#

np.random.seed(7)
deal_values = np.concatenate([
    np.random.normal(25000, 8000, 60),
    np.random.normal(80000, 20000, 30),
    np.random.normal(200000, 40000, 10),
])
deal_values      = np.abs(deal_values)
days_in_pipeline = deal_values / 500 + np.random.normal(0, 20, 100)
days_in_pipeline = np.abs(days_in_pipeline)




# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — FORMATTING: SUBPLOTS, TITLES, LABELS, GRID
# ══════════════════════════════════════════════════════════════
#
#  Formatting makes charts readable and presentation-ready.
#
#  Key formatting calls:
#    plt.figure(figsize=(w, h))          set canvas size in inches
#    plt.title("text", fontsize=14)      chart title
#    plt.xlabel("text")                  x-axis label
#    plt.ylabel("text")                  y-axis label
#    plt.legend(loc="upper left")        show legend
#    plt.xticks(rotation=45)             rotate x-axis tick labels
#    plt.grid(True, axis="y", alpha=0.3) gridlines
#    plt.tight_layout()                  auto-adjust spacing
#    plt.savefig("file.png", dpi=150)    save to file
#
#  Subplots — multiple charts in one figure:
#    fig, axes = plt.subplots(rows, cols, figsize=(w, h))
#    axes[row, col].plot(...)             each ax has the same methods
#    axes[row, col].set_title(...)        prefix "set_" for ax-level calls
#    fig.suptitle("Dashboard Title")      title for the whole figure
#
# EXAMPLE ──────────────────────────────────────────────────────

# 2x2 dashboard combining all chart types
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Sales Dashboard 2024", fontsize=16, fontweight="bold")

# Top-left: line chart
axes[0, 0].plot(months, revenue_2024, color="steelblue", linewidth=2, marker="o")
axes[0, 0].set_title("Monthly Revenue 2024")
axes[0, 0].set_xlabel("Month")
axes[0, 0].set_ylabel("Revenue (USD)")
axes[0, 0].tick_params(axis="x", rotation=45)
axes[0, 0].grid(axis="y", alpha=0.3)

# Top-right: bar chart
axes[0, 1].bar(departments, headcount, color="darkorange", edgecolor="white")
axes[0, 1].set_title("Headcount by Department")
axes[0, 1].set_xlabel("Department")
axes[0, 1].set_ylabel("Employees")

# Bottom-left: histogram
axes[1, 0].hist(salaries, bins=20, color="seagreen", edgecolor="white", alpha=0.8)
axes[1, 0].set_title("Salary Distribution")
axes[1, 0].set_xlabel("Salary (USD)")
axes[1, 0].set_ylabel("Count")

# Bottom-right: scatter
axes[1, 1].scatter(experience_years, revenue, color="purple", alpha=0.6, s=60)
axes[1, 1].set_title("Experience vs Revenue")
axes[1, 1].set_xlabel("Years Experience")
axes[1, 1].set_ylabel("Revenue (USD)")

plt.tight_layout()
plt.show()
print("Dashboard rendered.")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
#
#  Build a bar chart showing monthly profit (revenue minus expenses) for 2024.
#  Bars should be seagreen when profit >= 0 and crimson when negative.
#
#  Steps:
#    1. Calculate profit = [r - e for r, e in zip(revenue_2024, expenses_2024)]
#    2. Assign bar_colors: "seagreen" if p >= 0 else "crimson" for each month
#    3. Create a bar chart with those colors
#    4. Add plt.axhline(0, color="black", linewidth=1) for the zero baseline
#    5. Title: "Monthly Profit 2024", x label: "Month", y label: "Profit (USD)"
#    6. Call plt.tight_layout() then plt.show()
#
#  Expected output:
#      Bar chart with all green bars (all months are profitable in this dataset)
#
