# ══════════════════════════════════════════════════════════════
#  WEEK 4  |  DAY 1  |  NUMPY
# ══════════════════════════════════════════════════════════════
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Create NumPy arrays using various constructor functions
#  2. Perform array operations including shape, reshape, math, and broadcasting
#  3. Index and slice 1D and 2D arrays to extract subsets of data
#
#  TIME:  ~30-35 minutes
#
#  YOUTUBE
#  ───────
#  Search: "NumPy arrays tutorial Python data science"
#  Search: "NumPy indexing slicing 2D array"
# ══════════════════════════════════════════════════════════════

# Install if needed:  pip install numpy

import numpy as np

# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — CREATING ARRAYS (np.array, np.zeros, np.arange, np.linspace)
# ══════════════════════════════════════════════════════════════
# A NumPy array is a fixed-size, typed grid of numbers.
# Unlike Python lists, all elements must be the same type.
# Arrays are faster and use less memory than lists for numeric computation.
#
# CREATION FUNCTIONS:
#   np.array([1,2,3])        -- from a Python list
#   np.zeros(n)              -- array of n zeros (float64 by default)
#   np.ones(n)               -- array of n ones
#   np.arange(start, stop, step) -- evenly spaced values (like range())
#   np.linspace(start, stop, n)  -- n evenly spaced values inclusive
#   np.full(shape, value)    -- fill with a constant value
#   np.random.seed(42); np.random.randint(low, high, size) -- reproducible random ints

# EXAMPLE ──────────────────────────────────────────────────────
# From a list — quarterly revenue data in thousands
quarterly_revenue = np.array([142, 198, 155, 211, 169, 225, 180, 215])
print("Revenue array:", quarterly_revenue)
print("Type:", type(quarterly_revenue))         # <class 'numpy.ndarray'>
print("Data type:", quarterly_revenue.dtype)    # int64

# From a list of floats
conversion_rates = np.array([0.032, 0.041, 0.028, 0.055, 0.038])
print("\nConversion rates:", conversion_rates)
print("dtype:", conversion_rates.dtype)         # float64

# Zeros — initialise an output array before filling it in a loop
budget_allocation = np.zeros(4)
print("\nInitial budget slots:", budget_allocation)   # [0. 0. 0. 0.]

# Ones — useful for multiplying or masking
weights = np.ones(5) * 0.2      # equal weights summing to 1.0
print("Equal weights:", weights)                 # [0.2 0.2 0.2 0.2 0.2]

# arange — day numbers 1 through 30 (for a monthly simulation)
days = np.arange(1, 31)
print("\nDays in month:", days)

# linspace — 5 evenly spaced price points between $10 and $50 (inclusive)
price_grid = np.linspace(10, 50, 5)
print("Price grid:", price_grid)                 # [10. 20. 30. 40. 50.]

# Reproducible random data — simulate 12 months of unit sales
np.random.seed(42)
monthly_units = np.random.randint(800, 1500, size=12)
print("\nSimulated monthly units:", monthly_units)


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
# Create three arrays:
#   1. unit_prices: linspace from $25.00 to $100.00 with 8 values
#   2. units_sold:  arange starting at 50, ending before 450, step 50
#      (should produce: [50, 100, 150, 200, 250, 300, 350, 400])
#   3. revenue:     multiply unit_prices by units_sold element-wise
#
# Print all three arrays and then print the total revenue (sum).
#
# Expected output:
#   Prices:  [ 25.   35.71  46.43  57.14  67.86  78.57  89.29 100.  ]
#   Units:   [ 50 100 150 200 250 300 350 400]
#   Revenue: [ 1250.   3571.43  6964.29 11428.57 16964.29 23571.43 31250. 40000. ]
#   Total revenue: 135000.0




# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — ARRAY OPERATIONS (shape, reshape, math, broadcasting)
# ══════════════════════════════════════════════════════════════
# SHAPE AND RESHAPE:
#   arr.shape    -- tuple describing dimensions (rows, columns)
#   arr.reshape(r, c) -- change dimensions without copying data
#   arr.flatten() -- collapse to 1D
#
# ELEMENT-WISE MATH:
#   arr + 5, arr * 2, arr ** 0.5  -- applies to every element
#   np.sqrt(arr), np.log(arr)     -- universal functions (ufuncs)
#
# AGGREGATIONS:
#   arr.sum(), arr.mean(), arr.std(), arr.min(), arr.max()
#   Use axis=0 for column-wise, axis=1 for row-wise operations
#
# BROADCASTING:
#   NumPy automatically stretches smaller arrays to match larger ones.
#   Example: a 1D array of 3 values added to each row of a (4,3) matrix.

# EXAMPLE ──────────────────────────────────────────────────────
# Create a 2D array: 4 quarters x 3 regions
sales_matrix = np.array([
    [142000, 185000, 98000],    # Q1: West, East, Central
    [155000, 211000, 107000],   # Q2
    [169000, 225000, 115000],   # Q3
    [180000, 240000, 122000],   # Q4
])

print("Shape:", sales_matrix.shape)    # (4, 3)  -> 4 rows, 3 columns
print("Total elements:", sales_matrix.size)  # 12

# Column labels for reference
regions = ["West", "East", "Central"]

# Sum along axis=0 (collapse rows -> annual total per region)
annual_by_region = sales_matrix.sum(axis=0)
print("\nAnnual by region:")
for region, total in zip(regions, annual_by_region):
    print(f"  {region}: ${total:,}")

# Sum along axis=1 (collapse columns -> total per quarter)
quarterly_totals = sales_matrix.sum(axis=1)
print("\nQuarterly totals:", quarterly_totals)

# Math operations — apply a 5% growth rate to all values
projected = sales_matrix * 1.05
print("\nProjected (5% growth):")
print(projected.astype(int))

# Broadcasting — add regional bonuses (1D) to every quarter (2D)
regional_bonuses = np.array([5000, 8000, 3000])   # shape (3,)
adjusted = sales_matrix + regional_bonuses          # broadcasts across 4 rows
print("\nWith bonuses added:")
print(adjusted)

# Reshape — convert 12 monthly figures into a 3-by-4 grid (3 rows = quarters, 4 cols = years)
np.random.seed(7)
monthly_data = np.random.randint(100000, 200000, 12)
reshaped = monthly_data.reshape(3, 4)   # 3 groups of 4
print("\nReshape (3 x 4):")
print(reshaped)


# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
# A company has 3 sales regions over 4 months.
# monthly_sales below is a flat 1D array of 12 values (month1_reg1, month1_reg2, ...).
#
# Tasks:
#   1. Reshape into a (4, 3) array: 4 months as rows, 3 regions as columns
#   2. Calculate the total per region (sum of each column)
#   3. Calculate the average per month (mean of each row), rounded to 0 decimals
#   4. Multiply the entire matrix by 1.08 (annual forecast adjustment),
#      convert to int, and print
#
# Expected output:
#   Totals by region: [227000 271000 171000]
#   Average per month: [50333. 53667. 57333. 61667.]
#   Adjusted forecast:
#   [[ 56160  65880  41040]
#    [ 59400  70200  44280]
#    [ 62640  75600  47520]
#    [ 66960  81000  51840]]

monthly_sales = np.array([
    52000, 61000, 38000,
    55000, 65000, 41000,
    58000, 70000, 44000,
    62000, 75000, 48000,
])




# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — ARRAY INDEXING AND SLICING (2D ARRAYS)
# ══════════════════════════════════════════════════════════════
# Indexing:
#   arr[2]            -- 1D: third element
#   arr[row, col]     -- 2D: element at row, col
#   arr[-1]           -- last element
#
# Slicing:
#   arr[1:4]          -- elements at index 1, 2, 3
#   arr[::2]          -- every other element
#   arr[1:3, :]       -- 2D: rows 1-2, all columns
#   arr[:, 0]         -- 2D: all rows, first column only
#   arr[0:2, 1:3]     -- 2D: rows 0-1, columns 1-2
#
# Boolean indexing:
#   arr[arr > 100]    -- all elements greater than 100
#   arr[arr > 100] = 0 -- set those elements to 0

# EXAMPLE ──────────────────────────────────────────────────────
# Re-use the sales matrix from above
print("Full sales matrix:")
print(sales_matrix)

# Single element
print("\nQ2 East revenue:", sales_matrix[1, 1])    # 211000

# Entire row (one quarter)
print("Q3 all regions:", sales_matrix[2])           # [169000 225000 115000]

# Entire column (one region across all quarters)
print("All quarters for West:", sales_matrix[:, 0]) # [142000 155000 169000 180000]

# Sub-matrix: Q2 and Q3 for East and Central
print("\nQ2-Q3, East-Central:")
print(sales_matrix[1:3, 1:3])

# Last row (Q4)
print("Q4 data:", sales_matrix[-1])                 # [180000 240000 122000]

# Boolean indexing — which cells exceed $200,000?
high_revenue = sales_matrix[sales_matrix > 200000]
print("\nRevenue values above $200k:", high_revenue)

# Find which quarters East region exceeded $200k
east_sales = sales_matrix[:, 1]   # column 1 = East
strong_quarters = np.where(east_sales > 200000)[0] + 1  # +1 for 1-based quarter numbers
print("East: quarters above $200k:", strong_quarters)   # [2 3 4]


# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
# Use the pipeline_metrics array below (5 days x 4 metrics).
# Columns are: [rows_extracted, rows_validated, rows_loaded, duration_seconds]
#
# Tasks:
#   1. Print row 2 (Day 3 metrics)
#   2. Print the entire "duration_seconds" column (column 3)
#   3. Calculate the "load success rate" for each day:
#      rows_loaded / rows_extracted * 100 (round to 2 decimals)
#   4. Use boolean indexing to find which days had duration > 50 seconds
#      Print the day numbers (1-based)
#
# Expected output:
#   Day 3: [18500 18490 18200    51]
#   Durations: [42 58 51 29 87]
#   Load success rates: [99.67 99.09 98.38 98.89 98.39]
#   Days with duration > 50s: [2 3 5]

pipeline_metrics = np.array([
    [15000, 14987, 14950, 42],
    [22000, 21800, 21800, 58],
    [18500, 18490, 18200, 51],
    [9000,  8900,  8900,  29],
    [31000, 30500, 30500, 87],
])


