# ══════════════════════════════════════════════════════════════
#  WEEK 5  |  DAY 6  |  WEEKLY PROJECT — SALES DASHBOARD
# ══════════════════════════════════════════════════════════════
#
#  PROJECT GOAL
#  ────────────
#  Create a four-chart sales dashboard combining line, bar, pie,
#  and scatter plots — assembled into a single saved figure and
#  accompanied by a printed text summary.
#
#  SKILLS PRACTICED
#  ─────────────────
#  - Generating and working with a Pandas DataFrame
#  - matplotlib line, bar, pie, and scatter charts
#  - Subplots and figure layout (plt.subplots)
#  - Titles, axis labels, and legends
#  - Saving figures to a PNG file
#  - Groupby and aggregation for charting
#  - Finding min/max values for text summaries
#
#  TIME:  ~45-60 minutes
#
# ══════════════════════════════════════════════════════════════


# ── SETUP — provided by teacher, do not change ────────────────

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

np.random.seed(7)

months   = list(range(1, 13))
products = ["Laptop Pro", "Wireless Mouse", "USB Hub"]

# Generate 12 months × 3 products of unit sales (seasonality baked in)
seasonal = np.array([0.8, 0.75, 0.9, 1.0, 1.05, 1.1, 1.15, 1.2, 1.1, 1.0, 1.3, 1.5])
unit_prices = {"Laptop Pro": 1299.99, "Wireless Mouse": 49.99, "USB Hub": 34.99}

data = []
for month_idx, month in enumerate(months):
    for product in products:
        base_units = {"Laptop Pro": 30, "Wireless Mouse": 200, "USB Hub": 150}[product]
        units = int(base_units * seasonal[month_idx] * (1 + np.random.normal(0, 0.08)))
        revenue = round(units * unit_prices[product], 2)
        data.append({"month": month, "product": product, "units": units, "revenue": revenue})

df = pd.DataFrame(data)
print("Sales data ready:", df.shape)
print(df.head(6))

this_file      = os.path.dirname(__file__)
dashboard_path = os.path.join(this_file, "sales_dashboard.png")


# ══════════════════════════════════════════════════════════════
#  TASK 1 — Line Chart: Monthly Total Revenue
# ══════════════════════════════════════════════════════════════
#  Group df by "month" and sum "revenue" to get total revenue
#  per month across all three products.
#
#  Create a line chart (plt.figure, then plt.plot) showing total
#  revenue on the y-axis and month number (1–12) on the x-axis.
#  Requirements:
#    - Title: "Monthly Total Revenue"
#    - X label: "Month"
#    - Y label: "Revenue ($)"
#    - Use markers=True (marker="o")
#    - Grid on
#  Save the figure as "task1_line.png" in the same folder as this file.
#  Print "Task 1 saved." after saving.
#
#  Expected output:
#    Task 1 saved.
#




# ══════════════════════════════════════════════════════════════
#  TASK 2 — Bar Chart: Annual Revenue per Product
# ══════════════════════════════════════════════════════════════
#  Group df by "product" and sum "revenue" to get total annual
#  revenue per product.  Sort the result from highest to lowest.
#
#  Create a bar chart showing each product's annual revenue.
#  Requirements:
#    - Title: "Annual Revenue by Product"
#    - X label: "Product"
#    - Y label: "Total Revenue ($)"
#    - Bar color: "steelblue"
#    - Rotate x-axis tick labels 15 degrees
#  Save as "task2_bar.png".
#  Print "Task 2 saved." after saving.
#
#  Expected output:
#    Task 2 saved.
#




# ══════════════════════════════════════════════════════════════
#  TASK 3 — Pie Chart: Market Share per Product
# ══════════════════════════════════════════════════════════════
#  Use the annual revenue per product from Task 2 (already
#  grouped and summed).
#
#  Create a pie chart showing each product's share of total revenue.
#  Requirements:
#    - Title: "Product Market Share"
#    - Show percentage labels with 1 decimal place (autopct="%1.1f%%")
#    - startangle=90
#  Save as "task3_pie.png".
#  Print "Task 3 saved." after saving.
#
#  Expected output:
#    Task 3 saved.
#




# ══════════════════════════════════════════════════════════════
#  TASK 4 — Scatter Plot: Month vs Total Revenue
# ══════════════════════════════════════════════════════════════
#  Use the monthly totals computed in Task 1.
#
#  Create a scatter plot with month number on the x-axis and total
#  revenue on the y-axis to visualise seasonality.
#  Requirements:
#    - Title: "Seasonality: Month vs Revenue"
#    - X label: "Month"
#    - Y label: "Revenue ($)"
#    - marker color: "darkorange"
#    - marker size (s): 80
#    - Grid on
#  Save as "task4_scatter.png".
#  Print "Task 4 saved." after saving.
#
#  Expected output:
#    Task 4 saved.
#




# ══════════════════════════════════════════════════════════════
#  TASK 5 — 2x2 Dashboard Subplot
# ══════════════════════════════════════════════════════════════
#  Combine all four charts into a single figure using:
#    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
#
#  Top-left  (axes[0,0]) : line chart — monthly total revenue
#  Top-right (axes[0,1]) : bar chart  — annual revenue per product
#  Bottom-left  (axes[1,0]) : pie chart   — market share
#  Bottom-right (axes[1,1]) : scatter     — month vs revenue
#
#  Add a figure-level title:
#    fig.suptitle("Annual Sales Dashboard", fontsize=16, fontweight="bold")
#
#  Use fig.tight_layout() before saving.
#  Save the combined figure to dashboard_path (defined in setup).
#  Print the full path after saving.
#
#  Expected output:
#    Dashboard saved to: <path>/sales_dashboard.png
#




# ══════════════════════════════════════════════════════════════
#  TASK 6 — Text Summary
# ══════════════════════════════════════════════════════════════
#  Using the monthly totals and annual product totals computed
#  in previous tasks, print a formatted text summary.
#
#  You need to find:
#    - The best month (highest total revenue) and its revenue
#    - The worst month (lowest total revenue) and its revenue
#    - The best product (highest annual revenue) and its revenue
#    - Total annual revenue (sum of all monthly totals)
#
#  Print in exactly this format (values will vary):
#    ── Annual Sales Summary ──
#    Best month    : Month 12  ($74,250.12)
#    Worst month   : Month 2   ($45,110.34)
#    Best product  : Laptop Pro ($468,200.78)
#    Total revenue : $583,450.00
#
#  Expected output: see format above with your computed values.
#


