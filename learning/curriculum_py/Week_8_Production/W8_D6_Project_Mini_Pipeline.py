# ══════════════════════════════════════════════════════════════
#  WEEK 8  |  DAY 6  |  WEEKLY PROJECT — MINI DATA PIPELINE
# ══════════════════════════════════════════════════════════════
#
#  PROJECT GOAL
#  ────────────
#  Build a mini end-to-end data pipeline that simulates the
#  modern production pattern: message queue → object storage
#  → database → analytics queries. No external services are
#  required — Python simulates each layer using local files
#  and SQLite.
#
#  SKILLS PRACTICED
#  ─────────────────
#  - Simulating a message queue (Kafka) with file I/O
#  - Simulating object storage (MinIO/S3) with folders
#  - Data transformation: timestamps, filtering, enrichment
#  - SQLite loading and analytical SQL queries
#  - Logging and pipeline run reports
#
#  TIME:  ~45-60 minutes
#
# ══════════════════════════════════════════════════════════════


# ── SETUP — provided by teacher, do not change ────────────────

import json
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import os
import logging

this_dir = os.path.dirname(os.path.abspath(__file__))

# ── Storage layer folders ─────────────────────────────────────
RAW_LAYER       = os.path.join(this_dir, "raw_layer")        # simulates MinIO raw bucket
PROCESSED_LAYER = os.path.join(this_dir, "processed_layer")  # simulates MinIO processed bucket
DB_PATH         = os.path.join(this_dir, "city_metrics.db")

os.makedirs(RAW_LAYER, exist_ok=True)
os.makedirs(PROCESSED_LAYER, exist_ok=True)

# ── Logging ───────────────────────────────────────────────────
logger = logging.getLogger("mini_pipeline")
logger.setLevel(logging.INFO)

if not logger.handlers:
    _fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    _h = logging.StreamHandler()
    _h.setFormatter(_fmt)
    logger.addHandler(_h)

# ── Sample API response data ──────────────────────────────────
# 20 records simulating government open data about city spending.

_base_time = datetime(2025, 1, 1, 8, 0, 0)

SAMPLE_RECORDS = [
    {"record_id": 1,  "city": "Tel Aviv  ",   "category": "Infrastructure", "value": 142000, "timestamp": (_base_time + timedelta(hours=0)).isoformat()},
    {"record_id": 2,  "city": "Jerusalem",    "category": "Education",      "value": 98000,  "timestamp": (_base_time + timedelta(hours=1)).isoformat()},
    {"record_id": 3,  "city": "Haifa    ",    "category": "Health",         "value": 75000,  "timestamp": (_base_time + timedelta(hours=2)).isoformat()},
    {"record_id": 4,  "city": "Beer Sheva",   "category": "Infrastructure", "value": 63000,  "timestamp": (_base_time + timedelta(hours=3)).isoformat()},
    {"record_id": 5,  "city": "Netanya  ",    "category": "Education",      "value": 51000,  "timestamp": (_base_time + timedelta(hours=4)).isoformat()},
    {"record_id": 6,  "city": "Tel Aviv  ",   "category": "Health",         "value": -500,   "timestamp": (_base_time + timedelta(hours=5)).isoformat()},
    {"record_id": 7,  "city": "Rishon",       "category": "Infrastructure", "value": 87000,  "timestamp": (_base_time + timedelta(hours=6)).isoformat()},
    {"record_id": 8,  "city": "Petah Tikva",  "category": "Education",      "value": 44000,  "timestamp": (_base_time + timedelta(hours=7)).isoformat()},
    {"record_id": 9,  "city": "Ashdod  ",     "category": "Health",         "value": 39000,  "timestamp": (_base_time + timedelta(hours=8)).isoformat()},
    {"record_id": 10, "city": "Holon",        "category": "Infrastructure", "value": 0,      "timestamp": (_base_time + timedelta(hours=9)).isoformat()},
    {"record_id": 11, "city": "Jerusalem",    "category": "Health",         "value": 112000, "timestamp": (_base_time + timedelta(hours=10)).isoformat()},
    {"record_id": 12, "city": "Haifa    ",    "category": "Infrastructure", "value": 95000,  "timestamp": (_base_time + timedelta(hours=11)).isoformat()},
    {"record_id": 13, "city": "Tel Aviv  ",   "category": "Education",      "value": 133000, "timestamp": (_base_time + timedelta(hours=12)).isoformat()},
    {"record_id": 14, "city": "Beer Sheva",   "category": "Health",         "value": 58000,  "timestamp": (_base_time + timedelta(hours=13)).isoformat()},
    {"record_id": 15, "city": "Netanya  ",    "category": "Infrastructure", "value": -200,   "timestamp": (_base_time + timedelta(hours=14)).isoformat()},
    {"record_id": 16, "city": "Rishon",       "category": "Health",         "value": 47000,  "timestamp": (_base_time + timedelta(hours=15)).isoformat()},
    {"record_id": 17, "city": "Petah Tikva",  "category": "Infrastructure", "value": 69000,  "timestamp": (_base_time + timedelta(hours=16)).isoformat()},
    {"record_id": 18, "city": "Ashdod  ",     "category": "Education",      "value": 35000,  "timestamp": (_base_time + timedelta(hours=17)).isoformat()},
    {"record_id": 19, "city": "Holon",        "category": "Education",      "value": 52000,  "timestamp": (_base_time + timedelta(hours=18)).isoformat()},
    {"record_id": 20, "city": "Jerusalem",    "category": "Infrastructure", "value": 78000,  "timestamp": (_base_time + timedelta(hours=19)).isoformat()},
]


# ══════════════════════════════════════════════════════════════
#  TASK 1 — PRODUCE (simulate Kafka producer)
# ══════════════════════════════════════════════════════════════
#  Write a function called produce_to_queue(records) that:
#    - Saves each record as a separate JSON file in RAW_LAYER/
#    - Name each file: "record_{record_id}.json"
#    - Logs: "Produced N messages to raw layer"
#    - Returns the count of files written
#
#  After defining the function, call it with SAMPLE_RECORDS.
#  Store the return value in produced_count.
#  Print: "Files in raw layer:", produced_count
#
#  Expected output:
#      2025-01-01 00:00:00 | INFO     | Produced 20 messages to raw layer
#      Files in raw layer: 20
#




def produce_to_queue(records):
    pass   # replace with your code




# ══════════════════════════════════════════════════════════════
#  TASK 2 — CONSUME (simulate Kafka consumer)
# ══════════════════════════════════════════════════════════════
#  Write a function called consume_from_queue() that:
#    - Reads all .json files from RAW_LAYER/
#    - Parses each file as JSON and adds each record to a list
#    - Logs: "Consumed N messages from raw layer"
#    - Returns the list of dicts
#
#  After defining the function, call it and store the result
#  in consumed_records.
#  Print: "Records consumed:", len(consumed_records)
#
#  Expected output:
#      2025-01-01 00:00:00 | INFO     | Consumed 20 messages from raw layer
#      Records consumed: 20
#




def consume_from_queue():
    pass   # replace with your code




# ══════════════════════════════════════════════════════════════
#  TASK 3 — TRANSFORM
# ══════════════════════════════════════════════════════════════
#  Write a function called transform_records(records) that
#  returns a new list of dicts. For each record:
#    - Convert "timestamp" string to a datetime object
#      (use datetime.fromisoformat)
#    - Strip leading/trailing whitespace from "city" values
#    - Filter OUT records where value <= 0
#      (log: "Filtered N invalid records (value <= 0)")
#    - Add a new field "processed_at" = datetime.now().isoformat()
#  Log: "Transform complete. N records remain after filtering."
#  Return the cleaned list.
#
#  After defining the function, call it with consumed_records.
#  Store the result in transformed_records.
#  Print: "After transform:", len(transformed_records)
#
#  Expected output:
#      2025-01-01 00:00:00 | INFO     | Filtered 3 invalid records (value <= 0)
#      2025-01-01 00:00:00 | INFO     | Transform complete. 17 records remain after filtering.
#      After transform: 17
#




def transform_records(records):
    pass   # replace with your code




# ══════════════════════════════════════════════════════════════
#  TASK 4 — LOAD TO DATABASE
# ══════════════════════════════════════════════════════════════
#  Write a function called load_to_database(records, db_path) that:
#    - Converts the list of dicts to a pandas DataFrame
#    - Converts "timestamp" and "processed_at" columns to strings
#      before saving (SQLite does not store datetime objects natively)
#    - Writes the DataFrame to a SQLite table called "city_metrics"
#      (use to_sql with if_exists="replace", index=False)
#    - Logs: "Loaded N rows to city_metrics"
#    - Returns the row count
#
#  After defining the function, call it with transformed_records
#  and DB_PATH. Store the result in loaded_count.
#  Print: "Rows in database:", loaded_count
#
#  Expected output:
#      2025-01-01 00:00:00 | INFO     | Loaded 17 rows to city_metrics
#      Rows in database: 17
#




def load_to_database(records, db_path):
    pass   # replace with your code




# ══════════════════════════════════════════════════════════════
#  TASK 5 — ANALYTICAL QUERIES
# ══════════════════════════════════════════════════════════════
#  Open a sqlite3 connection to DB_PATH and run these 3 queries.
#  Print each result with a clear label.
#
#  Query A — Total value per city:
#    SELECT city, SUM(value) as total_value
#    FROM city_metrics
#    GROUP BY city
#    ORDER BY total_value DESC
#
#  Query B — Average value per category:
#    SELECT category, ROUND(AVG(value), 2) as avg_value
#    FROM city_metrics
#    GROUP BY category
#    ORDER BY avg_value DESC
#
#  Query C — Top 5 records by value:
#    SELECT record_id, city, category, value
#    FROM city_metrics
#    ORDER BY value DESC
#    LIMIT 5
#
#  Expected output (values depend on your filtered data):
#      --- Total value per city ---
#      Tel Aviv : 275000
#      Jerusalem: 288000
#      ...
#      --- Average value per category ---
#      Infrastructure: 87166.67
#      ...
#      --- Top 5 records by value ---
#      11  Jerusalem  Health  112000
#      ...
#




# ══════════════════════════════════════════════════════════════
#  TASK 6 — FULL PIPELINE RUN AND RUN REPORT
# ══════════════════════════════════════════════════════════════
#  Write a function called run_full_pipeline() that calls steps
#  1 through 4 in order using the provided SAMPLE_RECORDS data.
#  It should return a dict with keys:
#    "records_produced", "records_consumed",
#    "records_after_transform", "records_loaded"
#
#  After defining the function, call it, then re-run your
#  3 analytical queries from Task 5, and print the run report
#  in this format:
#
#  Expected output:
#      ══════════════════════════════════════
#       MINI PIPELINE RUN REPORT
#      ══════════════════════════════════════
#       Records produced       : 20
#       Records consumed       : 20
#       Records after transform: 17
#       Records loaded         : 17
#      ══════════════════════════════════════
#




def run_full_pipeline():
    pass   # replace with your code




