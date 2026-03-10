# ══════════════════════════════════════════════════════════════
#  WEEK 6  |  DAY 3  |  ADVANCED SQL
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Join tables using INNER JOIN and LEFT JOIN in sqlite3
#  2. Aggregate data with GROUP BY, HAVING, COUNT, SUM, AVG, MAX, MIN
#  3. Write subqueries (SELECT inside SELECT) for advanced filtering
#
#  TIME:  ~30 minutes
#
#  YOUTUBE
#  ───────
#  Search: "SQL INNER JOIN LEFT JOIN tutorial explained"
#  Search: "SQL GROUP BY HAVING subquery tutorial"
#
# ══════════════════════════════════════════════════════════════

import sqlite3

# ══════════════════════════════════════════════════════════════
#  SETUP — Rebuild the customers + orders schema from Day 2
# ══════════════════════════════════════════════════════════════
# We recreate the same two-table schema so this file is self-contained.

conn = sqlite3.connect(":memory:")
cur = conn.cursor()
cur.execute("PRAGMA foreign_keys = ON")

# Customers table
cur.execute("""
    CREATE TABLE customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name        TEXT    NOT NULL,
        email       TEXT    NOT NULL UNIQUE,
        region      TEXT    NOT NULL,
        tier        TEXT    DEFAULT 'standard'
    )
""")

# Orders table (child of customers)
cur.execute("""
    CREATE TABLE orders (
        order_id     INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id  INTEGER NOT NULL,
        order_date   TEXT    NOT NULL,
        status       TEXT    NOT NULL DEFAULT 'pending',
        total_amount REAL    NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    )
""")

# Products table
cur.execute("""
    CREATE TABLE products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        sku        TEXT NOT NULL UNIQUE,
        name       TEXT NOT NULL,
        category   TEXT NOT NULL,
        unit_price REAL NOT NULL
    )
""")

# Order items (many-to-many bridge: orders x products)
cur.execute("""
    CREATE TABLE order_items (
        item_id    INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id   INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity   INTEGER NOT NULL,
        unit_price REAL    NOT NULL,
        FOREIGN KEY (order_id)   REFERENCES orders(order_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    )
""")

conn.commit()

# Populate customers
cur.executemany(
    "INSERT INTO customers (name, email, region, tier) VALUES (?,?,?,?)",
    [
        ("Alice Ng",    "alice@corp.com",  "West",    "premium"),
        ("Bob Chen",    "bob@corp.com",    "East",    "standard"),
        ("Carol Diaz",  "carol@corp.com",  "West",    "premium"),
        ("Dave Park",   "dave@corp.com",   "Central", "standard"),
        ("Eve Torres",  "eve@corp.com",    "East",    "premium"),
    ]
)

# Populate products
cur.executemany(
    "INSERT INTO products (sku, name, category, unit_price) VALUES (?,?,?,?)",
    [
        ("SKU-001", "Laptop",   "Electronics", 899.99),
        ("SKU-002", "Monitor",  "Electronics", 349.99),
        ("SKU-003", "Keyboard", "Accessories", 89.99),
        ("SKU-004", "Mouse",    "Accessories", 39.99),
        ("SKU-005", "Headset",  "Accessories", 149.99),
    ]
)

# Populate orders (note Dave has no orders -- useful for LEFT JOIN demo)
cur.executemany(
    "INSERT INTO orders (customer_id, order_date, status, total_amount) VALUES (?,?,?,?)",
    [
        (1, "2024-01-10", "completed",  1439.98),
        (1, "2024-02-15", "completed",   849.99),
        (2, "2024-01-22", "completed",  3599.96),
        (3, "2024-03-05", "pending",     199.95),
        (2, "2024-03-18", "completed",  1049.97),
        (5, "2024-04-02", "completed",   349.99),
        (1, "2024-04-10", "cancelled",   200.00),
    ]
)

# Populate order items
cur.executemany(
    "INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (?,?,?,?)",
    [
        (1, 1, 1, 899.99), (1, 3, 1, 89.99), (1, 5, 3, 149.99),
        (2, 1, 1, 899.99),
        (3, 1, 4, 899.99),
        (4, 4, 5, 39.99),
        (5, 3, 5, 89.99), (5, 5, 4, 149.99),
        (6, 2, 1, 349.99),
    ]
)
conn.commit()
print("Database populated.")


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — INNER JOIN AND LEFT JOIN
# ══════════════════════════════════════════════════════════════
# JOIN combines rows from two tables based on a matching key column.
#
# INNER JOIN:
#   Returns ONLY rows where the key exists in BOTH tables.
#   Customers with no orders are excluded.
#
# LEFT JOIN:
#   Returns ALL rows from the LEFT table.
#   If no match in the right table, right-side columns are NULL.
#   Useful for finding customers with no orders, products with no sales, etc.
#
# Syntax:
#   SELECT a.col, b.col
#   FROM   left_table a
#   JOIN   right_table b ON a.key = b.key       -- INNER JOIN (default)
#   LEFT JOIN other_table c ON a.key = c.key    -- LEFT JOIN

# EXAMPLE ──────────────────────────────────────────────────────

# INNER JOIN: orders with customer names
print("\n=== INNER JOIN: Orders with Customer Info ===")
cur.execute("""
    SELECT
        o.order_id,
        c.name          AS customer,
        c.region,
        o.order_date,
        o.status,
        o.total_amount
    FROM   orders o
    JOIN   customers c ON o.customer_id = c.customer_id
    ORDER BY o.order_date
""")
print(f"{'ID':>3} {'Customer':<15} {'Region':<10} {'Date':<12} {'Status':<12} {'Amount':>10}")
print("-" * 68)
for row in cur.fetchall():
    oid, name, region, date, status, amount = row
    print(f"{oid:>3} {name:<15} {region:<10} {date:<12} {status:<12} ${amount:>9,.2f}")

# LEFT JOIN: all customers including those with no orders
print("\n=== LEFT JOIN: All Customers (even without orders) ===")
cur.execute("""
    SELECT
        c.name,
        c.region,
        c.tier,
        COUNT(o.order_id)    AS order_count,
        COALESCE(SUM(o.total_amount), 0) AS total_spent
    FROM   customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.name, c.region, c.tier
    ORDER BY total_spent DESC
""")
print(f"{'Customer':<15} {'Region':<10} {'Tier':<10} {'Orders':>7} {'Total Spent':>12}")
print("-" * 58)
for name, region, tier, count, total in cur.fetchall():
    print(f"{name:<15} {region:<10} {tier:<10} {count:>7} ${total:>11,.2f}")
# Dave Park (no orders) will appear with order_count=0 and total_spent=0

# Three-table JOIN: order items with product names
print("\n=== Three-table JOIN: Order Items Detail ===")
cur.execute("""
    SELECT
        o.order_id,
        c.name      AS customer,
        p.name      AS product,
        oi.quantity,
        oi.unit_price,
        oi.quantity * oi.unit_price AS line_total
    FROM   order_items oi
    JOIN   orders   o ON oi.order_id   = o.order_id
    JOIN   customers c ON o.customer_id = c.customer_id
    JOIN   products  p ON oi.product_id = p.product_id
    ORDER BY o.order_id, p.name
""")
for row in cur.fetchall():
    oid, cust, prod, qty, price, total = row
    print(f"  Order {oid} | {cust:<12} | {prod:<10} | qty={qty} | ${price:.2f} | ${total:.2f}")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
# Write a query that joins order_items + products to find:
#   - For each product CATEGORY:
#     total units sold (sum of quantity)
#     total revenue (sum of quantity * unit_price)
# Sort by total revenue descending.
#
# Then write a second query: LEFT JOIN products with order_items to find
# products that have NEVER been ordered (where order_items.product_id IS NULL).
#
# Expected output (Query 1):
#   Category      | Units Sold | Revenue
#   Electronics   |     7      | $5,449.93
#   Accessories   |    20      | $1,889.73
#
# Expected output (Query 2 -- no-sales products):
#   [Empty or shows SKU-004 Mouse depending on your data population]





# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — GROUP BY + HAVING, AGGREGATE FUNCTIONS
# ══════════════════════════════════════════════════════════════
# GROUP BY partitions rows into groups by column value.
# Aggregate functions run on each group: COUNT, SUM, AVG, MAX, MIN.
#
# HAVING is like WHERE but runs AFTER grouping -- it filters groups, not rows.
# Use WHERE to filter rows before grouping.
# Use HAVING to filter based on aggregate values.
#
# Syntax:
#   SELECT col, COUNT(*), SUM(amount)
#   FROM   table
#   WHERE  condition            -- filter rows first
#   GROUP BY col
#   HAVING COUNT(*) > 3         -- then filter groups
#   ORDER BY SUM(amount) DESC;

# EXAMPLE ──────────────────────────────────────────────────────

# Customers with more than 1 completed order
print("\n=== GROUP BY + HAVING: Frequent Buyers ===")
cur.execute("""
    SELECT
        c.name,
        COUNT(o.order_id)               AS order_count,
        ROUND(SUM(o.total_amount), 2)   AS total_spent,
        ROUND(AVG(o.total_amount), 2)   AS avg_order,
        MIN(o.order_date)               AS first_order,
        MAX(o.order_date)               AS last_order
    FROM   customers c
    JOIN   orders o ON c.customer_id = o.customer_id
    WHERE  o.status != 'cancelled'      -- exclude cancelled before grouping
    GROUP BY c.customer_id, c.name
    HAVING COUNT(o.order_id) > 1        -- only customers with 2+ orders
    ORDER BY total_spent DESC
""")
print(f"{'Customer':<15} {'Orders':>7} {'Total':>10} {'Avg Order':>10} {'First':>12} {'Last':>12}")
print("-" * 70)
for row in cur.fetchall():
    name, count, total, avg, first, last = row
    print(f"{name:<15} {count:>7} ${total:>9,.2f} ${avg:>9,.2f} {first:>12} {last:>12}")

# Product performance by category
print("\n=== GROUP BY: Product Performance ===")
cur.execute("""
    SELECT
        p.category,
        p.name,
        COUNT(oi.item_id)                    AS times_ordered,
        SUM(oi.quantity)                     AS units_sold,
        ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue,
        ROUND(AVG(oi.unit_price), 2)         AS avg_price
    FROM   products p
    LEFT JOIN order_items oi ON p.product_id = oi.product_id
    GROUP BY p.product_id, p.category, p.name
    ORDER BY revenue DESC
""")
for row in cur.fetchall():
    cat, name, times, units, rev, avg = row
    rev_str = f"${rev:,.2f}" if rev else "$0.00"
    print(f"  {cat:<15} {name:<10} | {times or 0} orders | {units or 0} units | {rev_str}")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
# Write a single SQL query that:
#   1. Groups by customer region
#   2. Counts the number of completed orders (status = 'completed') per region
#   3. Calculates total revenue per region
#   4. Calculates average order value per region
#   5. Filters to only regions with total revenue > $1000
#   6. Sorts by total revenue descending
#
# Print the results.
#
# Expected output:
#   Region    | Orders | Total Revenue | Avg Order
#   East      |   2    |   $4,649.93   | $2,324.97
#   West      |   2    |   $2,289.97   | $1,144.99
#   East      |   1    |     $349.99   |   $349.99





# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — SUBQUERIES (SELECT INSIDE SELECT)
# ══════════════════════════════════════════════════════════════
# A subquery is a SELECT statement embedded inside another SQL statement.
# It can appear in:
#   - WHERE clause  (filter based on a computed value)
#   - FROM clause   (treat the result as a temporary table)
#   - SELECT clause (compute a value per row)
#
# Types:
#   Scalar subquery: returns a single value
#   Row subquery:    returns a single row
#   Table subquery:  returns multiple rows (used with IN, EXISTS, etc.)

# EXAMPLE ──────────────────────────────────────────────────────

# Find customers who have spent MORE than the average customer total
print("\n=== SUBQUERY: Above-Average Spenders ===")
cur.execute("""
    SELECT
        c.name,
        c.tier,
        ROUND(SUM(o.total_amount), 2) AS total_spent
    FROM   customers c
    JOIN   orders o ON c.customer_id = o.customer_id
    WHERE  o.status = 'completed'
    GROUP BY c.customer_id, c.name, c.tier
    HAVING SUM(o.total_amount) > (
        -- subquery: compute average total spend across all customers
        SELECT AVG(customer_total)
        FROM (
            SELECT customer_id, SUM(total_amount) AS customer_total
            FROM   orders
            WHERE  status = 'completed'
            GROUP BY customer_id
        )
    )
    ORDER BY total_spent DESC
""")
print(f"{'Customer':<15} {'Tier':<10} {'Total Spent':>12}")
print("-" * 40)
for name, tier, total in cur.fetchall():
    print(f"{name:<15} {tier:<10} ${total:>11,.2f}")

# Find products priced higher than the average product price (scalar subquery in WHERE)
print("\n=== SUBQUERY: Above-Average Priced Products ===")
cur.execute("""
    SELECT name, unit_price
    FROM   products
    WHERE  unit_price > (SELECT AVG(unit_price) FROM products)
    ORDER BY unit_price DESC
""")
avg_price = cur.execute("SELECT ROUND(AVG(unit_price),2) FROM products").fetchone()[0]
print(f"Average product price: ${avg_price}")
for name, price in cur.fetchall():
    print(f"  {name}: ${price:.2f}")

# Find customers who have NOT placed any orders (NOT IN subquery)
print("\n=== SUBQUERY: Customers With No Orders ===")
cur.execute("""
    SELECT name, email, region
    FROM   customers
    WHERE  customer_id NOT IN (
        SELECT DISTINCT customer_id FROM orders
    )
""")
rows = cur.fetchall()
if rows:
    for name, email, region in rows:
        print(f"  {name} | {email} | {region}")
else:
    print("  All customers have placed at least one order.")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
# Write a query using a subquery or window-style logic to find:
# For each product CATEGORY, which product generated the MOST revenue?
#
# Approach:
#   1. Write an inner query that calculates revenue per product:
#      (SUM(quantity * unit_price) AS revenue) joined from order_items + products
#   2. Wrap it in an outer query that, for each category,
#      finds the row with maximum revenue
#
# Hint: You can use a subquery in the WHERE clause:
#   WHERE revenue = (SELECT MAX(revenue) FROM ... WHERE category = ...)
#
# Print: Category | Top Product | Revenue
#
# Expected output:
#   Electronics | Laptop   | $3,599.96
#   Accessories | Headset  | $1,049.94




conn.close()
print("\nConnection closed.")
