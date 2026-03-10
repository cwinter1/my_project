# ══════════════════════════════════════════════════════════════
#  WEEK 2  |  DAY 3  |  ERROR HANDLING
# ══════════════════════════════════════════════════════════════
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Catch and handle runtime errors using try/except
#  2. Handle multiple specific exception types to give useful error messages
#  3. Use finally for cleanup and raise to signal errors intentionally
#
#  TIME:  ~30-35 minutes
#
#  YOUTUBE
#  ───────
#  Search: "Python try except error handling tutorial"
#  Search: "Python raise custom exceptions finally"
# ══════════════════════════════════════════════════════════════


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — try / except BASICS
# ══════════════════════════════════════════════════════════════
# When Python encounters an error (exception) it normally stops and crashes.
# A try/except block lets you catch that error and decide what to do instead.
#
# Syntax:
#   try:
#       # code that might fail
#   except ExceptionType:
#       # what to do when it fails
#
# Rules:
#   - The try block runs first
#   - If an exception occurs, Python jumps to the matching except block
#   - If no exception occurs, the except block is skipped
#   - Using bare "except:" catches everything — avoid it; be specific

# EXAMPLE ──────────────────────────────────────────────────────
def parse_sale_amount(raw_value):
    # Data from a CSV often arrives as a string like "$1,500.00"
    # We need to strip formatting and convert to float
    try:
        cleaned = raw_value.replace("$", "").replace(",", "")
        return float(cleaned)
    except ValueError:
        # Triggered when the string cannot be converted to a number
        print(f"Could not parse '{raw_value}' as a number. Returning 0.0")
        return 0.0

print(parse_sale_amount("$1,250.00"))   # 1250.0
print(parse_sale_amount("$3,800.50"))   # 3800.5
print(parse_sale_amount("N/A"))         # prints warning, returns 0.0
print(parse_sale_amount(""))            # prints warning, returns 0.0

def divide_metrics(numerator, denominator):
    # Used when computing ratios like conversion rate = conversions / clicks
    try:
        return numerator / denominator
    except ZeroDivisionError:
        print("Cannot divide by zero — denominator is 0.")
        return None

print(divide_metrics(500, 1000))   # 0.5
print(divide_metrics(500, 0))      # prints warning, returns None


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
# A database export sometimes has employee IDs stored as strings,
# but some rows are corrupted and contain text like "ERR" or blank strings.
#
# Write a function called safe_parse_id that takes raw_id (a string)
# and returns it as an integer.
# If conversion fails (ValueError), print a warning and return -1.
#
# Test with: "1042", "2081", "ERR", "", "3500"
#
# Expected output:
#   1042
#   2081
#   Warning: could not convert 'ERR' to int. Using -1.
#   -1
#   Warning: could not convert '' to int. Using -1.
#   -1
#   3500




# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — MULTIPLE EXCEPTION TYPES
# ══════════════════════════════════════════════════════════════
# A single try block can have multiple except clauses to handle different errors.
#
# Common exception types in data work:
#   ValueError       — wrong type of value (e.g. converting "abc" to int)
#   TypeError        — wrong type of object (e.g. adding str + int)
#   FileNotFoundError — file or path does not exist
#   KeyError         — dictionary key not found
#   IndexError       — list index out of range
#   ZeroDivisionError — dividing by zero
#
# You can also catch multiple exceptions in one line:
#   except (ValueError, TypeError):

# EXAMPLE ──────────────────────────────────────────────────────
def load_config(config_dict, key):
    # Safely retrieve a config value and convert it to integer
    try:
        raw = config_dict[key]         # may raise KeyError
        return int(raw)                # may raise ValueError or TypeError
    except KeyError:
        print(f"Config key '{key}' not found. Using default 0.")
        return 0
    except (ValueError, TypeError):
        print(f"Config value '{config_dict.get(key)}' cannot be converted to int.")
        return 0

config = {"max_retries": "5", "timeout": "thirty", "batch_size": 100}

print(load_config(config, "max_retries"))   # 5
print(load_config(config, "timeout"))       # prints warning, returns 0
print(load_config(config, "batch_size"))    # 100
print(load_config(config, "missing_key"))   # prints warning, returns 0

def read_pipeline_file(filepath):
    # Attempt to open and read a pipeline definition file
    try:
        with open(filepath, "r") as f:
            return f.read()
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return None
    except PermissionError:
        print(f"Permission denied reading: {filepath}")
        return None

content = read_pipeline_file("pipelines/daily_etl.yaml")
# File not found: pipelines/daily_etl.yaml
print(content)   # None


# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
# A CSV row arrives as a dict. Write a function called process_row that:
#   1. Reads row["units"] — may raise KeyError if column is missing
#   2. Reads row["price"] — may raise KeyError
#   3. Multiplies units * price — may raise TypeError if either is None
#   4. Returns the product (units * price)
#
# Handle each error separately:
#   KeyError   -> print which column is missing, return None
#   TypeError  -> print "Multiplication failed due to invalid type", return None
#
# Test with these rows:
#   {"units": 10, "price": 29.99}          -> 299.9
#   {"units": 5}                           -> KeyError for 'price'
#   {"price": 15.00}                       -> KeyError for 'units'
#   {"units": None, "price": 10.00}        -> TypeError
#
# Expected output:
#   299.9
#   Missing column: 'price'
#   None
#   Missing column: 'units'
#   None
#   Multiplication failed due to invalid type
#   None




# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — finally AND raise
# ══════════════════════════════════════════════════════════════
# FINALLY:
#   The finally block runs regardless of whether an exception occurred or not.
#   Use it to clean up resources: close files, release connections, log completion.
#
# RAISE:
#   Use raise to throw an exception intentionally.
#   This is useful when you detect invalid data and want to stop execution.
#   You can raise built-in exceptions or create custom ones.
#
# Syntax:
#   raise ValueError("Descriptive error message here")

# EXAMPLE ──────────────────────────────────────────────────────
def connect_to_database(host, port):
    # Simulate opening a database connection
    connection = {"host": host, "port": port, "open": True}
    print(f"Connection opened to {host}:{port}")
    return connection

def close_database(connection):
    # Always close the connection when done
    connection["open"] = False
    print("Connection closed.")

def run_query(connection, query):
    # Use finally to guarantee the connection is closed even if the query fails
    try:
        if "DROP" in query.upper():
            raise ValueError("Dangerous query blocked: " + query)
        print(f"Running query: {query}")
        return [{"id": 1, "name": "Sales Report"}, {"id": 2, "name": "Inventory"}]
    except ValueError as e:
        print(f"Query error: {e}")
        return None
    finally:
        # This line runs whether the query succeeded or raised an error
        close_database(connection)

conn = connect_to_database("db.corp.com", 1433)
results = run_query(conn, "SELECT * FROM reports")
print(results)
print()

conn2 = connect_to_database("db.corp.com", 1433)
results2 = run_query(conn2, "DROP TABLE customers")
print(results2)

# Using raise to enforce data validation
def validate_batch_size(batch_size):
    # A batch size must be a positive integer no larger than 10000
    if not isinstance(batch_size, int):
        raise TypeError(f"batch_size must be an integer, got {type(batch_size).__name__}")
    if batch_size <= 0:
        raise ValueError(f"batch_size must be positive, got {batch_size}")
    if batch_size > 10000:
        raise ValueError(f"batch_size exceeds maximum of 10000, got {batch_size}")
    return True

try:
    validate_batch_size(500)
    print("Batch size is valid.")    # Batch size is valid.
except (TypeError, ValueError) as e:
    print("Validation failed:", e)

try:
    validate_batch_size(-50)
except ValueError as e:
    print("Validation failed:", e)   # Validation failed: batch_size must be positive, got -50


# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
# Write a function called run_pipeline_step that:
#   1. Accepts step_name (str) and row_count (int)
#   2. Uses raise to enforce: row_count must be >= 0 (raise ValueError if not)
#   3. Uses raise to enforce: step_name must be a non-empty string (raise TypeError if not)
#   4. If both checks pass, prints "Running step: <step_name> on <row_count> rows"
#      and returns True
#   5. Wrap THREE calls to this function in try/except blocks:
#      a. run_pipeline_step("extract", 1500)   -> valid
#      b. run_pipeline_step("transform", -10)  -> invalid row count
#      c. run_pipeline_step("", 500)           -> invalid step name
#   6. In each except block, print the error message.
#   7. Use a finally block inside run_pipeline_step that always prints
#      "Step check complete."
#
# Expected output:
#   Step check complete.
#   Running step: extract on 1500 rows
#   Step check complete.
#   Validation failed: row_count cannot be negative
#   Step check complete.
#   Validation failed: step_name must be a non-empty string


