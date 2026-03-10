# ══════════════════════════════════════════════════════════════
#  WEEK 12  |  DAY 3  |  STORE — BRONZE LAYER (MinIO / S3)
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Understand what MinIO and object storage are
#  2. Understand the Bronze / Silver / Gold data lake layers
#  3. Save and load JSON files (simulate S3 bucket operations)
#
#  PIPELINE CONTEXT
#  ─────────────────
#  This is Stage 3 of the capstone pipeline:
#    Day 1: Docker + Kafka setup (simulation)
#    Day 2: Extract data from API, produce to Kafka
#    Day 3: Store raw records in Bronze layer (MinIO)  <-- today
#    Day 4: Transform and load to PostgreSQL (Silver)
#    Day 5: Orchestrate the full pipeline with logging
#
#  TIME:  ~45 minutes
#
# ══════════════════════════════════════════════════════════════


import os
import json


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — WHAT IS MinIO / S3 OBJECT STORAGE
# ══════════════════════════════════════════════════════════════
#
#  Object storage treats data as named "objects" (files) inside
#  named "buckets" (top-level containers).  Unlike a filesystem,
#  there are no real sub-folders — the slash in a key like
#  "bronze/2024-01-15/raw_data.json" is just part of the name.
#
#  AWS S3 (Simple Storage Service) is the most widely used
#  object storage service in cloud data engineering.
#
#  MinIO is an open-source, self-hosted object storage server
#  that is 100% compatible with the S3 API.  Data engineers run
#  MinIO locally (via Docker) to develop and test pipelines
#  before deploying them to AWS.
#
#  Why object storage for a data pipeline?
#    - Raw files can be any size — no schema required
#    - Easy to version: keep every daily snapshot forever
#    - Cheap storage cost compared to a database
#    - S3-compatible tools (boto3, Spark, Pandas) work with MinIO
#
#  SIMULATION: in this lesson, a local folder acts as the bucket.
#    Real MinIO bucket  : s3://my-pipeline/bronze/
#    Simulation folder  : ./bronze/
#
#  The Python code is identical except for the boto3 client call.
#
# EXAMPLE ──────────────────────────────────────────────────────

# Simulation: create a local folder to represent the bucket.
bronze_folder = os.path.join(os.path.dirname(__file__), "bronze_demo")
os.makedirs(bronze_folder, exist_ok=True)

print(f"Bronze bucket (simulation) ready at: {bronze_folder}")
print("  In production this would be an S3 or MinIO bucket.")

# REAL MODE (requires Docker + boto3 + running MinIO) ──────────
# import boto3
#
# s3 = boto3.client(
#     "s3",
#     endpoint_url="http://localhost:9000",
#     aws_access_key_id="minioadmin",
#     aws_secret_access_key="minioadmin",
# )
# s3.create_bucket(Bucket="my-pipeline")
# print("MinIO bucket created.")
# ──────────────────────────────────────────────────────────────


# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — BRONZE / SILVER / GOLD NAMING CONVENTION
# ══════════════════════════════════════════════════════════════
#
#  The Medallion Architecture organizes data into three layers.
#  Each layer is a separate folder (or S3 prefix):
#
#    BRONZE  — raw, unprocessed data exactly as received
#              Filename pattern: raw_YYYY-MM-DD.json
#              Never delete or modify Bronze files.
#              If something goes wrong you can always replay
#              the pipeline from Bronze.
#
#    SILVER  — cleaned and validated data
#              Nulls filled, types corrected, columns renamed
#              Filename pattern: cleaned_YYYY-MM-DD.json
#              or loaded into a relational table (Day 4).
#
#    GOLD    — aggregated, business-ready data
#              Grouped by city/year, KPIs computed, joined with
#              other tables.  Used directly by dashboards and
#              analysts.
#
#  Typical folder structure:
#
#    data/
#      bronze/
#        raw_2024-01-14.json
#        raw_2024-01-15.json
#      silver/
#        cleaned_2024-01-14.json
#        cleaned_2024-01-15.json
#      gold/
#        kpis_january_2024.json
#
# EXAMPLE ──────────────────────────────────────────────────────

layer_names = ["bronze", "silver", "gold"]
descriptions = {
    "bronze": "Raw data as received — never modified",
    "silver": "Cleaned and typed — ready for analysis",
    "gold":   "Aggregated — ready for dashboards",
}

print("\nMedallion Architecture layers:")
for layer in layer_names:
    print(f"  {layer.upper():8s} | {descriptions[layer]}")

print("\nExample filename convention:")
for layer, prefix in [("bronze", "raw"), ("silver", "cleaned"), ("gold", "kpis")]:
    print(f"  {layer}/  ->  {prefix}_2024-01-15.json")


# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — SAVING AND LOADING JSON FILES
# ══════════════════════════════════════════════════════════════
#
#  Python's built-in json module provides two key functions:
#
#    json.dumps(obj)   — serialize Python object to a JSON string
#    json.loads(s)     — parse a JSON string back to Python object
#
#  For files you typically use:
#    json.dump(obj, f)    — write to an open file object
#    json.load(f)         — read from an open file object
#
#  indent=2 makes the JSON human-readable (one key per line).
#  ensure_ascii=False preserves non-ASCII characters (Hebrew text).
#
#  After writing, you can verify the file with os.path.getsize()
#  to confirm it is not empty before moving to the next stage.
#
# EXAMPLE ──────────────────────────────────────────────────────

sample_records = [
    {"_id": 1, "district": "North",  "accidents": 42, "year": 2022},
    {"_id": 2, "district": "South",  "accidents": 31, "year": 2022},
    {"_id": 3, "district": "Center", "accidents": 78, "year": 2022},
]

# Write to a JSON file.
demo_filepath = os.path.join(bronze_folder, "raw_demo.json")
with open(demo_filepath, "w", encoding="utf-8") as f:
    json.dump(sample_records, f, indent=2, ensure_ascii=False)

file_size = os.path.getsize(demo_filepath)
print(f"\nWrote {len(sample_records)} records to {demo_filepath}")
print(f"  File size: {file_size} bytes")

# Read it back.
with open(demo_filepath, "r", encoding="utf-8") as f:
    loaded = json.load(f)

print(f"Read back {len(loaded)} records.")
print(f"  First record: {loaded[0]}")

# REAL MODE (requires boto3 + running MinIO) ───────────────────
# json_string = json.dumps(sample_records, indent=2, ensure_ascii=False)
# s3.put_object(
#     Bucket="my-pipeline",
#     Key="bronze/raw_2024-01-15.json",
#     Body=json_string.encode("utf-8"),
# )
# response = s3.get_object(Bucket="my-pipeline", Key="bronze/raw_2024-01-15.json")
# loaded = json.loads(response["Body"].read().decode("utf-8"))
# ──────────────────────────────────────────────────────────────


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
#
#  Write a function save_to_bronze(records, output_folder, run_date)
#  that saves the records list as a JSON file.
#
#  Rules:
#    - The filename must be f"raw_{run_date}.json"
#    - The file must be written inside output_folder
#    - Use indent=2 and ensure_ascii=False
#    - The function must return the full filepath (string)
#
#  After calling the function, print:
#    Saved 6 records to bronze/raw_2024-01-15.json (312 bytes)
#  (The actual byte count will vary.)
#
#  Expected output:
#    Saved 6 records to <path>/raw_2024-01-15.json (NNN bytes)

# --- starting data ---
output_folder = os.path.join(os.path.dirname(__file__), "bronze")
os.makedirs(output_folder, exist_ok=True)

run_date = "2024-01-15"

records_to_save = [
    {"_id": 1, "district": "North",    "accidents": 42, "year": 2022},
    {"_id": 2, "district": "South",    "accidents": 31, "year": 2022},
    {"_id": 3, "district": "Center",   "accidents": 78, "year": 2022},
    {"_id": 4, "district": "Haifa",    "accidents": 55, "year": 2023},
    {"_id": 5, "district": "Tel Aviv", "accidents": 91, "year": 2023},
    {"_id": 6, "district": "Jerusalem","accidents": 47, "year": 2023},
]




# (write your code here)




# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
#
#  Write a function list_bronze_files(folder)
#  that returns a list of (filename, size_bytes) tuples for
#  every .json file found in folder.
#
#  Rules:
#    - Use os.listdir() to iterate over files in folder
#    - Include only files whose name ends with ".json"
#    - For each file, get its size in bytes with os.path.getsize()
#    - Return a list of (filename, size_bytes) tuples
#    - Sort the list by filename alphabetically
#
#  After calling the function, print each tuple on its own line.
#
#  Expected output (after Exercise 1 has run):
#    Bronze files in <folder>:
#      raw_2024-01-15.json  |  312 bytes

# --- starting data ---
# output_folder is defined above (from Exercise 1)




# (write your code here)




# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
#
#  Write a function load_from_bronze(filepath)
#  that reads a JSON file at filepath and returns a list of
#  record dicts.
#
#  Rules:
#    - Open the file with encoding="utf-8"
#    - Use json.load() to parse it
#    - Return the parsed list
#
#  Call the function with the filepath returned by save_to_bronze
#  in Exercise 1. Print the count of records loaded and the
#  last record in the list.
#
#  Expected output:
#    Loaded 6 records from bronze/raw_2024-01-15.json
#    Last record: {'_id': 6, 'district': 'Jerusalem', 'accidents': 47, 'year': 2023}

# --- starting data ---
# Use the filepath variable returned from Exercise 1 above




# (write your code here)




