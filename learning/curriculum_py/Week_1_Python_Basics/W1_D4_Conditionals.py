# ══════════════════════════════════════════════════════════════
#  WEEK 1  |  DAY 4  |  CONDITIONALS
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Write if/elif/else chains and understand that only one branch runs
#  2. Use comparison operators to evaluate conditions
#  3. Combine conditions with logical operators: and, or, not
#  4. Check membership using the "in" operator
#
#  TIME:  ~40 minutes  (4 concepts x 10 min each)
#
#  YOUTUBE
#  ───────
#  Search: "Python if elif else for beginners"
#  Search: "Python logical operators and or not"
#
# ══════════════════════════════════════════════════════════════


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 -- if / elif / else
# ══════════════════════════════════════════════════════════════
#
#  Conditionals let your code make decisions -- run different code
#  depending on whether a condition is True or False.
#
#  Syntax:
#    if condition:
#        # runs if condition is True
#    elif another_condition:
#        # runs if the first was False and this one is True
#    else:
#        # runs if ALL above conditions were False
#
#  Rules:
#    - Indentation (4 spaces) marks the code block -- Python requires it
#    - Only ONE branch runs -- as soon as a True condition is found, the rest is skipped
#    - elif and else are optional; you can have as many elif as needed
#
# EXAMPLE ──────────────────────────────────────────────

credit_score = 710

if credit_score >= 750:
    print("Excellent credit")
elif credit_score >= 700:
    print("Good credit")
elif credit_score >= 650:
    print("Fair credit")
else:
    print("Poor credit")

# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
#
#  Starting data is provided below -- do not change that line.
#  Write an if/elif/else chain to classify the temperature:
#    temperature >= 35   -> print "ALERT: Too hot"
#    temperature >= 20   -> print "OK: Normal"
#    temperature >= 5    -> print "WARNING: Cold"
#    anything else       -> print "ALERT: Too cold"
#
#  Expected output:
#      ALERT: Too hot
#

# --- starting data (do not change this line) ---
temperature = 38






# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 -- COMPARISON OPERATORS
# ══════════════════════════════════════════════════════════════
#
#  Comparison operators evaluate two values and return True or False.
#
#    ==   equal to                 5 == 5  -> True
#    !=   not equal to             5 != 3  -> True
#    >    greater than             7 > 3   -> True
#    <    less than                2 < 8   -> True
#    >=   greater than or equal    5 >= 5  -> True
#    <=   less than or equal       4 <= 6  -> True
#
#  Common mistake: using = (assignment) instead of == (comparison).
#    if status = "active":    <- SyntaxError -- wrong
#    if status == "active":   <- correct
#
# EXAMPLE ──────────────────────────────────────────────

employee_status = "active"

if employee_status == "active":
    print("Access granted")
elif employee_status == "suspended":
    print("Access suspended -- contact HR")
else:
    print("Access denied -- unknown status")

# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
#
#  Starting data is provided below -- do not change that line.
#  Write an if/elif/else chain to classify the file size:
#    file_size_mb > 500  -> print "ERROR: Too large to process"
#    file_size_mb > 100  -> print "WARNING: Large file, loading may be slow"
#    file_size_mb > 0    -> print "OK: File ready"
#    anything else       -> print "ERROR: Empty file"
#
#  Expected output:
#      WARNING: Large file, loading may be slow
#

# --- starting data (do not change this line) ---
file_size_mb = 250






# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 -- LOGICAL OPERATORS: and, or, not
# ══════════════════════════════════════════════════════════════
#
#  Logical operators combine multiple conditions into one expression.
#
#    and  -- True only if BOTH sides are True
#           income > 50000 and years_employed >= 2
#
#    or   -- True if AT LEAST ONE side is True
#           is_admin or is_manager
#
#    not  -- flips True to False and False to True
#           not has_bad_debt
#
#  You can chain them:
#    if income > 50000 and years >= 2 and not has_bad_debt:
#
#  Parentheses help readability when mixing and/or:
#    if (role == "admin") or (role == "manager" and dept == "IT"):
#
# EXAMPLE ──────────────────────────────────────────────

income         = 75000
years_employed = 3
has_bad_debt   = False

if income > 50000 and years_employed >= 2 and not has_bad_debt:
    print("Loan approved")
else:
    print("Loan denied")

# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
#
#  Starting data is provided below -- do not change those lines.
#  Write conditional logic to determine the access level:
#    is_manager is True                          -> "Full admin access"
#    role == "engineer" and years_exp >= 3       -> "Full data access"
#    role == "analyst"  and years_exp >= 3       -> "Read + write access"
#    role == "analyst"  and years_exp < 3        -> "Read-only access"
#    anything else                               -> "No access"
#
#  Expected output:
#      Read + write access
#

# --- starting data (do not change these lines) ---
role       = "analyst"
years_exp  = 4
is_manager = False






# ══════════════════════════════════════════════════════════════
#  CONCEPT 4 -- THE "in" OPERATOR
# ══════════════════════════════════════════════════════════════
#
#  The "in" operator checks whether a value exists inside a collection.
#  It returns True or False.
#
#  Works with:
#    - Lists:    "apple" in ["apple", "banana"]  -> True
#    - Strings:  "ERROR" in "Connection ERROR"   -> True
#    - Dicts:    "name" in my_dict               -> checks keys
#
#  "not in" is the opposite: checks that something does NOT exist.
#    ".pdf" not in allowed_formats
#
#  This is cleaner and more readable than chaining multiple == comparisons.
#
# EXAMPLE ──────────────────────────────────────────────

file_ext        = ".csv"
allowed_formats = [".csv", ".xlsx", ".json"]
log_line        = "2024-01-15 ERROR: Connection timeout"

if file_ext in allowed_formats:
    print("File format accepted")
else:
    print("File format rejected")

if "ERROR" in log_line:
    print("Issue found in log:", log_line)

# ══════════════════════════════════════════════════════════════
#  EXERCISE 4
# ══════════════════════════════════════════════════════════════
#
#  Starting data is provided below -- do not change those lines.
#  Write a chain of conditions to classify the file for loading.
#  Check in this exact order:
#    1. If the file extension is NOT in [".csv", ".xlsx"]   -> "SKIP: Unsupported format"
#    2. If row_count == 0                                    -> "SKIP: Empty file"
#    3. If has_nulls is True                                 -> "WARNING: Nulls found, clean before loading"
#    4. Otherwise                                            -> "READY: File OK to load"
#
#  To get the file extension: use file_name.split(".")[-1] then add a dot in front.
#
#  Expected output:
#      WARNING: Nulls found, clean before loading
#

# --- starting data (do not change these lines) ---
file_name = "customers_2024.xlsx"
row_count = 15000
has_nulls = True




