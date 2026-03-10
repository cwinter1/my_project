# ══════════════════════════════════════════════════════════════
#  WEEK 10  |  DAY 5  |  PROJECT — BUILD A RAG PIPELINE
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  This project combines everything from Week 10:
#  1. Understand what RAG (Retrieval-Augmented Generation) is
#  2. Build a complete RAG pipeline from scratch
#  3. Connect ChromaDB + LLM to answer questions from a custom knowledge base
#  4. Understand the limitations and when to use RAG vs fine-tuning
#
#  TIME:  ~50 minutes
#
#  YOUTUBE
#  ───────
#  Search: "RAG pipeline Python from scratch tutorial"
#  Search: "LangChain RAG tutorial ChromaDB 2025"
#  Search: "RAG vs fine-tuning when to use each"
#
#  INSTALL:
#    pip install chromadb openai langchain langchain-openai
#
# ══════════════════════════════════════════════════════════════

import os
import json


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — WHAT IS RAG?
# ══════════════════════════════════════════════════════════════
#
# RAG = Retrieval-Augmented Generation
#
# Problem: LLMs have a knowledge cutoff (they don't know your company's data).
# Solution: Before asking the LLM a question, RETRIEVE relevant documents
#           from your own knowledge base, then AUGMENT the prompt with them.
#
# RAG Pipeline:
#   1. INDEX:   Load documents -> chunk them -> embed -> store in vector DB
#   2. QUERY:   User asks a question -> embed the question -> find similar chunks
#   3. GENERATE: Send question + retrieved chunks to LLM -> get answer
#
# Simple diagram:
#   User question
#       |
#   Embed question  -> Vector DB -> Find top-K similar chunks
#                                        |
#   Build prompt: "Answer this question using ONLY the context below:
#                  Context: [retrieved chunks]
#                  Question: [user question]"
#                                        |
#                                 LLM -> Final answer

# EXAMPLE ──────────────────────────────────────────────────────
print("=" * 55)
print("PROJECT: RAG Pipeline")
print("=" * 55)
print()
print("We will build a Q&A system over a custom knowledge base.")
print("The system will only answer from the provided documents.")


# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — PREPARE THE KNOWLEDGE BASE
# ══════════════════════════════════════════════════════════════

# EXAMPLE ──────────────────────────────────────────────────────
print()
print("STEP 1: Knowledge Base")
print("-" * 40)

# Our knowledge base: data engineering concepts
# In a real project these could come from PDFs, docs, confluence pages, etc.
knowledge_base = [
    {
        "id": "etl_001",
        "text": "ETL stands for Extract, Transform, Load. It is the process of moving "
                "data from source systems, cleaning and reshaping it, and loading it "
                "into a destination like a data warehouse. Common ETL tools include "
                "Apache Spark, dbt, Talend, and Python with pandas."
    },
    {
        "id": "dw_001",
        "text": "A data warehouse is a centralized repository for structured data "
                "optimized for analytical queries. Unlike transactional databases (OLTP), "
                "data warehouses (OLAP) are optimized for read-heavy workloads. "
                "Popular options: Snowflake, BigQuery, Redshift, Azure Synapse."
    },
    {
        "id": "airflow_001",
        "text": "Apache Airflow is an open-source workflow orchestration tool. "
                "Pipelines are defined as DAGs (Directed Acyclic Graphs) in Python. "
                "Each node in the DAG is a Task. Airflow schedules, monitors, and "
                "retries tasks automatically. Alternatives include Prefect and Luigi."
    },
    {
        "id": "spark_001",
        "text": "Apache Spark is a distributed computing framework for processing "
                "large datasets. PySpark is the Python API for Spark. Spark stores "
                "data in RDDs and DataFrames, and processes data in memory for speed. "
                "Use Spark when data exceeds what fits on a single machine (typically > 1TB)."
    },
    {
        "id": "sql_join_001",
        "text": "SQL JOINs combine rows from two or more tables based on a related column. "
                "INNER JOIN returns only matching rows. LEFT JOIN returns all left-table rows "
                "plus matching right-table rows (nulls where no match). "
                "RIGHT JOIN is the reverse. FULL OUTER JOIN returns all rows from both tables."
    },
    {
        "id": "pandas_001",
        "text": "Pandas is a Python library for data manipulation and analysis. "
                "The main data structure is a DataFrame — a 2D table with labeled columns. "
                "Key operations: read_csv, read_excel, merge, groupby, pivot_table, fillna. "
                "Pandas is best for datasets that fit in memory (typically < 1-2GB)."
    },
    {
        "id": "api_001",
        "text": "A REST API (Application Programming Interface) allows systems to "
                "communicate over HTTP. GET requests retrieve data, POST requests send data. "
                "Responses are typically in JSON format. In Python, use the 'requests' library. "
                "Always handle errors: check response.status_code before using the data."
    },
    {
        "id": "dbt_001",
        "text": "dbt (data build tool) is a transformation tool for analytics engineering. "
                "It runs SQL SELECT statements and creates tables/views in your data warehouse. "
                "dbt handles dependency management, testing, and documentation automatically. "
                "It follows ELT (Extract, Load, Transform) rather than ETL."
    },
]

print(f"Knowledge base: {len(knowledge_base)} documents loaded")
for doc in knowledge_base:
    print(f"  [{doc['id']}] {doc['text'][:60]}...")


# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — RETRIEVE AND GENERATE
# ══════════════════════════════════════════════════════════════
#
# The retrieval step finds the most relevant documents for a question.
# The generation step sends the question + context to the LLM.

# EXAMPLE ──────────────────────────────────────────────────────
print()
print("STEP 2: Index Documents in ChromaDB")
print("-" * 40)

# import chromadb
#
# chroma_client = chromadb.Client()
# collection = chroma_client.create_collection("de_knowledge_base")
#
# collection.add(
#     documents=[doc["text"] for doc in knowledge_base],
#     ids=[doc["id"] for doc in knowledge_base]
# )
# print(f"Indexed {len(knowledge_base)} documents in ChromaDB")

print("(Uncomment ChromaDB code after: pip install chromadb)")

print()
print("STEP 3: Retrieval Function")
print("-" * 40)

def retrieve(question, n_results=2):
    """
    Find the most relevant documents for a question.
    Returns a list of text chunks.
    """
    # Uncomment once ChromaDB is set up:
    # results = collection.query(query_texts=[question], n_results=n_results)
    # return results["documents"][0]

    # Placeholder — simple keyword search for now
    question_lower = question.lower()
    matches = []
    for doc in knowledge_base:
        if any(word in doc["text"].lower() for word in question_lower.split()):
            matches.append(doc["text"])
        if len(matches) >= n_results:
            break
    return matches if matches else [knowledge_base[0]["text"]]

# Test the retrieval
test_questions = [
    "What is Airflow used for?",
    "When should I use Spark instead of pandas?",
    "What is the difference between ETL and ELT?",
]

for q in test_questions:
    chunks = retrieve(q)
    print(f"\nQ: {q}")
    print(f"  Retrieved: {chunks[0][:80]}...")

print()
print("STEP 4: Generate Answers with LLM")
print("-" * 40)

def answer_question(question):
    """
    RAG pipeline: retrieve relevant docs -> build augmented prompt -> call LLM.
    """
    # Step 1: Retrieve
    context_chunks = retrieve(question, n_results=2)
    context = "\n\n".join(context_chunks)

    # Step 2: Build augmented prompt
    system_prompt = (
        "You are a data engineering assistant. "
        "Answer ONLY using the context provided. "
        "If the answer is not in the context, say 'I don't have that information.'"
    )
    user_prompt = f"Context:\n{context}\n\nQuestion: {question}"

    # Step 3: Call LLM (uncomment once you have an API key)
    # from openai import OpenAI
    # client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    # response = client.chat.completions.create(
    #     model="gpt-4o-mini",
    #     messages=[
    #         {"role": "system", "content": system_prompt},
    #         {"role": "user",   "content": user_prompt}
    #     ],
    #     max_tokens=200
    # )
    # return response.choices[0].message.content.strip()

    # Placeholder response:
    return f"[LLM would answer using context: {context[:100]}...]"

# Test the full pipeline
print()
for question in test_questions:
    print(f"Q: {question}")
    answer = answer_question(question)
    print(f"A: {answer}")
    print()


# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
# Expand the knowledge base by adding 3 more documents covering
# topics you find important.
# Ideas: Python virtual environments, git for data engineers, Docker basics,
#        data quality checks, streaming vs batch processing.
# Re-index after adding (re-run the ChromaDB step).
#
# Expected output:
#     knowledge_base list now has 11 documents
#     ChromaDB collection has 11 indexed documents




# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
# Ask the system a question it CANNOT answer from the knowledge base:
#   "What is the capital of France?"
#
# The LLM should respond: "I don't have that information."
# Test this and verify the system doesn't hallucinate.
# Print the question and the answer.
#
# Expected output:
#     Q: What is the capital of France?
#     A: I don't have that information.




# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
# Modify the answer_question() function to also return the SOURCE document IDs
# that were used. Print the answer AND the sources.
#
# Expected output:
#     Q: What is Airflow used for?
#     A: Apache Airflow is a workflow orchestration tool...
#     Sources: airflow_001




# ══════════════════════════════════════════════════════════════
#  FINAL REFLECTION
# ══════════════════════════════════════════════════════════════
# Answer these questions as comments:
#
#   1. What is the main advantage of RAG over asking the LLM directly?
#   2. What happens if the knowledge base has outdated or wrong information?
#   3. When would you fine-tune a model instead of using RAG?
#      (Hint: fine-tuning changes the model itself; RAG adds external knowledge)
