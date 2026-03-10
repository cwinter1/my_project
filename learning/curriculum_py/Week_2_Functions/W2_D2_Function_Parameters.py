# ══════════════════════════════════════════════════════════════
#  WEEK 2  |  DAY 2  |  FUNCTION PARAMETERS
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Distinguish between positional and keyword arguments
#  2. Use default parameter values to make arguments optional
#  3. Accept variable-length arguments using *args and **kwargs
#
#  TIME:  ~30 minutes  (3 concepts × 10 min each)
#
#  YOUTUBE
#  ───────
#  Search: "Python positional keyword arguments explained"
#  Search: "Python args kwargs tutorial"
#
# ══════════════════════════════════════════════════════════════


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — POSITIONAL VS KEYWORD ARGUMENTS
# ══════════════════════════════════════════════════════════════
#
#  When you call a function, you pass arguments to fill the parameters.
#
#  POSITIONAL arguments: matched by their position (order matters)
#  KEYWORD arguments: matched by name (order does not matter)
#
#  Rules:
#    - Positional arguments must come before keyword arguments in a call
#    - Using keyword arguments makes code easier to read
#    - You can mix both in a single call
#
# EXAMPLE ──────────────────────────────────────────────────────

def create_employee_record(name, department, salary):
    # Build a dictionary representing one employee
    return {
        "name": name,
        "department": department,
        "salary": salary,
    }

# Positional — order must match the function signature
rec1 = create_employee_record("Alice Ng", "Engineering", 95000)
print(rec1)
# {'name': 'Alice Ng', 'department': 'Engineering', 'salary': 95000}

# Keyword — order does not matter
rec2 = create_employee_record(salary=72000, name="Bob Chen", department="Sales")
print(rec2)
# {'name': 'Bob Chen', 'department': 'Sales', 'salary': 72000}

# Mix: first argument positional, rest as keyword
rec3 = create_employee_record("Carla Diaz", salary=85000, department="Finance")
print(rec3)
# {'name': 'Carla Diaz', 'department': 'Finance', 'salary': 85000}

def transfer_funds(source_account, destination_account, amount, currency):
    return f"Transfer {amount} {currency} from {source_account} to {destination_account}"

# Keyword arguments make this self-documenting
result = transfer_funds(
    source_account="ACC-001",
    destination_account="ACC-042",
    amount=15000,
    currency="USD",
)
print(result)
# Transfer 15000 USD from ACC-001 to ACC-042


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
#
#  Write a function called create_order that accepts:
#    customer_id, product_name, quantity, unit_price
#
#  It should return a dict with those four keys plus a "total" key
#  (quantity * unit_price).
#
#  Call the function TWICE:
#    1. Using positional arguments: "CUST-007", "Laptop", 3, 899.99
#    2. Using keyword arguments in a different order: unit_price=19.99,
#       quantity=10, customer_id="CUST-012", product_name="USB Cable"
#
#  Print both results.
#
#  Expected output (first call):
#      {'customer_id': 'CUST-007', 'product_name': 'Laptop', 'quantity': 3,
#       'unit_price': 899.99, 'total': 2699.97}
#




# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — DEFAULT PARAMETERS
# ══════════════════════════════════════════════════════════════
#
#  A default parameter gives a parameter a fallback value.
#  The caller can omit that argument and the default will be used.
#
#  Syntax:
#    def func(param=default_value):
#
#  Rules:
#    - Parameters with defaults must come AFTER parameters without defaults
#    - Defaults are evaluated once when the function is defined,
#      so never use a mutable object (list, dict) as a default value
#
# EXAMPLE ──────────────────────────────────────────────────────

def generate_report(dataset_name, rows, format="csv", include_header=True):
    # Build a report configuration dictionary
    config = {
        "dataset": dataset_name,
        "rows": rows,
        "format": format,
        "header": include_header,
    }
    return config

# Only required arguments — defaults apply
r1 = generate_report("sales_q1", 1500)
print(r1)
# {'dataset': 'sales_q1', 'rows': 1500, 'format': 'csv', 'header': True}

# Override one default
r2 = generate_report("inventory", 300, format="json")
print(r2)
# {'dataset': 'inventory', 'rows': 300, 'format': 'json', 'header': True}

# Override both defaults
r3 = generate_report("audit_log", 50, format="txt", include_header=False)
print(r3)
# {'dataset': 'audit_log', 'rows': 50, 'format': 'txt', 'header': False}

def calculate_compound_interest(principal, rate, years, compounding_periods=12):
    # Standard compound interest formula
    amount = principal * (1 + rate / compounding_periods) ** (compounding_periods * years)
    return round(amount, 2)

print(calculate_compound_interest(10000, 0.05, 10))       # 16470.09 (monthly)
print(calculate_compound_interest(10000, 0.05, 10, 1))    # 16288.95 (annual)


# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
#
#  A data pipeline sends email notifications when jobs complete.
#  Write a function called send_notification that accepts:
#    recipient (required)
#    subject (required)
#    priority (default: "normal")
#    send_copy_to_manager (default: False)
#
#  It should return a dict with all four keys.
#
#  Call it three times:
#    1. send_notification("alice@corp.com", "Pipeline complete")
#    2. send_notification("bob@corp.com", "ETL failed", priority="high")
#    3. send_notification("carol@corp.com", "Report ready", priority="low",
#                         send_copy_to_manager=True)
#
#  Print each result.
#
#  Expected output (first call):
#      {'recipient': 'alice@corp.com', 'subject': 'Pipeline complete',
#       'priority': 'normal', 'send_copy_to_manager': False}
#




# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — *args AND **kwargs
# ══════════════════════════════════════════════════════════════
#
#  Sometimes you do not know in advance how many arguments a function will receive.
#
#  *args    — collects extra POSITIONAL arguments into a tuple
#  **kwargs — collects extra KEYWORD arguments into a dict
#
#  Naming convention: "args" and "kwargs" are just convention; the * and ** matter.
#
#  Common use cases:
#    - Functions that accept a variable number of data columns
#    - Building wrappers around other functions
#    - Creating flexible configuration builders
#
# EXAMPLE ──────────────────────────────────────────────────────

def sum_sales_figures(*amounts):
    # amounts is a tuple of all positional arguments passed in
    total = 0
    for amount in amounts:
        total += amount
    return total

print(sum_sales_figures(100, 200, 300))           # 600
print(sum_sales_figures(5000, 12000, 8500, 3200)) # 28700

def build_pipeline_config(pipeline_name, **settings):
    # settings is a dict of all keyword arguments passed in
    config = {"name": pipeline_name}
    config.update(settings)
    return config

cfg1 = build_pipeline_config("daily_sales_etl", schedule="06:00", retries=3)
print(cfg1)
# {'name': 'daily_sales_etl', 'schedule': '06:00', 'retries': 3}

cfg2 = build_pipeline_config(
    "inventory_sync",
    schedule="hourly",
    source="erp_db",
    destination="warehouse_db",
    notify_on_failure=True,
)
print(cfg2)
# {'name': 'inventory_sync', 'schedule': 'hourly', 'source': 'erp_db',
#  'destination': 'warehouse_db', 'notify_on_failure': True}

# Combining *args and **kwargs in the same function
def log_event(event_type, *messages, **metadata):
    # event_type is positional, messages collects extra strings,
    # metadata collects extra keyword info
    print(f"[{event_type}]", " | ".join(messages))
    for key, value in metadata.items():
        print(f"  {key}: {value}")

log_event("INFO", "Pipeline started", "Reading source files",
          pipeline_id="PL-44", user="admin")
# [INFO] Pipeline started | Reading source files
#   pipeline_id: PL-44
#   user: admin


# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
#
#  Write a function called build_summary_report that:
#    - Takes report_title as a required first argument (string)
#    - Accepts any number of numeric values via *args (monthly figures)
#    - Accepts any keyword arguments via **kwargs (metadata tags)
#
#  The function should return a dict with:
#    "title"   : the report_title
#    "months"  : how many figures were passed in *args
#    "total"   : sum of all *args values
#    "average" : total / months (rounded to 2 decimal places), or 0 if no months
#    plus all the kwargs key-value pairs merged into the dict
#
#  Call it with:
#    build_summary_report("Q1 Revenue", 45000, 52000, 61000,
#                         region="West", analyst="Jess Tran")
#
#  Expected output:
#      {'title': 'Q1 Revenue', 'months': 3, 'total': 158000,
#       'average': 52666.67, 'region': 'West', 'analyst': 'Jess Tran'}
#




