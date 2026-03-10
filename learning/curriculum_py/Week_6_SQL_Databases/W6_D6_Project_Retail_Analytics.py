# ══════════════════════════════════════════════════════════════
#  WEEK 6  |  DAY 6  |  PROJECT — RETAIL ANALYTICS WITH SQL
# ══════════════════════════════════════════════════════════════
#
#  PROJECT GOAL
#  ────────────
#  Build a SQLite retail database from scratch, populate it with
#  sales data, answer real business questions using SQL queries,
#  and export summary results to a CSV file using Python.
#
#  SKILLS USED
#  ───────────
#  - sqlite3: connect, cursor, execute, fetchall
#  - CREATE TABLE, INSERT INTO
#  - SELECT with WHERE, GROUP BY, ORDER BY, LIMIT
#  - JOIN across multiple tables
#  - Aggregate functions: SUM, COUNT, AVG, MAX
#  - Exporting query results with the csv module
#
#  TIME:  ~45-60 minutes
#
# ══════════════════════════════════════════════════════════════

import sqlite3
import csv
import os


# ══════════════════════════════════════════════════════════════
#  PART 1 — SET UP THE DATABASE AND TABLES
# ══════════════════════════════════════════════════════════════
# We create an in-memory SQLite database (no file saved to disk).
# Two tables: products and sales.
# products  — one row per product with its name and category.
# sales     — one row per transaction with product_id, quantity, price, date.
#
# sqlite3.connect(":memory:") creates a fresh database in RAM.
# cursor.execute() runs a single SQL statement.
# conn.commit() saves pending changes.
#
# EXAMPLE ──────────────────────────────────────────────────────

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE products (
        product_id   INTEGER PRIMARY KEY,
        product_name TEXT    NOT NULL,
        category     TEXT    NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE sales (
        sale_id    INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        quantity   INTEGER NOT NULL,
        price      REAL    NOT NULL,
        sale_date  TEXT    NOT NULL,
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    )
""")

conn.commit()
print("Tables created successfully.")


# ══════════════════════════════════════════════════════════════
#  PART 2 — INSERT DATA
# ══════════════════════════════════════════════════════════════
# executemany() inserts multiple rows in one call.
# Each tuple in the list maps to one row.
#
# EXAMPLE ──────────────────────────────────────────────────────

products_data = [
    (1, "Laptop",       "Electronics"),
    (2, "Mouse",        "Electronics"),
    (3, "Desk Chair",   "Furniture"),
    (4, "Notebook",     "Stationery"),
    (5, "Headphones",   "Electronics"),
    (6, "Standing Desk","Furniture"),
    (7, "Pen Set",      "Stationery"),
    (8, "Monitor",      "Electronics"),
]

sales_data = [
    (1, 3,  1200.00, "2024-01-05"),
    (2, 10,   25.00, "2024-01-06"),
    (1, 1,  1150.00, "2024-01-07"),
    (3, 2,   350.00, "2024-01-08"),
    (4, 50,    2.50, "2024-01-09"),
    (5, 5,    80.00, "2024-01-10"),
    (6, 1,   600.00, "2024-01-11"),
    (7, 30,    1.20, "2024-01-12"),
    (8, 2,   450.00, "2024-01-13"),
    (2, 15,   25.00, "2024-01-14"),
    (1, 2,  1180.00, "2024-01-15"),
    (3, 1,   360.00, "2024-01-16"),
    (5, 8,    82.00, "2024-01-17"),
    (4, 100,   2.50, "2024-01-18"),
    (8, 3,   455.00, "2024-01-19"),
]

cursor.executemany(
    "INSERT INTO products (product_id, product_name, category) VALUES (?, ?, ?)",
    products_data
)
cursor.executemany(
    "INSERT INTO sales (product_id, quantity, price, sale_date) VALUES (?, ?, ?, ?)",
    sales_data
)
conn.commit()
print(f"Inserted {len(products_data)} products and {len(sales_data)} sales.")


# ══════════════════════════════════════════════════════════════
#  TASK 1 — TOTAL REVENUE PER CATEGORY
# ══════════════════════════════════════════════════════════════
# Write a SQL query that JOINs sales and products, then calculates
# total revenue (quantity * price) for each category.
# Sort results from highest to lowest revenue.
#
# Expected output (approximate):
#   Electronics  |  16270.0
#   Furniture    |  1310.0
#   Stationery   |  386.0
#
# --- starting data ---
# Use the existing conn and cursor objects above.
# Revenue formula: quantity * price per sale row, then SUM grouped by category.




query_revenue_by_category = """

"""




# ══════════════════════════════════════════════════════════════
#  PART 3 — QUERY: TOP SELLING PRODUCTS
# ══════════════════════════════════════════════════════════════
# To find top products by total units sold, we GROUP BY product_id,
# SUM the quantity, and ORDER BY that sum descending.
# JOIN brings in the product name from the products table.
#
# EXAMPLE ──────────────────────────────────────────────────────

cursor.execute("""
    SELECT p.product_name,
           SUM(s.quantity) AS total_units
    FROM   sales s
    JOIN   products p ON s.product_id = p.product_id
    GROUP  BY s.product_id
    ORDER  BY total_units DESC
    LIMIT  5
""")

top_products = cursor.fetchall()
print("\nTop 5 products by units sold:")
for name, units in top_products:
    print(f"  {name:<20}  {units} units")


# ══════════════════════════════════════════════════════════════
#  TASK 2 — AVERAGE SALE PRICE PER PRODUCT
# ══════════════════════════════════════════════════════════════
# Write a query that returns the average price per sale for each
# product, joined with the product name.
# Show only products where the average price is greater than 100.
# Sort alphabetically by product name.
#
# Expected output (approximate):
#   Desk Chair   |  355.0
#   Laptop       |  1176.67
#   Monitor      |  453.33
#   Standing Desk|  600.0
#
# --- starting data ---
# Use the existing conn and cursor objects above.




query_avg_price = """

"""




# ══════════════════════════════════════════════════════════════
#  PART 4 — QUERY: SALES IN A DATE RANGE
# ══════════════════════════════════════════════════════════════
# WHERE with date string comparison works in SQLite when dates are
# stored in YYYY-MM-DD format (lexicographic ordering matches chronological).
#
# EXAMPLE ──────────────────────────────────────────────────────

cursor.execute("""
    SELECT s.sale_date,
           p.product_name,
           s.quantity,
           s.price,
           (s.quantity * s.price) AS revenue
    FROM   sales s
    JOIN   products p ON s.product_id = p.product_id
    WHERE  s.sale_date BETWEEN '2024-01-10' AND '2024-01-15'
    ORDER  BY s.sale_date
""")

date_range_sales = cursor.fetchall()
print("\nSales from 2024-01-10 to 2024-01-15:")
print(f"  {'Date':<12} {'Product':<20} {'Qty':>4} {'Price':>8} {'Revenue':>10}")
for row in date_range_sales:
    date, name, qty, price, rev = row
    print(f"  {date:<12} {name:<20} {qty:>4} {price:>8.2f} {rev:>10.2f}")


# ══════════════════════════════════════════════════════════════
#  TASK 3 — EXPORT RESULTS TO CSV
# ══════════════════════════════════════════════════════════════
# Query the database for total revenue and total units per product.
# Write the results to a CSV file named "retail_summary.csv"
# in the same folder as this script.
#
# The CSV should have these columns:
#   product_name, category, total_units, total_revenue
#
# Expected CSV content (first few rows, values approximate):
#   product_name,category,total_units,total_revenue
#   Laptop,Electronics,6,7130.0
#   Notebook,Stationery,150,375.0
#   ...
#
# --- starting data ---
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "retail_summary.csv")




query_export = """

"""




# ══════════════════════════════════════════════════════════════
#  PART 5 — CLOSE THE CONNECTION
# ══════════════════════════════════════════════════════════════
# Always close the database connection when finished.
# For in-memory databases this also discards all data.
#
# EXAMPLE ──────────────────────────────────────────────────────

conn.close()
print("\nDatabase connection closed.")
print("Project complete.")
