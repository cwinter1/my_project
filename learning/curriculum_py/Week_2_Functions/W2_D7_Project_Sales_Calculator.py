# ══════════════════════════════════════════════════════════════
#  WEEK 2  |  DAY 7  |  WEEKLY PROJECT — SALES CALCULATOR
# ══════════════════════════════════════════════════════════════
#
#  PROJECT GOAL
#  ────────────
#  Build a reusable sales calculator for a sales team's monthly
#  reports — writing functions, using default parameters, and
#  adding error handling.
#
#  SKILLS PRACTICED
#  ─────────────────
#  - Defining and calling functions
#  - Parameters and return values
#  - Default parameter values
#  - Raising and handling exceptions (ValueError, TypeError)
#  - Loops inside functions
#  - List comprehensions
#  - Working with lists of dicts
#
#  TIME:  ~45-60 minutes
#
# ══════════════════════════════════════════════════════════════


# ── SETUP — provided by teacher, do not change ────────────────

sales = [
    {"product": "Laptop Pro",    "units_sold": 42,  "unit_price": 1299.99, "region": "West"},
    {"product": "Wireless Mouse","units_sold": 130, "unit_price": 49.99,   "region": "East"},
    {"product": "USB Hub",       "units_sold": 95,  "unit_price": 34.99,   "region": "West"},
    {"product": "Laptop Pro",    "units_sold": 28,  "unit_price": 1299.99, "region": "East"},
    {"product": "Webcam HD",     "units_sold": 60,  "unit_price": 89.99,   "region": "North"},
    {"product": "Wireless Mouse","units_sold": 85,  "unit_price": 49.99,   "region": "West"},
    {"product": "Webcam HD",     "units_sold": 45,  "unit_price": 89.99,   "region": "East"},
    {"product": "USB Hub",       "units_sold": 110, "unit_price": 34.99,   "region": "North"},
]


# ══════════════════════════════════════════════════════════════
#  TASK 1 — calculate_revenue(units_sold, unit_price)
# ══════════════════════════════════════════════════════════════
#  Write a function called calculate_revenue that takes two
#  parameters: units_sold and unit_price.
#  It should return the product of the two values.
#
#  Test it with these calls and print each result:
#    calculate_revenue(42, 1299.99)
#    calculate_revenue(130, 49.99)
#
#  Expected output:
#    54599.58
#    6498.7
#




# ══════════════════════════════════════════════════════════════
#  TASK 2 — top_product(sales_list)
# ══════════════════════════════════════════════════════════════
#  Write a function called top_product that takes the sales list
#  as its only parameter.
#
#  Inside the function:
#    - Build a dict that maps each product name to its total
#      revenue across all rows (use calculate_revenue from Task 1)
#    - Find and return the product name with the highest total revenue
#
#  Call the function with the provided sales list and print the result.
#
#  Expected output:
#    Top product by revenue: Laptop Pro
#




# ══════════════════════════════════════════════════════════════
#  TASK 3 — revenue_by_region(sales_list)
# ══════════════════════════════════════════════════════════════
#  Write a function called revenue_by_region that takes the sales
#  list as its only parameter.
#
#  Inside the function:
#    - Build a dict that maps each region name to its total revenue
#    - Return the dict
#
#  Call the function and print each region and its revenue, rounded
#  to 2 decimal places, one per line.
#
#  Expected output:
#    East  : $86,952.24
#    North : $9,288.55
#    West  : $64,024.39
#  (Regions may print in any order — exact totals depend on the data.)
#




# ══════════════════════════════════════════════════════════════
#  TASK 4 — apply_discount(price, discount_percent=10)
# ══════════════════════════════════════════════════════════════
#  Write a function called apply_discount that takes two parameters:
#    price            -- the original price
#    discount_percent -- the percentage to deduct (default: 10)
#
#  It should return the discounted price rounded to 2 decimal places.
#  Formula: price - (price * discount_percent / 100)
#
#  Test with these calls and print each result:
#    apply_discount(1299.99)           # uses default 10%
#    apply_discount(1299.99, 15)       # 15% discount
#    apply_discount(49.99, 5)          # 5% discount
#
#  Expected output:
#    1169.99
#    1104.99
#    47.49
#




# ══════════════════════════════════════════════════════════════
#  TASK 5 — Add Error Handling to calculate_revenue
# ══════════════════════════════════════════════════════════════
#  Rewrite calculate_revenue so that it raises a ValueError with
#  a descriptive message if either units_sold or unit_price is
#  negative.
#
#  Test your error handling with a try/except block:
#    try:
#        print(calculate_revenue(-5, 99.99))
#    except ValueError as e:
#        print("Error caught:", e)
#
#  Also confirm valid calls still work:
#    print(calculate_revenue(10, 49.99))
#
#  Expected output:
#    Error caught: units_sold cannot be negative
#    499.9
#




# ══════════════════════════════════════════════════════════════
#  TASK 6 — Full Report
# ══════════════════════════════════════════════════════════════
#  Call all five functions using the provided sales list and
#  print a formatted summary report.  Use the results you have
#  already computed where possible.
#
#  Expected output format:
#    ── Monthly Sales Report ──
#    Top product         : Laptop Pro
#    Discounted top price: $1,169.99
#    Revenue by region   :
#      East  : $86,952.24
#      North : $9,288.55
#      West  : $64,024.39
#    Total revenue       : $160,265.18
#  (Region order and exact totals depend on your calculations.)
#


