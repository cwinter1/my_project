# ══════════════════════════════════════════════════════════════
#  WEEK 10  |  DAY 3  |  LANGCHAIN BASICS
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Understand what LangChain is and why it exists
#  2. Create a simple chain: prompt → LLM → output
#  3. Use prompt templates to build reusable prompts
#  4. Chain multiple steps together using LCEL (LangChain Expression Language)
#
#  TIME:  ~35 minutes
#
#  YOUTUBE
#  ───────
#  Search: "LangChain tutorial Python beginners 2025"
#  Search: "LangChain LCEL chains explained"
#  Search: "LangChain vs raw OpenAI API when to use"
#
#  INSTALL:
#    pip install langchain langchain-openai langchain-anthropic
#
#  NOTE: You need an API key set as an environment variable (from Day 1).
#
# ══════════════════════════════════════════════════════════════

import os


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — WHAT IS LANGCHAIN AND WHY USE IT?
# ══════════════════════════════════════════════════════════════
#
# LangChain is a framework that makes building LLM applications easier.
# Instead of writing raw API calls every time, LangChain gives you:
#   - PromptTemplate  — reusable prompts with variables  ({topic}, {language})
#   - LLM wrappers    — same interface for OpenAI, Anthropic, Gemini, etc.
#   - Chains          — connect steps together: prompt | llm | parser
#   - Memory          — keep conversation history
#   - Tools           — let the LLM call functions (search, calculator, etc.)
#
# Raw API call — works but not reusable:
#   response = client.chat.completions.create(model=..., messages=[...])
#
# LangChain chain — reusable and composable:
#   chain = prompt_template | llm | output_parser
#   result = chain.invoke({"topic": "data engineering"})
#
# When to use LangChain vs raw API:
#   Raw API   — simple one-off calls, full control, no extra dependencies
#   LangChain — complex multi-step apps, RAG, agents, memory, tool use

# EXAMPLE ──────────────────────────────────────────────────────
print("=" * 55)
print("CONCEPT 1: LangChain Architecture")
print("=" * 55)
print()
print("Chain = PromptTemplate | LLM | OutputParser")
print()
print("  PromptTemplate:  'Translate {text} to {language}'")
print("       |")
print("  LLM (GPT-4o / Claude):  processes the filled-in prompt")
print("       |")
print("  OutputParser:  extracts the text from the response object")

# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
# For each use case, describe the 3 components of the chain as comments:
#   PromptTemplate: what variables does it need?
#   LLM: which model would you use? (fast=haiku/gpt-4o-mini, smart=claude/gpt-4o)
#   OutputParser: what format do you want? (plain text, JSON, list)
#
# Use case A: Summarize customer reviews for a product manager
# Use case B: Convert a SQL query into plain English for a non-technical stakeholder
# Use case C: Generate a Python function docstring given the function code
#
# Expected output:
#     3 chain designs as comments, each with PromptTemplate, LLM, OutputParser





# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — PROMPT TEMPLATES
# ══════════════════════════════════════════════════════════════
#
# A PromptTemplate is a prompt with placeholders that get filled in at runtime.
# It keeps your prompts clean and reusable.

# EXAMPLE ──────────────────────────────────────────────────────

print()
print("=" * 55)
print("CONCEPT 2: Prompt Templates")
print("=" * 55)

# from langchain_openai import ChatOpenAI
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
#
# llm = ChatOpenAI(model="gpt-4o-mini", api_key=os.environ.get("OPENAI_API_KEY"))
#
# # Create a reusable prompt template
# prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are a {role}. Give concise, direct answers."),
#     ("user",   "{question}")
# ])
#
# # Build the chain
# chain = prompt | llm | StrOutputParser()
#
# # Use the same chain for different roles and questions
# print(chain.invoke({"role": "data engineer",  "question": "What is an ETL pipeline?"}))
# print()
# print(chain.invoke({"role": "data analyst",   "question": "What is a pivot table?"}))
# print()
# print(chain.invoke({"role": "ML engineer",    "question": "What is overfitting?"}))

print("Template code shown above — uncomment once you have an API key.")
print()
print("Notice: same chain, different inputs — different context-aware answers.")

# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
# Build a chain called "classifier_chain" with this template:
#
#   system: "You are a text classifier. Respond with ONLY one word."
#   user:   "Classify this text as {category_type}: {text}"
#
# Test it with:
#   {"category_type": "sentiment (positive/negative/neutral)",
#    "text": "The delivery was fast but the product broke after one day."}
#
#   {"category_type": "support ticket type (billing/technical/shipping/other)",
#    "text": "I was charged twice for my subscription this month."}
#
# (Uncomment and test once you have an API key)
#
# Expected output:
#     negative
#     billing





# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — CHAINING MULTIPLE STEPS (LCEL)
# ══════════════════════════════════════════════════════════════
#
# LCEL (LangChain Expression Language) lets you chain steps with the | operator.
# Output of one step automatically becomes input of the next.
#
# Example: a two-step chain
#   Step 1: Extract key facts from a document
#   Step 2: Turn those facts into a structured report

# EXAMPLE ──────────────────────────────────────────────────────

print()
print("=" * 55)
print("CONCEPT 3: Multi-Step Chain (LCEL)")
print("=" * 55)

# from langchain_openai import ChatOpenAI
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
#
# llm = ChatOpenAI(model="gpt-4o-mini", api_key=os.environ.get("OPENAI_API_KEY"))
# parser = StrOutputParser()
#
# # Step 1: extract facts
# step1_prompt = ChatPromptTemplate.from_template(
#     "Extract 3 key facts from this text as bullet points:\n{raw_text}"
# )
#
# # Step 2: turn facts into a summary
# step2_prompt = ChatPromptTemplate.from_template(
#     "Write a 2-sentence executive summary based on these facts:\n{facts}"
# )
#
# # Build the two-step chain
# chain = (
#     step1_prompt
#     | llm
#     | parser
#     | (lambda facts: {"facts": facts})   # pass output to next step's variable
#     | step2_prompt
#     | llm
#     | parser
# )
#
# result = chain.invoke({"raw_text": """
#     Q3 Results: Revenue reached 2.4M, up 12% vs Q2.
#     Top product: Laptop Pro generated 35% of total revenue.
#     Challenge: 8% return rate due to logistics issues.
#     Plan: hire 2 logistics managers, launch Laptop Pro 2 in Q4.
# """})
# print("Final summary:")
# print(result)

print("Multi-step chain code shown above — uncomment once you have an API key.")

# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
# Design a 3-step LangChain pipeline for this data engineering task:
#
# Input: a plain English description of a data transformation
#   "I need a query that shows total revenue per city, only for cities
#    with more than 10 orders, sorted from highest to lowest revenue."
#
# Step 1: Convert the description to a SQL query
# Step 2: Add comments to the SQL query explaining each part
# Step 3: Rate the query for efficiency (1-5) with a brief reason
#
# Write the 3 ChatPromptTemplate templates as strings.
# Build the chain with LCEL (use the pattern shown above).
# (Uncomment and test once you have a key)
#
# Expected output:
#     Step 1: a SQL SELECT with GROUP BY, HAVING, ORDER BY
#     Step 2: the same SQL with inline comments
#     Step 3: efficiency rating 1-5 with reasoning

task_description = ("I need a query that shows total revenue per city, only for cities "
                    "with more than 10 orders, sorted from highest to lowest revenue.")




