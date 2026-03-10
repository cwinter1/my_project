# ══════════════════════════════════════════════════════════════
#  WEEK 1  |  DAY 1  |  VARIABLES AND DATA TYPES
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Create and name variables using Python snake_case convention
#  2. Identify the 4 core data types: str, int, float, bool
#  3. Use the type() function to inspect and verify data types
#
#  TIME:  ~30 minutes  (3 concepts × 10 min each)
#
#  YOUTUBE
#  ───────
#  Search: "Python variables and data types for beginners"
#  Search: "Python type() function explained"
#
# ══════════════════════════════════════════════════════════════


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — VARIABLES
# ══════════════════════════════════════════════════════════════
#
#  A variable is a named container that stores a value in memory.
#  You create one with a single = sign:  name = value
#
#  Naming rules (snake_case convention):
#    - All lowercase letters
#    - Words separated by underscores
#    - Must start with a letter or underscore, NOT a number
#    - No spaces or special characters (except underscore)
#
#  Good names:  employee_name, total_sales, is_active, record_count
#  Bad names:   Employee Name, 1stValue, total-sales, TotalSales
#
#  You can reassign a variable at any time — the new value replaces the old one.
#  Python figures out the type automatically; you do not declare it yourself.
#
# EXAMPLE ──────────────────────────────────────────────────────

employee_name   = "Sarah Levi"   # text value — wrap in quotes
employee_age    = 34             # whole number — no quotes
employee_salary = 95000.0        # decimal number — no quotes
is_active       = True           # True/False — capital first letter, no quotes

print(employee_name)
print(employee_age)
print(employee_salary)
print(is_active)

# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
#
#  Create 4 variables with these exact names and values:
#    customer_name  = "David Cohen"
#    customer_age   = 45
#    credit_score   = 720.5
#    is_premium     = True
#
#  Then print each variable on its own line (4 print statements).
#
#  Expected output:
#      David Cohen
#      45
#      720.5
#      True
#






# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — THE 4 CORE DATA TYPES
# ══════════════════════════════════════════════════════════════
#
#  Python has 4 basic data types you will use constantly in data work:
#
#    str   — text, enclosed in quotes:  "hello",  "123",  "True"
#    int   — whole number, no decimal:  42,  -7,  0
#    float — decimal number:  3.14,  100.0,  -0.5
#    bool  — exactly two values:  True  or  False  (capital first letter, no quotes)
#
#  COMMON MISTAKE 1: putting a number inside quotes makes it a string, not a number.
#    price = "29.99"  — this is str — you CANNOT do math with it
#    price =  29.99   — this is float — you CAN do math with it
#
#  COMMON MISTAKE 2: forgetting quotes around text values.
#    city = Tel Aviv   — Python crashes (it looks for a variable named Tel)
#    city = "Tel Aviv" — correct
#
# EXAMPLE ──────────────────────────────────────────────────────

product_name   = "Wireless Mouse"   # str   — text in quotes
product_price  = 49.99              # float — decimal, no quotes
units_in_stock = 200                # int   — whole number, no quotes
is_available   = True               # bool  — capital T, no quotes

print(product_name)
print(product_price)
print(units_in_stock)
print(is_available)

# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
#
#  The 4 lines below contain 2 type mistakes.
#  Copy all 4 lines into your exercise area, fix the 2 wrong ones,
#  then print all 4 variables.
#
#  Lines to copy and fix:
#    order_id      = "10042"    <- WRONG type — should be an integer
#    order_total   = 250.75     <- correct
#    customer_city = Tel Aviv   <- WRONG — will crash, add the missing quotes
#    is_shipped    = True       <- correct
#
#  Expected output:
#      10042
#      250.75
#      Tel Aviv
#      True
#






# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — THE type() FUNCTION
# ══════════════════════════════════════════════════════════════
#
#  type(value) returns the data type of any value or variable.
#  Output looks like:  <class 'str'>  or  <class 'int'>  etc.
#
#  When to use it:
#    - When you receive data from a file or API and need to confirm types
#    - When a number looks correct but behaves unexpectedly — type() reveals the truth
#    - When debugging: "why can't I do math on this number?"
#
#  You can combine type() with print() to show value and type on one line:
#    print(value, "->", type(value))
#
#  This pattern is extremely common in data cleaning and debugging.
#
# EXAMPLE ──────────────────────────────────────────────────────

# Print just the type of each employee variable
print(type(employee_name))      # <class 'str'>
print(type(employee_age))       # <class 'int'>
print(type(employee_salary))    # <class 'float'>
print(type(is_active))          # <class 'bool'>

# Print value and type together on one line
print(employee_name,    "->", type(employee_name))
print(employee_age,     "->", type(employee_age))
print(employee_salary,  "->", type(employee_salary))
print(is_active,        "->", type(is_active))

# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
#
#  Five variables are defined for you below as starting data — do not change them.
#  Print each one in the format:   value -> type
#  Use the same pattern shown in the example above.
#
#  Expected output:
#      2024 -> <class 'str'>
#      2024 -> <class 'int'>
#      20.24 -> <class 'float'>
#      True -> <class 'str'>
#      True -> <class 'bool'>
#

# --- starting data (do not change these lines) ---
field_a = "2024"
field_b = 2024
field_c = 20.24
field_d = "True"
field_e = True




