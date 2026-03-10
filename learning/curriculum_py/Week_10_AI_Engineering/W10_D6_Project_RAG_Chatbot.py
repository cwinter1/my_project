# ══════════════════════════════════════════════════════════════
#  WEEK 10  |  DAY 6  |  PROJECT — MINIMAL RAG CHATBOT
# ══════════════════════════════════════════════════════════════
#
#  PROJECT GOAL
#  ────────────
#  Build a minimal Retrieval-Augmented Generation (RAG) chatbot
#  from scratch: encode a small knowledge base with simulated
#  embeddings, retrieve the most relevant chunks with cosine
#  similarity, construct a grounded prompt, and call an LLM API
#  (shown as a commented stub — requires your own API key).
#
#  SKILLS USED
#  ───────────
#  - Text chunking and a simulated embedding function
#  - Cosine similarity search over a vector store (plain Python)
#  - Prompt construction with retrieved context
#  - LLM API call pattern (openai client — commented stub)
#  - Separating retrieval logic from generation logic
#
#  TIME:  ~45-60 minutes
#
# ══════════════════════════════════════════════════════════════

import math


# ══════════════════════════════════════════════════════════════
#  PART 1 — THE KNOWLEDGE BASE
# ══════════════════════════════════════════════════════════════
# In a real RAG system the knowledge base would be a folder of
# documents.  Here we use a small list of text chunks that
# represent articles about a fictional tech company, "NovaCorp".
# Each chunk is a short paragraph that answers a specific question.
#
# EXAMPLE ──────────────────────────────────────────────────────

knowledge_base = [
    "NovaCorp was founded in 2010 by Sarah Levi and Dan Katz in Tel Aviv, Israel.",
    "NovaCorp's flagship product is DataFlow, a real-time data pipeline platform used by over 500 enterprise clients.",
    "DataFlow supports connectors for Kafka, PostgreSQL, Snowflake, and Google BigQuery.",
    "NovaCorp raised a Series B round of 40 million dollars in 2022, led by Vertex Ventures.",
    "The engineering team at NovaCorp uses Python, Go, and Kubernetes for infrastructure.",
    "NovaCorp's pricing model is usage-based: clients pay per gigabyte of data processed.",
    "Customer support is available 24/7 via the NovaCorp portal at support.novacorp.io.",
    "DataFlow version 3.0 introduced automatic schema detection and a drag-and-drop pipeline editor.",
    "NovaCorp has offices in Tel Aviv, London, and New York as of 2024.",
    "The NovaCorp SLA guarantees 99.9% uptime for all enterprise tier customers.",
]

print(f"Knowledge base loaded: {len(knowledge_base)} chunks.")


# ══════════════════════════════════════════════════════════════
#  PART 2 — SIMULATED EMBEDDINGS
# ══════════════════════════════════════════════════════════════
# Real embeddings are dense vectors produced by a neural network.
# Here we simulate them with a simple bag-of-words approach:
# count word frequencies, then normalize to unit length.
# This is enough to demonstrate cosine similarity retrieval.
#
# cosine_similarity(a, b) = dot(a, b) / (|a| * |b|)
# A score of 1.0 means the vectors point in the same direction.
#
# EXAMPLE ──────────────────────────────────────────────────────

def simple_embed(text):
    """
    Convert a text string into a normalized word-frequency vector.
    Returns a dict mapping each word to its normalized frequency.
    """
    words  = text.lower().split()
    counts = {}
    for word in words:
        # strip punctuation from word ends
        word = word.strip(".,!?;:\"'()-")
        if word:
            counts[word] = counts.get(word, 0) + 1

    # normalize to unit length
    magnitude = math.sqrt(sum(v ** 2 for v in counts.values()))
    if magnitude == 0:
        return counts
    return {word: freq / magnitude for word, freq in counts.items()}


def cosine_similarity(vec_a, vec_b):
    """Return cosine similarity between two word-frequency dicts."""
    common_words = set(vec_a) & set(vec_b)
    dot_product  = sum(vec_a[w] * vec_b[w] for w in common_words)
    return dot_product   # both vecs are already unit-normalized


# Build the vector store: list of (chunk_text, embedding) tuples
vector_store = [(chunk, simple_embed(chunk)) for chunk in knowledge_base]

# Quick test
test_query = "funding and investors"
test_vec   = simple_embed(test_query)
scores     = [(chunk, cosine_similarity(test_vec, vec)) for chunk, vec in vector_store]
scores.sort(key=lambda x: x[1], reverse=True)

print("\nTest retrieval for 'funding and investors':")
for chunk, score in scores[:3]:
    print(f"  score={score:.4f}  |  {chunk[:70]}...")


# ══════════════════════════════════════════════════════════════
#  TASK 1 — RETRIEVAL FUNCTION
# ══════════════════════════════════════════════════════════════
# Write a function called retrieve(query, top_k=3) that:
#   1. Embeds the query using simple_embed()
#   2. Computes cosine similarity against every chunk in vector_store
#   3. Returns the top_k chunks as a list of strings, sorted by
#      similarity (highest first)
#
# Test it with the query "What databases does DataFlow connect to?"
# Expected top result should contain "Kafka" and "PostgreSQL".
#
# --- starting data ---
# Use: vector_store, simple_embed(), cosine_similarity()




def retrieve(query, top_k=3):
    pass




# ══════════════════════════════════════════════════════════════
#  PART 3 — PROMPT CONSTRUCTION
# ══════════════════════════════════════════════════════════════
# A RAG prompt has two parts:
#   - Context: the retrieved chunks, numbered and pasted in.
#   - Instruction: the actual user question, with an instruction
#     to answer using only the provided context.
#
# Keeping context and question separate makes it easy to adjust
# either part without touching the other.
#
# EXAMPLE ──────────────────────────────────────────────────────

def build_prompt(question, context_chunks):
    """
    Construct a RAG-style prompt from retrieved chunks and a question.
    Returns the full prompt string.
    """
    context_block = "\n".join(
        f"[{i+1}] {chunk}" for i, chunk in enumerate(context_chunks)
    )
    prompt = (
        "You are a helpful assistant for NovaCorp.\n"
        "Answer the question using ONLY the context provided below.\n"
        "If the answer is not in the context, say 'I don't have that information.'\n\n"
        f"CONTEXT:\n{context_block}\n\n"
        f"QUESTION: {question}\n\n"
        "ANSWER:"
    )
    return prompt


# Test prompt construction with hard-coded chunks
sample_chunks = [
    knowledge_base[1],
    knowledge_base[2],
]
sample_question = "What connectors does DataFlow support?"
sample_prompt   = build_prompt(sample_question, sample_chunks)

print("\nSample prompt preview (first 400 chars):")
print(sample_prompt[:400])


# ══════════════════════════════════════════════════════════════
#  TASK 2 — END-TO-END RAG PIPELINE
# ══════════════════════════════════════════════════════════════
# Write a function called rag_answer(question) that:
#   1. Calls retrieve(question, top_k=3) to get relevant chunks
#   2. Calls build_prompt(question, chunks) to build the prompt
#   3. Prints the prompt to the console
#   4. Returns the prompt string (the actual LLM call is in Task 3)
#
# Test it with the question: "Where are NovaCorp's offices?"
# Verify that the printed prompt contains context about Tel Aviv.
#
# --- starting data ---
# Use: retrieve(), build_prompt()




def rag_answer(question):
    pass




# ══════════════════════════════════════════════════════════════
#  PART 4 — LLM API CALL (COMMENTED STUB)
# ══════════════════════════════════════════════════════════════
# The function below shows how you would send the prompt to the
# OpenAI API.  It is commented out because it requires an API key.
# To use it: set your key in the environment variable OPENAI_API_KEY,
# uncomment the code, and call call_llm(prompt) inside rag_answer().
#
# EXAMPLE ──────────────────────────────────────────────────────

# import os
# from openai import OpenAI
#
# def call_llm(prompt):
#     """Send a RAG prompt to the OpenAI API and return the answer text."""
#     client   = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
#     response = client.chat.completions.create(
#         model    = "gpt-4o-mini",
#         messages = [
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user",   "content": prompt},
#         ],
#         max_tokens   = 200,
#         temperature  = 0.2,
#     )
#     return response.choices[0].message.content

# Example usage (uncomment after adding API key):
# question = "What is NovaCorp's pricing model?"
# chunks   = retrieve(question, top_k=3)
# prompt   = build_prompt(question, chunks)
# answer   = call_llm(prompt)
# print("LLM answer:", answer)


# ══════════════════════════════════════════════════════════════
#  TASK 3 — EVALUATE RETRIEVAL QUALITY
# ══════════════════════════════════════════════════════════════
# Run the retrieve() function on the three questions below.
# For each question, print the top 3 retrieved chunks and their
# similarity scores.
# Manually judge: does the top chunk actually answer the question?
# Add a comment next to each result: # GOOD or # NEEDS IMPROVEMENT
#
# Questions to test:
#   "Who founded NovaCorp and when?"
#   "What is the uptime guarantee?"
#   "How much does DataFlow cost?"
#
# Expected top chunk for question 1 should mention "Sarah Levi".
# Expected top chunk for question 2 should mention "99.9%".
#
# --- starting data ---
test_questions = [
    "Who founded NovaCorp and when?",
    "What is the uptime guarantee?",
    "How much does DataFlow cost?",
]




# for question in test_questions:
#     results = retrieve(question, top_k=3)
#     ...




print("\nProject complete.")
