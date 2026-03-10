# ══════════════════════════════════════════════════════════════
#  WEEK 2  |  DAY 1  |  FUNCTIONS BASICS
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Define and call functions using def and return
#  2. Understand how local and global scope affect variable access
#  3. Compose functions by calling one function from inside another
#
#  TIME:  ~30 minutes  (3 concepts × 10 min each)
#
#  YOUTUBE
#  ───────
#  Search: "Python functions def return explained"
#  Search: "Python local vs global scope variables"
#
# ══════════════════════════════════════════════════════════════


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — DEFINING FUNCTIONS WITH def AND return
# ══════════════════════════════════════════════════════════════
#
#  A function is a reusable block of code that performs a specific task.
#  Define it once, call it as many times as needed.
#
#  Syntax:
#    def function_name(parameter):
#        # body of the function
#        return value
#
#  Rules:
#    - The def keyword starts the definition
#    - Parameters are optional placeholders for input values
#    - return sends a value back to the caller
#    - Without return, the function returns None
#    - Call the function by writing its name followed by parentheses
#
# EXAMPLE ──────────────────────────────────────────────────────

def calculate_annual_salary(monthly_salary):
    # Multiply monthly pay by 12 to get the yearly total
    annual = monthly_salary * 12
    return annual

def format_employee_name(first, last):
    # Combine first and last name into a display-friendly string
    full_name = first + " " + last
    return full_name

# Call the functions and store their results
yearly = calculate_annual_salary(5500)
print(yearly)          # 66000

name = format_employee_name("Maria", "Santos")
print(name)            # Maria Santos

# A function without return still works but produces None
def log_sale(amount):
    print("Sale recorded:", amount)

result = log_sale(250)
print(result)          # None  (nothing was returned)


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
#
#  A sales team tracks revenue as units_sold * unit_price.
#  Write a function called calculate_revenue that takes units_sold
#  and unit_price as parameters and returns the total revenue.
#  Then call it with units_sold=120 and unit_price=49.99 and print the result.
#
#  Expected output:
#      5998.8
#




# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — SCOPE: LOCAL VS GLOBAL VARIABLES
# ══════════════════════════════════════════════════════════════
#
#  Scope determines where a variable can be read or changed.
#
#  LOCAL variable:
#    - Created inside a function
#    - Only visible inside that function
#    - Destroyed when the function finishes
#
#  GLOBAL variable:
#    - Created outside any function, at the module level
#    - Visible everywhere in the file
#    - To modify it inside a function you must declare: global variable_name
#
#  Best practice: avoid modifying globals inside functions.
#                 Pass values in as parameters and return new values instead.
#
# EXAMPLE ──────────────────────────────────────────────────────

company_name = "Acme Corp"   # global variable

def get_department_report(department):
    # department_total is a local variable — only exists here
    department_total = 0
    if department == "Sales":
        department_total = 120000
    elif department == "Engineering":
        department_total = 180000
    # We can READ the global company_name without any special keyword
    report = company_name + " | " + department + " budget: " + str(department_total)
    return report

print(get_department_report("Sales"))
# Acme Corp | Sales budget: 120000

# Demonstrating that local variables are not accessible outside the function
def compute_bonus(salary):
    bonus = salary * 0.10    # local variable
    return bonus

print(compute_bonus(60000))  # 6000.0
# print(bonus)               # This would raise NameError — bonus is not defined here


# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
#
#  The variable tax_rate is defined globally below.
#  Write a function called calculate_net_pay that takes gross_pay as a
#  parameter, reads the global tax_rate, and returns gross_pay after
#  subtracting taxes. Do NOT use the global keyword to modify tax_rate.
#  Call the function with gross_pay=4000 and print the result.
#
#  Expected output:
#      3320.0
#

tax_rate = 0.17   # 17 percent tax




# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — FUNCTIONS THAT CALL OTHER FUNCTIONS (COMPOSITION)
# ══════════════════════════════════════════════════════════════
#
#  You can call one function from inside another function.
#  This is called function composition and is the foundation of clean code.
#  Break a large problem into small, focused functions, then combine them.
#
#  Pattern:
#    def step_a(x): ...
#    def step_b(x): ...
#    def pipeline(x):
#        result_a = step_a(x)
#        result_b = step_b(result_a)
#        return result_b
#
# EXAMPLE ──────────────────────────────────────────────────────

def get_base_price(product_id):
    # Simulate a price lookup — in production this would query a database
    prices = {
        "WIDGET_A": 29.99,
        "WIDGET_B": 49.99,
        "WIDGET_C": 99.99,
    }
    return prices.get(product_id, 0.0)

def apply_discount(price, discount_percent):
    # Reduce price by the given percentage
    discount_amount = price * (discount_percent / 100)
    return price - discount_amount

def add_tax(price, tax_percent=8.5):
    # Add sales tax to the price
    tax_amount = price * (tax_percent / 100)
    return price + tax_amount

def get_final_price(product_id, discount_percent):
    # Compose all three functions into one end-to-end calculation
    base = get_base_price(product_id)                    # step 1: look up price
    discounted = apply_discount(base, discount_percent)  # step 2: apply deal
    final = add_tax(discounted)                          # step 3: add tax
    return round(final, 2)

print(get_final_price("WIDGET_B", 10))   # 48.89
print(get_final_price("WIDGET_C", 25))   # 81.19


# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
#
#  Build a three-function pipeline to calculate total employee compensation.
#
#  Step 1: Write calculate_base_pay(hours_worked, hourly_rate)
#          Returns hours_worked * hourly_rate
#
#  Step 2: Write calculate_overtime_pay(hours_worked, hourly_rate)
#          If hours_worked > 40, overtime hours are paid at 1.5x the hourly_rate.
#          Returns the overtime pay only (0 if no overtime).
#
#  Step 3: Write calculate_total_pay(hours_worked, hourly_rate)
#          Calls both functions above and returns base_pay + overtime_pay.
#
#  Test with hours_worked=48 and hourly_rate=25 and print the result.
#
#  Expected output:
#      Total pay: 1300.0
#




