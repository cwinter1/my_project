# ══════════════════════════════════════════════════════════════
#  WEEK 8  |  DAY 2  |  ORCHESTRATION AND AIRFLOW
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Understand what a DAG is and how Apache Airflow orchestrates pipelines
#  2. Write a basic Airflow DAG in Python (as a commented template)
#  3. Configure task dependencies, sensors, and retries in Airflow
#
#  TIME:  ~30 minutes
#
#  YOUTUBE
#  ───────
#  Search: "Apache Airflow tutorial Python DAG beginner"
#  Search: "Prefect Python orchestration tutorial"
#
# ══════════════════════════════════════════════════════════════

# NOTE: Airflow code is shown as COMMENTED TEMPLATES.
# Running Airflow requires a local installation (pip install apache-airflow)
# and a running Airflow webserver + scheduler process.
# Prefect is shown as a simpler alternative that runs without a server.
#
# Install Airflow:  pip install apache-airflow
# Install Prefect: pip install prefect


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — WHAT IS A DAG AND HOW AIRFLOW WORKS
# ══════════════════════════════════════════════════════════════
# ORCHESTRATION is the automated coordination of pipeline steps:
#   - Deciding WHEN to run each step
#   - Deciding in what ORDER steps run
#   - Handling failures, retries, and alerts
#   - Providing visibility into what ran, when, and what failed
#
# DAG = Directed Acyclic Graph
#   Directed:  edges point in one direction (A -> B means B runs after A)
#   Acyclic:   no cycles (B cannot be upstream of A if A is upstream of B)
#   Graph:     a network of nodes (tasks) and edges (dependencies)
#
# AIRFLOW CONCEPTS:
#   DAG:       the pipeline definition (a Python file in the dags/ folder)
#   Task:      one unit of work (a Python function, a SQL query, a shell command)
#   Operator:  a task template (PythonOperator, BashOperator, SqlOperator)
#   Trigger:   what starts the DAG (schedule, manual, sensor, API call)
#   XCom:      mechanism for tasks to pass data to each other
#
# HOW AIRFLOW RUNS:
#   1. You place a .py file defining a DAG in the dags/ folder
#   2. The Airflow Scheduler reads it and schedules runs based on the cron string
#   3. The Airflow Executor runs each task when its dependencies are met
#   4. The Airflow Webserver shows the status in a visual UI

# EXAMPLE ──────────────────────────────────────────────────────

print("=== AIRFLOW CONCEPTS ===")
concepts = [
    ("DAG",       "The entire pipeline definition -- a Python file with tasks and dependencies"),
    ("Task",      "One unit of work (extract, transform, load, email, etc.)"),
    ("Operator",  "A reusable task template (Python, Bash, SQL, Email)"),
    ("Schedule",  "Cron expression or timedelta: when the DAG runs automatically"),
    ("Backfill",  "Run the DAG for historical dates it missed"),
    ("XCom",      "Cross-communication: one task passes a value to another"),
    ("Sensor",    "A task that waits for a condition (file to arrive, API to respond)"),
]
for name, desc in concepts:
    print(f"  {name:<12}: {desc}")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
# A daily ETL pipeline has these steps in order:
#   1. Check if the source file exists
#   2. Extract data from CSV
#   3. Validate the data
#   4. Transform the data
#   5. Load to database
#   6. Send completion email
#
# Write a function called describe_dag_tasks(steps) that:
#   - Accepts a list of step names
#   - For each step, prints: "Task N: <step_name> | depends on: <previous_step>"
#   - The first step has no dependency
#
# Expected output:
#   Task 1: check_file_exists  | depends on: (start)
#   Task 2: extract_csv        | depends on: check_file_exists
#   Task 3: validate_data      | depends on: extract_csv
#   Task 4: transform_data     | depends on: validate_data
#   Task 5: load_to_database   | depends on: transform_data
#   Task 6: send_email         | depends on: load_to_database
# --- starting data ---
steps = ["check_file_exists", "extract_csv", "validate_data",
         "transform_data", "load_to_database", "send_email"]





# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — WRITING A BASIC AIRFLOW DAG (COMMENTED TEMPLATE)
# ══════════════════════════════════════════════════════════════
# An Airflow DAG file must:
#   1. Create a DAG object with an id, start_date, and schedule
#   2. Define task functions (using @task decorator or Operators)
#   3. Set task dependencies using >> operator

# EXAMPLE ──────────────────────────────────────────────────────

# TEMPLATE -- A complete daily sales ETL DAG (save this as dags/daily_sales_etl.py)
"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email  import EmailOperator
from datetime import datetime, timedelta
import pandas as pd

# Default arguments applied to all tasks
default_args = {
    "owner":            "data_team",
    "email":            ["data-alerts@company.com"],
    "email_on_failure": True,
    "email_on_retry":   False,
    "retries":          2,
    "retry_delay":      timedelta(minutes=5),
}

# Define the DAG
with DAG(
    dag_id="daily_sales_etl",
    default_args=default_args,
    description="Extract, transform, and load daily sales data",
    schedule="0 6 * * *",          # cron: every day at 06:00 UTC
    start_date=datetime(2024, 1, 1),
    catchup=False,                  # do not backfill missed runs
    tags=["sales", "etl", "daily"],
) as dag:

    # Task 1: Extract
    def extract_sales(**context):
        print("Extracting sales data...")
        # In production: read from S3, SFTP, or database
        df = pd.read_csv("s3://my-bucket/raw/sales/{{ ds }}.csv")
        # Pass row count to next task via XCom
        context["ti"].xcom_push(key="row_count", value=len(df))
        df.to_parquet("/tmp/raw_sales.parquet")
        return f"Extracted {len(df)} rows"

    # Task 2: Transform
    def transform_sales(**context):
        row_count = context["ti"].xcom_pull(task_ids="extract", key="row_count")
        print(f"Transforming {row_count} rows...")
        df = pd.read_parquet("/tmp/raw_sales.parquet")
        df["revenue"] = df["qty"] * df["price"]
        df.to_parquet("/tmp/clean_sales.parquet")
        return "Transform complete"

    # Task 3: Load
    def load_sales(**context):
        print("Loading to warehouse...")
        df = pd.read_parquet("/tmp/clean_sales.parquet")
        # In production: load to Snowflake, BigQuery, or Redshift
        print(f"Loaded {len(df)} rows")

    # Create operator instances
    task_extract   = PythonOperator(task_id="extract",   python_callable=extract_sales)
    task_transform = PythonOperator(task_id="transform", python_callable=transform_sales)
    task_load      = PythonOperator(task_id="load",      python_callable=load_sales)
    task_email     = EmailOperator(
        task_id="notify",
        to=["data-team@company.com"],
        subject="Daily Sales ETL Complete",
        html_content="<p>ETL ran successfully for {{ ds }}</p>",
    )

    # Set dependencies: each task runs after the previous one completes
    task_extract >> task_transform >> task_load >> task_email
"""

print("\n=== AIRFLOW DAG TEMPLATE ===")
print("See commented code above for a complete DAG definition.")
print()
print("CRON SCHEDULE EXAMPLES:")
cron_examples = [
    ("0 6 * * *",     "Every day at 06:00 UTC"),
    ("0 */4 * * *",   "Every 4 hours"),
    ("0 9 * * 1",     "Every Monday at 09:00 UTC"),
    ("0 8 1 * *",     "First day of every month at 08:00 UTC"),
    ("@daily",        "Once per day (shorthand for '0 0 * * *')"),
    ("@hourly",       "Once per hour"),
]
for cron, description in cron_examples:
    print(f"  '{cron}'  ->  {description}")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
# Write a function called parse_cron(cron_expression) that returns a plain-English
# description of the cron schedule.
#
# Handle these patterns (you can use simple string matching, not a full parser):
#   "@daily"           -> "Every day at midnight"
#   "@hourly"          -> "Every hour"
#   "@weekly"          -> "Every Sunday at midnight"
#   "@monthly"         -> "First day of every month at midnight"
#   "0 6 * * *"        -> "Every day at 06:00"
#   "0 */4 * * *"      -> "Every 4 hours"
#   "0 9 * * 1"        -> "Every Monday at 09:00"
#   Anything else      -> "Custom schedule: <expression>"
#
# Test with all the examples above.
#
# Expected output:
#   @daily      -> Every day at midnight
#   @hourly     -> Every hour
#   0 6 * * *   -> Every day at 06:00
#   0 */4 * * * -> Every 4 hours
#   0 9 * * 1   -> Every Monday at 09:00





# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — TASK DEPENDENCIES, SENSORS, AND RETRIES
# ══════════════════════════════════════════════════════════════
# TASK DEPENDENCIES:
#   task_a >> task_b           -- b runs after a (a upstream of b)
#   task_a >> [task_b, task_c] -- b and c run in parallel after a
#   [task_b, task_c] >> task_d -- d runs after BOTH b and c finish
#   task_a << task_b           -- same as task_b >> task_a (a depends on b)
#
# SENSORS:
#   A sensor is a special task that WAITS for a condition before allowing
#   downstream tasks to proceed.
#   FileSensor:      waits for a file to appear on a filesystem
#   HttpSensor:      waits for an HTTP endpoint to return 200
#   SqlSensor:       waits for a SQL query to return non-empty results
#   ExternalTaskSensor: waits for a task in ANOTHER DAG to complete
#
# RETRIES:
#   retries=3            -- try the task up to 3 additional times on failure
#   retry_delay=timedelta(minutes=5)  -- wait 5 minutes between retries
#   retry_exponential_backoff=True    -- increase delay exponentially
#
# TASK TRIGGER RULES:
#   trigger_rule="all_success"   -- run only if ALL upstream tasks succeeded (default)
#   trigger_rule="all_done"      -- run regardless of upstream success/failure
#   trigger_rule="one_failed"    -- run if at least one upstream task failed (alerting)

# EXAMPLE ──────────────────────────────────────────────────────

print("\n=== AIRFLOW DEPENDENCY PATTERNS ===")

dependency_patterns = [
    ("Linear chain",        "extract >> transform >> load >> notify",
                            "Each step waits for the previous to complete"),
    ("Fan-out",             "extract >> [transform_a, transform_b, transform_c]",
                            "Three transforms run in parallel after extract"),
    ("Fan-in",              "[transform_a, transform_b] >> load",
                            "Load waits for BOTH transforms to complete"),
    ("Diamond",             "extract >> [clean, validate] >> merge >> load",
                            "Classic ETL with parallel middle steps"),
    ("Conditional",         "check_file >> [extract, skip_task]",
                            "Branch based on whether source file exists"),
]

for name, pattern, description in dependency_patterns:
    print(f"\n  {name}:")
    print(f"    Code:    {pattern}")
    print(f"    Meaning: {description}")

# PREFECT -- A SIMPLER ALTERNATIVE TO AIRFLOW
print("\n=== PREFECT ALTERNATIVE ===")
print("""
Prefect is a modern workflow orchestration tool that is easier to set up than Airflow.
It does not require a separate server or database for local runs.

Install:  pip install prefect

Example Prefect flow:

    from prefect import flow, task

    @task
    def extract():
        return [1, 2, 3]

    @task
    def transform(data):
        return [x * 2 for x in data]

    @task
    def load(data):
        print("Loaded:", data)

    @flow(name="daily_sales_etl")
    def sales_pipeline():
        raw = extract()
        clean = transform(raw)
        load(clean)

    if __name__ == "__main__":
        sales_pipeline()

# Run locally: python my_pipeline.py
# Deploy to Prefect Cloud for scheduling, monitoring, and alerting
""")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
# Build a simple in-memory DAG executor (no Airflow needed).
#
# Write a class called SimpleDag that:
#   - Has an add_task(name, func, depends_on=[]) method
#   - Has a run() method that:
#       1. Builds the execution order from dependencies (topological sort)
#       2. Runs each task in the correct order
#       3. Prints: "Running task: <name>" before each task
#       4. Catches exceptions and prints: "Task <name> FAILED: <error>"
#          but continues to other tasks where possible
#       5. Returns a dict: {task_name: "success"/"failed"}
#
# Define these tasks (use simple print functions):
#   extract:   prints "Extracting..." returns 100
#   validate:  depends on extract, prints "Validating 100 rows..."
#   transform: depends on validate, prints "Transforming..."
#   load:      depends on transform, prints "Loading..."
#   notify:    depends on load, prints "Sending notification..."
#
# Expected output:
#   Running task: extract    -> Extracting...
#   Running task: validate   -> Validating...
#   Running task: transform  -> Transforming...
#   Running task: load       -> Loading...
#   Running task: notify     -> Sending notification...
#   {'extract': 'success', 'validate': 'success', ...}




