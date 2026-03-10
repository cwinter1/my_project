# ══════════════════════════════════════════════════════════════
#  WEEK 3  |  DAY 6  |  WEEKLY PROJECT — LIVE DATA FETCHER
# ══════════════════════════════════════════════════════════════
#
#  PROJECT GOAL
#  ────────────
#  Build a data fetcher that pulls live JSON data from a public
#  API, saves it to a file, and provides keyword search over
#  that saved data — exporting results to CSV.
#
#  SKILLS PRACTICED
#  ─────────────────
#  - HTTP GET requests with the requests library
#  - Reading and writing JSON files
#  - Reading and writing CSV files
#  - Defining and calling functions
#  - String methods (lower, in)
#  - Working with lists of dicts
#  - os.path for file paths
#
#  TIME:  ~45-60 minutes
#
# ══════════════════════════════════════════════════════════════


# ── SETUP — provided by teacher, do not change ────────────────

import requests
import json
import csv
import os

TARGET_URL   = "https://jsonplaceholder.typicode.com/posts"
DATA_FILE    = os.path.join(os.path.dirname(__file__), "posts_data.json")
RESULTS_FILE = os.path.join(os.path.dirname(__file__), "search_results.csv")


# ══════════════════════════════════════════════════════════════
#  TASK 1 — Fetch and Inspect the Data
# ══════════════════════════════════════════════════════════════
#  Make a GET request to TARGET_URL.
#  Print the HTTP status code.
#  Parse the response as JSON and print the total number of records.
#
#  Expected output:
#    Status code: 200
#    Records returned: 100
#




# ══════════════════════════════════════════════════════════════
#  TASK 2 — Extract Relevant Fields
# ══════════════════════════════════════════════════════════════
#  From the full response, build a new list called posts.
#  Each item should be a dict with exactly three keys:
#    "id"     — the post's id (integer)
#    "userId" — the post's userId (integer)
#    "title"  — the first 50 characters of the title (string)
#
#  Print the first 3 items to verify your extraction.
#
#  Expected output (titles may be truncated differently):
#    {'id': 1, 'userId': 1, 'title': 'sunt aut facere repellat provident occaecat'}
#    {'id': 2, 'userId': 1, 'title': 'qui est esse'}
#    {'id': 3, 'userId': 1, 'title': 'ea molestias quasi exercitationem repellat q'}
#




# ══════════════════════════════════════════════════════════════
#  TASK 3 — Save to JSON File
# ══════════════════════════════════════════════════════════════
#  Write the posts list to the file at DATA_FILE as valid JSON.
#  Use json.dump with indent=2 so the file is human-readable.
#  Print a confirmation message after saving.
#
#  Expected output:
#    Saved 100 posts to posts_data.json
#




# ══════════════════════════════════════════════════════════════
#  TASK 4 — search_posts(keyword)
# ══════════════════════════════════════════════════════════════
#  Write a function called search_posts that takes a single
#  parameter: keyword (a string).
#
#  Inside the function:
#    - Open and read DATA_FILE using json.load
#    - Return a list of post dicts where the keyword appears
#      anywhere in the title (case-insensitive)
#
#  Do not print anything inside the function — just return the list.
#
#  Test the function with one keyword and print how many results
#  it found:
#    results = search_posts("qui")
#    print(f"'qui' found in {len(results)} titles")
#
#  Expected output:
#    'qui' found in 3 titles
#  (Exact count depends on the live data.)
#




# ══════════════════════════════════════════════════════════════
#  TASK 5 — Search with Three Keywords
# ══════════════════════════════════════════════════════════════
#  Call search_posts with these three keywords:
#    "qui", "est", "vel"
#
#  For each keyword, print the keyword and the number of matching
#  titles, then print the title of each matching post indented
#  by two spaces.
#
#  Expected output format:
#    Keyword: "qui" — 3 matches
#      qui est esse
#      ...
#    Keyword: "est" — 5 matches
#      ...
#    Keyword: "vel" — 4 matches
#      ...
#  (Counts are approximate — live data may vary.)
#




# ══════════════════════════════════════════════════════════════
#  TASK 6 — Export Search Results to CSV
# ══════════════════════════════════════════════════════════════
#  Combine all results from your three searches in Task 5 into
#  a single list called all_results.  Remove duplicates by
#  checking that each post id appears only once.
#
#  Write all_results to RESULTS_FILE as a CSV with these columns:
#    id, userId, title
#
#  Use csv.DictWriter with the fieldnames in that order.
#  Print a confirmation message after saving.
#
#  Expected output:
#    Exported N unique results to search_results.csv
#  (N depends on how many unique posts matched across all keywords.)
#


