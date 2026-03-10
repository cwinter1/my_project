# ══════════════════════════════════════════════════════════════
#  WEEK 3  |  DAY 1  |  FILE HANDLING
# ══════════════════════════════════════════════════════════════
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Read a file safely using open() with the with statement
#  2. Write new content and append to existing files
#  3. Build platform-safe file paths using os.path utilities
#
#  TIME:  ~30-35 minutes
#
#  YOUTUBE
#  ───────
#  Search: "Python read write files open with statement"
#  Search: "Python os.path file paths tutorial"
# ══════════════════════════════════════════════════════════════

import os

# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — READING A FILE WITH open() AND THE with STATEMENT
# ══════════════════════════════════════════════════════════════
# open() returns a file object you can iterate over or read from.
#
# Syntax:
#   with open("path/to/file.txt", "r") as f:
#       content = f.read()
#
# Mode strings:
#   "r"   -- read only (default)
#   "w"   -- write (creates or overwrites)
#   "a"   -- append (adds to end)
#   "rb"  -- read binary (images, PDFs)
#
# The with statement (context manager) automatically closes the file
# when the block ends, even if an error occurs inside the block.
#
# Read methods:
#   f.read()          -- returns entire file as one string
#   f.readlines()     -- returns a list of lines (each ends with \n)
#   for line in f:    -- iterate line by line (memory efficient for large files)

# EXAMPLE ──────────────────────────────────────────────────────
# First create a sample file so we have something to read
sample_path = os.path.join(os.path.dirname(__file__), "sample_log.txt")

with open(sample_path, "w") as f:
    f.write("2024-01-15,pipeline_start,SUCCESS\n")
    f.write("2024-01-15,extract_step,SUCCESS\n")
    f.write("2024-01-15,transform_step,SUCCESS\n")
    f.write("2024-01-15,load_step,FAILURE\n")
    f.write("2024-01-15,pipeline_end,FAILURE\n")

# Read the whole file at once
with open(sample_path, "r") as f:
    entire_content = f.read()

print("--- Entire file ---")
print(entire_content)

# Read line by line (memory efficient for large files)
print("--- Line by line ---")
with open(sample_path, "r") as f:
    for line in f:
        # strip() removes the trailing newline character
        parts = line.strip().split(",")
        date, step, status = parts[0], parts[1], parts[2]
        print(f"  {date} | {step:20s} | {status}")

# Read into a list and filter
with open(sample_path, "r") as f:
    lines = f.readlines()

failures = [l.strip() for l in lines if "FAILURE" in l]
print("\nFailed steps:")
for f_line in failures:
    print(" ", f_line)
# 2024-01-15,load_step,FAILURE
# 2024-01-15,pipeline_end,FAILURE


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
# The file sample_log.txt is already created above and available at sample_path.
#
# Write code that:
#   1. Reads the file line by line
#   2. Counts the total number of lines
#   3. Counts how many lines contain "SUCCESS"
#   4. Counts how many lines contain "FAILURE"
#   5. Prints a summary
#
# Expected output:
#   Total entries: 5
#   Successful:    3
#   Failed:        2




# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — WRITING AND APPENDING TO FILES
# ══════════════════════════════════════════════════════════════
# "w" mode creates a new file or OVERWRITES an existing one completely.
# "a" mode creates a new file or APPENDS to the end of an existing one.
#
# Use "w" when you want a fresh output each run.
# Use "a" when you want to accumulate data across multiple runs
# (e.g. daily log files, incremental exports).
#
# Always use the with statement so files are closed properly.

# EXAMPLE ──────────────────────────────────────────────────────
output_path = os.path.join(os.path.dirname(__file__), "pipeline_report.txt")

# Write a fresh report
pipeline_results = [
    ("extract",   "SUCCESS", 15000),
    ("validate",  "SUCCESS", 14987),
    ("transform", "SUCCESS", 14987),
    ("load",      "SUCCESS", 14987),
]

with open(output_path, "w") as f:
    f.write("PIPELINE RUN REPORT\n")
    f.write("=" * 40 + "\n")
    for step, status, rows in pipeline_results:
        f.write(f"{step:<15} {status:<10} {rows:>6} rows\n")

print(f"Report written to: {output_path}")

# Append a footer after the fact
with open(output_path, "a") as f:
    f.write("=" * 40 + "\n")
    f.write("Status: COMPLETE\n")

# Verify by reading back
with open(output_path, "r") as f:
    print(f.read())

# Writing multiple lines at once with writelines()
error_log_path = os.path.join(os.path.dirname(__file__), "errors.txt")
error_lines = [
    "2024-01-16 08:01 | row 42  | NULL value in required column 'customer_id'\n",
    "2024-01-16 08:01 | row 107 | Invalid date format '15/01/2024'\n",
    "2024-01-16 08:01 | row 284 | Amount -999 out of acceptable range\n",
]

with open(error_log_path, "w") as f:
    f.writelines(error_lines)

print(f"Error log written: {error_log_path}")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
# Simulate two separate pipeline runs that each append to the same log file.
#
# Run 1 data (write fresh):
#   date="2024-01-20", run_id="RUN-001", status="SUCCESS", rows=12500
#
# Run 2 data (append):
#   date="2024-01-21", run_id="RUN-002", status="FAILURE", rows=0
#
# Each entry should be written as one line:
#   "2024-01-20 | RUN-001 | SUCCESS | 12500 rows\n"
#
# After both runs, read the file back and print all lines.
# Save the file as "run_history.txt" in the same folder as this script.
#
# Expected output:
#   2024-01-20 | RUN-001 | SUCCESS | 12500 rows
#   2024-01-21 | RUN-002 | FAILURE | 0 rows




# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — WORKING WITH FILE PATHS USING os.path
# ══════════════════════════════════════════════════════════════
# Hardcoded paths like "C:\\Users\\alice\\project\\data.csv" break on other
# machines. Use os.path to build paths dynamically and portably.
#
# Key functions:
#   os.path.dirname(__file__)       -- directory containing the current script
#   os.path.join(a, b, c)           -- join path parts with the correct separator
#   os.path.exists(path)            -- True if path exists
#   os.path.isfile(path)            -- True if path is a file
#   os.path.isdir(path)             -- True if path is a directory
#   os.path.basename(path)          -- last component (filename)
#   os.path.splitext(filename)      -- split name and extension
#   os.makedirs(path, exist_ok=True)-- create folder(s), no error if already exists

# EXAMPLE ──────────────────────────────────────────────────────
# Get the directory this script lives in
this_dir = os.path.dirname(__file__)
print("Script directory:", this_dir)

# Navigate up to a sibling folder (datasets lives next to Curriculum weeks)
datasets_dir = os.path.join(this_dir, "..", "datasets")
datasets_dir = os.path.normpath(datasets_dir)   # resolve ".." to clean path
print("Datasets directory:", datasets_dir)

# Build a path to a specific file
titanic_path = os.path.join(datasets_dir, "titanic_train.xlsx")
print("Titanic file path:", titanic_path)
print("File exists:", os.path.exists(titanic_path))

# Inspect a filename
filename = "sales_report_Q3_2024.csv"
name, ext = os.path.splitext(filename)
print(f"Name: {name},  Extension: {ext}")
# Name: sales_report_Q3_2024,  Extension: .csv

# Create a temp output directory if it does not exist
temp_dir = os.path.join(this_dir, "temp_output")
os.makedirs(temp_dir, exist_ok=True)
print("Temp dir created:", os.path.isdir(temp_dir))   # True

# List all .txt files created in this lesson
txt_files = [f for f in os.listdir(this_dir) if f.endswith(".txt")]
print("Text files in this folder:", txt_files)


# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
# Write a function called inventory_folder(folder_path) that:
#   1. Lists all files in folder_path (non-recursive, top level only)
#   2. For each file, collects: filename, extension, size in bytes (os.path.getsize)
#   3. Returns a list of dicts:
#      [{"name": "file.txt", "ext": ".txt", "size_bytes": 245}, ...]
#   4. If the folder does not exist, prints a warning and returns []
#
# Call it on the directory this script is in (os.path.dirname(__file__))
# and print each entry.
#
# Expected output (will vary — these are the files we created above):
#   {'name': 'sample_log.txt',       'ext': '.txt', 'size_bytes': 125}
#   {'name': 'pipeline_report.txt',  'ext': '.txt', 'size_bytes': 182}
#   {'name': 'errors.txt',           'ext': '.txt', 'size_bytes': 197}
#   {'name': 'run_history.txt',      'ext': '.txt', 'size_bytes': 85}
#   (plus this .py file)


