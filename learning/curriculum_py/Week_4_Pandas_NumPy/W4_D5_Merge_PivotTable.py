# ══════════════════════════════════════════════════════════════
#  WEEK 4  |  DAY 5  |  MERGE AND PIVOT TABLES
# ══════════════════════════════════════════════════════════════
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Combine DataFrames using pd.merge() with inner, left, and right joins
#  2. Stack DataFrames vertically using pd.concat()
#  3. Build pivot tables with pd.pivot_table() for cross-tabulation analysis
#
#  TIME:  ~30-35 minutes
#
#  YOUTUBE
#  ───────
#  Search: "pandas merge join DataFrames tutorial"
#  Search: "pandas pivot_table tutorial"
# ══════════════════════════════════════════════════════════════

import pandas as pd
import numpy as np
import os

# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — pd.merge() — INNER, LEFT, RIGHT JOIN
# ══════════════════════════════════════════════════════════════
# pd.merge() combines two DataFrames based on a shared key column.
# This mirrors SQL JOIN operations.
#
# JOIN TYPES:
#   "inner"  -- only rows where the key exists IN BOTH tables
#   "left"   -- all rows from the LEFT table; matched rows from right (NaN if no match)
#   "right"  -- all rows from the RIGHT table; matched rows from left
#   "outer"  -- all rows from BOTH tables (NaN where no match)
#
# Syntax:
#   pd.merge(left_df, right_df, on="key_column", how="inner")
#   pd.merge(left, right, left_on="left_col", right_on="right_col", how="left")

# EXAMPLE ──────────────────────────────────────────────────────
# --- Sample data: customers and their orders ---
customers = pd.DataFrame({
    "customer_id": [1, 2, 3, 4, 5],
    "name":        ["Alice Ng", "Bob Chen", "Carol Diaz", "Dave Park", "Eve Torres"],
    "region":      ["West",     "East",     "West",        "Central",   "East"],
})

orders = pd.DataFrame({
    "order_id":    ["O-001", "O-002", "O-003", "O-004", "O-005", "O-006"],
    "customer_id": [1,        2,        1,        3,        2,        7],    # 7 has no customer record
    "amount":      [1200,     850,      3400,     700,      1900,     500],
    "product":     ["Laptop", "Mouse",  "Server", "Keyboard","Monitor","Cable"],
})

print("=== Customers ===")
print(customers)
print("\n=== Orders ===")
print(orders)

# INNER JOIN: only customers who have placed orders
inner_result = pd.merge(customers, orders, on="customer_id", how="inner")
print("\n=== INNER JOIN (both must match) ===")
print(inner_result)
print(f"Rows: {len(inner_result)}")  # 5 orders matched to 3 distinct customers

# LEFT JOIN: all customers, even those with no orders
left_result = pd.merge(customers, orders, on="customer_id", how="left")
print("\n=== LEFT JOIN (all customers) ===")
print(left_result)
# Eve Torres (id=5) and Dave Park (id=4) have no orders -> NaN in order columns

# RIGHT JOIN: all orders, even those with no matching customer
right_result = pd.merge(customers, orders, on="customer_id", how="right")
print("\n=== RIGHT JOIN (all orders) ===")
print(right_result)
# Order O-006 (customer_id=7) has no matching customer -> NaN in customer columns

# Merging on different column names
products = pd.DataFrame({
    "sku":         ["P100", "P101", "P102"],
    "product_name": ["Laptop", "Mouse", "Monitor"],
    "cost":        [600,     15,      180],
})

# orders has "product" column, products has "product_name"
orders_with_cost = pd.merge(
    orders,
    products,
    left_on="product",
    right_on="product_name",
    how="left",
)
orders_with_cost["margin"] = orders_with_cost["amount"] - orders_with_cost["cost"]
print("\n=== Orders with Cost and Margin ===")
print(orders_with_cost[["order_id", "product", "amount", "cost", "margin"]])


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
# Merge the sales_reps and sales_results DataFrames to produce a combined report.
#
# Use a LEFT join on rep_id.
# Print the full merged result.
# Then print: total revenue per region (group by region, sum revenue).
#
# Expected output:
#   rep_name    region   quota   revenue  pct_of_quota
#   Tom Reyes   West     200000  185000   92.5
#   Priya Mehta East     300000  312000   104.0
#   Sara Jones  Central  150000  154000   102.7
#   Omar Nasser East     150000   98000   65.3
#   Lena Kim    West     175000  142000   81.1
#   (Dave Lee has no sales data -> revenue NaN)
#
#   Revenue by region:
#   Central     154000
#   East        410000
#   West        327000

sales_reps = pd.DataFrame({
    "rep_id":   [101, 102, 103, 104, 105, 106],
    "rep_name": ["Tom Reyes", "Priya Mehta", "Sara Jones",
                 "Omar Nasser", "Lena Kim", "Dave Lee"],
    "region":   ["West", "East", "Central", "East", "West", "Central"],
    "quota":    [200000, 300000, 150000, 150000, 175000, 125000],
})

sales_results = pd.DataFrame({
    "rep_id":  [101, 102, 103, 104, 105],
    "revenue": [185000, 312000, 154000, 98000, 142000],
})




# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — pd.concat() FOR STACKING DATAFRAMES
# ══════════════════════════════════════════════════════════════
# pd.concat() stacks DataFrames along an axis.
# Most commonly used to combine datasets that have the same columns
# (e.g. monthly files, regional exports, paginated API responses).
#
# Syntax:
#   pd.concat([df1, df2, df3])             -- stack vertically (axis=0, default)
#   pd.concat([df1, df2], axis=1)          -- join side by side (axis=1)
#   pd.concat([df1, df2], ignore_index=True)  -- reset index to 0, 1, 2...
#   pd.concat([df1, df2], keys=["q1","q2"])   -- add multi-level index

# EXAMPLE ──────────────────────────────────────────────────────
# Quarterly sales files that need to be combined
q1_sales = pd.DataFrame({
    "date":    ["2024-01-15", "2024-02-22", "2024-03-08"],
    "rep":     ["Tom Reyes",  "Priya Mehta", "Sara Jones"],
    "revenue": [45000,         62000,          38000],
    "quarter": ["Q1", "Q1", "Q1"],
})

q2_sales = pd.DataFrame({
    "date":    ["2024-04-10", "2024-05-18", "2024-06-25"],
    "rep":     ["Tom Reyes",  "Lena Kim",   "Priya Mehta"],
    "revenue": [52000,         41000,         71000],
    "quarter": ["Q2", "Q2", "Q2"],
})

q3_sales = pd.DataFrame({
    "date":    ["2024-07-05", "2024-08-14", "2024-09-30"],
    "rep":     ["Sara Jones", "Tom Reyes",  "Omar Nasser"],
    "revenue": [49000,         58000,         32000],
    "quarter": ["Q3", "Q3", "Q3"],
})

# Combine all three quarters into one DataFrame
full_year = pd.concat([q1_sales, q2_sales, q3_sales], ignore_index=True)
print("\n=== Full Year Sales (concat) ===")
print(full_year)
print(f"\nTotal rows: {len(full_year)}")

# Total revenue per quarter
by_quarter = full_year.groupby("quarter")["revenue"].sum().reset_index()
print("\nRevenue by quarter:")
print(by_quarter)

# Combine with keys to track source
full_keyed = pd.concat(
    [q1_sales, q2_sales, q3_sales],
    keys=["Q1", "Q2", "Q3"],
    names=["quarter_label", "original_index"],
)
print("\nWith source keys:")
print(full_keyed)


# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
# Three regional managers submitted their monthly reports as separate DataFrames.
# Combine them into one and answer:
#   1. How many total rows?
#   2. What is total revenue per region?
#   3. Which rep had the single highest revenue?
#
# Expected output:
#   Total rows: 9
#   Revenue by region:
#   ...
#   Top earner: <name> ($<amount>)

west_report = pd.DataFrame({
    "rep":     ["Tom Reyes", "Lena Kim",   "Beth Morris"],
    "region":  ["West", "West", "West"],
    "month":   ["Jan", "Jan", "Jan"],
    "revenue": [45000, 38000, 52000],
})

east_report = pd.DataFrame({
    "rep":     ["Priya Mehta", "Omar Nasser", "Chen Liu"],
    "region":  ["East", "East", "East"],
    "month":   ["Jan", "Jan", "Jan"],
    "revenue": [71000, 31000, 58000],
})

central_report = pd.DataFrame({
    "rep":     ["Sara Jones", "Mike Brown", "Ana Costa"],
    "region":  ["Central", "Central", "Central"],
    "month":   ["Jan", "Jan", "Jan"],
    "revenue": [49000, 36000, 44000],
})




# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — pd.pivot_table()
# ══════════════════════════════════════════════════════════════
# A pivot table cross-tabulates data: rows are one category,
# columns are another, values are aggregated numbers.
# This is exactly what Excel's PivotTable feature does.
#
# Syntax:
#   pd.pivot_table(
#       df,
#       values="amount_col",      -- which column to aggregate
#       index="row_category",     -- what becomes the rows
#       columns="col_category",   -- what becomes the columns
#       aggfunc="sum",            -- aggregation: sum, mean, count, etc.
#       fill_value=0,             -- replace NaN with 0
#       margins=True,             -- add row/column totals
#   )

# EXAMPLE ──────────────────────────────────────────────────────
# Load Titanic for pivot practice
titanic_path = os.path.join(os.path.dirname(__file__), "..", "datasets", "titanic_train.xlsx")

try:
    df_titanic = pd.read_excel(titanic_path)
except FileNotFoundError:
    # Inline fallback
    np.random.seed(99)
    n = 200
    df_titanic = pd.DataFrame({
        "Survived": np.random.choice([0, 1], n),
        "Pclass":   np.random.choice([1, 2, 3], n, p=[0.25, 0.25, 0.50]),
        "Sex":      np.random.choice(["male", "female"], n, p=[0.65, 0.35]),
        "Age":      np.random.uniform(1, 70, n).round(0),
        "Fare":     np.random.uniform(5, 300, n).round(2),
        "Embarked": np.random.choice(["S", "C", "Q"], n, p=[0.72, 0.19, 0.09]),
    })

# Pivot: survival rate by Pclass and Sex
pivot_survival = pd.pivot_table(
    df_titanic,
    values="Survived",
    index="Pclass",
    columns="Sex",
    aggfunc="mean",
    fill_value=0,
).round(2)

print("\n=== Survival Rate by Class and Gender ===")
print(pivot_survival)

# Pivot: average fare by class and embarkation port
pivot_fare = pd.pivot_table(
    df_titanic,
    values="Fare",
    index="Pclass",
    columns="Embarked",
    aggfunc="mean",
    fill_value=0,
    margins=True,      # adds "All" row and column
    margins_name="Total",
).round(2)

print("\n=== Average Fare by Class and Port ===")
print(pivot_fare)

# Count of passengers: class vs sex
pivot_count = pd.pivot_table(
    df_titanic,
    values="PassengerId" if "PassengerId" in df_titanic.columns else "Survived",
    index="Pclass",
    columns="Sex",
    aggfunc="count",
    fill_value=0,
    margins=True,
)
print("\n=== Passenger Count by Class and Sex ===")
print(pivot_count)


# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
# Use the full_year DataFrame created in Concept 2 (three quarterly periods,
# three reps per quarter) to build a pivot table.
#
# Task A: Create a pivot table with:
#   rows = rep
#   columns = quarter
#   values = revenue
#   aggfunc = sum
#   fill_value = 0
#   margins = True
# Print it.
#
# Task B: From the pivot, identify which rep had the highest total revenue
# across all three quarters. Print: "Top rep: <name> ($<total>)"
#
# Expected output:
#   quarter  Q1     Q2     Q3     All
#   rep
#   Lena Kim      0  41000      0   41000
#   Omar Nasser   0      0  32000   32000
#   Priya Mehta  62000  71000      0  133000
#   Sara Jones   38000      0  49000   87000
#   Tom Reyes    45000  52000  58000  155000
#   All         145000 164000 139000  448000
#
#   Top rep: Tom Reyes ($155000)


