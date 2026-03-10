# ══════════════════════════════════════════════════════════════
#  WEEK 12  |  DAY 5  |  ORCHESTRATE — FINAL PIPELINE RUN
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Configure Python logging with timestamp and level
#  2. Orchestrate a multi-stage pipeline by chaining outputs
#  3. Build a structured run report with timing and error counts
#
#  PIPELINE CONTEXT
#  ─────────────────
#  This is Stage 5 (final) of the capstone pipeline:
#    Day 1: Docker + Kafka setup (simulation)
#    Day 2: Extract data from API, produce to Kafka
#    Day 3: Store raw records in Bronze layer (MinIO)
#    Day 4: Transform and load to PostgreSQL (Silver)
#    Day 5: Orchestrate the full pipeline with logging  <-- today
#
#  Today we wire all four stages together into a single
#  run_pipeline() function.  Each stage's output becomes the
#  next stage's input.  Failures are caught per-stage so one
#  broken stage does not crash the entire pipeline.
#
#  TIME:  ~45 minutes
#
# ══════════════════════════════════════════════════════════════


import logging
import time
import os
import json
import sqlite3
from datetime import datetime


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — PYTHON LOGGING MODULE
# ══════════════════════════════════════════════════════════════
#
#  The logging module is the standard way to emit structured
#  messages in Python programs.  Unlike print(), log messages
#  include a level (DEBUG, INFO, WARNING, ERROR, CRITICAL) and
#  can be routed to files, external systems, or filtered by
#  level at runtime.
#
#  basicConfig() sets up the root logger with one call:
#    level   — minimum severity to display (INFO = show INFO+)
#    format  — format string for each log line
#    handlers — where to send log output (default: stderr)
#
#  Useful format tokens:
#    %(asctime)s    — timestamp (e.g. 2024-01-15 10:22:05,123)
#    %(levelname)s  — INFO, WARNING, ERROR, etc.
#    %(message)s    — the message string
#
#  The four main log levels in order of severity:
#    logging.debug(msg)    — verbose detail (disabled in INFO mode)
#    logging.info(msg)     — normal progress messages
#    logging.warning(msg)  — something unexpected but not fatal
#    logging.error(msg)    — a stage failed; pipeline may continue
#
#  Call basicConfig only once per program (at the top-level
#  script).  Calling it inside a function has no effect if the
#  root logger was already configured.
#
# EXAMPLE ──────────────────────────────────────────────────────

# Configure the root logger (call this once at the top of the script).
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logging.info("Logging is configured.")
logging.info("Pipeline script starting.")
logging.warning("This is a WARNING — something unexpected but the script continues.")
logging.error("This is an ERROR — a stage would have failed here.")
logging.info("After the ERROR, the pipeline continues.")


# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — ORCHESTRATION PATTERN
# ══════════════════════════════════════════════════════════════
#
#  Orchestration means running each stage in order and passing
#  the output of one stage as the input to the next.
#
#  The pattern for a robust pipeline:
#
#    try:
#        stage_output = run_stage(previous_output)
#        logging.info(f"Stage done: {len(stage_output)} records")
#    except Exception as e:
#        logging.error(f"Stage failed: {e}")
#        stage_output = []   # continue with empty data
#
#  If a stage fails, we set its output to [] and let the next
#  stage run.  The downstream stage will produce 0 records,
#  which is safe.  The run report will capture the error.
#
#  Why catch Exception (broad) instead of a specific type?
#  In orchestration code, we want to catch any unexpected error
#  (database down, disk full, network timeout) so the orchestrator
#  itself never crashes.  The error is recorded in the report.
#
# EXAMPLE ──────────────────────────────────────────────────────

def stage_extract_sim(resource_id, limit):
    """Simulate the extract stage — return fake records."""
    records = [
        {"_id": i, "district": f"District_{i % 4 + 1}", "count": i * 10, "year": 2023}
        for i in range(1, limit + 1)
    ]
    return records

def stage_transform_sim(raw_records):
    """Simulate the transform stage — add loaded_at to each record."""
    cleaned = []
    for r in raw_records:
        r_copy = dict(r)
        r_copy["loaded_at"] = datetime.now().isoformat()
        cleaned.append(r_copy)
    return cleaned

def stage_load_sim(records):
    """Simulate the load stage — insert into in-memory SQLite."""
    conn = sqlite3.connect(":memory:")
    c = conn.cursor()
    c.execute("CREATE TABLE pipeline_data (id INTEGER, district TEXT, count INTEGER, year INTEGER, loaded_at TEXT)")
    rows = [(r["_id"], r["district"], r["count"], r["year"], r["loaded_at"]) for r in records]
    c.executemany("INSERT INTO pipeline_data VALUES (?, ?, ?, ?, ?)", rows)
    conn.commit()
    c.execute("SELECT COUNT(*) FROM pipeline_data")
    row_count = c.fetchone()[0]
    conn.close()
    return row_count

# Run the three stages in sequence, passing outputs forward.
logging.info("Orchestration demo starting.")

try:
    raw = stage_extract_sim("demo-resource", limit=10)
    logging.info(f"Stage EXTRACT done: {len(raw)} records fetched")
except Exception as e:
    logging.error(f"Stage EXTRACT failed: {e}")
    raw = []

try:
    cleaned = stage_transform_sim(raw)
    logging.info(f"Stage TRANSFORM done: {len(cleaned)} records cleaned")
except Exception as e:
    logging.error(f"Stage TRANSFORM failed: {e}")
    cleaned = []

try:
    loaded_count = stage_load_sim(cleaned)
    logging.info(f"Stage LOAD done: {loaded_count} rows in database")
except Exception as e:
    logging.error(f"Stage LOAD failed: {e}")
    loaded_count = 0

logging.info("Orchestration demo complete.")


# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — RUN REPORT
# ══════════════════════════════════════════════════════════════
#
#  A run report is a dict that captures the outcome of one
#  pipeline execution.  It is printed at the end of every run
#  so the operator can see at a glance what happened.
#
#  Standard run report keys:
#
#    started_at        — ISO timestamp when run_pipeline() started
#    finished_at       — ISO timestamp when run_pipeline() ended
#    duration_seconds  — float, finished - started in seconds
#    records_fetched   — int, how many records the extract stage got
#    records_loaded    — int, how many rows were written to the DB
#    errors            — list of error message strings (empty = success)
#
#  Use time.time() to measure elapsed time:
#    t_start = time.time()
#    ... do work ...
#    duration = round(time.time() - t_start, 2)
#
#  After building the report dict, print it one key per line
#  for readability.
#
# EXAMPLE ──────────────────────────────────────────────────────

t0 = time.time()
time.sleep(0.05)   # simulate work taking 50 ms
t1 = time.time()

demo_report = {
    "started_at":       datetime.now().isoformat()[:19],
    "finished_at":      datetime.now().isoformat()[:19],
    "duration_seconds": round(t1 - t0, 2),
    "records_fetched":  10,
    "records_loaded":   10,
    "errors":           [],
}

print("\nRun report example:")
for key, value in demo_report.items():
    print(f"  {key:<22} : {value}")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
#
#  Set up logging and write a function run_pipeline(resource_id,
#  output_folder, db_path) that orchestrates all four stages.
#
#  The stages (all simulated inline — no imports needed):
#    Stage 1 EXTRACT  : call stage_extract_sim(resource_id, limit=20)
#    Stage 2 PRODUCE  : append each record to a list called topic_queue
#    Stage 3 BRONZE   : call json.dumps() on topic_queue, write to file
#                       named f"{output_folder}/raw_{today}.json"
#                       where today = datetime.now().strftime("%Y-%m-%d")
#    Stage 4 LOAD     : call stage_load_sim(topic_queue)
#
#  After each stage, log an INFO message:
#    "Stage EXTRACT complete: 20 records"
#    "Stage PRODUCE complete: 20 records in queue"
#    "Stage BRONZE complete: saved to raw_2024-01-15.json"
#    "Stage LOAD complete: 20 rows in database"
#
#  Call run_pipeline("gov-resource-001", output_folder, ":memory:")
#
#  Expected output (logging lines):
#    2024-01-15 10:22:05  INFO      Stage EXTRACT complete: 20 records
#    2024-01-15 10:22:05  INFO      Stage PRODUCE complete: 20 records in queue
#    2024-01-15 10:22:05  INFO      Stage BRONZE complete: saved to raw_2024-01-15.json
#    2024-01-15 10:22:05  INFO      Stage LOAD complete: 20 rows in database

# --- starting data ---
output_folder = os.path.join(os.path.dirname(__file__), "pipeline_output")
os.makedirs(output_folder, exist_ok=True)




# (write your code here)




# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
#
#  Modify run_pipeline from Exercise 1 to add per-stage
#  error handling.
#
#  Wrap each stage call in try/except Exception as e:
#    - On success: log INFO as before
#    - On failure: log ERROR with the message, set stage output to []
#      and append the error message string to an errors list
#    - The pipeline must always reach Stage 4 even if earlier stages fail
#
#  To test the error path, add this line at the top of run_pipeline
#  (before Stage 1):
#    raise_on_stage = 2   # set to 1,2,3,4 to simulate a failure
#
#  Then in Stage 2's try block, before the main code, add:
#    if raise_on_stage == 2:
#        raise RuntimeError("Simulated Stage 2 failure")
#
#  Call run_pipeline with raise_on_stage = 2.
#
#  Expected output:
#    INFO      Stage EXTRACT complete: 20 records
#    ERROR     Stage PRODUCE failed: Simulated Stage 2 failure
#    INFO      Stage BRONZE complete: saved to raw_2024-01-15.json
#    INFO      Stage LOAD complete: 0 rows in database
#    WARNING   Pipeline completed with 1 error(s)

# --- starting data ---
# No additional variables needed




# (write your code here)




# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
#
#  Add a run report to run_pipeline from Exercise 2.
#
#  At the START of run_pipeline, record:
#    t_start    = time.time()
#    started_at = datetime.now().isoformat()[:19]
#
#  At the END (after all four stages and error checks), build
#  a run_report dict with these exact keys:
#    started_at        — string from above
#    finished_at       — datetime.now().isoformat()[:19]
#    duration_seconds  — round(time.time() - t_start, 2)
#    records_fetched   — count from Stage 1 (0 if failed)
#    records_loaded    — count from Stage 4 (0 if failed)
#    errors            — list of error strings (empty = clean run)
#
#  Print the run report one key per line, then return it.
#
#  Call run_pipeline with raise_on_stage = 0 (no failures) and
#  print the returned report to verify all keys are present.
#
#  Expected output:
#    INFO      Stage EXTRACT complete: 20 records
#    INFO      Stage PRODUCE complete: 20 records in queue
#    INFO      Stage BRONZE complete: saved to raw_2024-01-15.json
#    INFO      Stage LOAD complete: 20 rows in database
#    Run report:
#      started_at             : 2024-01-15T10:22:05
#      finished_at            : 2024-01-15T10:22:05
#      duration_seconds       : 0.02
#      records_fetched        : 20
#      records_loaded         : 20
#      errors                 : []

# --- starting data ---
# No additional variables needed




# (write your code here)




