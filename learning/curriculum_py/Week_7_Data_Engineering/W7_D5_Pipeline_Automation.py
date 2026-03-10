# ══════════════════════════════════════════════════════════════
#  WEEK 7  |  DAY 5  |  PIPELINE AUTOMATION
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Set up Python's logging module for structured pipeline logs
#  2. Schedule a pipeline to run at intervals using the schedule library
#  3. Wrap pipeline steps in try/except for error recovery and alerting
#
#  TIME:  ~30-35 minutes
#
#  YOUTUBE
#  ───────
#  Search: "Python logging module tutorial data engineering"
#  Search: "Python schedule library automate tasks"
#
# ══════════════════════════════════════════════════════════════

# Install if needed:  pip install schedule

import logging
import os
import time
from datetime import datetime
import pandas as pd
import io

this_dir = os.path.dirname(__file__)


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — LOGGING WITH PYTHON'S logging MODULE
# ══════════════════════════════════════════════════════════════
#
# print() is fine for quick debugging, but for production pipelines you need:
#   - Timestamps on every message
#   - Severity levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
#   - Log output to both the console AND a file simultaneously
#   - Ability to filter by level (suppress DEBUG in production)
#
# LOGGING LEVELS (from lowest to highest severity):
#   DEBUG    -- detailed diagnostic information (development only)
#   INFO     -- general operational messages (job started, rows read)
#   WARNING  -- something unexpected but not a failure
#   ERROR    -- a step failed but the pipeline can continue
#   CRITICAL -- the pipeline cannot continue
#
# SETUP PATTERN:
#   logging.basicConfig(...)  -- one-time configuration
#   logger = logging.getLogger("pipeline_name")
#   logger.info("message")
#   logger.error("message", exc_info=True)  -- includes stack trace

# EXAMPLE ──────────────────────────────────────────────────────

def setup_logger(pipeline_name, log_dir=None, level=logging.INFO):
    """
    Create a logger with console and optional file handlers.
    Returns a configured logger.
    """
    logger = logging.getLogger(pipeline_name)
    logger.setLevel(level)

    # Prevent adding duplicate handlers if function is called multiple times
    if logger.handlers:
        logger.handlers.clear()

    # Formatter: include timestamp, level, logger name, and message
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler — always add this
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler — add only if log_dir is specified
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f"{pipeline_name}.log")
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.info(f"Logging to file: {log_file}")

    return logger

# Create a logger for the daily sales pipeline
log_dir = os.path.join(this_dir, "logs")
logger = setup_logger("daily_sales_etl", log_dir=log_dir)

# Use the logger in pipeline steps
logger.info("Pipeline starting")
logger.info("Reading source file: sales_feed.csv")
logger.debug("Debug message — only visible in DEBUG mode")
logger.warning("Null values found in 'region' column — filling with 'Unknown'")
logger.info("Transformed 10 rows successfully")
logger.info("Loaded 10 rows to database")
logger.info("Pipeline complete")

# Simulate an error log
try:
    result = 1 / 0
except ZeroDivisionError as e:
    logger.error(f"Calculation failed: {e}", exc_info=True)

print("\nCheck the logs/ folder for daily_sales_etl.log")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1 — Logged Pipeline Steps
# ══════════════════════════════════════════════════════════════
#
# Create a new logger called "inventory_sync" that writes to the logs/ folder.
# Write a function called run_logged_pipeline(logger) that:
#   1. Logs INFO: "Starting inventory sync"
#   2. Logs INFO: "Connecting to source database"
#   3. Logs WARNING: "Source has 3 rows with null SKU — skipping them"
#   4. Logs INFO: "Processing 497 valid rows"
#   5. Logs INFO: "Loading to warehouse..."
#   6. Logs INFO: "Sync complete. Rows loaded: 497"
#   7. Returns True
#
# Call run_logged_pipeline with your new logger.
# Print: "Pipeline returned:", result
#
# Expected output (with timestamps):
#     2024-01-15 12:00:00 | INFO     | inventory_sync | Starting inventory sync
#     ...
#     Pipeline returned: True





# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — SCHEDULING WITH THE schedule LIBRARY
# ══════════════════════════════════════════════════════════════
#
# The schedule library lets you define when a function should run:
#   every 5 minutes, every hour, every day at 6:00 AM, etc.
#
# INSTALLATION: pip install schedule
#
# PATTERN:
#   import schedule
#   import time
#
#   def my_job():
#       print("Running job...")
#
#   schedule.every(5).minutes.do(my_job)
#   schedule.every().hour.do(my_job)
#   schedule.every().day.at("06:00").do(my_job)
#   schedule.every().monday.at("08:30").do(my_job)
#
#   while True:
#       schedule.run_pending()
#       time.sleep(1)
#
# The while True loop keeps the script running and checks for pending jobs.
# NOTE: schedule does NOT run in the background — it needs a dedicated process.
# For production automation, use cron (Linux), Task Scheduler (Windows),
# or Airflow/Prefect (see Week 8).

# EXAMPLE ──────────────────────────────────────────────────────

try:
    import schedule

    # Define the pipeline job
    def run_sales_etl_job():
        logger.info("Scheduled run starting...")
        # In production this would call your actual pipeline function
        logger.info("Extracting data...")
        logger.info("Transforming data...")
        logger.info("Loading data...")
        logger.info("Scheduled run complete.")
        return schedule.CancelJob   # return this to cancel after running once

    # Set up the schedule
    schedule.every(1).seconds.do(run_sales_etl_job)  # every second for demo

    print("\n=== SCHEDULE DEMO ===")
    print("Scheduled: run_sales_etl_job every 1 second")
    print("Running for 3 seconds then stopping...")

    # Run the loop for a short demo (time.sleep(1) then break avoids blocking forever)
    start_time = time.time()
    while True:
        schedule.run_pending()
        time.sleep(1)
        if time.time() - start_time > 3:   # run for 3 seconds max for demo
            break

    print("Schedule demo complete.")
    schedule.clear()   # clear all scheduled jobs

except ImportError:
    print("\nschedule not installed. Run: pip install schedule")
    print("Example schedule patterns:")
    print("  schedule.every(5).minutes.do(job)")
    print("  schedule.every().day.at('06:00').do(job)")
    print("  schedule.every().monday.do(job)")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 2 — Scheduled Job Simulator
# ══════════════════════════════════════════════════════════════
#
# Without actually blocking execution, write a function called
# simulate_scheduled_runs(job_function, run_count) that:
#   1. Calls job_function run_count times with a 0.1 second pause between calls
#   2. Prints "Run X of Y: <datetime_now>" before each call
#   3. Catches any exception from job_function and logs it as a warning
#   4. Returns a dict: {"total_runs": n, "successful": n, "failed": n}
#
# Write a job function called sample_job() that:
#   - Prints "Job executed"
#   - Returns True
#
# Call simulate_scheduled_runs(sample_job, 3) and print the summary.
#
# Expected output:
#     Run 1 of 3: 2024-01-15 12:00:00
#     Job executed
#     Run 2 of 3: 2024-01-15 12:00:00
#     Job executed
#     Run 3 of 3: 2024-01-15 12:00:00
#     Job executed
#     {'total_runs': 3, 'successful': 3, 'failed': 0}





# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — ERROR RECOVERY: try/except AROUND PIPELINE STEPS
# ══════════════════════════════════════════════════════════════
#
# A production pipeline must:
#   1. Catch errors at each step and log them (not crash silently)
#   2. Decide whether to continue or abort when a step fails
#   3. Send an alert (email, Slack, etc.) on critical failures
#   4. Record the failure in a log for post-mortem analysis
#
# PATTERNS:
#   - Wrap each stage in try/except
#   - Use a "pipeline_status" variable to track state
#   - Use finally to run cleanup code (close connections, write final log entry)
#   - Use raise to re-raise critical errors that must stop everything

# EXAMPLE ──────────────────────────────────────────────────────

# Simulated data source
SALES_CSV = """sale_id,sale_date,rep,product,qty,price
1,2024-01-10,Alice,Laptop,1,1299.99
2,2024-01-11,Bob,Monitor,2,399.99
3,CORRUPT_ROW
4,2024-01-13,Carol,Keyboard,3,149.99
"""

def extract_step(csv_data, pipeline_logger):
    """Extract step with error handling."""
    pipeline_logger.info("[EXTRACT] Starting extraction")
    try:
        df = pd.read_csv(io.StringIO(csv_data))
        pipeline_logger.info(f"[EXTRACT] Read {len(df)} rows")
        return df
    except Exception as e:
        pipeline_logger.error(f"[EXTRACT] Failed: {e}")
        raise   # re-raise to signal abort to the caller

def transform_step(df, pipeline_logger):
    """Transform step with error handling."""
    pipeline_logger.info("[TRANSFORM] Starting transformation")
    errors = []
    try:
        df["qty"]   = pd.to_numeric(df["qty"],   errors="coerce")
        df["price"] = pd.to_numeric(df["price"], errors="coerce")
        before = len(df)
        df = df.dropna(subset=["qty", "price"])
        dropped = before - len(df)
        if dropped > 0:
            pipeline_logger.warning(f"[TRANSFORM] Dropped {dropped} invalid rows")
            errors.append(f"{dropped} rows dropped")
        df["revenue"] = (df["qty"] * df["price"]).round(2)
        pipeline_logger.info(f"[TRANSFORM] Output: {len(df)} clean rows")
        return df
    except Exception as e:
        pipeline_logger.error(f"[TRANSFORM] Failed: {e}")
        raise

def load_step(df, output_path, pipeline_logger):
    """Load step with error handling."""
    pipeline_logger.info(f"[LOAD] Writing {len(df)} rows to {os.path.basename(output_path)}")
    try:
        df.to_csv(output_path, index=False)
        pipeline_logger.info("[LOAD] Complete")
        return len(df)
    except Exception as e:
        pipeline_logger.error(f"[LOAD] Failed: {e}")
        raise

def run_pipeline_with_recovery(csv_data, output_path, pipeline_logger):
    """
    Run the full ETL pipeline with error recovery at each step.
    Returns a run report dict.
    """
    run_report = {
        "pipeline": "daily_sales_etl",
        "start_time": datetime.now().isoformat(),
        "status": "started",
        "rows_extracted": 0,
        "rows_loaded": 0,
        "errors": [],
    }

    pipeline_logger.info("="*50)
    pipeline_logger.info("PIPELINE RUN STARTING")

    try:
        # Extract
        raw_df = extract_step(csv_data, pipeline_logger)
        run_report["rows_extracted"] = len(raw_df)

        # Transform
        clean_df = transform_step(raw_df, pipeline_logger)

        # Load
        rows_loaded = load_step(clean_df, output_path, pipeline_logger)
        run_report["rows_loaded"] = rows_loaded
        run_report["status"] = "success"

    except Exception as e:
        run_report["status"] = "failed"
        run_report["errors"].append(str(e))
        pipeline_logger.critical(f"PIPELINE FAILED: {e}")
        # In production: send_alert(email="data-team@corp.com", message=str(e))

    finally:
        run_report["end_time"] = datetime.now().isoformat()
        pipeline_logger.info(f"PIPELINE {run_report['status'].upper()}")
        pipeline_logger.info("="*50)

    return run_report

# Run the pipeline
output = os.path.join(this_dir, "recovered_output.csv")
report = run_pipeline_with_recovery(SALES_CSV, output, logger)

print("\n=== RUN REPORT ===")
for key, value in report.items():
    print(f"  {key:<20}: {value}")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 3 — Retry Logic
# ══════════════════════════════════════════════════════════════
#
# A common pattern in production is to retry a step if it fails (e.g. network error).
#
# Write a function called run_with_retry(func, max_attempts=3, delay_sec=0.5, **kwargs)
# that:
#   1. Tries to call func(**kwargs) up to max_attempts times
#   2. If the call succeeds (no exception), returns the result
#   3. If it fails, logs a WARNING with the attempt number and error
#   4. Waits delay_sec seconds between attempts (use time.sleep)
#   5. If all attempts fail, logs an ERROR and returns None
#
# To test: write a function called flaky_extract(fail_count) that uses a
# mutable list or global to track how many times it has been called,
# raising an Exception on the first fail_count calls, then succeeding.
#
# Test: flaky_extract should fail twice then succeed on attempt 3.
#
# Expected output:
#     WARNING: Attempt 1 failed: Simulated failure
#     WARNING: Attempt 2 failed: Simulated failure
#     INFO: Attempt 3 succeeded.
#     Result: 'success'




