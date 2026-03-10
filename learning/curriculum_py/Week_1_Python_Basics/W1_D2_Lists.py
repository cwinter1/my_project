# ══════════════════════════════════════════════════════════════
#  WEEK 1  |  DAY 2  |  LISTS
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Create a list and check its length with len()
#  2. Access individual items using index and negative index
#  3. Modify a list with append(), insert(), and remove()
#  4. Extract a portion of a list using slicing
#
#  TIME:  ~40 minutes  (4 concepts × 10 min each)
#
#  YOUTUBE
#  ───────
#  Search: "Python lists for beginners"
#  Search: "Python list slicing explained"
#
# ══════════════════════════════════════════════════════════════


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — CREATING A LIST
# ══════════════════════════════════════════════════════════════
#
#  A list is an ordered collection of values, enclosed in square brackets [].
#  Items are separated by commas.
#  A list can hold any data type, and even a mix of types.
#
#  Syntax:
#    my_list = [item1, item2, item3]
#
#  Lists are ordered — every item has a position number (called an index).
#  len(my_list) returns the number of items in the list.
#
# EXAMPLE ──────────────────────────────────────────────────────

monthly_sales = [42000, 55000, 38000, 61000, 70000, 48000]   # list of ints
regions       = ["North", "South", "East", "West", "Central"] # list of strings

print(monthly_sales)
print(regions)
print(len(monthly_sales))   # 6
print(len(regions))         # 5

# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
#
#  Create a list called cities containing these 5 strings in this order:
#    "Tel Aviv", "Jerusalem", "Haifa", "Beer Sheva", "Eilat"
#
#  Print the list, then print its length on a separate line.
#
#  Expected output:
#      ['Tel Aviv', 'Jerusalem', 'Haifa', 'Beer Sheva', 'Eilat']
#      5
#






# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — INDEXING
# ══════════════════════════════════════════════════════════════
#
#  Each item in a list has an index — its position number.
#  Indexing starts at 0, not 1.
#
#    list[0]   — first item
#    list[1]   — second item
#    list[-1]  — last item (negative index counts from the end)
#    list[-2]  — second-to-last item
#
#  Accessing an index that does not exist causes an IndexError.
#
# EXAMPLE ──────────────────────────────────────────────────────

print(regions[0])    # North  — first item
print(regions[-1])   # Central — last item
print(regions[1])    # South  — second item

# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
#
#  Using the cities list you created in Exercise 1, print:
#    1. The first city (use index 0)
#    2. The last city (use a negative index)
#    3. The third city (use index 2)
#
#  Expected output:
#      Tel Aviv
#      Eilat
#      Haifa
#






# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — MODIFYING A LIST
# ══════════════════════════════════════════════════════════════
#
#  Lists are mutable — you can change them after creation.
#
#  Three essential methods:
#    list.append(item)          — adds item to the END of the list
#    list.insert(index, item)   — inserts item at a specific position
#    list.remove(item)          — removes the first occurrence of item
#
#  After any modification the list is changed permanently (in memory).
#  Print the list after each step to see the change.
#
# EXAMPLE ──────────────────────────────────────────────────────

products = ["Keyboard", "Monitor", "Mouse"]

products.append("Webcam")          # add to end
print(products)                    # ['Keyboard', 'Monitor', 'Mouse', 'Webcam']

products.insert(1, "USB Hub")      # insert at position 1
print(products)                    # ['Keyboard', 'USB Hub', 'Monitor', 'Mouse', 'Webcam']

products.remove("Monitor")         # remove by value
print(products)                    # ['Keyboard', 'USB Hub', 'Mouse', 'Webcam']

# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
#
#  Starting data is provided below — do not change that line.
#  Perform 3 steps in order, printing the list after each step:
#
#  Step 1: Add "Earbuds" to the end of the list, then print
#  Step 2: Remove "Tablet" from the list, then print
#  Step 3: Insert "Smart Watch" at position 0, then print
#
#  Expected output:
#      ['Laptop', 'Tablet', 'Phone', 'Charger', 'Earbuds']
#      ['Laptop', 'Phone', 'Charger', 'Earbuds']
#      ['Smart Watch', 'Laptop', 'Phone', 'Charger', 'Earbuds']
#

# --- starting data (do not change this line) ---
inventory = ["Laptop", "Tablet", "Phone", "Charger"]






# ══════════════════════════════════════════════════════════════
#  CONCEPT 4 — SLICING
# ══════════════════════════════════════════════════════════════
#
#  Slicing extracts a portion of a list and returns it as a new list.
#
#  Syntax:
#    list[start:end]    — items from index start up to (but NOT including) end
#    list[:end]         — from the beginning up to (not including) end
#    list[start:]       — from start to the end of the list
#    list[-3:]          — last 3 items
#
#  The start index is INCLUSIVE; the end index is EXCLUSIVE.
#  Example: list[1:4] gives items at index 1, 2, 3  — NOT 4.
#
# EXAMPLE ──────────────────────────────────────────────────────

revenue = [10000, 12000, 9000, 14000, 15000, 11000, 13000, 16000, 17000, 18000]

print(revenue[0:4])    # first 4 items: [10000, 12000, 9000, 14000]
print(revenue[-3:])    # last 3 items:  [16000, 17000, 18000]
print(revenue[1:4])    # items at index 1, 2, 3: [12000, 9000, 14000]

# ══════════════════════════════════════════════════════════════
#  EXERCISE 4
# ══════════════════════════════════════════════════════════════
#
#  Starting data is provided below — do not change that line.
#  Using slicing only (no indexing, no loops), print:
#    1. Q1 — the first 3 months
#    2. Q3 — months at index 6, 7, 8
#    3. Last 3 months — use a negative start index
#
#  Print each result labeled as shown in the expected output.
#
#  Expected output:
#      Q1: [42, 55, 38]
#      Q3: [53, 66, 72]
#      Last 3: [80, 45, 90]
#

# --- starting data (do not change this line) ---
sales = [42, 55, 38, 61, 70, 48, 53, 66, 72, 80, 45, 90]




