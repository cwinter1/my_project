# ══════════════════════════════════════════════════════════════
#  WEEK 12  |  DAY 1  |  DOCKER AND KAFKA SETUP
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ────────────────────────────────────
#  - Understand what Docker is and why data engineers use it
#  - Understand what Kafka is: topics, producers, consumers, offsets
#  - Simulate a Kafka topic using a plain Python list
#  - Write producer and consumer functions
#  - Build a small end-to-end pipeline in simulation mode
#
#  PROJECT GOAL FOR TODAY
#  ────────────────────────────────────
#  By the end of this file you will have a working simulation
#  of a Kafka message queue.  Day 2 will plug real data into it.
#
#  TIME:  ~45 minutes
#
# ══════════════════════════════════════════════════════════════


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — WHAT IS DOCKER AND WHY DATA ENGINEERS USE IT
# ══════════════════════════════════════════════════════════════
#
#  Docker lets you run software in a "container" — a lightweight,
#  isolated environment that includes everything the software needs.
#
#  Without Docker, setting up Kafka requires:
#    - Installing Java
#    - Downloading and configuring Kafka
#    - Managing ports and config files by hand
#    - Different steps on Windows, Mac, and Linux
#
#  With Docker, one command starts everything:
#    docker-compose up -d
#
#  Containers are:
#    Portable     — same image runs on any machine
#    Isolated     — each service gets its own network and filesystem
#    Disposable   — delete the container, start fresh any time
#    Reproducible — your teammate gets the same environment
#
#  Data engineers use Docker to run:
#    - Kafka and Zookeeper (message streaming)
#    - MinIO (object storage, like a local S3)
#    - PostgreSQL (relational database)
#    - Airflow (workflow orchestration)
#    - Spark (distributed data processing)
#
#  Key vocabulary:
#    Image      — the blueprint (downloaded from Docker Hub)
#    Container  — a running instance of an image
#    Volume     — persistent storage that survives container restarts
#    Port       — the number that maps container port to host port
#                 e.g.  "9092:9092" means container 9092 = host 9092
#
# EXAMPLE ──────────────────────────────────────────────────────
# This is a simulation — no Docker needed.
# We print what the equivalent Docker commands would be.

docker_commands = [
    "docker-compose up -d                    # start all services",
    "docker ps                               # list running containers",
    "docker-compose logs kafka               # view Kafka logs",
    "docker-compose down                     # stop all services",
]

print("Common Docker commands a data engineer uses:")
for cmd in docker_commands:
    print(f"  {cmd}")

# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — WHAT IS KAFKA
# ══════════════════════════════════════════════════════════════
#
#  Kafka is a distributed message streaming platform.
#  It decouples the service that produces data from the service
#  that consumes and processes data.
#
#  Core concepts:
#
#    Topic      — a named channel for a specific type of message.
#                 Example: "traffic-accidents", "hotel-bookings"
#
#    Producer   — any program that writes (publishes) messages
#                 to a topic.  In our pipeline: the API fetcher.
#
#    Consumer   — any program that reads (subscribes to) messages
#                 from a topic.  In our pipeline: the MinIO writer.
#
#    Message    — a single unit of data (usually a JSON string).
#
#    Offset     — the position of a message in the topic.
#                 Message 0 = first message ever written.
#                 The consumer tracks its current offset so it
#                 knows where to continue after a restart.
#
#    Partition  — Kafka splits topics into partitions for scale.
#                 We use 1 partition in this capstone.
#
#  Why use Kafka instead of writing directly to the database?
#    - The producer and consumer can run at different speeds
#    - If the database is down, messages wait in Kafka safely
#    - Multiple consumers can read the same topic independently
#    - Messages are retained for days — you can replay them
#
# EXAMPLE ──────────────────────────────────────────────────────
# SIMULATION: a Python list acts as a single Kafka topic.
# Each element in the list is one message (a string or dict).

# The "topic" is just a list held in memory.
topic_queue = []

# A simple producer function: appends one message to the topic.
def produce(topic, message):
    topic.append(message)
    print(f"  [PRODUCER] sent: {message}")

# A simple consumer function: reads from a given offset.
# Returns the messages it read and the new offset position.
def consume(topic, offset):
    new_messages = topic[offset:]
    new_offset = len(topic)
    return new_messages, new_offset

# Demonstrate producing three messages.
produce(topic_queue, "record_001")
produce(topic_queue, "record_002")
produce(topic_queue, "record_003")

# Consume starting from offset 0.
messages, current_offset = consume(topic_queue, 0)
print(f"\n[CONSUMER] read {len(messages)} message(s), new offset = {current_offset}")
for m in messages:
    print(f"  -> {m}")

# REAL MODE (requires Docker + confluent-kafka) ─────────────────
# from confluent_kafka import Producer, Consumer
#
# producer_config = {"bootstrap.servers": "localhost:9092"}
# p = Producer(producer_config)
# p.produce("gov-data-raw", value="record_001".encode("utf-8"))
# p.flush()
#
# consumer_config = {
#     "bootstrap.servers": "localhost:9092",
#     "group.id": "pipeline-group",
#     "auto.offset.reset": "earliest",
# }
# c = Consumer(consumer_config)
# c.subscribe(["gov-data-raw"])
# msg = c.poll(timeout=5.0)
# if msg:
#     print(msg.value().decode("utf-8"))
# c.close()
# ──────────────────────────────────────────────────────────────


# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — OFFSET TRACKING
# ══════════════════════════════════════════════════════════════
#
#  In real Kafka, each consumer group maintains its own offset.
#  This means:
#    - Two different consumers can read the same topic
#      independently without interfering.
#    - If a consumer crashes at offset 7, it restarts at 7
#      and does not re-read messages 0-6.
#    - A consumer can "seek" back to offset 0 to replay all data.
#
#  In our simulation, offset is just an integer we pass around.
#
# EXAMPLE ──────────────────────────────────────────────────────

topic_b = []

# Produce 5 messages.
for i in range(5):
    produce(topic_b, f"event_{i}")

# Consumer A reads all 5 messages from offset 0.
msgs_a, offset_a = consume(topic_b, 0)
print(f"\n[CONSUMER A] read {len(msgs_a)} messages, offset now = {offset_a}")

# Produce 3 more messages while consumer A was busy.
produce(topic_b, "event_5")
produce(topic_b, "event_6")
produce(topic_b, "event_7")

# Consumer A resumes from where it left off (offset 5).
new_msgs_a, offset_a = consume(topic_b, offset_a)
print(f"[CONSUMER A] caught up: {len(new_msgs_a)} new messages, offset = {offset_a}")

# Consumer B starts fresh from offset 0 (reads everything).
msgs_b, offset_b = consume(topic_b, 0)
print(f"[CONSUMER B] independent read: {len(msgs_b)} messages total")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
#
#  A logistics company tracks package scans at warehouses.
#  Each scan is a message produced to the "scans" topic.
#
#  Task:
#    Write a producer function called add_scan(topic, scan_dict)
#    that appends a dictionary to the topic list and prints a
#    confirmation message.
#
#    Then write a consumer function called read_scans(topic, offset)
#    that returns a tuple of (list_of_messages, new_offset).
#
#    Use the starting data below to produce all 4 scans,
#    then consume them from offset 0.
#
#  Expected output:
#    [SCAN PRODUCER] added: {'package_id': 'PKG-001', 'location': 'Tel Aviv', 'status': 'arrived'}
#    [SCAN PRODUCER] added: {'package_id': 'PKG-002', 'location': 'Haifa', 'status': 'arrived'}
#    [SCAN PRODUCER] added: {'package_id': 'PKG-001', 'location': 'Haifa', 'status': 'departed'}
#    [SCAN PRODUCER] added: {'package_id': 'PKG-003', 'location': 'Jerusalem', 'status': 'arrived'}
#    [SCAN CONSUMER] read 4 scans, offset = 4
#    {'package_id': 'PKG-001', 'location': 'Tel Aviv', 'status': 'arrived'}
#    {'package_id': 'PKG-002', 'location': 'Haifa', 'status': 'arrived'}
#    {'package_id': 'PKG-001', 'location': 'Haifa', 'status': 'departed'}
#    {'package_id': 'PKG-003', 'location': 'Jerusalem', 'status': 'arrived'}

# --- starting data ---
scans_topic = []

scan_records = [
    {"package_id": "PKG-001", "location": "Tel Aviv",   "status": "arrived"},
    {"package_id": "PKG-002", "location": "Haifa",      "status": "arrived"},
    {"package_id": "PKG-001", "location": "Haifa",      "status": "departed"},
    {"package_id": "PKG-003", "location": "Jerusalem",  "status": "arrived"},
]




# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
#
#  The same logistics system has two independent consumers:
#    - "warehouse_system" tracks arrivals
#    - "billing_system"  tracks departures
#
#  Each system maintains its own offset in a dict called
#  consumer_offsets.
#
#  Task:
#    After producing all 4 scans from Exercise 1 (use scan_records
#    and the same scans_topic), write code that:
#      1. Reads all messages with warehouse_system (offset starts at 0)
#      2. Produces 2 more scans (PKG-004 arrived in Beer Sheva,
#         PKG-005 arrived in Eilat)
#      3. warehouse_system reads again from its saved offset —
#         should get only the 2 new messages
#      4. billing_system reads from offset 0 — should get all 6
#
#  Expected output (final two reads):
#    [warehouse_system] caught up: 2 new scans, offset = 6
#    [billing_system] total scans read: 6, offset = 6

# --- starting data ---
consumer_offsets = {
    "warehouse_system": 0,
    "billing_system":   0,
}

extra_scans = [
    {"package_id": "PKG-004", "location": "Beer Sheva", "status": "arrived"},
    {"package_id": "PKG-005", "location": "Eilat",      "status": "arrived"},
]




# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
#
#  Now build a small end-to-end pipeline.
#  You have a list of 5 employee records as dicts.
#  The pipeline has three steps:
#    1. Producer: loop over the records, produce each one
#       to a topic called "employees_topic"
#    2. Consumer: consume all messages from offset 0
#    3. Processor: for each consumed message, print the
#       employee name and salary formatted as:
#         "Loaded: <name> | salary: <salary>"
#
#  Expected output:
#    [PIPELINE] Producing 5 records...
#    [PRODUCER] sent record 1: David Cohen
#    [PRODUCER] sent record 2: Sarah Levi
#    [PRODUCER] sent record 3: Avi Mizrahi
#    [PRODUCER] sent record 4: Noa Shapiro
#    [PRODUCER] sent record 5: Yael Ben-David
#    [PIPELINE] Consuming from offset 0...
#    Loaded: David Cohen | salary: 12000
#    Loaded: Sarah Levi | salary: 15500
#    Loaded: Avi Mizrahi | salary: 9800
#    Loaded: Noa Shapiro | salary: 13200
#    Loaded: Yael Ben-David | salary: 11000
#    [PIPELINE] Done. 5 records processed.

# --- starting data ---
employees_topic = []

employee_records = [
    {"name": "David Cohen",    "department": "Engineering", "salary": 12000},
    {"name": "Sarah Levi",     "department": "Marketing",   "salary": 15500},
    {"name": "Avi Mizrahi",    "department": "Engineering", "salary": 9800},
    {"name": "Noa Shapiro",    "department": "HR",          "salary": 13200},
    {"name": "Yael Ben-David", "department": "Marketing",   "salary": 11000},
]




