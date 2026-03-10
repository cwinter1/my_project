# ══════════════════════════════════════════════════════════════
#  WEEK 6  |  DAY 5  |  PROJECT: RETAIL DATABASE
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  Build a complete retail database from scratch using sqlite3:
#  create tables -> insert data -> run analytical queries -> export to CSV
#
#  TIME:  ~30 minutes
#
#  YOUTUBE
#  ───────
#  Search: "sqlite3 Python complete project tutorial"
#  Search: "SQL analytical queries retail database"
#
# ══════════════════════════════════════════════════════════════

import sqlite3
import csv
import os

# ══════════════════════════════════════════════════════════════
#  SETUP
# ══════════════════════════════════════════════════════════════
this_dir = os.path.dirname(__file__)
conn = sqlite3.connect(":memory:")
cur = conn.cursor()
cur.execute("PRAGMA foreign_keys = ON")

print("=" * 60)
print("RETAIL DATABASE PROJECT")
print("=" * 60)


# ══════════════════════════════════════════════════════════════
#  STEP 1 — CREATE ALL FOUR TABLES (demonstrated for you)
# ══════════════════════════════════════════════════════════════
# Schema:
#   products      (product_id, sku, name, category, unit_price, stock_qty)
#   customers     (customer_id, name, email, city, tier)
#   orders        (order_id, customer_id FK, order_date, status)
#   order_items   (item_id, order_id FK, product_id FK, quantity, unit_price)

cur.execute("""
    CREATE TABLE products (
        product_id  INTEGER PRIMARY KEY AUTOINCREMENT,
        sku         TEXT    NOT NULL UNIQUE,
        name        TEXT    NOT NULL,
        category    TEXT    NOT NULL,
        unit_price  REAL    NOT NULL CHECK (unit_price > 0),
        stock_qty   INTEGER NOT NULL DEFAULT 0 CHECK (stock_qty >= 0)
    )
""")

cur.execute("""
    CREATE TABLE customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name        TEXT    NOT NULL,
        email       TEXT    NOT NULL UNIQUE,
        city        TEXT    NOT NULL,
        tier        TEXT    NOT NULL DEFAULT 'standard'
                            CHECK (tier IN ('standard','silver','gold','platinum'))
    )
""")

cur.execute("""
    CREATE TABLE orders (
        order_id    INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        order_date  TEXT    NOT NULL,
        status      TEXT    NOT NULL DEFAULT 'pending'
                            CHECK (status IN ('pending','processing','shipped','completed','cancelled')),
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    )
""")

cur.execute("""
    CREATE TABLE order_items (
        item_id     INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id    INTEGER NOT NULL,
        product_id  INTEGER NOT NULL,
        quantity    INTEGER NOT NULL CHECK (quantity > 0),
        unit_price  REAL    NOT NULL CHECK (unit_price > 0),
        FOREIGN KEY (order_id)   REFERENCES orders(order_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    )
""")

conn.commit()
print("\nStep 1 complete: All 4 tables created.")


# ══════════════════════════════════════════════════════════════
#  STEP 2 — INSERT SAMPLE DATA (demonstrated for you)
# ══════════════════════════════════════════════════════════════

# Products
products_data = [
    ("SKU-001", "Laptop Pro 15",     "Electronics", 1299.99, 45),
    ("SKU-002", "Ultrabook 13",      "Electronics", 999.99,  60),
    ("SKU-003", "Wireless Monitor",  "Electronics", 399.99,  80),
    ("SKU-004", "Mechanical Keyboard","Accessories", 149.99, 200),
    ("SKU-005", "Ergonomic Mouse",   "Accessories", 79.99,  350),
    ("SKU-006", "USB Hub 7-Port",    "Accessories", 49.99,  500),
    ("SKU-007", "Webcam HD 1080p",   "Peripherals", 89.99,  120),
    ("SKU-008", "Noise-Cancel Headset","Peripherals",199.99, 90),
    ("SKU-009", "Standing Desk Mat", "Office",       59.99, 250),
    ("SKU-010", "Cable Management Kit","Office",      24.99, 400),
]
cur.executemany(
    "INSERT INTO products (sku, name, category, unit_price, stock_qty) VALUES (?,?,?,?,?)",
    products_data
)

# Customers
customers_data = [
    ("Alice Ng",    "alice@techcorp.com",  "San Francisco", "platinum"),
    ("Bob Chen",    "bob@startup.io",      "New York",      "gold"),
    ("Carol Diaz",  "carol@acme.com",      "Chicago",       "silver"),
    ("Dave Park",   "dave@globalinc.com",  "Seattle",       "standard"),
    ("Eve Torres",  "eve@media.co",        "Austin",        "gold"),
    ("Frank Wu",    "frank@retail.com",    "Boston",        "silver"),
    ("Grace Lee",   "grace@bigcorp.com",   "Denver",        "platinum"),
    ("Hank Morris", "hank@smb.net",        "Miami",         "standard"),
]
cur.executemany(
    "INSERT INTO customers (name, email, city, tier) VALUES (?,?,?,?)",
    customers_data
)

# Orders
orders_data = [
    (1, "2024-01-08",  "completed"),
    (2, "2024-01-15",  "completed"),
    (1, "2024-01-20",  "completed"),
    (3, "2024-02-03",  "completed"),
    (4, "2024-02-10",  "completed"),
    (5, "2024-02-18",  "completed"),
    (2, "2024-03-01",  "completed"),
    (6, "2024-03-12",  "completed"),
    (7, "2024-03-22",  "completed"),
    (1, "2024-04-05",  "completed"),
    (3, "2024-04-14",  "pending"),
    (8, "2024-04-20",  "processing"),
    (5, "2024-05-01",  "cancelled"),
    (7, "2024-05-08",  "completed"),
    (2, "2024-05-15",  "completed"),
]
cur.executemany(
    "INSERT INTO orders (customer_id, order_date, status) VALUES (?,?,?)",
    orders_data
)

# Order items
order_items_data = [
    # Order 1: Alice bought Laptop + Keyboard
    (1, 1, 1, 1299.99), (1, 4, 1, 149.99),
    # Order 2: Bob bought Monitor + Mouse + USB Hub
    (2, 3, 1, 399.99), (2, 5, 2, 79.99), (2, 6, 1, 49.99),
    # Order 3: Alice bought Webcam + Headset
    (3, 7, 2, 89.99), (3, 8, 1, 199.99),
    # Order 4: Carol bought Laptop + Mouse
    (4, 1, 1, 1299.99), (4, 5, 1, 79.99),
    # Order 5: Dave bought USB Hub x3
    (5, 6, 3, 49.99),
    # Order 6: Eve bought Monitor + Keyboard + Headset
    (6, 3, 1, 399.99), (6, 4, 1, 149.99), (6, 8, 1, 199.99),
    # Order 7: Bob bought Laptop Pro
    (7, 1, 1, 1299.99),
    # Order 8: Frank bought Desk Mat x2 + Cable Kit x2
    (8, 9, 2, 59.99), (8, 10, 2, 24.99),
    # Order 9: Grace bought Ultrabook
    (9, 2, 1, 999.99),
    # Order 10: Alice bought Mouse + USB Hub
    (10, 5, 1, 79.99), (10, 6, 2, 49.99),
    # Order 11: Carol pending -- Keyboard x2
    (11, 4, 2, 149.99),
    # Order 12: Hank processing -- Webcam
    (12, 7, 1, 89.99),
    # Order 13: Eve cancelled
    (13, 8, 2, 199.99),
    # Order 14: Grace -- Monitor + Mouse
    (14, 3, 1, 399.99), (14, 5, 1, 79.99),
    # Order 15: Bob -- Headset x2
    (15, 8, 2, 199.99),
]
cur.executemany(
    "INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (?,?,?,?)",
    order_items_data
)

conn.commit()
print(f"Step 2 complete: Data inserted.")
print(f"  Products: {cur.execute('SELECT COUNT(*) FROM products').fetchone()[0]}")
print(f"  Customers: {cur.execute('SELECT COUNT(*) FROM customers').fetchone()[0]}")
print(f"  Orders: {cur.execute('SELECT COUNT(*) FROM orders').fetchone()[0]}")
print(f"  Order items: {cur.execute('SELECT COUNT(*) FROM order_items').fetchone()[0]}")


# ══════════════════════════════════════════════════════════════
#  STEP 3 — ANALYTICAL QUERIES
# ══════════════════════════════════════════════════════════════
# Complete each of the 5 tasks below.
# Each is marked with TASK X and describes what to query.


# ══════════════════════════════════════════════════════════════
#  TASK 1 — Top 5 Products by Revenue
# ══════════════════════════════════════════════════════════════
# Query: Join order_items + products + orders
#        Filter to orders with status = 'completed'
#        Group by product name
#        Sum (quantity * unit_price) as total_revenue
#        Sort descending, LIMIT 5
# Print: product name | units sold | total revenue
#
# Expected output:
#   Laptop Pro 15    |  4 units | $5,199.96
#   Wireless Monitor |  4 units | $1,599.96
#   Noise-Cancel ... |  6 units | $1,199.94
#   Ergonomic Mouse  |  5 units |   $399.95
#   Mechanical Keybd |  3 units |   $449.97

print("\n" + "="*60)
print("TASK 1: Top 5 Products by Revenue")
print("="*60)





# ══════════════════════════════════════════════════════════════
#  TASK 2 — Customer Lifetime Value Report
# ══════════════════════════════════════════════════════════════
# Query: Join orders + order_items + customers
#        Filter to status = 'completed'
#        Group by customer name and tier
#        Calculate: order_count, total_spent, avg_order_value
#        Sort by total_spent descending
# Print all columns

print("\n" + "="*60)
print("TASK 2: Customer Lifetime Value")
print("="*60)





# ══════════════════════════════════════════════════════════════
#  TASK 3 — Monthly Revenue Trend
# ══════════════════════════════════════════════════════════════
# Query: Join orders + order_items
#        Filter to status = 'completed'
#        Extract year and month from order_date using SUBSTR(order_date, 1, 7)
#        Group by year-month
#        Sum revenue (quantity * unit_price)
#        Sort chronologically
# Print: Month | Revenue

print("\n" + "="*60)
print("TASK 3: Monthly Revenue Trend")
print("="*60)





# ══════════════════════════════════════════════════════════════
#  TASK 4 — Category Performance Summary
# ══════════════════════════════════════════════════════════════
# Query: Join order_items + products + orders
#        Filter to completed orders
#        Group by product category
#        Calculate: total_orders (distinct order_id count), units_sold, revenue
#        Sort by revenue descending
# Print all columns

print("\n" + "="*60)
print("TASK 4: Category Performance")
print("="*60)





# ══════════════════════════════════════════════════════════════
#  TASK 5 — Customers With Pending or Processing Orders
# ══════════════════════════════════════════════════════════════
# Query: Join customers + orders
#        Filter to status IN ('pending', 'processing')
#        Show customer name, email, order_id, order_date, status

print("\n" + "="*60)
print("TASK 5: Open Orders (Pending/Processing)")
print("="*60)





# ══════════════════════════════════════════════════════════════
#  STEP 4 — EXPORT RESULTS TO CSV (demonstrated for you)
# ══════════════════════════════════════════════════════════════
# After running your queries, export one result to CSV.

print("\n" + "="*60)
print("STEP 4: Export Top Products to CSV")
print("="*60)

# Run the top products query and export
cur.execute("""
    SELECT
        p.name                                   AS product,
        p.category,
        SUM(oi.quantity)                         AS units_sold,
        ROUND(SUM(oi.quantity * oi.unit_price),2) AS total_revenue
    FROM   order_items oi
    JOIN   products p  ON oi.product_id = p.product_id
    JOIN   orders   o  ON oi.order_id   = o.order_id
    WHERE  o.status = 'completed'
    GROUP BY p.product_id, p.name, p.category
    ORDER BY total_revenue DESC
""")
rows = cur.fetchall()
headers = ["product", "category", "units_sold", "total_revenue"]

output_csv = os.path.join(this_dir, "product_performance.csv")
with open(output_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(rows)

print(f"Exported {len(rows)} products to: {output_csv}")

# Verify
with open(output_csv, "r") as f:
    for i, line in enumerate(f):
        print(" ", line.strip())
        if i >= 4:
            print("  ...")
            break

conn.close()
print("\nDatabase connection closed. Project complete.")
