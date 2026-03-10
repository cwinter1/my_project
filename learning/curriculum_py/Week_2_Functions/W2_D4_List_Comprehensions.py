# ══════════════════════════════════════════════════════════════
#  WEEK 2  |  DAY 4  |  LIST COMPREHENSIONS
# ══════════════════════════════════════════════════════════════
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Write a basic list comprehension to transform a list in one line
#  2. Add a conditional filter to a list comprehension
#  3. Build dictionary comprehensions to create dicts from iterable data
#
#  TIME:  ~30-35 minutes
#
#  YOUTUBE
#  ───────
#  Search: "Python list comprehension tutorial"
#  Search: "Python dict comprehension examples"
# ══════════════════════════════════════════════════════════════


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — BASIC LIST COMPREHENSION  [x for x in list]
# ══════════════════════════════════════════════════════════════
# A list comprehension builds a new list by applying an expression
# to every item in an existing iterable.
#
# Syntax:
#   new_list = [expression for item in iterable]
#
# This is equivalent to:
#   new_list = []
#   for item in iterable:
#       new_list.append(expression)
#
# List comprehensions are faster and more readable for simple transformations.

# EXAMPLE ──────────────────────────────────────────────────────
# Raw employee salary data from a spreadsheet import
salaries_raw = [72000, 85000, 91000, 67500, 110000, 54000, 98000]

# Apply a 5% raise to every salary
salaries_raised = [s * 1.05 for s in salaries_raw]
print(salaries_raised)
# [75600.0, 89250.0, 95550.0, 70875.0, 115500.0, 56700.0, 102900.0]

# Convert department names to uppercase for a report header
departments = ["sales", "engineering", "finance", "operations", "hr"]
departments_upper = [d.upper() for d in departments]
print(departments_upper)
# ['SALES', 'ENGINEERING', 'FINANCE', 'OPERATIONS', 'HR']

# Extract just the year from a list of date strings
dates = ["2024-01-15", "2024-03-22", "2024-07-08", "2023-11-30"]
years = [d[:4] for d in dates]
print(years)
# ['2024', '2024', '2024', '2023']

# Calculate monthly totals from a list of weekly figures (4 weeks per month)
weekly_sales = [12000, 15000, 11000, 14000, 9000, 13000, 16000, 10000]
monthly_totals = [sum(weekly_sales[i:i+4]) for i in range(0, len(weekly_sales), 4)]
print(monthly_totals)
# [52000, 48000]


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
# A pipeline returns product names with extra whitespace and inconsistent casing.
# Use a list comprehension to clean the list:
#   - Strip whitespace from each name (.strip())
#   - Convert to title case (.title())
#
# Expected output:
#   ['Laptop', 'Usb Cable', 'Monitor', 'Keyboard', 'Mouse']

raw_products = ["  laptop  ", "USB CABLE", " monitor", "KEYBOARD ", "  mouse  "]




# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — FILTERED COMPREHENSION  [x for x in list if condition]
# ══════════════════════════════════════════════════════════════
# Add an if clause to include only items that meet a condition.
#
# Syntax:
#   new_list = [expression for item in iterable if condition]
#
# Only items where the condition is True are included in the result.
# The if clause acts as a filter — it does not change the values.

# EXAMPLE ──────────────────────────────────────────────────────
# Keep only high-value orders (over $5000) for a VIP report
orders = [1200, 8500, 340, 6700, 4999, 5001, 12000, 450, 7800]
high_value_orders = [o for o in orders if o > 5000]
print(high_value_orders)
# [8500, 6700, 5001, 12000, 7800]

# Extract active employees only
employees = [
    {"name": "Alice", "status": "active", "salary": 92000},
    {"name": "Bob",   "status": "inactive", "salary": 75000},
    {"name": "Carol", "status": "active", "salary": 88000},
    {"name": "Dave",  "status": "on_leave", "salary": 81000},
    {"name": "Eve",   "status": "active", "salary": 95000},
]

active_names = [e["name"] for e in employees if e["status"] == "active"]
print(active_names)
# ['Alice', 'Carol', 'Eve']

# Filter and transform at the same time: get salary*1.1 for high earners
high_earner_raises = [e["salary"] * 1.1 for e in employees
                      if e["status"] == "active" and e["salary"] > 90000]
print(high_earner_raises)
# [101200.0, 104500.0]

# Remove empty or null values from an import
raw_ids = ["EMP001", "", "EMP002", None, "EMP003", "  ", "EMP004"]
clean_ids = [id.strip() for id in raw_ids if id and id.strip()]
print(clean_ids)
# ['EMP001', 'EMP002', 'EMP003', 'EMP004']


# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
# A sales pipeline export contains deals at various stages.
# Use a filtered list comprehension to answer both questions below.
#
# Task A: Build a list of deal names where stage == "closed_won"
# Task B: Build a list of values for deals in "negotiation" stage
#         where value > 30000
#
# Expected output:
#   ['Deal A', 'Deal C', 'Deal E']
#   [55000]

pipeline = [
    {"deal": "Deal A", "stage": "closed_won",  "value": 45000},
    {"deal": "Deal B", "stage": "negotiation", "value": 22000},
    {"deal": "Deal C", "stage": "closed_won",  "value": 67000},
    {"deal": "Deal D", "stage": "prospecting", "value": 8000},
    {"deal": "Deal E", "stage": "closed_won",  "value": 31000},
    {"deal": "Deal F", "stage": "negotiation", "value": 55000},
]




# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — DICT COMPREHENSION  {k: v for k, v in items}
# ══════════════════════════════════════════════════════════════
# A dict comprehension builds a dictionary from an iterable in one expression.
#
# Syntax:
#   new_dict = {key_expr: value_expr for item in iterable}
#   new_dict = {key_expr: value_expr for item in iterable if condition}
#
# Common use cases:
#   - Inverting a lookup table (swap keys and values)
#   - Building an index from a list of records
#   - Transforming values in a dict while keeping the same keys

# EXAMPLE ──────────────────────────────────────────────────────
# Build an index mapping employee ID to name for fast lookups
employee_list = [
    {"id": "E001", "name": "Alice Ng",   "dept": "Engineering"},
    {"id": "E002", "name": "Bob Chen",   "dept": "Sales"},
    {"id": "E003", "name": "Carol Diaz", "dept": "Finance"},
    {"id": "E004", "name": "Dave Park",  "dept": "Engineering"},
]

id_to_name = {e["id"]: e["name"] for e in employee_list}
print(id_to_name)
# {'E001': 'Alice Ng', 'E002': 'Bob Chen', 'E003': 'Carol Diaz', 'E004': 'Dave Park'}

# Invert a product code lookup table
code_to_product = {"P100": "Laptop", "P101": "Monitor", "P102": "Keyboard"}
product_to_code = {v: k for k, v in code_to_product.items()}
print(product_to_code)
# {'Laptop': 'P100', 'Monitor': 'P101', 'Keyboard': 'P102'}

# Apply a 10% discount to all prices in a pricing dict
prices = {"Laptop": 999.99, "Monitor": 349.99, "Keyboard": 89.99, "Mouse": 39.99}
discounted = {product: round(price * 0.90, 2) for product, price in prices.items()}
print(discounted)
# {'Laptop': 899.99, 'Monitor': 314.99, 'Keyboard': 80.99, 'Mouse': 35.99}

# Build a dict of department name to total payroll, filtered to > $200k
payroll_data = [
    {"dept": "Engineering", "salary": 95000},
    {"dept": "Sales",       "salary": 72000},
    {"dept": "Engineering", "salary": 88000},
    {"dept": "Finance",     "salary": 81000},
    {"dept": "Sales",       "salary": 67000},
]

# First aggregate by department
totals = {}
for row in payroll_data:
    dept = row["dept"]
    totals[dept] = totals.get(dept, 0) + row["salary"]

# Then filter with a dict comprehension
high_payroll = {dept: total for dept, total in totals.items() if total > 150000}
print(high_payroll)
# {'Engineering': 183000}


# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
# A product catalog is stored as a list of dicts.
# Complete two tasks using dict comprehensions.
#
# Task A: Build a dict mapping SKU -> price for all in-stock products only
# Task B: Build a dict mapping name -> price_with_tax (price * 1.08, rounded to 2)
#         for ALL products regardless of stock status
#
# Expected output (Task A):
#   {'SKU-001': 19.99, 'SKU-003': 89.99, 'SKU-004': 129.99}
#
# Expected output (Task B):
#   {'Widget A': 21.59, 'Widget B': 37.79, 'Gadget X': 97.19,
#    'Gadget Y': 140.39, 'Component Z': 10.79}

products = [
    {"sku": "SKU-001", "name": "Widget A",    "price": 19.99,  "in_stock": True},
    {"sku": "SKU-002", "name": "Widget B",    "price": 34.99,  "in_stock": False},
    {"sku": "SKU-003", "name": "Gadget X",    "price": 89.99,  "in_stock": True},
    {"sku": "SKU-004", "name": "Gadget Y",    "price": 129.99, "in_stock": True},
    {"sku": "SKU-005", "name": "Component Z", "price": 9.99,   "in_stock": False},
]


