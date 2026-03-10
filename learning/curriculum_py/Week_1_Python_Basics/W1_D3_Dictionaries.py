# ══════════════════════════════════════════════════════════════
#  WEEK 1  |  DAY 3  |  DICTIONARIES
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Create a dictionary and understand key-value structure
#  2. Access values using bracket notation and the .get() method
#  3. Add, update, and delete entries in a dictionary
#  4. Loop through a dictionary using .items()
#
#  TIME:  ~40 minutes  (4 concepts × 10 min each)
#
#  YOUTUBE
#  ───────
#  Search: "Python dictionaries for beginners"
#  Search: "Python dictionary methods items get"
#
# ══════════════════════════════════════════════════════════════


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — CREATING A DICTIONARY
# ══════════════════════════════════════════════════════════════
#
#  A dictionary stores data as key-value pairs, enclosed in curly braces {}.
#  Each pair is written as:  "key": value
#  Pairs are separated by commas.
#
#  Syntax:
#    my_dict = {"key1": value1, "key2": value2}
#
#  Keys are usually strings. Values can be any type.
#
#  Dictionary vs List:
#    List:  ordered by position — you access items by index number (0, 1, 2...)
#    Dict:  labeled by name — you access items by key ("name", "price"...)
#
#  Use a dict when each value has a meaningful label (like a row of data).
#
# EXAMPLE ──────────────────────────────────────────────────────

employee = {
    "name":       "Avi Ben-David",
    "age":        41,
    "department": "Data Engineering",
    "salary":     110000.0,
    "is_active":  True
}

print(employee)

# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
#
#  Create a dictionary called product with exactly these keys and values:
#    name      -> "Laptop Pro 15"
#    brand     -> "TechCo"
#    price     -> 4500.0
#    stock     -> 12
#    available -> True
#
#  Print the full dictionary.
#
#  Expected output:
#      {'name': 'Laptop Pro 15', 'brand': 'TechCo', 'price': 4500.0, 'stock': 12, 'available': True}
#






# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — ACCESSING VALUES
# ══════════════════════════════════════════════════════════════
#
#  Two ways to get a value from a dictionary:
#
#  1. Bracket notation:  dict["key"]
#     - Returns the value for that key
#     - Raises a KeyError if the key does not exist
#
#  2. .get() method:  dict.get("key")
#     - Returns the value if the key exists
#     - Returns None if the key does not exist (no crash)
#     - You can provide a fallback:  dict.get("key", "default value")
#
#  Use .get() whenever the key might not be present — it is the safe choice.
#
# EXAMPLE ──────────────────────────────────────────────────────

print(employee["name"])                            # Avi Ben-David
print(employee["salary"])                          # 110000.0
print(employee.get("department"))                  # Data Engineering
print(employee.get("bonus"))                       # None — key does not exist
print(employee.get("bonus", "No bonus data"))      # No bonus data — fallback used

# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
#
#  Using the product dictionary you created in Exercise 1, print:
#    1. The product name using bracket notation
#    2. The price using bracket notation
#    3. The value for the key "category" — use .get() with fallback "Uncategorized"
#
#  Expected output:
#      Laptop Pro 15
#      4500.0
#      Uncategorized
#






# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — ADD, UPDATE, DELETE
# ══════════════════════════════════════════════════════════════
#
#  Dictionaries are mutable — you can change them after creation.
#
#  Add a new key:     dict["new_key"] = value
#  Update a key:      dict["existing_key"] = new_value   (same syntax as add)
#  Delete a key:      del dict["key"]
#
#  Python uses the same syntax for add and update.
#  If the key exists, the value is replaced. If it does not exist, it is created.
#
# EXAMPLE ──────────────────────────────────────────────────────

employee["department"] = "Platform Engineering"   # update existing key
print(employee)

employee["years_at_company"] = 5                  # add new key
print(employee)

del employee["is_active"]                         # delete a key
print(employee)

# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
#
#  Using the product dictionary from Exercise 1, make 3 changes in order:
#    1. Update the price to 3999.99
#    2. Add a new key "category" with value "Electronics"
#    3. Delete the "available" key
#
#  Then print the final dictionary.
#
#  Expected output:
#      {'name': 'Laptop Pro 15', 'brand': 'TechCo', 'price': 3999.99, 'stock': 12, 'category': 'Electronics'}
#






# ══════════════════════════════════════════════════════════════
#  CONCEPT 4 — LOOPING WITH .items()
# ══════════════════════════════════════════════════════════════
#
#  .items() lets you loop through a dictionary and access both
#  the key and the value at the same time.
#
#  Syntax:
#    for key, value in my_dict.items():
#        print(key, value)
#
#  You can also list all keys or all values:
#    my_dict.keys()    — returns all keys
#    my_dict.values()  — returns all values
#
#  Looping with .items() is the most common way to process dict data row by row.
#
# EXAMPLE ──────────────────────────────────────────────────────

monthly_revenue = {"January": 85000, "February": 92000, "March": 78000, "April": 105000}

for month, revenue in monthly_revenue.items():
    print(month + ":", revenue)

print("All months:", list(monthly_revenue.keys()))
print("All revenues:", list(monthly_revenue.values()))

# ══════════════════════════════════════════════════════════════
#  EXERCISE 4
# ══════════════════════════════════════════════════════════════
#
#  Create a dictionary called salaries with exactly these key-value pairs:
#    "Alice"   -> 75000
#    "Bob"     -> 82000
#    "Charlie" -> 68000
#
#  Loop through it using .items() and print each name and salary
#  in the format:   Name: salary
#
#  After the loop, calculate the total of all salaries and print it
#  in the format:   Total payroll: amount
#
#  Expected output:
#      Alice: 75000
#      Bob: 82000
#      Charlie: 68000
#      Total payroll: 225000
#




