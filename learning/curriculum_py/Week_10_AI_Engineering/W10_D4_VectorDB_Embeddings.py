# ══════════════════════════════════════════════════════════════
#  WEEK 10  |  DAY 4  |  VECTOR DATABASES & EMBEDDINGS
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Understand what embeddings are and why they matter
#  2. Convert text into embedding vectors using an API
#  3. Find similar documents using cosine similarity
#  4. Store and query vectors with ChromaDB (local vector database)
#
#  TIME:  ~40 minutes
#
#  YOUTUBE
#  ───────
#  Search: "embeddings explained visually 3Blue1Brown"
#  Search: "vector databases explained simply"
#  Search: "ChromaDB Python tutorial RAG"
#
#  INSTALL:
#    pip install chromadb openai numpy
#
# ══════════════════════════════════════════════════════════════

import os
import json
import numpy as np


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — WHAT ARE EMBEDDINGS?
# ══════════════════════════════════════════════════════════════
#
# An EMBEDDING is a list of numbers (a vector) that represents text.
# Similar texts get similar vectors.
#
# Example:
#   "I love data engineering"  →  [0.12, -0.45, 0.88, ..., 0.03]  (1536 numbers)
#   "I enjoy working with data" →  [0.11, -0.43, 0.90, ..., 0.04]  (very similar!)
#   "The cat sat on the mat"   →  [-0.72, 0.34, -0.11, ..., 0.67] (very different)
#
# Why does this matter?
#   - Search: find documents that are SEMANTICALLY similar (not just keyword match)
#   - Recommendation: find similar products, articles, customers
#   - RAG: find the most relevant chunks of text to feed to an LLM
#
# SEMANTIC vs KEYWORD search:
#   Query: "Python code for ETL"
#   Keyword search finds: documents containing the words "Python", "code", "ETL"
#   Semantic search finds: documents ABOUT Python ETL, even if worded differently
#       e.g., "Writing data pipelines with pandas and SQLAlchemy" — no exact words!

# EXAMPLE ──────────────────────────────────────────────────────
print("=" * 55)
print("CONCEPT 1: Embeddings Visualized")
print("=" * 55)

# Simulate embeddings with simple 2D vectors (real ones have 1536 dimensions)
texts = ["data engineering pipeline", "ETL process", "machine learning model",
         "neural network training", "SQL database query"]

# Fake 2D embeddings just to show the concept
fake_embeddings = {
    "data engineering pipeline": [0.8, 0.2],
    "ETL process":               [0.75, 0.25],    # close to "data engineering pipeline"
    "machine learning model":    [0.1, 0.9],
    "neural network training":   [0.15, 0.85],    # close to "machine learning model"
    "SQL database query":        [0.6, 0.4],      # somewhere in between
}

print("Text similarity (closer = more similar):")
for text, vec in fake_embeddings.items():
    bar_x = "=" * int(vec[0] * 20)
    print(f"  {text:35} x={vec[0]:.2f} {bar_x}")

# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
# For each pair of sentences below, rate their semantic similarity 1-5
# (1 = completely different, 5 = almost identical meaning)
# Write your answers as comments. Don't look it up — use your intuition.
#
# Pair A:
#   S1: "Load data from CSV to a SQL database"
#   S2: "Import a spreadsheet into a relational database"
#   Similarity: ?
#
# Pair B:
#   S1: "Train a machine learning model"
#   S2: "Ride a bicycle to work"
#   Similarity: ?
#
# Pair C:
#   S1: "The model is overfitting to training data"
#   S2: "The algorithm memorized the examples instead of learning patterns"
#   Similarity: ?
#
# Expected output:
#     Pair A: ~4-5 (same concept, different words)
#     Pair B: ~1 (completely unrelated)
#     Pair C: ~5 (same meaning, different phrasing)





# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — COSINE SIMILARITY
# ══════════════════════════════════════════════════════════════
#
# To compare two embedding vectors, we use COSINE SIMILARITY.
# It measures the angle between two vectors:
#   1.0  = identical direction = very similar
#   0.0  = perpendicular = unrelated
#  -1.0  = opposite direction = opposite meaning
#
# Formula: cosine_similarity = (A . B) / (|A| * |B|)

# EXAMPLE ──────────────────────────────────────────────────────
print()
print("=" * 55)
print("CONCEPT 2: Cosine Similarity")
print("=" * 55)

def cosine_similarity(vec_a, vec_b):
    """Calculate cosine similarity between two vectors."""
    a = np.array(vec_a)
    b = np.array(vec_b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Compare pairs using our fake 2D embeddings
pairs = [
    ("data engineering pipeline", "ETL process"),
    ("data engineering pipeline", "machine learning model"),
    ("machine learning model",    "neural network training"),
    ("ETL process",               "SQL database query"),
]

for text_a, text_b in pairs:
    sim = cosine_similarity(fake_embeddings[text_a], fake_embeddings[text_b])
    print(f"  {text_a:35} vs  {text_b}")
    print(f"  Similarity: {sim:.3f}\n")

# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
# Given a query vector, find which text in the corpus is most similar.
#
# query = "database data loading"
# fake query vector: [0.65, 0.35]
#
# corpus = the 5 texts from fake_embeddings above
#
# Loop through all 5 texts, calculate cosine_similarity with the query,
# and print: text -> similarity score
# Then print: "Most similar: [text name]"
#
# Expected output (approximate):
#   data engineering pipeline   -> 0.9xx
#   ETL process                 -> 0.9xx
#   machine learning model      -> 0.4xx
#   neural network training     -> 0.5xx
#   SQL database query          -> 0.9xx
#   Most similar: SQL database query

query_vector = [0.65, 0.35]




# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — CHROMADB: A LOCAL VECTOR DATABASE
# ══════════════════════════════════════════════════════════════
#
# ChromaDB stores text + embeddings locally so you can:
#   - Add documents once
#   - Query by meaning many times (fast!)
#   - No cloud or API needed (runs on your machine)
#
# Main operations:
#   collection.add()    — store documents with IDs
#   collection.query()  — find N most similar documents to a query text

# EXAMPLE ──────────────────────────────────────────────────────
print()
print("=" * 55)
print("CONCEPT 3: ChromaDB Vector Store")
print("=" * 55)

# import chromadb
#
# # Create a local in-memory database
# client = chromadb.Client()
# collection = client.create_collection("data_knowledge_base")
#
# # Add documents (ChromaDB generates embeddings automatically)
# documents = [
#     "An ETL pipeline extracts data from sources, transforms it, and loads it to a target.",
#     "Linear regression predicts a continuous numeric value from input features.",
#     "A decision tree classifier splits data into branches based on feature thresholds.",
#     "SQL JOINs combine rows from two or more tables based on a related column.",
#     "Pandas groupby splits data into groups and applies aggregate functions.",
#     "A data warehouse stores structured, historical data for analytical queries.",
#     "Apache Airflow is an orchestration tool that schedules and monitors pipelines.",
# ]
#
# collection.add(
#     documents=documents,
#     ids=[f"doc_{i}" for i in range(len(documents))]
# )
# print(f"Added {len(documents)} documents to ChromaDB")
#
# # Query: find 2 most relevant documents for a question
# query = "How do I combine data from two tables?"
# results = collection.query(query_texts=[query], n_results=2)
#
# print(f"\nQuery: '{query}'")
# print("Most relevant documents:")
# for doc, dist in zip(results["documents"][0], results["distances"][0]):
#     print(f"  Similarity: {1-dist:.3f}  |  {doc[:80]}...")

print("ChromaDB example shown above — uncomment after: pip install chromadb")

# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
# Build a simple FAQ search system using ChromaDB.
#
# 1. Create a ChromaDB collection called "de_faq"
# 2. Add at least 8 FAQ entries (questions + answers combined as one string)
#    Include topics like: ETL, SQL, pandas, data warehouse, APIs, etc.
# 3. Write a function search_faq(question) that queries ChromaDB
#    and returns the 2 most relevant FAQ entries
# 4. Test with 3 different questions
#
# Example FAQ entry:
#   "What is an ETL pipeline? ETL stands for Extract, Transform, Load.
#    It is a process to move data from source systems to a data warehouse."
#
# Expected output:
#     For each test question: the 2 most relevant FAQ entries with similarity scores




