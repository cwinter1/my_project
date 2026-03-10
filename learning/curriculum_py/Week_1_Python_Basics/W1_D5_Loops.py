# ══════════════════════════════════════════════════════════════
#  WEEK 1  |  DAY 5  |  LOOPS
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Loop over a list and a range with a for loop
#  2. Use the accumulator pattern to calculate totals while looping
#  3. Control loop flow with break and continue
#  4. Use a while loop to repeat until a condition is met
#
#  TIME:  ~40 minutes  (4 concepts x 10 min each)
#
#  YOUTUBE
#  ───────
#  Search: "Python for loop and range beginners"
#  Search: "Python while loop break continue explained"
#
# ══════════════════════════════════════════════════════════════


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 -- for LOOP OVER A LIST AND range()
# ══════════════════════════════════════════════════════════════
#
#  A for loop repeats a block of code once for each item in a sequence.
#
#  Looping over a list:
#    for item in my_list:
#        print(item)        <- runs once per item
#
#  Looping with range():
#    range(5)        -> 0, 1, 2, 3, 4
#    range(1, 6)     -> 1, 2, 3, 4, 5
#    range(0, 10, 2) -> 0, 2, 4, 6, 8
#
#  The variable after "for" takes the value of each item in turn.
#  You can name it anything; convention is to use a meaningful singular noun.
#
# EXAMPLE ──────────────────────────────────────────────

regions = ["North", "South", "East", "West"]

for region in regions:             # loop through a list
    print(region)

for i in range(1, 4):              # loop through a range
    print("Loading file_" + str(i) + ".csv")

# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
#
#  Starting data is provided below -- do not change that line.
#  Loop through the columns list and print each column name on its own line.
#  After the loop ends, print "Total columns: 5" on a separate line.
#
#  Expected output:
#      customer_id
#      name
#      email
#      city
#      signup_date
#      Total columns: 5
#

# --- starting data (do not change this line) ---
columns = ["customer_id", "name", "email", "city", "signup_date"]






# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 -- ACCUMULATOR PATTERN
# ══════════════════════════════════════════════════════════════
#
#  A common pattern in loops: start with a counter or total at zero,
#  then add to it on each iteration.
#
#    total = 0
#    for value in my_list:
#        total += value    <- shorthand for: total = total + value
#
#  You can track multiple things at once:
#    total = 0
#    count = 0
#    for value in my_list:
#        total += value
#        count += 1
#
#  After the loop you can calculate derived values like average = total / count.
#
# EXAMPLE ──────────────────────────────────────────────

monthly_sales = [42000, 55000, 38000, 61000, 70000, 48000]

total = 0
count = 0
for sale in monthly_sales:
    total += sale
    count += 1

print("Total sales:", total)
print("Months:", count)
print("Average:", total / count)

# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
#
#  Starting data is provided below -- do not change that line.
#  Loop through the transactions list.
#  Skip any negative values (they are refunds -- ignore them).
#  Count the positive transactions and sum them.
#  After the loop print the count and total on separate lines.
#
#  Expected output:
#      Positive transactions: 6
#      Total revenue: 3625
#

# --- starting data (do not change this line) ---
transactions = [250, -50, 800, -200, 1500, 75, -30, 400, 600, -100]






# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 -- break AND continue
# ══════════════════════════════════════════════════════════════
#
#  break and continue give you control over the loop flow.
#
#  continue  -- skip the rest of the current iteration and move to the next item
#               useful for skipping bad or irrelevant data
#
#  break     -- exit the loop immediately, even if items remain
#               useful for stopping as soon as you find what you need
#
#  Both only affect the innermost loop they are in.
#
# EXAMPLE ──────────────────────────────────────────────

# break: stop at the first ERROR in a log
log_entries = ["INFO: start", "INFO: loaded", "ERROR: timeout", "INFO: retry"]

for entry in log_entries:
    if "ERROR" in entry:
        print("Found error:", entry)
        break

# continue: skip None values when cleaning data
raw_values = [10, None, 30, None, 50]

for val in raw_values:
    if val is None:
        continue          # skip this item, move to the next
    print(val)

# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
#
#  Starting data is provided below -- do not change that line.
#  Loop through raw_cities.
#  If an item is None, skip it using continue.
#  For each non-None item: strip whitespace with .strip() and fix the case
#  with .title(), then print the cleaned result.
#
#  Expected output:
#      Tel Aviv
#      Jerusalem
#      Haifa
#      Beer Sheva
#

# --- starting data (do not change this line) ---
raw_cities = ["  Tel Aviv ", "JERUSALEM", None, "haifa  ", " Beer Sheva"]






# ══════════════════════════════════════════════════════════════
#  CONCEPT 4 -- while LOOP
# ══════════════════════════════════════════════════════════════
#
#  A while loop repeats a block of code as long as a condition is True.
#  Use it when you do not know in advance how many iterations you need.
#
#  Syntax:
#    while condition:
#        # code block
#
#  WARNING: if the condition never becomes False, the loop runs forever.
#  Always make sure something inside the loop will eventually make it stop.
#
#  Common patterns:
#    - Decrement a counter each iteration
#    - Pop items from a list until it is empty
#    - Break out of the loop when a target is found
#
# EXAMPLE ──────────────────────────────────────────────

attempts = 0
max_attempts = 5
connected = False

while attempts < max_attempts and not connected:
    attempts += 1
    print("Attempt", attempts, "-- connecting to server...")
    if attempts == 3:
        connected = True
        print("Connected successfully on attempt", attempts)

# ══════════════════════════════════════════════════════════════
#  EXERCISE 4
# ══════════════════════════════════════════════════════════════
#
#  Starting data is provided below -- do not change that line.
#  Use a while loop to process the queue.
#  While the queue is not empty:
#    - Remove the first item with .pop(0)
#    - Print "Processing: " followed by the filename
#  After the loop ends, print "Queue empty. Done."
#
#  Expected output:
#      Processing: sales_jan.csv
#      Processing: sales_feb.csv
#      Processing: sales_mar.csv
#      Queue empty. Done.
#

# --- starting data (do not change this line) ---
queue = ["sales_jan.csv", "sales_feb.csv", "sales_mar.csv"]




