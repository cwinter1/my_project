# ══════════════════════════════════════════════════════════════
#  WEEK 2  |  DAY 6  |  CLASSES AND OBJECT-ORIENTED PROGRAMMING
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Understand what a class is and how to create one with __init__ and self
#  2. Add methods to give objects behavior
#  3. Use attributes to track state across method calls
#
#  TIME:  ~45 minutes  (3 concepts x 15 min each)
#
#  YOUTUBE
#  ───────
#  Search: "Python classes and objects for beginners"
#  Search: "Python OOP __init__ self explained"
#
# ══════════════════════════════════════════════════════════════


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 -- WHAT IS A CLASS
# ══════════════════════════════════════════════════════════════
#
#  A class is a blueprint or template for creating objects.
#  An object is one specific instance built from that blueprint.
#
#  Real-world analogy: a DataFrame is a class. df = pd.DataFrame() is one instance.
#  The blueprint defines what data it holds and what it can do.
#  Every instance gets its own independent copy of that data.
#
#  Syntax:
#    class MyClass:
#        def __init__(self, param1, param2):
#            self.param1 = param1     <- stores the value as an attribute
#            self.param2 = param2
#
#  __init__ is the constructor -- runs automatically when you create an instance.
#  self refers to the specific object being created.
#  self.name stores the value on the object so every method can access it later.
#
#  Creating an instance:
#    obj = MyClass("value1", "value2")
#    print(obj.param1)               -> value1
#
# EXAMPLE ──────────────────────────────────────────────

class DataRecord:
    def __init__(self, name, value, timestamp):
        self.name      = name        # store name on the object
        self.value     = value       # store value on the object
        self.timestamp = timestamp   # store timestamp on the object

# create an instance
record1 = DataRecord("Revenue", 95000, "2024-01-15")

# access attributes
print(record1.name)       # Revenue
print(record1.value)      # 95000
print(record1.timestamp)  # 2024-01-15

# create a second instance -- completely independent from record1
record2 = DataRecord("Expenses", 42000, "2024-01-15")
print(record2.name)       # Expenses

# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
#
#  Create a class called SalesRecord with 3 attributes set in __init__:
#    name        -- the product name
#    quantity    -- number of units sold
#    unit_price  -- price per unit
#
#  Add a method called total_value(self) that returns quantity * unit_price.
#  (A method is a function defined inside the class, with self as first parameter.)
#
#  Create 2 instances with this data:
#    Instance 1: name="Laptop",  quantity=10, unit_price=15000
#    Instance 2: name="Phone",   quantity=20, unit_price=2000
#
#  For each instance, print the name and the result of total_value() on one line.
#
#  Expected output:
#      Laptop: 150000
#      Phone: 40000
#





# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 -- METHODS
# ══════════════════════════════════════════════════════════════
#
#  A method is a function defined inside a class.
#  Methods give objects behavior -- they define what an object can do.
#
#  Every method receives self as its first parameter.
#  self gives the method access to the object's attributes.
#
#  Syntax:
#    class MyClass:
#        def __init__(self, ...):
#            self.x = ...
#
#        def my_method(self):
#            print(self.x)         <- access the attribute via self
#
#  Calling a method:
#    obj = MyClass(...)
#    obj.my_method()               <- Python passes self automatically
#
#  Methods can also accept extra parameters beyond self:
#    def set_value(self, new_value):
#        self.x = new_value
#
# EXAMPLE ──────────────────────────────────────────────

class ETLRecord:
    def __init__(self, source, destination):
        self.source      = source
        self.destination = destination

    def extract(self):
        print("Extracting data from:", self.source)

    def transform(self):
        print("Transforming data...")

    def load(self):
        print("Loading data into:", self.destination)

# create an instance and call all 3 methods
job = ETLRecord("sales_db", "warehouse")
job.extract()
job.transform()
job.load()

# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
#
#  Rewrite the SalesRecord class from Exercise 1 and add a new method
#  called summary(self) that prints a formatted line in this exact format:
#    Product: <name> | Qty: <quantity> | Unit: <unit_price> | Total: <total_value>
#
#  Create 3 instances with this data:
#    Instance 1: name="Laptop",  quantity=10,  unit_price=15000
#    Instance 2: name="Phone",   quantity=20,  unit_price=2000
#    Instance 3: name="Tablet",  quantity=5,   unit_price=3500
#
#  Call summary() on each instance.
#
#  Expected output:
#      Product: Laptop | Qty: 10 | Unit: 15000 | Total: 150000
#      Product: Phone | Qty: 20 | Unit: 2000 | Total: 40000
#      Product: Tablet | Qty: 5 | Unit: 3500 | Total: 17500
#





# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 -- CLASS WITH REAL STATE
# ══════════════════════════════════════════════════════════════
#
#  The most powerful feature of classes in data engineering:
#  a class can remember and update its own data across multiple method calls.
#  This is called state.
#
#  Example: a pipeline that counts records processed, tracks errors, and
#  stores the last run time -- all in one object that persists throughout a session.
#
#  State is stored in attributes set in __init__.
#  Methods read and update those attributes.
#  After calling several methods, the object remembers everything that happened.
#
#  This is exactly why ETL pipelines are built as classes:
#    - __init__ sets up the job configuration
#    - extract(), transform(), load() do the work and update the state
#    - report() or status() prints a summary of everything that happened
#
# EXAMPLE ──────────────────────────────────────────────

from datetime import datetime

class DataPipeline:
    def __init__(self, name):
        self.name           = name
        self.records_loaded = 0          # starts at zero
        self.last_run       = None       # not run yet

    def load(self, data_list):
        self.records_loaded += len(data_list)   # add to running total
        self.last_run = datetime.now()           # update last run time
        print("Loaded", len(data_list), "records")

    def status(self):
        print("Pipeline:     ", self.name)
        print("Total loaded: ", self.records_loaded)
        print("Last run:     ", self.last_run)

# run the pipeline twice -- state accumulates across calls
pipeline = DataPipeline("customer_sync")
pipeline.load([1, 2, 3, 4, 5])   # load 5 records
pipeline.load([6, 7, 8])          # load 3 more
pipeline.status()                 # shows 8 total

# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
#
#  Create a class called ETLJob that tracks the following state.
#
#  Attributes (all set in __init__, which takes job_name as its only parameter):
#    job_name        -- the name passed in
#    rows_extracted  -- starts at 0
#    rows_loaded     -- starts at 0
#    errors          -- starts as an empty list []
#
#  Methods:
#    extract(self, row_count)
#      -- sets self.rows_extracted = row_count
#      -- prints "Extracted N rows"  (where N is row_count)
#
#    load(self, row_count)
#      -- sets self.rows_loaded = row_count
#      -- prints "Loaded N rows"
#
#    log_error(self, message)
#      -- appends message to self.errors
#      -- prints "ERROR: " followed by the message
#
#    report(self)
#      -- prints a summary using all 4 fields (see expected output below)
#
#  Create one instance: daily_sales_job = ETLJob("daily_sales_job")
#  Then call these methods in order:
#    1. daily_sales_job.extract(1000)
#    2. daily_sales_job.load(998)
#    3. daily_sales_job.log_error("2 rows failed validation")
#    4. daily_sales_job.report()
#
#  Expected output:
#      Extracted 1000 rows
#      Loaded 998 rows
#      ERROR: 2 rows failed validation
#      ── Job Report: daily_sales_job ──
#      Rows extracted: 1000
#      Rows loaded:    998
#      Errors:         1
#      Error details:  ['2 rows failed validation']
#




