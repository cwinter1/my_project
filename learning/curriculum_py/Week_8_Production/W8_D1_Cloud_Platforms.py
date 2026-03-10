# ══════════════════════════════════════════════════════════════
#  WEEK 8  |  DAY 1  |  CLOUD PLATFORMS
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Compare the three major cloud providers and their storage services
#  2. Read and write data to AWS S3 using boto3 (code as commented templates)
#  3. Understand cloud data warehouses and when to use each
#  4. Compare containers (Kubernetes) vs serverless (Lambda) for cloud compute
#
#  TIME:  ~40 minutes
#
#  YOUTUBE
#  ───────
#  Search: "AWS S3 Python boto3 tutorial"
#  Search: "Snowflake BigQuery Redshift comparison"
#  Search: "Kubernetes vs AWS Lambda serverless explained"
#  Search: "Docker and Kubernetes explained for beginners"
#  Search: "AWS Lambda tutorial Python beginner"
#
#  RECOMMENDED CHANNELS:
#  TechWorld with Nana — "Kubernetes Explained in 6 Minutes"
#  Fireship — "Serverless was a big mistake... or was it?"
#  ByteByteGo — "Kubernetes Explained in 15 Minutes"
#
# ══════════════════════════════════════════════════════════════

# NOTE: All cloud code is shown as COMMENTED TEMPLATES.
# Real cloud access requires valid credentials and running services.
# The concepts apply directly once you have your credentials configured.
#
# Install if needed:
#   pip install boto3              (AWS)
#   pip install google-cloud-storage (GCP)
#   pip install azure-storage-blob   (Azure)


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — CLOUD STORAGE: S3, GCP STORAGE, AZURE BLOB
# ══════════════════════════════════════════════════════════════
# Cloud object storage stores files (objects) in logical containers (buckets/containers).
# Unlike a database, it stores files in their original format (CSV, Parquet, JSON, etc.).
# It is cheap, scalable, and accessible from anywhere.
#
# SERVICE COMPARISON TABLE:
#
# Feature           | AWS S3            | GCP Cloud Storage   | Azure Blob Storage
# ------------------|-------------------|---------------------|------------------
# Container name    | Bucket            | Bucket              | Container
# Object/file URL   | s3://bucket/key   | gs://bucket/path    | https://account.blob.core.windows.net/container/blob
# Free tier         | 5 GB (12 months)  | 5 GB (always free)  | 5 GB (12 months)
# Python library    | boto3             | google-cloud-storage| azure-storage-blob
# Auth method       | IAM roles / keys  | Service account     | Connection string / Managed Identity
# Data format used  | CSV, Parquet, JSON| CSV, Parquet, JSON  | CSV, Parquet, JSON
#
# COMMON USE CASES IN DATA ENGINEERING:
#   - Landing zone: raw files dropped by source systems
#   - Data lake: long-term storage of all historical data
#   - Staging area: files ready to be loaded into a warehouse
#   - Outputs: reports and exports served to end users

# EXAMPLE ──────────────────────────────────────────────────────

print("=== CLOUD STORAGE COMPARISON ===")

services = [
    {"provider": "AWS",   "service": "Amazon S3",           "bucket_term": "bucket",    "protocol": "s3://"},
    {"provider": "GCP",   "service": "Google Cloud Storage","bucket_term": "bucket",    "protocol": "gs://"},
    {"provider": "Azure", "service": "Azure Blob Storage",  "bucket_term": "container", "protocol": "https://"},
]

for s in services:
    print(f"\n{s['provider']} — {s['service']}")
    print(f"  Container: {s['bucket_term']}")
    print(f"  Protocol:  {s['protocol']}<bucket_name>/<object_key>")

print()
print("All three offer:")
print("  - Object versioning (keep all previous versions)")
print("  - Lifecycle policies (auto-delete or archive after N days)")
print("  - Server-side encryption at rest")
print("  - Fine-grained access control (IAM / RBAC)")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
# Write a function called describe_storage_path(provider, bucket, folder, filename)
# that returns the full storage URL for a file.
#
# Rules:
#   AWS:   s3://<bucket>/<folder>/<filename>
#   GCP:   gs://<bucket>/<folder>/<filename>
#   Azure: https://<bucket>.blob.core.windows.net/<folder>/<filename>
#           (for Azure, bucket is the storage account name)
#
# Call it for all three providers:
#   describe_storage_path("AWS",   "my-data-lake", "raw/sales", "2024_01_sales.csv")
#   describe_storage_path("GCP",   "my-data-lake", "raw/sales", "2024_01_sales.csv")
#   describe_storage_path("Azure", "mydatalake",   "raw/sales", "2024_01_sales.csv")
#
# Expected output:
#   AWS:   s3://my-data-lake/raw/sales/2024_01_sales.csv
#   GCP:   gs://my-data-lake/raw/sales/2024_01_sales.csv
#   Azure: https://mydatalake.blob.core.windows.net/raw/sales/2024_01_sales.csv





# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — READING AND WRITING TO AWS S3 USING BOTO3
# ══════════════════════════════════════════════════════════════
# boto3 is the AWS SDK for Python.
# Authentication: set AWS credentials via environment variables or AWS CLI.
#
#   Set credentials (one-time setup):
#     aws configure                  (using AWS CLI)
#   -- or --
#     export AWS_ACCESS_KEY_ID=...   (environment variables)
#     export AWS_SECRET_ACCESS_KEY=...
#
# BOTO3 S3 OPERATIONS:
#   s3.upload_file(local_path, bucket, s3_key)
#   s3.download_file(bucket, s3_key, local_path)
#   s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
#   s3.delete_object(Bucket=bucket, Key=s3_key)

# EXAMPLE ──────────────────────────────────────────────────────

# TEMPLATE: boto3 S3 read/write (commented — requires real AWS credentials)
"""
import boto3
import pandas as pd
import io

# Create an S3 client
s3 = boto3.client("s3")

# --- UPLOAD a DataFrame as CSV to S3 ---
def upload_df_to_s3(df, bucket, key):
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=csv_buffer.getvalue()
    )
    print(f"Uploaded {len(df)} rows to s3://{bucket}/{key}")

# Usage:
# upload_df_to_s3(df_sales, "my-data-lake", "raw/sales/2024_01.csv")


# --- DOWNLOAD a CSV from S3 into a DataFrame ---
def download_df_from_s3(bucket, key):
    obj = s3.get_object(Bucket=bucket, Key=key)
    df = pd.read_csv(io.BytesIO(obj["Body"].read()))
    print(f"Downloaded {len(df)} rows from s3://{bucket}/{key}")
    return df

# Usage:
# df = download_df_from_s3("my-data-lake", "raw/sales/2024_01.csv")


# --- LIST all files in a folder ---
def list_s3_objects(bucket, prefix):
    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    if "Contents" not in response:
        return []
    return [obj["Key"] for obj in response["Contents"]]

# Usage:
# files = list_s3_objects("my-data-lake", "raw/sales/")
# for f in files:
#     print(f)


# --- Read a Parquet file from S3 (Parquet is faster than CSV for large data) ---
def read_parquet_from_s3(bucket, key):
    obj = s3.get_object(Bucket=bucket, Key=key)
    df = pd.read_parquet(io.BytesIO(obj["Body"].read()))
    return df
"""

print("\n=== boto3 TEMPLATES ===")
print("See commented code above for patterns to use once you have AWS credentials.")
print()
print("KEY OPERATIONS:")
print("  Upload DataFrame as CSV:     s3.put_object(Bucket=..., Key=..., Body=csv_string)")
print("  Download CSV into DataFrame: pd.read_csv(io.BytesIO(s3.get_object(...)['Body'].read()))")
print("  List files in folder:        s3.list_objects_v2(Bucket=..., Prefix='folder/')")
print("  Upload file directly:        s3.upload_file(local_path, bucket, key)")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
# In S3, files are organized by their "key" (the full path including filename).
# A common convention is: environment/layer/source/year/month/filename
# Example: prod/raw/crm/2024/01/contacts_20240115.csv
#
# Write a function called build_s3_key(env, layer, source, date_str, filename)
# where date_str is "YYYY-MM-DD" format.
# The function should parse year and month from date_str and build the key.
#
# Call it with:
#   build_s3_key("prod", "raw", "crm", "2024-01-15", "contacts.csv")
#   build_s3_key("dev",  "processed", "erp", "2024-03-22", "orders_clean.parquet")
#
# Expected output:
#   prod/raw/crm/2024/01/contacts.csv
#   dev/processed/erp/2024/03/orders_clean.parquet





# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — CLOUD DATA WAREHOUSES: SNOWFLAKE, BIGQUERY, REDSHIFT
# ══════════════════════════════════════════════════════════════
# A data warehouse is a database optimized for analytical queries on large datasets.
# Unlike transactional databases (fast for INSERT/UPDATE on individual rows),
# warehouses scan billions of rows quickly using columnar storage.
#
# Key features:
#   - Separate compute from storage (scale each independently)
#   - Columnar storage (only read the columns a query needs)
#   - Massively parallel processing (MPP)
#   - SQL interface (standard SQL plus extensions)

# EXAMPLE ──────────────────────────────────────────────────────

print("\n=== CLOUD DATA WAREHOUSE COMPARISON ===")

warehouses = [
    {
        "name": "Snowflake",
        "provider": "Multi-cloud (AWS/GCP/Azure)",
        "pricing": "Per second of compute (virtual warehouses)",
        "best_for": "Multi-cloud orgs, easy scaling, strong SQL support",
        "python_lib": "pip install snowflake-connector-python",
        "conn_example": "snowflake.connector.connect(user=..., password=..., account=...)",
    },
    {
        "name": "BigQuery",
        "provider": "Google Cloud (GCP)",
        "pricing": "Per TB of data scanned (serverless)",
        "best_for": "Serverless, GCP-native, very large datasets, ML integration",
        "python_lib": "pip install google-cloud-bigquery",
        "conn_example": "bigquery.Client(project='my-project')",
    },
    {
        "name": "Redshift",
        "provider": "Amazon Web Services (AWS)",
        "pricing": "Per node hour (provisioned) or per TB (serverless)",
        "best_for": "AWS-native, tight S3 integration, existing AWS infrastructure",
        "python_lib": "pip install redshift-connector  or  sqlalchemy-redshift",
        "conn_example": "redshift_connector.connect(host=..., database=..., user=..., password=...)",
    },
]

for wh in warehouses:
    print(f"\n{'='*50}")
    print(f"  {wh['name']} ({wh['provider']})")
    print(f"  Pricing:   {wh['pricing']}")
    print(f"  Best for:  {wh['best_for']}")
    print(f"  Python:    {wh['python_lib']}")
    print(f"  Connect:   {wh['conn_example']}")

print("\n=== PANDAS + WAREHOUSES ===")
print("All three work with pandas via SQLAlchemy or native connectors:")
print()
print("  # Snowflake + pandas")
print("  from snowflake.sqlalchemy import URL")
print("  engine = create_engine(URL(account=..., user=..., password=..., database=...))")
print("  df = pd.read_sql('SELECT * FROM sales.fact_orders LIMIT 1000', engine)")
print()
print("  # BigQuery + pandas")
print("  from google.cloud import bigquery")
print("  client = bigquery.Client()")
print("  df = client.query('SELECT * FROM dataset.table LIMIT 1000').to_dataframe()")
print()
print("  # Redshift + pandas (uses psycopg2 or redshift_connector)")
print("  import redshift_connector")
print("  conn = redshift_connector.connect(host=..., database=..., user=..., password=...)")
print("  df = pd.read_sql('SELECT * FROM public.sales LIMIT 1000', conn)")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
# Write a function called recommend_warehouse(scenario) that returns a
# recommendation based on the input scenario string.
#
# Rules:
#   If "gcp" or "google" in scenario (case-insensitive): recommend "BigQuery"
#   If "aws" or "amazon" in scenario: recommend "Redshift"
#   If "multi-cloud" or "snowflake" in scenario: recommend "Snowflake"
#   Otherwise: recommend "Snowflake (default choice for new projects)"
#
# Also print a one-sentence explanation.
#
# Test with:
#   recommend_warehouse("We run everything on AWS and use S3 for data lake storage")
#   recommend_warehouse("Our data team uses GCP for ML workloads")
#   recommend_warehouse("We have some AWS, some Azure, and want flexibility")
#   recommend_warehouse("We are a startup just getting started")
#
# Expected output:
#   Scenario: We run everything on AWS...
#   Recommendation: Redshift
#   Reason: Native AWS integration with tight S3 coupling
#   ...




# ══════════════════════════════════════════════════════════════
#  CONCEPT 4 — CLOUD COMPUTE: CONTAINERS VS SERVERLESS
# ══════════════════════════════════════════════════════════════
# So far we covered where to STORE data (S3, warehouses).
# Now: where does your CODE actually RUN in the cloud?
#
# There are two main models. Think of it like cooking:
#   Containers  = renting a full kitchen (you control everything)
#   Serverless  = ordering from a restaurant (they handle it all)
#
#
# CONTAINERS (Docker -> Kubernetes)
# ─────────────────────────────────
# Step 1: You write a Dockerfile — a recipe that says:
#           "Start with Python 3.11, install pandas, copy my script"
# Step 2: Docker builds that recipe into an IMAGE (a snapshot of your app)
# Step 3: You RUN the image — now it is a running CONTAINER
# Step 4: Kubernetes (K8s) manages many containers across many servers:
#           - If one crashes, K8s restarts it automatically
#           - If traffic increases, K8s starts more copies
#           - If a server dies, K8s moves containers to healthy servers
#
# WHAT KUBERNETES LOOKS LIKE IN PRACTICE:
#
#   You write a YAML file like this:
#     apiVersion: apps/v1
#     kind: Deployment
#     spec:
#       replicas: 3          <- "run 3 copies of my app"
#       containers:
#         - name: etl-worker
#           image: my-etl:v2 <- the Docker image to run
#           resources:
#             memory: "512Mi"
#             cpu: "250m"
#
#   Then: kubectl apply -f deployment.yaml
#   Kubernetes reads this and starts 3 containers on your cluster.
#
# MANAGED KUBERNETES SERVICES (so you don't build the cluster yourself):
#   AWS:   EKS (Elastic Kubernetes Service)
#   GCP:   GKE (Google Kubernetes Engine)
#   Azure: AKS (Azure Kubernetes Service)
#
# REAL USE CASES FOR CONTAINERS:
#   - A FastAPI service that serves ML predictions 24/7
#   - A Kafka consumer that processes real-time events non-stop
#   - An Airflow scheduler running your DAGs
#   - A Spark job that needs 64 GB of RAM for 4 hours
#
#
# SERVERLESS (AWS Lambda / GCP Cloud Functions / Azure Functions)
# ──────────────────────────────────────────────────────────────
# You write a single function. The cloud runs it when something happens.
# No servers. No Docker. No Kubernetes. Just: event -> function -> done.
#
# WHAT A LAMBDA FUNCTION LOOKS LIKE:
#
#   def lambda_handler(event, context):
#       # event = the trigger data (e.g., which file was uploaded)
#       bucket = event["Records"][0]["s3"]["bucket"]["name"]
#       key = event["Records"][0]["s3"]["object"]["key"]
#       # ... process the file ...
#       return {"statusCode": 200, "body": "Done"}
#
# TRIGGERS (what makes a Lambda function run):
#   - A file is uploaded to S3          (S3 event trigger)
#   - An HTTP request hits an API       (API Gateway trigger)
#   - A timer fires (e.g., every hour)  (CloudWatch/EventBridge schedule)
#   - A message arrives in a queue      (SQS/SNS trigger)
#
# REAL USE CASES FOR SERVERLESS:
#   - CSV lands in S3 -> Lambda cleans it -> loads to warehouse
#   - Every night at 2 AM -> Lambda generates a report
#   - User uploads an image -> Lambda resizes it
#   - API endpoint that gets 10 requests/day (would waste money on a server)
#
# LIMITS TO KNOW:
#   - Max execution time: 15 minutes (Lambda), 9 minutes (Cloud Functions)
#   - Max memory: 10 GB (Lambda)
#   - Cold start: first call after idle takes 0.5-2 seconds extra
#   - No persistent disk (everything must fit in memory or /tmp)
#
#
# COMPARISON TABLE:
#
# Feature              | Containers (K8s)         | Serverless (Lambda)
# ---------------------|--------------------------|---------------------------
# You manage servers?  | Yes (or managed K8s)     | No
# Startup time         | Already running          | Cold start (0.5-2 sec)
# Max run time         | Unlimited                | 15 minutes (Lambda)
# Scaling              | Manual or auto-scaler    | Automatic and instant
# Cost when idle       | You still pay            | Zero
# Deployment           | Docker + YAML + kubectl  | Upload function code
# Best for             | APIs, streaming, ML      | Event triggers, ETL, cron
# Learning curve       | High                     | Low
#
# DATA ENGINEERING RULE OF THUMB:
#   Short ETL triggered by a file upload?    -> Serverless
#   Always-on API serving predictions?       -> Containers
#   Kafka consumer running 24/7?             -> Containers
#   Nightly report that runs for 2 minutes?  -> Serverless
#   Training an ML model for 3 hours?        -> Containers
#   Tiny microservice with 5 requests/day?   -> Serverless

# EXAMPLE ──────────────────────────────────────────────────────

print("\n=== CONTAINERS VS SERVERLESS ===")

compute_options = [
    {
        "model": "Containers (Kubernetes)",
        "examples": ["AWS EKS", "GCP GKE", "Azure AKS"],
        "how_it_works": "Package code in Docker image -> deploy to cluster -> K8s manages scaling",
        "pay_for": "Cluster nodes running 24/7 (or per-pod with AWS Fargate)",
        "best_for": "Long-running services, full control, complex apps",
        "deploy_command": "docker build + kubectl apply -f deployment.yaml",
    },
    {
        "model": "Serverless (Functions)",
        "examples": ["AWS Lambda", "GCP Cloud Functions", "Azure Functions"],
        "how_it_works": "Upload function -> attach trigger -> cloud runs it on demand",
        "pay_for": "Each invocation (per millisecond of execution)",
        "best_for": "Event-driven tasks, short jobs, zero-maintenance ETL",
        "deploy_command": "aws lambda create-function --function-name my-etl ...",
    },
]

for opt in compute_options:
    print(f"\n{opt['model']}")
    print(f"  Services:  {', '.join(opt['examples'])}")
    print(f"  How:       {opt['how_it_works']}")
    print(f"  Pricing:   {opt['pay_for']}")
    print(f"  Best for:  {opt['best_for']}")
    print(f"  Deploy:    {opt['deploy_command']}")

print("\n--- Real-world scenario matching ---")

scenarios = [
    ("CSV lands in S3, clean and load to warehouse (takes 30 sec)",    "Serverless",  "Short, event-triggered, no server needed"),
    ("REST API serving ML predictions at 1000 req/sec",                "Containers",  "Always-on, high traffic, needs fast response"),
    ("Run a data quality check every night at 2 AM (takes 90 sec)",    "Serverless",  "Scheduled, short, would waste money as a server"),
    ("Kafka consumer processing a real-time click stream 24/7",        "Containers",  "Always-on, long-running, stateful connection"),
    ("Resize user-uploaded images on demand (takes 3 sec each)",       "Serverless",  "Event-driven, very short, unpredictable volume"),
]

for scenario, choice, reason in scenarios:
    print(f"\n  Scenario: {scenario}")
    print(f"  -> {choice}")
    print(f"     Why: {reason}")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 4
# ══════════════════════════════════════════════════════════════
# Write a function called pick_compute(description) that recommends
# "Serverless" or "Containers" based on keywords in the description.
#
# Rules (check lowercase version of description):
#   If any of these words appear: "trigger", "event", "nightly",
#     "cron", "short", "upload", "schedule" -> return "Serverless"
#   If any of these words appear: "streaming", "always-on", "api",
#     "long-running", "training", "24/7", "real-time" -> return "Containers"
#   Otherwise -> return "Could be either -- need more details"
#
# Print the description, recommendation, and a short reason.
#
# Test with:
#   pick_compute("A nightly cron job that cleans up old temp files")
#   pick_compute("An always-on API that serves ML predictions")
#   pick_compute("Trigger a transform when a CSV is uploaded to S3")
#   pick_compute("A streaming pipeline consuming from Kafka 24/7")
#   pick_compute("Generate a monthly PDF report")
#
# Expected output:
#   A nightly cron job that cleans up old temp files
#     -> Serverless (matched: nightly, cron)
#
#   An always-on API that serves ML predictions
#     -> Containers (matched: always-on, api)
#
#   Trigger a transform when a CSV is uploaded to S3
#     -> Serverless (matched: trigger, upload)
#
#   A streaming pipeline consuming from Kafka 24/7
#     -> Containers (matched: streaming, 24/7)
#
#   Generate a monthly PDF report
#     -> Could be either -- need more details




