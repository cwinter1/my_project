# ══════════════════════════════════════════════════════════════
#  WEEK 6  |  DAY 2  |  DATABASE DESIGN
# ══════════════════════════════════════════════════════════════
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Understand primary keys, foreign keys, and table relationships
#  2. Design and create a two-table schema with a foreign key relationship
#  3. Enforce data integrity with UNIQUE and NOT NULL constraints
#
#  TIME:  ~30-35 minutes
#
#  YOUTUBE
#  ───────
#  Search: "SQL primary key foreign key relationships explained"
#  Search: "database design normalization tutorial"
# ══════════════════════════════════════════════════════════════

import sqlite3

# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — PRIMARY KEYS, FOREIGN KEYS, RELATIONSHIPS
# ══════════════════════════════════════════════════════════════
# A relational database stores data in multiple related tables.
# Tables are linked through key columns.
#
# PRIMARY KEY:
#   - Uniquely identifies each row in a table
#   - Cannot be NULL
#   - Usually an auto-incrementing integer (AUTOINCREMENT)
#   - Each table has exactly one primary key
#
# FOREIGN KEY:
#   - A column in one table that references the PRIMARY KEY of another table
#   - Enforces referential integrity: you cannot add a foreign key value
#     that does not exist in the referenced table
#   - Creates a parent-child relationship between tables
#
# RELATIONSHIP TYPES:
#   One-to-Many (most common):
#     One customer can have MANY orders
#     customer_id is the PK in customers,
#     and a FK in orders
#
#   Many-to-Many:
#     An order can contain MANY products, a product can be on MANY orders
#     Resolved with a junction table: order_items(order_id, product_id)
#
# ENABLING FOREIGN KEYS IN SQLite:
#   SQLite does NOT enforce FKs by default.
#   You must run: PRAGMA foreign_keys = ON;
#   in each connection where you want enforcement.

# EXAMPLE ──────────────────────────────────────────────────────
conn = sqlite3.connect(":memory:")
cur = conn.cursor()

# Enable foreign key enforcement
cur.execute("PRAGMA foreign_keys = ON")

print("=== Database Design Demo ===")
print("Foreign key enforcement: ON")

# Create the parent table
cur.execute("""
    CREATE TABLE customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name        TEXT    NOT NULL,
        email       TEXT    NOT NULL UNIQUE,
        region      TEXT    NOT NULL,
        joined_date TEXT    DEFAULT (date('now'))
    )
""")

# Create the child table with FK reference
cur.execute("""
    CREATE TABLE orders (
        order_id    INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        order_date  TEXT    NOT NULL,
        status      TEXT    DEFAULT 'pending',
        total_amount REAL   NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    )
""")

conn.commit()
print("Tables 'customers' and 'orders' created.")

# Insert customers
cur.executemany("""
    INSERT INTO customers (name, email, region, joined_date)
    VALUES (?,?,?,?)
""", [
    ("Alice Ng",    "alice@corp.com",  "West",    "2020-01-15"),
    ("Bob Chen",    "bob@corp.com",    "East",    "2019-07-01"),
    ("Carol Diaz",  "carol@corp.com",  "West",    "2021-03-22"),
    ("Dave Park",   "dave@corp.com",   "Central", "2022-06-10"),
])
conn.commit()

# Insert orders (customer_id refers to customers table)
cur.executemany("""
    INSERT INTO orders (customer_id, order_date, status, total_amount)
    VALUES (?,?,?,?)
""", [
    (1, "2024-01-10", "completed", 1250.00),
    (1, "2024-02-15", "completed", 850.00),
    (2, "2024-01-22", "completed", 3400.00),
    (3, "2024-03-05", "pending",   700.00),
    (2, "2024-03-18", "completed", 1900.00),
    (1, "2024-04-01", "cancelled", 200.00),
])
conn.commit()

print(f"\nInserted {cur.execute('SELECT COUNT(*) FROM customers').fetchone()[0]} customers")
print(f"Inserted {cur.execute('SELECT COUNT(*) FROM orders').fetchone()[0]} orders")

# Demonstrate FK enforcement — try to insert an order for a non-existent customer
print("\n--- Testing FK enforcement ---")
try:
    cur.execute("INSERT INTO orders (customer_id, order_date, total_amount) VALUES (?,?,?)",
                (999, "2024-05-01", 500.00))
    conn.commit()
    print("Order inserted (FK not enforced — PRAGMA may not have taken effect)")
except sqlite3.IntegrityError as e:
    print(f"FK violation caught: {e}")
    # FOREIGN KEY constraint failed


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
# Add a third table called "products" to the same database.
# Schema:
#   product_id    INTEGER PRIMARY KEY AUTOINCREMENT
#   sku           TEXT NOT NULL UNIQUE
#   name          TEXT NOT NULL
#   category      TEXT NOT NULL
#   unit_price    REAL NOT NULL
#   stock_qty     INTEGER DEFAULT 0
#
# Insert 5 products:
#   ("SKU-001", "Laptop",   "Electronics", 899.99, 50)
#   ("SKU-002", "Monitor",  "Electronics", 349.99, 80)
#   ("SKU-003", "Keyboard", "Accessories", 89.99,  200)
#   ("SKU-004", "Mouse",    "Accessories", 39.99,  300)
#   ("SKU-005", "Headset",  "Accessories", 149.99, 75)
#
# Then verify by selecting all products and printing them.
#
# Expected output:
#   Products in DB:
#   1 | SKU-001 | Laptop   | Electronics | $899.99 | 50 units
#   2 | SKU-002 | Monitor  | Electronics | $349.99 | 80 units
#   ...




# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — CREATING A 2-TABLE SCHEMA WITH FK RELATIONSHIP
# ══════════════════════════════════════════════════════════════
# Let us build a second, more detailed example.
# A CRM-style schema: sales_reps have many deals.
#
# This demonstrates the full FK relationship clearly.

# EXAMPLE ──────────────────────────────────────────────────────
conn2 = sqlite3.connect(":memory:")
cur2 = conn2.cursor()
cur2.execute("PRAGMA foreign_keys = ON")

# Parent table: sales reps
cur2.execute("""
    CREATE TABLE sales_reps (
        rep_id      INTEGER PRIMARY KEY AUTOINCREMENT,
        name        TEXT    NOT NULL,
        email       TEXT    NOT NULL UNIQUE,
        region      TEXT    NOT NULL,
        hire_date   TEXT    NOT NULL,
        quota       REAL    DEFAULT 0
    )
""")

# Child table: deals (each deal belongs to one rep)
cur2.execute("""
    CREATE TABLE deals (
        deal_id     INTEGER PRIMARY KEY AUTOINCREMENT,
        rep_id      INTEGER NOT NULL,
        company     TEXT    NOT NULL,
        stage       TEXT    NOT NULL DEFAULT 'prospecting',
        value       REAL    NOT NULL,
        close_date  TEXT,
        FOREIGN KEY (rep_id) REFERENCES sales_reps(rep_id)
            ON DELETE CASCADE    -- if a rep is deleted, their deals are too
    )
""")

conn2.commit()

# Populate
cur2.executemany(
    "INSERT INTO sales_reps (name, email, region, hire_date, quota) VALUES (?,?,?,?,?)",
    [
        ("Tom Reyes",   "tom@corp.com",   "West",    "2020-03-01", 200000),
        ("Priya Mehta", "priya@corp.com", "East",    "2019-06-15", 300000),
        ("Sara Jones",  "sara@corp.com",  "Central", "2021-01-10", 150000),
    ]
)

cur2.executemany(
    "INSERT INTO deals (rep_id, company, stage, value, close_date) VALUES (?,?,?,?,?)",
    [
        (1, "Acme Ltd",   "closed_won",  45000, "2024-01-31"),
        (1, "Beta Corp",  "negotiation", 22000, None),
        (2, "Gamma Inc",  "closed_won",  67000, "2024-02-28"),
        (2, "Delta LLC",  "closed_won",  31000, "2024-03-15"),
        (3, "Epsilon SA", "prospecting", 8000,  None),
        (2, "Zeta Group", "negotiation", 55000, None),
    ]
)
conn2.commit()

# Show the relationship via a JOIN (preview of Day 3)
print("\n=== Deals with Rep Names ===")
cur2.execute("""
    SELECT r.name, d.company, d.stage, d.value
    FROM   deals d
    JOIN   sales_reps r ON d.rep_id = r.rep_id
    ORDER BY r.name, d.value DESC
""")
for rep, company, stage, value in cur2.fetchall():
    print(f"  {rep:<15} | {company:<12} | {stage:<15} | ${value:>9,.2f}")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
# Using the FIRST connection (conn, which has customers and orders),
# create a third table "order_items" that creates a many-to-many bridge
# between orders and products.
#
# Schema:
#   item_id     INTEGER PRIMARY KEY AUTOINCREMENT
#   order_id    INTEGER NOT NULL (FK to orders)
#   product_id  INTEGER NOT NULL (FK to products, which you created in Exercise 1)
#   quantity    INTEGER NOT NULL
#   unit_price  REAL NOT NULL
#   FOREIGN KEY (order_id) REFERENCES orders(order_id)
#   FOREIGN KEY (product_id) REFERENCES products(product_id)
#
# Insert these order items:
#   (order_id=1, product_id=1, qty=1, price=899.99)   -- Laptop
#   (order_id=1, product_id=3, qty=1, price=89.99)    -- Keyboard
#   (order_id=2, product_id=2, qty=2, price=349.99)   -- 2 Monitors
#   (order_id=3, product_id=1, qty=3, price=899.99)   -- 3 Laptops
#   (order_id=4, product_id=4, qty=5, price=39.99)    -- 5 Mice
#
# Print a summary: for each order_id, print the number of items and the subtotal
# (sum of quantity * unit_price)
#
# Expected output:
#   Order 1: 2 items, subtotal = $989.98
#   Order 2: 1 items, subtotal = $699.98
#   Order 3: 1 items, subtotal = $2,699.97
#   Order 4: 1 items, subtotal = $199.95




# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — DATA INTEGRITY: UNIQUE CONSTRAINT, NOT NULL
# ══════════════════════════════════════════════════════════════
# Constraints enforce rules at the database level, not just in your Python code.
# The database rejects any insert or update that violates a constraint.
#
# NOT NULL:
#   Column cannot contain a NULL value.
#   Use for columns that are always required.
#
# UNIQUE:
#   All values in the column must be distinct.
#   A table can have multiple UNIQUE constraints.
#   UNIQUE allows one NULL (in most databases).
#
# CHECK:
#   Validates that values satisfy a custom expression.
#   CHECK (salary > 0)
#   CHECK (status IN ('active', 'inactive', 'pending'))
#
# DEFAULT:
#   Provides a fallback value when none is supplied.

# EXAMPLE ──────────────────────────────────────────────────────
conn3 = sqlite3.connect(":memory:")
cur3 = conn3.cursor()

# A table with comprehensive constraints
cur3.execute("""
    CREATE TABLE pipeline_runs (
        run_id       INTEGER PRIMARY KEY AUTOINCREMENT,
        pipeline_name TEXT   NOT NULL,
        run_date      TEXT   NOT NULL DEFAULT (date('now')),
        status        TEXT   NOT NULL CHECK (status IN ('running','success','failed','skipped')),
        rows_processed INTEGER DEFAULT 0 CHECK (rows_processed >= 0),
        duration_sec  REAL   CHECK (duration_sec >= 0),
        triggered_by  TEXT   NOT NULL DEFAULT 'scheduler',
        UNIQUE (pipeline_name, run_date)   -- only one run per pipeline per day
    )
""")
conn3.commit()

# Valid insert
cur3.execute("""
    INSERT INTO pipeline_runs (pipeline_name, run_date, status, rows_processed, duration_sec)
    VALUES (?,?,?,?,?)
""", ("daily_sales_etl", "2024-01-15", "success", 15000, 42.7))
conn3.commit()
print("\nValid run inserted.")

# Test NOT NULL violation
print("\n--- Testing NOT NULL ---")
try:
    cur3.execute("INSERT INTO pipeline_runs (pipeline_name) VALUES (?)", (None,))
    conn3.commit()
except sqlite3.IntegrityError as e:
    print(f"NOT NULL violation: {e}")

# Test CHECK constraint violation
print("\n--- Testing CHECK constraint ---")
try:
    cur3.execute("""
        INSERT INTO pipeline_runs (pipeline_name, run_date, status, rows_processed)
        VALUES (?,?,?,?)
    """, ("inventory_sync", "2024-01-15", "crashed", 0))  # "crashed" is not in allowed values
    conn3.commit()
except sqlite3.IntegrityError as e:
    print(f"CHECK violation: {e}")

# Test UNIQUE violation
print("\n--- Testing UNIQUE constraint ---")
try:
    cur3.execute("""
        INSERT INTO pipeline_runs (pipeline_name, run_date, status)
        VALUES (?,?,?)
    """, ("daily_sales_etl", "2024-01-15", "failed"))   # same pipeline + date as row 1
    conn3.commit()
except sqlite3.IntegrityError as e:
    print(f"UNIQUE violation: {e}")

# Show what was inserted successfully
cur3.execute("SELECT * FROM pipeline_runs")
print("\nPipeline runs table:")
for row in cur3.fetchall():
    print(" ", row)

conn.close()
conn2.close()
conn3.close()
print("\nAll connections closed.")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
# Create a new in-memory database with a table called "inventory" using:
#   item_id     INTEGER PRIMARY KEY AUTOINCREMENT
#   sku         TEXT NOT NULL UNIQUE
#   name        TEXT NOT NULL
#   quantity    INTEGER NOT NULL CHECK (quantity >= 0)
#   unit_cost   REAL NOT NULL CHECK (unit_cost > 0)
#   category    TEXT NOT NULL DEFAULT 'General'
#   last_updated TEXT DEFAULT (date('now'))
#
# Insert 3 valid items.
# Then try to insert 3 invalid items (each violating a different constraint):
#   1. Duplicate SKU (UNIQUE violation)
#   2. Negative quantity (CHECK violation)
#   3. NULL sku (NOT NULL violation)
#
# Wrap each bad insert in a try/except and print the error type.
#
# Expected output:
#   3 valid items inserted.
#   UNIQUE violation: UNIQUE constraint failed: inventory.sku
#   CHECK violation: CHECK constraint failed: quantity >= 0
#   NOT NULL violation: NOT NULL constraint failed: inventory.sku


