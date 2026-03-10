# ══════════════════════════════════════════════════════════════
#  WEEK 1  |  DAY 6  |  WEEKLY PROJECT — EMPLOYEE REGISTRY
# ══════════════════════════════════════════════════════════════
#
#  PROJECT GOAL
#  ────────────
#  Build an employee registry for a tech company by working through
#  a list of employee records using variables, lists, dicts,
#  conditionals, and loops.
#
#  SKILLS PRACTICED
#  ─────────────────
#  - Variables and data types (strings, ints, floats, booleans)
#  - Lists of dictionaries
#  - for loops and the accumulator pattern
#  - Conditionals (if / elif / else)
#  - String formatting with f-strings
#
#  TIME:  ~45-60 minutes
#
# ══════════════════════════════════════════════════════════════


# ── SETUP — provided by teacher, do not change ────────────────

employees = [
    {"name": "Alice Chen",    "age": 31, "salary": 95000,  "department": "Engineering", "is_active": True},
    {"name": "Bob Martinez",  "age": 45, "salary": 120000, "department": "Management",  "is_active": True},
    {"name": "Carol Smith",   "age": 28, "salary": 87000,  "department": "Engineering", "is_active": False},
    {"name": "David Kim",     "age": 37, "salary": 103000, "department": "Engineering", "is_active": True},
    {"name": "Eva Nguyen",    "age": 52, "salary": 78000,  "department": "Marketing",   "is_active": False},
]


# ══════════════════════════════════════════════════════════════
#  TASK 1 — Print Name and Department
# ══════════════════════════════════════════════════════════════
#  Loop through the employees list.
#  For each employee, print their name and department on one line
#  using this exact format:
#    Alice Chen — Engineering
#
#  Expected output:
#    Alice Chen — Engineering
#    Bob Martinez — Management
#    Carol Smith — Engineering
#    David Kim — Engineering
#    Eva Nguyen — Marketing
#




# ══════════════════════════════════════════════════════════════
#  TASK 2 — Count Active Employees
# ══════════════════════════════════════════════════════════════
#  Loop through employees and count how many have is_active == True.
#  Use a counter variable that starts at 0 and increases by 1 each
#  time you find an active employee.
#  After the loop, print the result.
#
#  Expected output:
#    Active employees: 3
#




# ══════════════════════════════════════════════════════════════
#  TASK 3 — Find the Highest-Paid Employee
# ══════════════════════════════════════════════════════════════
#  Loop through employees and track the employee with the
#  highest salary.  Use two variables — one for the highest salary
#  seen so far and one for the name that goes with it.
#  Start with highest_salary = 0 and highest_name = "".
#  After the loop, print the result.
#
#  Expected output:
#    Highest paid: Bob Martinez ($120,000)
#




# ══════════════════════════════════════════════════════════════
#  TASK 4 — Filter Engineering Department
# ══════════════════════════════════════════════════════════════
#  Create a new list called engineering that contains only the
#  employee dicts where department == "Engineering".
#  Use a for loop and append.
#  After the loop, print the count and each engineer's name.
#
#  Expected output:
#    Engineering headcount: 3
#    Alice Chen
#    Carol Smith
#    David Kim
#




# ══════════════════════════════════════════════════════════════
#  TASK 5 — Calculate Average Salary
# ══════════════════════════════════════════════════════════════
#  Loop through employees and accumulate the total salary.
#  After the loop, divide by the number of employees to get
#  the average.  Round to 2 decimal places.
#  Print the result.
#
#  Expected output:
#    Average salary: $96,600.00
#




# ══════════════════════════════════════════════════════════════
#  TASK 6 — Print Formatted Summary
# ══════════════════════════════════════════════════════════════
#  Use the values you calculated in Tasks 2, 3, and 5 to print
#  a formatted summary report.  Print exactly this structure
#  (values will match your computed results):
#
#  Expected output:
#    ── Employee Registry Summary ──
#    Total employees : 5
#    Active employees: 3
#    Average salary  : $96,600.00
#    Highest paid    : Bob Martinez
#


