# ══════════════════════════════════════════════════════════════
#  WEEK 12  |  DAY 2  |  EXTRACT — API AND KAFKA PRODUCER
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Call a real REST API and parse its JSON response
#  2. Produce records to a Kafka topic (simulated with a list)
#  3. Handle network errors gracefully with try/except
#
#  PIPELINE CONTEXT
#  ─────────────────
#  This is Stage 2 of the capstone pipeline:
#    Day 1: Docker + Kafka setup (simulation)
#    Day 2: Extract data from API, produce to Kafka  <-- today
#    Day 3: Store raw records in Bronze layer (MinIO)
#    Day 4: Transform and load to PostgreSQL (Silver)
#    Day 5: Orchestrate the full pipeline with logging
#
#  TIME:  ~45 minutes
#
# ══════════════════════════════════════════════════════════════


import requests
import json


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — CALLING A REST API WITH requests.get()
# ══════════════════════════════════════════════════════════════
#
#  The Israeli Government Open Data portal exposes public
#  datasets through a standard REST API called CKAN.
#
#  The base URL for all data searches is:
#    https://data.gov.il/api/3/action/datastore_search
#
#  Key query parameters:
#    resource_id  — the unique ID of the specific dataset table
#    limit        — maximum number of records to return
#    offset       — how many records to skip (used for pagination)
#
#  The response is always JSON with this structure:
#    {
#      "success": true,
#      "result": {
#        "total": 12345,
#        "records": [
#          {"field1": "value1", "field2": "value2"},
#          ...
#        ]
#      }
#    }
#
#  We access records with: response.json()["result"]["records"]
#
#  A timeout parameter is important for production code — if the
#  server is slow, we do not want the program to hang forever.
#
# EXAMPLE ──────────────────────────────────────────────────────
# SIMULATION: instead of calling the real API, we build a fake
# response dict that matches the real structure exactly.
# This lets the code run without a network connection.

def make_fake_api_response(resource_id, limit):
    """Return a dict that mimics the structure of a real CKAN API response."""
    records = []
    for i in range(1, limit + 1):
        records.append({
            "_id": i,
            "resource_id": resource_id,
            "district": f"District_{i % 6 + 1}",
            "count": i * 17,
            "year": 2020 + (i % 4),
        })
    return {
        "success": True,
        "result": {
            "total": limit * 3,   # pretend there are more records beyond the limit
            "records": records,
        },
    }

# Simulate the API call and parse the records.
fake_response_data = make_fake_api_response("5e87a7a1-2f6f-41c1-8aec-7216d52a6cf6", limit=5)

records = fake_response_data["result"]["records"]
print(f"API call returned {len(records)} records.")
print(f"First record: {records[0]}")

# REAL MODE (requires network access) ──────────────────────────
# url = "https://data.gov.il/api/3/action/datastore_search"
# params = {
#     "resource_id": "5e87a7a1-2f6f-41c1-8aec-7216d52a6cf6",
#     "limit": 50,
# }
# response = requests.get(url, params=params, timeout=10)
# response.raise_for_status()
# records = response.json()["result"]["records"]
# ──────────────────────────────────────────────────────────────


# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — PRODUCING RECORDS TO KAFKA
# ══════════════════════════════════════════════════════════════
#
#  In a real Kafka setup, a producer serializes each record to
#  JSON and sends it to a broker running at localhost:9092.
#  The broker writes it to the named topic on disk.
#
#  In simulation mode, the "topic" is just a Python list.
#  Each element in the list is one record (a dict).
#  Appending to the list is equivalent to producing a message.
#
#  The producer function:
#    1. Accepts a list of record dicts and a topic list
#    2. Iterates over records
#    3. Appends each record dict to the topic list
#    4. Returns the count of records produced
#
#  Keeping a count lets the orchestrator log how many records
#  moved through each stage of the pipeline.
#
# EXAMPLE ──────────────────────────────────────────────────────

# SIMULATION: topic is a plain Python list.
demo_topic = []

def produce_to_topic(records_list, topic):
    """Append each record dict to the topic list. Return count produced."""
    count = 0
    for record in records_list:
        topic.append(record)
        count += 1
    return count

sample_records = [
    {"id": 1, "city": "Tel Aviv",    "value": 100},
    {"id": 2, "city": "Jerusalem",   "value": 200},
    {"id": 3, "city": "Haifa",       "value": 150},
]

produced = produce_to_topic(sample_records, demo_topic)
print(f"\nProduced {produced} records to demo topic.")
print(f"Topic now contains {len(demo_topic)} messages.")

# REAL MODE (requires Docker + confluent-kafka) ─────────────────
# from confluent_kafka import Producer
# import json
#
# producer_config = {"bootstrap.servers": "localhost:9092"}
# p = Producer(producer_config)
#
# for record in sample_records:
#     p.produce("gov-data-raw", value=json.dumps(record).encode("utf-8"))
#
# p.flush()   # wait until all messages are delivered
# print(f"Produced {len(sample_records)} messages to topic gov-data-raw")
# ──────────────────────────────────────────────────────────────


# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — ERROR HANDLING FOR NETWORK CALLS
# ══════════════════════════════════════════════════════════════
#
#  Network calls can fail for many reasons:
#    - The server is down or unreachable
#    - The URL is wrong (404 Not Found)
#    - The request takes too long (timeout)
#    - The response is not valid JSON (malformed response)
#
#  requests.exceptions.RequestException is the base class for
#  all requests errors. Catching it covers connection errors,
#  timeouts, and HTTP errors in one except block.
#
#  Best practice pattern for a fetch function:
#    1. Wrap the requests.get() call in try/except
#    2. On error: print or log the error message
#    3. Return an empty list so the pipeline can continue
#       (downstream code receives [] and produces 0 messages)
#
#  Returning an empty list instead of raising is called
#  "graceful degradation" — the pipeline does not crash,
#  it just continues with no data for this batch.
#
# EXAMPLE ──────────────────────────────────────────────────────

def safe_fetch(url, params):
    """Fetch JSON from url with params. Return records list or [] on error."""
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()["result"]["records"]
    except requests.exceptions.RequestException as e:
        print(f"  [ERROR] Network request failed: {e}")
        return []

# Test with a deliberately broken URL to trigger the error path.
result = safe_fetch("https://this-server-does-not-exist.example.com/api", {})
print(f"\nsafe_fetch with bad URL returned: {result}")
print(f"  Pipeline can continue — received empty list: {result == []}")


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
#
#  Write a function fetch_gov_data(resource_id, limit=50)
#  that calls the Israeli Government Open Data API and returns
#  a list of record dicts.
#
#  API URL: https://data.gov.il/api/3/action/datastore_search
#  Pass resource_id and limit as query parameters.
#  Wrap the call in try/except requests.exceptions.RequestException.
#  On error, print the error and return an empty list.
#
#  Call the function with:
#    resource_id = "5e87a7a1-2f6f-41c1-8aec-7216d52a6cf6"
#    limit       = 50
#
#  Print the count of records fetched and the first record.
#  If the network is unavailable, the function must return []
#  without crashing.
#
#  Expected output (network available):
#    Fetched 50 records from resource 5e87a7a1-2f6f-41c1-8aec-7216d52a6cf6
#    First record: {'_id': 1, ...}
#
#  Expected output (network unavailable):
#    [ERROR] Network request failed: ...
#    Fetched 0 records from resource 5e87a7a1-2f6f-41c1-8aec-7216d52a6cf6

# --- starting data ---
GOV_API_URL = "https://data.gov.il/api/3/action/datastore_search"
TARGET_RESOURCE_ID = "5e87a7a1-2f6f-41c1-8aec-7216d52a6cf6"




# (write your code here)




# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
#
#  Write a function produce_records(records, topic_queue)
#  that appends each record dict to topic_queue and returns
#  the count of records produced.
#
#  The function must:
#    - Iterate over the records list
#    - Append each record dict directly (not as JSON string)
#    - Return the integer count of records appended
#
#  Use the sample_data below as the records to produce.
#  Create an empty list called pipeline_topic as the queue.
#  Call produce_records and print the count returned.
#  Then print the length of pipeline_topic to confirm.
#
#  Expected output:
#    produce_records returned: 4
#    pipeline_topic length   : 4

# --- starting data ---
pipeline_topic = []

sample_data = [
    {"_id": 1, "district": "North",  "accidents": 42, "year": 2022},
    {"_id": 2, "district": "South",  "accidents": 31, "year": 2022},
    {"_id": 3, "district": "Center", "accidents": 78, "year": 2022},
    {"_id": 4, "district": "North",  "accidents": 39, "year": 2023},
]




# (write your code here)




# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
#
#  Combine both functions from Exercise 1 and Exercise 2.
#
#  Write code that:
#    1. Calls fetch_gov_data(TARGET_RESOURCE_ID, limit=50)
#       and stores the result in fetched_records
#    2. Creates an empty list called main_topic
#    3. Calls produce_records(fetched_records, main_topic)
#       and stores the return value in produced_count
#    4. Prints the summary line shown below
#
#  If the network is unavailable, fetched_records will be []
#  and produced_count will be 0 — this is the expected behavior.
#
#  Expected output (network available):
#    Fetched 50 records, produced 50 to topic
#
#  Expected output (network unavailable):
#    [ERROR] Network request failed: ...
#    Fetched 0 records, produced 0 to topic

# --- starting data ---
main_topic = []




# (write your code here)




