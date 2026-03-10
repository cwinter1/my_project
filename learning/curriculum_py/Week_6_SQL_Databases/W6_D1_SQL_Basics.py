# ══════════════════════════════════════════════════════════════
#  WEEK 6  |  DAY 1  |  SQL BASICS
# ══════════════════════════════════════════════════════════════
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Create a SQLite database and table entirely in Python using sqlite3
#  2. Insert rows and query data with SELECT, WHERE, and ORDER BY
#  3. Update and delete rows with WHERE conditions
#
#  TIME:  ~30-35 minutes
#
#  YOUTUBE
#  ───────
#  Search: "Python sqlite3 tutorial create table insert select"
#  Search: "SQL UPDATE DELETE WHERE Python sqlite3"
# ══════════════════════════════════════════════════════════════

# sqlite3 is part of the Python standard library — no pip install needed.
# We use ":memory:" to run everything in RAM with no files created.
# This is perfect for learning because it is self-contained and repeatable.

import sqlite3

# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — CREATING A SQLite DATABASE AND TABLE
# ══════════════════════════════════════════════════════════════
# sqlite3 workflow:
#   1. Connect:   conn = sqlite3.connect(":memory:")
#   2. Get cursor: cur = conn.cursor()
#   3. Execute SQL: cur.execute("SQL STATEMENT")
#   4. Commit:    conn.commit()   (required after INSERT/UPDATE/DELETE)
#   5. Close:     conn.close()
#
# SQL DATA TYPES used in SQLite:
#   INTEGER   -- whole numbers
#   REAL      -- floating point
#   TEXT      -- strings
#   BLOB      -- raw binary data
#   NULL      -- missing value
#
# CREATE TABLE syntax:
#   CREATE TABLE table_name (
#       column_name datatype CONSTRAINT,
#       ...
#   );
# Constraints: PRIMARY KEY, NOT NULL, UNIQUE, DEFAULT value

# EXAMPLE ──────────────────────────────────────────────────────
# Create an in-memory database
conn = sqlite3.connect(":memory:")
cur = conn.cursor()

# Create the employees table
cur.execute("""
    CREATE TABLE employees (
        emp_id      INTEGER PRIMARY KEY AUTOINCREMENT,
        name        TEXT    NOT NULL,
        department  TEXT    NOT NULL,
        salary      REAL    NOT NULL,
        start_date  TEXT,
        is_active   INTEGER DEFAULT 1
    )
""")

# Create the departments table
cur.execute("""
    CREATE TABLE departments (
        dept_id   INTEGER PRIMARY KEY AUTOINCREMENT,
        name      TEXT    NOT NULL UNIQUE,
        budget    REAL    DEFAULT 0.0,
        manager   TEXT
    )
""")

conn.commit()
print("Tables created successfully.")

# Verify tables exist
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cur.fetchall()
print("Tables in DB:", [t[0] for t in tables])   # ['employees', 'departments']


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
# Using the same in-memory connection (conn, cur), create a table called "sales"
# with these columns:
#   sale_id     INTEGER PRIMARY KEY AUTOINCREMENT
#   sale_date   TEXT NOT NULL
#   product     TEXT NOT NULL
#   quantity    INTEGER NOT NULL
#   unit_price  REAL NOT NULL
#   rep_name    TEXT
#
# After creating it, verify it was created by querying sqlite_master.
# Print: "Tables now in DB: ['employees', 'departments', 'sales']"
#
# Expected output:
#   Sales table created.
#   Tables now in DB: ['employees', 'departments', 'sales']




# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — INSERT, SELECT, WHERE, ORDER BY
# ══════════════════════════════════════════════════════════════
# INSERT adds rows to a table.
# SELECT retrieves rows from a table.
#
# INSERT syntax:
#   INSERT INTO table_name (col1, col2) VALUES (val1, val2);
# Always use ? placeholders for values — NEVER build SQL strings with f-strings.
# (f-string SQL is vulnerable to SQL injection attacks)
#
# SELECT syntax:
#   SELECT col1, col2 FROM table_name;
#   SELECT * FROM table_name WHERE condition;
#   SELECT * FROM table_name ORDER BY col DESC;
#   SELECT * FROM table_name WHERE col = ? -- use ? for parameters
#
# fetchall()  -- return all matching rows as a list of tuples
# fetchone()  -- return the first matching row
# fetchmany(n)-- return the next n rows

# EXAMPLE ──────────────────────────────────────────────────────
# Insert employee data using executemany (batch insert)
employees_data = [
    ("Alice Ng",    "Engineering", 95000, "2021-03-15"),
    ("Bob Chen",    "Sales",       72000, "2019-07-01"),
    ("Carol Diaz",  "Finance",     81000, "2020-11-20"),
    ("Dave Park",   "Engineering", 88000, "2022-01-10"),
    ("Eve Torres",  "Sales",       67500, "2023-05-30"),
    ("Frank Wu",    "Finance",     79000, "2021-08-14"),
    ("Grace Lee",   "Engineering", 105000,"2018-04-22"),
]

cur.executemany(
    "INSERT INTO employees (name, department, salary, start_date) VALUES (?,?,?,?)",
    employees_data,
)
conn.commit()
print(f"\nInserted {cur.rowcount} employee(s).")

# SELECT all employees
print("\n=== All Employees ===")
cur.execute("SELECT emp_id, name, department, salary FROM employees ORDER BY emp_id")
for row in cur.fetchall():
    emp_id, name, dept, salary = row
    print(f"  [{emp_id}] {name:<15} | {dept:<15} | ${salary:>9,.2f}")

# SELECT with WHERE
print("\n=== Engineering Department ===")
cur.execute("""
    SELECT name, salary
    FROM   employees
    WHERE  department = ?
    ORDER BY salary DESC
""", ("Engineering",))

for name, salary in cur.fetchall():
    print(f"  {name}: ${salary:,.2f}")

# Aggregate functions
print("\n=== Salary Statistics ===")
cur.execute("""
    SELECT
        department,
        COUNT(*)            AS headcount,
        ROUND(AVG(salary),2) AS avg_salary,
        MIN(salary)         AS min_salary,
        MAX(salary)         AS max_salary
    FROM employees
    GROUP BY department
    ORDER BY avg_salary DESC
""")

rows = cur.fetchall()
print(f"{'Department':<15} {'Count':>6} {'Avg Salary':>12} {'Min':>10} {'Max':>10}")
print("-" * 58)
for dept, count, avg, low, high in rows:
    print(f"{dept:<15} {count:>6} ${avg:>11,.2f} ${low:>9,.2f} ${high:>9,.2f}")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
# Insert these rows into the "sales" table you created in Exercise 1:
#   ("2024-01-15", "Laptop",   3, 899.99, "Bob Chen")
#   ("2024-01-16", "Monitor",  5, 349.99, "Eve Torres")
#   ("2024-01-17", "Keyboard", 10, 89.99, "Bob Chen")
#   ("2024-01-18", "Laptop",   1, 899.99, "Carol Diaz")
#   ("2024-01-19", "Mouse",   20, 39.99,  "Eve Torres")
#
# Then:
# A. SELECT all rows and print them
# B. SELECT only rows where unit_price > 100, print them
# C. SELECT and print total quantity and total revenue (quantity*unit_price)
#    for each product, ordered by total revenue descending
#
# Expected output (part C):
#   Product   | Total Qty | Total Revenue
#   Laptop    |     4     |   $3,599.96
#   Monitor   |     5     |   $1,749.95
#   Keyboard  |    10     |     $899.90
#   Mouse     |    20     |     $799.80




# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — UPDATE AND DELETE WITH WHERE
# ══════════════════════════════════════════════════════════════
# UPDATE changes existing row values.
# DELETE removes rows from the table.
# Always use WHERE — without it, UPDATE and DELETE affect EVERY row.
#
# UPDATE syntax:
#   UPDATE table_name SET col1 = val1, col2 = val2 WHERE condition;
#
# DELETE syntax:
#   DELETE FROM table_name WHERE condition;
#
# After UPDATE or DELETE, always commit:
#   conn.commit()

# EXAMPLE ──────────────────────────────────────────────────────
print("\n=== BEFORE UPDATE ===")
cur.execute("SELECT name, salary, is_active FROM employees WHERE department = 'Sales'")
for row in cur.fetchall():
    print(f"  {row[0]}: ${row[1]:,.2f}  active={row[2]}")

# Give all Sales employees a 10% raise
cur.execute("""
    UPDATE employees
    SET    salary = ROUND(salary * 1.10, 2)
    WHERE  department = 'Sales'
""")
conn.commit()
print(f"Rows updated: {cur.rowcount}")

print("\n=== AFTER UPDATE (Sales +10%) ===")
cur.execute("SELECT name, salary FROM employees WHERE department = 'Sales'")
for row in cur.fetchall():
    print(f"  {row[0]}: ${row[1]:,.2f}")

# Soft-delete: mark an employee as inactive (preferred over hard delete)
cur.execute("UPDATE employees SET is_active = 0 WHERE name = ?", ("Frank Wu",))
conn.commit()
print(f"\nSoft-deleted Frank Wu. Rows affected: {cur.rowcount}")

# Verify
cur.execute("SELECT name, is_active FROM employees")
for name, active in cur.fetchall():
    status = "active" if active else "INACTIVE"
    print(f"  {name}: {status}")

# Hard delete a record
cur.execute("DELETE FROM employees WHERE name = ? AND is_active = 0", ("Frank Wu",))
conn.commit()
print(f"\nHard-deleted inactive employees. Rows removed: {cur.rowcount}")

cur.execute("SELECT COUNT(*) FROM employees")
print(f"Remaining employees: {cur.fetchone()[0]}")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
# Using the "sales" table from Exercise 2:
#
# A. Update the unit_price of "Laptop" to 849.99 (price reduction)
#    Print: "Updated X laptop price records"
#
# B. Delete all sales where quantity > 15
#    Print: "Deleted X bulk order records"
#
# C. After the changes, SELECT all remaining rows and print them
#
# D. Add a new column "is_commission_paid" using ALTER TABLE:
#    ALTER TABLE sales ADD COLUMN is_commission_paid INTEGER DEFAULT 0
#    Then update all rows where rep_name = "Bob Chen" to set is_commission_paid = 1
#    Print how many of Bob's sales were updated
#
# Expected output:
#   Updated 2 laptop price records
#   Deleted 1 bulk order records
#   [remaining rows printed]
#   Updated 2 Bob Chen commission records




# Always close the connection when done
conn.close()
print("\nDatabase connection closed.")
