# ══════════════════════════════════════════════════════════════
#  WEEK 11  |  DAY 1  |  LANGGRAPH & AI AGENTS
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. Understand what an AI Agent is (vs a simple chain)
#  2. Know when to use LangGraph vs LangChain
#  3. Build a simple LangGraph workflow with nodes and edges
#  4. Add conditional routing — let the agent decide what to do next
#
#  TIME:  ~40 minutes
#
#  YOUTUBE
#  ───────
#  Search: "LangGraph tutorial Python agents 2025"
#  Search: "AI agents explained LangGraph vs LangChain"
#  Search: "LangGraph state machine workflow tutorial"
#
#  INSTALL:
#    pip install langgraph langchain-openai
#
# ══════════════════════════════════════════════════════════════

import os
from typing import TypedDict, Annotated


# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — CHAINS VS AGENTS
# ══════════════════════════════════════════════════════════════
#
# CHAIN:  fixed sequence of steps.  A -> B -> C -> done.
#         Good for: predictable, structured tasks (summarize, classify, translate)
#
# AGENT:  the LLM DECIDES what to do next at each step.
#         It can call tools, loop back, branch, or stop — based on the situation.
#         Good for: open-ended tasks (research, coding assistant, customer support)
#
# LANGGRAPH:  framework for building STATEFUL agents as a graph.
#   - NODES:  steps (functions or LLM calls)
#   - EDGES:  connections between steps (fixed or conditional)
#   - STATE:  a dictionary shared between all nodes (carries data through the graph)
#
# Example agent graph:
#
#   START -> classify_intent
#                |
#        ┌───────┴───────┐
#    "sql_question"   "general_question"
#        |                   |
#   run_sql_agent      answer_directly
#        |                   |
#        └───────┬───────┘
#             format_answer
#                |
#              END

# EXAMPLE ──────────────────────────────────────────────────────
print("=" * 55)
print("CONCEPT 1: Chains vs Agents")
print("=" * 55)
print()
print("Chain: A -> B -> C  (fixed, predictable)")
print("Agent: A -> ? -> ?  (LLM decides based on state)")
print()
print("LangGraph components:")
print("  StateGraph  -> the overall graph")
print("  Node        -> a function that reads and updates State")
print("  Edge        -> connection from one node to the next")
print("  Conditional -> the LLM decides which edge to take")

# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
# Design the graph for a customer support agent that handles 3 types of requests:
#   1. Billing questions     -> send to billing_team node
#   2. Technical issues      -> send to tech_support node
#   3. General inquiries     -> answer_directly node
#
# Draw the graph as ASCII art or describe it in comments:
#   START -> which nodes? -> what edges? -> END
#
# Also answer:
#   What information should be in the STATE? (what does each node need to know?)
#
# Expected output:
#     An ASCII graph diagram as comments
#     A STATE dictionary definition with at least 3 fields





# ══════════════════════════════════════════════════════════════
#  CONCEPT 2 — BUILDING A SIMPLE LANGGRAPH WORKFLOW
# ══════════════════════════════════════════════════════════════
#
# A LangGraph State is just a TypedDict — a dictionary with typed keys.
# Each node receives the state and returns updates to it.

# EXAMPLE ──────────────────────────────────────────────────────

print()
print("=" * 55)
print("CONCEPT 2: LangGraph State + Nodes")
print("=" * 55)

# from langgraph.graph import StateGraph, END
# from langchain_openai import ChatOpenAI
# from langchain_core.messages import HumanMessage, AIMessage
#
# # Define the State — data that flows through all nodes
# class AgentState(TypedDict):
#     question:   str
#     intent:     str    # filled by classify node
#     answer:     str    # filled by answer node
#
# llm = ChatOpenAI(model="gpt-4o-mini", api_key=os.environ.get("OPENAI_API_KEY"))
#
# # Node 1: classify the intent
# def classify_intent(state: AgentState) -> dict:
#     prompt = f"""Classify this question into one of these categories:
#     sql / python / general
#
#     Question: {state['question']}
#     Respond with ONLY the category word."""
#
#     response = llm.invoke([HumanMessage(content=prompt)])
#     intent = response.content.strip().lower()
#     print(f"  [classify] intent = {intent}")
#     return {"intent": intent}
#
# # Node 2a: answer SQL questions
# def answer_sql(state: AgentState) -> dict:
#     prompt = f"You are a SQL expert. Answer this SQL question: {state['question']}"
#     response = llm.invoke([HumanMessage(content=prompt)])
#     return {"answer": response.content}
#
# # Node 2b: answer Python questions
# def answer_python(state: AgentState) -> dict:
#     prompt = f"You are a Python expert. Answer this Python question: {state['question']}"
#     response = llm.invoke([HumanMessage(content=prompt)])
#     return {"answer": response.content}
#
# # Node 2c: answer general questions
# def answer_general(state: AgentState) -> dict:
#     prompt = f"Answer this question helpfully: {state['question']}"
#     response = llm.invoke([HumanMessage(content=prompt)])
#     return {"answer": response.content}
#
# # Routing function — decides which node to go to next
# def route_by_intent(state: AgentState) -> str:
#     intent = state.get("intent", "general")
#     if "sql" in intent:     return "answer_sql"
#     if "python" in intent:  return "answer_python"
#     return "answer_general"
#
# # Build the graph
# graph = StateGraph(AgentState)
# graph.add_node("classify_intent", classify_intent)
# graph.add_node("answer_sql",      answer_sql)
# graph.add_node("answer_python",   answer_python)
# graph.add_node("answer_general",  answer_general)
#
# graph.set_entry_point("classify_intent")
# graph.add_conditional_edges("classify_intent", route_by_intent)
# graph.add_edge("answer_sql",     END)
# graph.add_edge("answer_python",  END)
# graph.add_edge("answer_general", END)
#
# app = graph.compile()
#
# # Run the agent
# test_questions = [
#     "How do I write a JOIN in SQL?",
#     "What is a list comprehension in Python?",
#     "What does a data engineer do?",
# ]
#
# for q in test_questions:
#     result = app.invoke({"question": q, "intent": "", "answer": ""})
#     print(f"\nQ: {q}")
#     print(f"Intent: {result['intent']}")
#     print(f"A: {result['answer'][:150]}...")

print("LangGraph code shown above — uncomment after: pip install langgraph langchain-openai")

# ══════════════════════════════════════════════════════════════
#  EXERCISE 2
# ══════════════════════════════════════════════════════════════
# Extend the graph above by adding a 4th intent: "data_engineering".
# When the question is about ETL, pipelines, Airflow, Spark, or data engineering:
#   -> route to a new "answer_de" node
#
# Steps:
#   1. Add "data engineering" as a possible intent in the classify prompt
#   2. Create an "answer_de" node with a system prompt for DE questions
#   3. Add routing logic for "data_engineering" in route_by_intent
#   4. Add the node and edge to the graph
#   5. Test with: "How does Apache Airflow schedule pipelines?"
#
# Expected output:
#     [classify] intent = data_engineering
#     Q: How does Apache Airflow schedule pipelines?
#     A: (answer about Airflow DAGs and scheduling)




# ══════════════════════════════════════════════════════════════
#  CONCEPT 3 — WHEN TO USE AGENTS VS CHAINS
# ══════════════════════════════════════════════════════════════
#
# Use a CHAIN when:
#   - The steps are fixed and predictable
#   - You know exactly what will happen before it runs
#   - Example: document summarization, translation, classification
#
# Use an AGENT when:
#   - The LLM needs to make decisions mid-task
#   - The number of steps is variable
#   - The task requires tools (search, code execution, API calls)
#   - Example: research assistant, coding helper, customer support bot
#
# WARNING: agents can be unpredictable and expensive.
#   - They can loop forever if not given a stop condition
#   - Each step uses tokens (= money)
#   - Always set max_iterations and test with simple cases first

# EXAMPLE ──────────────────────────────────────────────────────

print()
print("=" * 55)
print("CONCEPT 3: Agent Best Practices")
print("=" * 55)
print()
print("Rules for production agents:")
print("  1. Always set max_iterations to prevent infinite loops")
print("  2. Log every node execution for debugging")
print("  3. Handle errors in each node (try/except)")
print("  4. Test each node in isolation before connecting them")
print("  5. Monitor token usage — agents can be expensive")

# ══════════════════════════════════════════════════════════════
#  EXERCISE 3
# ══════════════════════════════════════════════════════════════
# Design (on paper / as comments) an agent that:
#   - Takes a natural language data request: "Show me sales by city for Q3 2024"
#   - Decides whether to query a database, call an API, or read a file
#   - Executes the appropriate action
#   - Formats and returns the result as a table
#
# Your design should include:
#   - The State dictionary structure (what fields?)
#   - The node names and what each one does
#   - The routing logic (what determines which path?)
#   - A potential failure scenario and how you'd handle it
#
# Expected output:
#     A complete agent design as comments with State, nodes, edges, and error handling




