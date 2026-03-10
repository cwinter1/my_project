# ══════════════════════════════════════════════════════════════
#  WEEK 12  |  CAPSTONE PROJECT  |  OVERVIEW
# ══════════════════════════════════════════════════════════════
#
#  PROJECT GOAL
#  ────────────────────────────────────
#  Build a real data engineering pipeline from scratch using
#  Israeli Government open data.  The pipeline ingests live data
#  from the government API, streams it through Kafka, stores raw
#  files in MinIO object storage (the "Bronze" layer), transforms
#  and loads clean records into PostgreSQL (the "Silver" layer),
#  and exposes the results as a Grafana dashboard.
#
#  Every day you build one stage.  By Day 5 you have a working
#  end-to-end pipeline that a junior data engineer could put on
#  a resume.
#
#  SIMULATION MODE vs REAL MODE
#  ────────────────────────────────────
#  Each day file contains two modes:
#
#    SIMULATION MODE  — runs on any machine right now with no
#                       extra software.  Uses Python lists,
#                       local files, and SQLite to mimic each
#                       service.  You learn the logic without
#                       fighting with Docker.
#
#    REAL MODE        — the production code shown in comments.
#                       Activate it once Docker is running by
#                       uncommenting the relevant block.  The
#                       APIs are identical; only the connection
#                       target changes.
#
#  TIME:  This file is read-only — no exercises here.
#         Estimated total capstone time: ~4-5 hours across 5 days.
#
# ══════════════════════════════════════════════════════════════


# ══════════════════════════════════════════════════════════════
#  ARCHITECTURE DIAGRAM
# ══════════════════════════════════════════════════════════════
#
#   Israeli Gov API
#   (data.gov.il)
#         |
#         |  HTTP GET (requests)
#         v
#   ┌─────────────┐
#   │  PRODUCER   │  Day 2 — fetch records, push to Kafka topic
#   │  (Python)   │
#   └──────┬──────┘
#          |
#          |  Kafka topic: "gov-data-raw"
#          v
#   ┌─────────────┐
#   │    KAFKA    │  Day 1 — message broker, decouples stages
#   │  (broker)   │
#   └──────┬──────┘
#          |
#          |  Consumer reads messages
#          v
#   ┌─────────────┐
#   │    MinIO    │  Day 3 — object storage, saves raw JSON files
#   │  (Bronze)   │          (like AWS S3 but runs locally)
#   └──────┬──────┘
#          |
#          |  Load raw files, transform records
#          v
#   ┌─────────────┐
#   │ PostgreSQL  │  Day 4 — relational DB, stores clean records
#   │  (Silver)   │
#   └──────┬──────┘
#          |
#          |  SQL queries / metrics
#          v
#   ┌─────────────┐
#   │   Grafana   │  Day 5 — dashboard shows charts from the DB
#   │ (dashboard) │
#   └─────────────┘
#
#   SIMULATION equivalents:
#     Kafka     ->  Python list  (in-memory queue)
#     MinIO     ->  local folder (bronze_layer/)
#     PostgreSQL->  SQLite file  (pipeline.db)
#     Grafana   ->  printed summary + matplotlib (optional)
#
# ══════════════════════════════════════════════════════════════


# ══════════════════════════════════════════════════════════════
#  5-DAY PLAN
# ══════════════════════════════════════════════════════════════
#
#  Day 1  —  Docker & Kafka Setup
#            Understand containers and message brokers.
#            Simulate a Kafka topic with a Python list.
#            Learn: producer, consumer, topic, offset.
#
#  Day 2  —  Extract: API → Producer
#            Call the Israeli Gov API with requests.
#            Parse JSON records.
#            Push records to the Kafka queue (simulated or real).
#
#  Day 3  —  Store: Consumer → MinIO (Bronze Layer)
#            Read messages from the queue.
#            Save raw JSON files to a local folder (or real MinIO).
#            Learn: Bronze/Silver/Gold naming convention.
#
#  Day 4  —  Transform & Load: Bronze → PostgreSQL (Silver Layer)
#            Read raw files, clean nulls, rename columns.
#            Load clean records into SQLite (or real PostgreSQL).
#            Write SQL queries to explore the loaded data.
#
#  Day 5  —  Orchestrate: Full Pipeline Run
#            Wire all 4 stages together in one function.
#            Add logging with timestamps.
#            Generate a run report (records fetched, loaded, errors).
#
# ══════════════════════════════════════════════════════════════


# ══════════════════════════════════════════════════════════════
#  DATA SOURCE — ISRAELI GOVERNMENT OPEN DATA API
# ══════════════════════════════════════════════════════════════
#
#  Base URL:
#    https://data.gov.il/api/3/action/datastore_search
#
#  Query parameters:
#    resource_id  — identifies the specific dataset table
#    limit        — max number of records to return (default 100)
#    offset       — skip N records (for pagination)
#
#  Full example URL:
#    https://data.gov.il/api/3/action/datastore_search
#      ?resource_id=5e87a7a1-2f6f-41c1-8aec-7216d52a6cf6
#      &limit=100
#
#  The response is JSON with this shape:
#    {
#      "success": true,
#      "result": {
#        "total": 12345,
#        "records": [
#          {"_id": 1, "field1": "value", "field2": 42, ...},
#          ...
#        ]
#      }
#    }
#
#  Resource IDs used in this capstone:
#    Traffic accidents: 5e87a7a1-2f6f-41c1-8aec-7216d52a6cf6
#
#  Find more datasets at:  https://data.gov.il/dataset
#
# ══════════════════════════════════════════════════════════════


# ══════════════════════════════════════════════════════════════
#  SETUP REQUIREMENTS
# ══════════════════════════════════════════════════════════════
#
#  SIMULATION MODE — no extra installation needed.
#  Just make sure these standard/common packages are available:
#    pip install requests
#
#  REAL MODE — install Docker Desktop first, then:
#    pip install confluent-kafka boto3 psycopg2-binary
#
#  Docker Desktop download:
#    https://www.docker.com/products/docker-desktop/
#
#  To start all services at once, run from your project folder:
#    docker-compose up -d
#
#  (See the docker-compose.yml snippet below.)
#
# ══════════════════════════════════════════════════════════════


# ══════════════════════════════════════════════════════════════
#  DOCKER COMPOSE CONFIGURATION
# ══════════════════════════════════════════════════════════════
#
#  Save the following as  docker-compose.yml  in your project
#  folder, then run:  docker-compose up -d
#
# ─────────────────────────────────────────────────────────────
#
# version: "3.8"
# services:
#
#   zookeeper:
#     image: confluentinc/cp-zookeeper:7.5.0
#     environment:
#       ZOOKEEPER_CLIENT_PORT: 2181
#       ZOOKEEPER_TICK_TIME: 2000
#     ports:
#       - "2181:2181"
#
#   kafka:
#     image: confluentinc/cp-kafka:7.5.0
#     depends_on:
#       - zookeeper
#     ports:
#       - "9092:9092"
#     environment:
#       KAFKA_BROKER_ID: 1
#       KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
#       KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
#       KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
#
#   minio:
#     image: minio/minio:latest
#     ports:
#       - "9000:9000"
#       - "9001:9001"
#     environment:
#       MINIO_ROOT_USER: minioadmin
#       MINIO_ROOT_PASSWORD: minioadmin
#     command: server /data --console-address ":9001"
#     volumes:
#       - minio_data:/data
#
#   postgres:
#     image: postgres:15
#     ports:
#       - "5432:5432"
#     environment:
#       POSTGRES_USER: pipeline
#       POSTGRES_PASSWORD: pipeline123
#       POSTGRES_DB: govdata
#     volumes:
#       - pg_data:/var/lib/postgresql/data
#
#   grafana:
#     image: grafana/grafana:latest
#     ports:
#       - "3000:3000"
#     environment:
#       GF_SECURITY_ADMIN_PASSWORD: admin
#     depends_on:
#       - postgres
#
# volumes:
#   minio_data:
#   pg_data:
#
# ─────────────────────────────────────────────────────────────
#
#  Service URLs once docker-compose is running:
#    Kafka broker:      localhost:9092
#    MinIO console:     http://localhost:9001  (minioadmin / minioadmin)
#    PostgreSQL:        localhost:5432  (pipeline / pipeline123 / govdata)
#    Grafana:           http://localhost:3000  (admin / admin)
#
# ══════════════════════════════════════════════════════════════


# ══════════════════════════════════════════════════════════════
#  HOW TO WORK THROUGH THE CAPSTONE
# ══════════════════════════════════════════════════════════════
#
#  Step 1.  Open W12_D1_Docker_Kafka_Setup.py
#           Read each concept section, run the examples,
#           then solve the 3 exercises.
#
#  Step 2.  Each day file stands alone — you can run Day 3
#           without having finished Day 2.  The simulation
#           code is self-contained.
#
#  Step 3.  Once you have completed all 5 day files in
#           SIMULATION mode, set up Docker and switch each
#           file to REAL mode one service at a time.
#
#  Step 4.  On Day 5, run the full pipeline and generate
#           the run report.  That report is your capstone
#           deliverable.
#
#  Recommended order:
#    W12_D1 -> W12_D2 -> W12_D3 -> W12_D4 -> W12_D5
#
# ══════════════════════════════════════════════════════════════
