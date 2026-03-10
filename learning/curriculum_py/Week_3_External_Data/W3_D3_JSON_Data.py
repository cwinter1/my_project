# ══════════════════════════════════════════════════════════════
#  WEEK 3  |  DAY 3  |  JSON DATA
# ══════════════════════════════════════════════════════════════
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Parse JSON strings into Python objects and convert back using json.loads/dumps
#  2. Read from and write to JSON files using json.load and json.dump
#  3. Navigate and extract values from nested JSON structures
#
#  TIME:  ~30-35 minutes
#
#  YOUTUBE
#  ───────
#  Search: "Python json module loads dumps tutorial"
#  Search: "Python working with nested JSON data"
# ══════════════════════════════════════════════════════════════

import json
import os

# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — WHAT IS JSON, json.loads() AND json.dumps()
# ══════════════════════════════════════════════════════════════
# JSON (JavaScript Object Notation) is the standard format for data exchange
# between web APIs, services, and databases.
#
# JSON types map directly to Python types:
#   JSON           Python
#   object  {}  -> dict
#   array   []  -> list
#   string  ""  -> str
#   number      -> int or float
#   true/false  -> True/False
#   null        -> None
#
# KEY FUNCTIONS:
#   json.loads(string)    -- parse a JSON STRING into a Python object (loads = load string)
#   json.dumps(obj)       -- convert a Python object INTO a JSON string (dumps = dump string)
#   json.dumps(obj, indent=2) -- pretty-print with indentation

# EXAMPLE ──────────────────────────────────────────────────────
# A JSON string coming from an API response
api_response_text = '''
{
    "status": "success",
    "pipeline_id": "PL-2024-001",
    "rows_processed": 15000,
    "duration_seconds": 42.7,
    "steps": ["extract", "validate", "transform", "load"],
    "metadata": {
        "source": "erp_database",
        "destination": "data_warehouse",
        "triggered_by": "scheduler"
    }
}
'''

# Parse the JSON string into a Python dict
data = json.loads(api_response_text)

print(type(data))                           # <class 'dict'>
print(data["status"])                       # success
print(data["rows_processed"])               # 15000
print(data["steps"])                        # ['extract', 'validate', 'transform', 'load']
print(data["metadata"]["source"])           # erp_database

# Accessing nested values
for step in data["steps"]:
    print(f"  Step: {step}")

# Convert a Python object back to a JSON string
result = {
    "pipeline_id": "PL-2024-002",
    "status": "complete",
    "rows": 8742,
    "errors": [],
    "success": True,
    "skipped": None,
}

# Without indentation (compact — good for storage)
compact = json.dumps(result)
print("\nCompact JSON:")
print(compact)

# With indentation (pretty — good for logging and human reading)
pretty = json.dumps(result, indent=2)
print("\nPretty JSON:")
print(pretty)


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
# The string below represents a webhook payload from a CRM system.
# Parse it and extract specific values.
#
# Print:
#   1. The event name
#   2. The deal id and value formatted as: "Deal DEAL-8821 closed for $125,000"
#   3. All tags joined with a comma: "enterprise, annual, new_logo"
#
# Expected output:
#   Event: deal_closed
#   Deal DEAL-8821 closed for $125,000
#   Tags: enterprise, annual, new_logo

crm_payload = '''
{
    "event": "deal_closed",
    "timestamp": "2024-10-15T14:32:00Z",
    "deal": {
        "id": "DEAL-8821",
        "name": "Acme Enterprise License",
        "value": 125000,
        "currency": "USD",
        "owner": "Sarah Lim"
    },
    "tags": ["enterprise", "annual", "new_logo"]
}
'''




# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — READING AND WRITING JSON FILES (json.load, json.dump)
# ══════════════════════════════════════════════════════════════
# json.load(file_object)           -- read and parse a JSON FILE
# json.dump(obj, file_object)      -- write a Python object as JSON to a FILE
#
# Note the naming:
#   loads / dumps  -- work with STRINGS (the s = string)
#   load  / dump   -- work with FILE OBJECTS (no s)

# EXAMPLE ──────────────────────────────────────────────────────
this_dir = os.path.dirname(__file__)
config_path = os.path.join(this_dir, "pipeline_config.json")

# Write a pipeline configuration to a JSON file
pipeline_config = {
    "pipeline_name": "daily_sales_etl",
    "version": "2.1.0",
    "schedule": "06:00",
    "source": {
        "type": "csv",
        "path": "/data/raw/sales/",
        "pattern": "sales_*.csv"
    },
    "destination": {
        "type": "database",
        "connection": "warehouse_prod",
        "table": "fact_sales"
    },
    "settings": {
        "batch_size": 5000,
        "retries": 3,
        "alert_on_failure": True,
        "email": "data-team@company.com"
    }
}

with open(config_path, "w") as f:
    json.dump(pipeline_config, f, indent=2)

print(f"Config written to: {config_path}")

# Read the configuration back
with open(config_path, "r") as f:
    loaded_config = json.load(f)

print("Pipeline name:", loaded_config["pipeline_name"])
print("Schedule:", loaded_config["schedule"])
print("Batch size:", loaded_config["settings"]["batch_size"])
print("Source path:", loaded_config["source"]["path"])

# Append a new run record to a JSON log file
run_log_path = os.path.join(this_dir, "run_log.json")

# Load existing log if it exists, otherwise start fresh
if os.path.exists(run_log_path):
    with open(run_log_path, "r") as f:
        run_log = json.load(f)
else:
    run_log = []

new_run = {
    "run_id": f"RUN-{len(run_log) + 1:04d}",
    "status": "success",
    "rows": 14987,
    "duration": 38.2
}
run_log.append(new_run)

with open(run_log_path, "w") as f:
    json.dump(run_log, f, indent=2)

print(f"\nRun log now has {len(run_log)} entry/entries.")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
# Read the pipeline_config.json file that was just created.
# Write a function called validate_config(config) that:
#   1. Checks that "pipeline_name" is a non-empty string
#   2. Checks that "settings"["batch_size"] is a positive integer
#   3. Checks that "settings"["retries"] is between 1 and 10 (inclusive)
#   4. Returns a dict: {"valid": True/False, "errors": [list of error strings]}
#
# Call it with the loaded config and print whether it is valid.
# Then call it with a deliberately broken config that has batch_size = -1
# and print the errors.
#
# Expected output:
#   Config valid: True
#   Errors: []
#   Config valid: False
#   Errors: ['batch_size must be a positive integer']




# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — WORKING WITH NESTED JSON
# ══════════════════════════════════════════════════════════════
# Real-world JSON from APIs is often deeply nested.
# Use .get() to safely access dict keys (returns None if key is missing).
# Loop over lists to process arrays of objects.
# Flatten nested data when loading into a database or DataFrame.

# EXAMPLE ──────────────────────────────────────────────────────
# A typical API response with nested arrays of objects
api_data = {
    "company": "TechCorp",
    "report_date": "2024-Q3",
    "departments": [
        {
            "name": "Engineering",
            "budget": 2400000,
            "headcount": 25,
            "projects": [
                {"id": "P-001", "name": "Data Platform", "status": "active",  "cost": 850000},
                {"id": "P-002", "name": "API Gateway",   "status": "complete","cost": 420000},
            ]
        },
        {
            "name": "Sales",
            "budget": 1800000,
            "headcount": 18,
            "projects": [
                {"id": "P-003", "name": "CRM Migration", "status": "active", "cost": 310000},
            ]
        },
        {
            "name": "Finance",
            "budget": 950000,
            "headcount": 8,
            "projects": []
        },
    ]
}

# Flatten: extract all projects from all departments into a flat list
flat_projects = []
for dept in api_data["departments"]:
    dept_name = dept["name"]
    for project in dept.get("projects", []):   # .get handles missing key safely
        flat_projects.append({
            "department": dept_name,
            "project_id": project["id"],
            "project_name": project["name"],
            "status": project["status"],
            "cost": project["cost"],
        })

print("\nAll projects (flattened):")
for p in flat_projects:
    print(f"  {p['department']:<15} | {p['project_id']} | {p['project_name']:<20} | {p['status']}")

# Calculate total project cost by department
dept_costs = {}
for p in flat_projects:
    dept_costs[p["department"]] = dept_costs.get(p["department"], 0) + p["cost"]

print("\nProject costs by department:")
for dept, cost in dept_costs.items():
    print(f"  {dept}: ${cost:,}")

# Safely access a deeply nested value with .get chaining
# (fallback to None at each level if key is missing)
missing_dept = None
for dept in api_data["departments"]:
    if dept["name"] == "HR":
        missing_dept = dept
        break

hr_budget = (missing_dept or {}).get("budget")
print("\nHR budget:", hr_budget)   # None  (HR department does not exist)


# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
# The JSON string below represents a sales performance report.
# Parse it and produce a flat summary.
#
# Tasks:
#   1. Parse the JSON string into a Python object
#   2. Loop over each region, then each rep within that region
#   3. Build a flat list of dicts with keys:
#      region, rep_name, deals_closed, revenue
#   4. Find the rep with the highest revenue and print their details
#   5. Print the total revenue across all reps
#
# Expected output:
#   Top performer: Priya Mehta | East | $312,000
#   Total revenue: $891,000

sales_json = '''
{
    "regions": [
        {
            "name": "West",
            "reps": [
                {"name": "Tom Reyes",   "deals_closed": 12, "revenue": 185000},
                {"name": "Lena Kim",    "deals_closed": 9,  "revenue": 142000}
            ]
        },
        {
            "name": "East",
            "reps": [
                {"name": "Priya Mehta", "deals_closed": 18, "revenue": 312000},
                {"name": "Omar Nasser", "deals_closed": 7,  "revenue": 98000}
            ]
        },
        {
            "name": "Central",
            "reps": [
                {"name": "Sara Jones",  "deals_closed": 11, "revenue": 154000}
            ]
        }
    ]
}
'''


