# ==============================================================================
# PYTHON DATA CURRICULUM — FULL LEARNING PATH
# Senior BI Developer / Data Analyst -> Principal AI Solutions Engineer
# Focus: Reliability, Observability, Guardrails
# ==============================================================================
#
# HOW THIS CURRICULUM WORKS:
# ---------------------------
# Each lesson is a .ipynb notebook you open in VS Code (with Jupyter extension).
# Every lesson is structured as: CONCEPT -> EXAMPLE -> EXERCISE (repeated per topic)
#
#   CONCEPT  -> plain English explanation (markdown cell — just read)
#   EXAMPLE  -> working code that runs — read it, then run the cell
#   EXERCISE -> your turn: write code in the blank area below each exercise header
#               Check: does your output match "Expected output:" in the comments?
#
# TIME PER LESSON: ~30-40 minutes  (3-4 concepts x 10 min each)
# PACE: 1 lesson per day (5 days/week = 12 weeks total)
#
# HOW TO RUN A LESSON:
# ---------------------
#   1. Open the .ipynb file in VS Code
#   2. Read the first markdown CONCEPT cell
#   3. Run the EXAMPLE code cell — see the output
#   4. Write your answer in the blank cells below Exercise 1, run it
#   5. Continue: Concept 2 -> Example 2 -> Exercise 2 -> etc.
#
# ENGINEERING THREAD (runs W1-W12):
# -----------------------------------
# Every week introduces one Royal Road Standard — a non-negotiable engineering
# practice carried forward into every later week:
#   W1  dataclasses        W7  pytest-style tests     W10  LangSmith tracing
#   W2  Pydantic I/O       W8  FastAPI /health         W11  Guardrails middleware
#   W3  Retry + logging    W9  MLflow tracking         W12  Full observability
#   W4  Data assertions    W5  logging module          W6   Parameterized SQL
#
# CUMULATIVE PROJECT (W6-W12):
# -----------------------------------
# The Smart Schema Agent grows one capability per week:
#   W6  Schema introspection      W10  LangChain NL->SQL
#   W7  Audit log                 W11  Multi-agent (LangGraph)
#   W8  Safety layer              W12  FastAPI production wrapper
#   W9  Query classifier (ML)
#
# ==============================================================================


# ==============================================================================
# WEEK 1 — PYTHON BASICS          (Folder: Week_1_Python_Basics)
# ==============================================================================
# D1  W1_D1_Variables_DataTypes.ipynb    Variables, str, int, float, bool
# D2  W1_D2_Lists.ipynb                  Lists, indexing, append, remove, slicing
# D3  W1_D3_Dictionaries.ipynb           Key-value pairs, dict methods
#                                        + ROYAL ROAD W1: dataclasses
# D4  W1_D4_Conditionals.ipynb           if / elif / else, comparison operators
# D5  W1_D5_Loops.ipynb                  for, while, break, continue, range()
# D6  W1_D6_Project_Employee_Registry    Weekly project


# ==============================================================================
# WEEK 2 — FUNCTIONS & CONTROL FLOW  (Folder: Week_2_Functions)
# ==============================================================================
# D1  W2_D1_Functions_Basics.ipynb       def, return, calling functions
# D2  W2_D2_Function_Parameters.ipynb    default args, *args, **kwargs, scope
#                                        + ROYAL ROAD W2: Pydantic BaseModel
# D3  W2_D3_Error_Handling.ipynb         try / except / finally, raising errors
# D4  W2_D4_List_Comprehensions.ipynb    [x for x in list if condition]
# D5  W2_D5_Modules.ipynb                import, standard library, custom modules
# D6  W2_D6_Classes_OOP.ipynb            Classes, __init__, methods, inheritance
# D7  W2_D7_Project_Sales_Calculator     Weekly project


# ==============================================================================
# WEEK 3 — FILE HANDLING & EXTERNAL DATA  (Folder: Week_3_External_Data)
# ==============================================================================
# D1  W3_D1_File_Handling.ipynb          open(), read, write, with statement
# D2  W3_D2_CSV_Data.ipynb               csv module, pandas read_csv, write_csv
# D3  W3_D3_JSON_Data.ipynb              json.load, json.dump, nested JSON
# D4  W3_D4_API_Requests.ipynb           requests library, GET/POST, parse JSON
#                                        + ROYAL ROAD W3: retry logic + structured logging
# D5  W3_D5_Web_Scraping.ipynb           BeautifulSoup, extract tables from HTML
# D6  W3_D6_Project_Live_Data_Fetcher    Weekly project


# ==============================================================================
# WEEK 4 — NUMPY & PANDAS            (Folder: Week_4_Pandas_NumPy)
# ==============================================================================
# D1  W4_D1_NumPy.ipynb                  Arrays, shape, operations, math functions
# D2  W4_D2_Pandas_Basics.ipynb          Series, DataFrame, read_excel, select
# D3  W4_D3_Data_Cleaning.ipynb          Nulls, duplicates, type conversion
#                                        + ROYAL ROAD W4: data quality assertions
# D4  W4_D4_Filtering_GroupBy.ipynb      Boolean filter, groupby, agg functions
# D5  W4_D5_Merge_PivotTable.ipynb       merge (inner/left/right), pivot_table
# D6  W4_D6_Project_Titanic_Analysis     Weekly project
#
# Datasets used: datasets/titanic_train.xlsx, datasets/police.xlsx


# ==============================================================================
# WEEK 5 — VISUALIZATION & ANALYSIS  (Folder: Week_5_Visualization)
# ==============================================================================
# D1  W5_D1_Matplotlib.ipynb             Line, bar, scatter, histogram
# D2  W5_D2_Seaborn.ipynb                Statistical plots, heatmap, styling
# D3  W5_D3_Time_Series.ipynb            Datetime, resample, rolling windows
# D4  W5_D4_Statistics.ipynb             describe(), corr(), basic distributions
# D5  W5_D5_Project_Sales_Analysis.ipynb Mini-project: full analysis pipeline
#                                        + ROYAL ROAD W5: logging module
# D6  W5_D6_Project_Sales_Dashboard      Weekly project
#
# Datasets used: datasets/hotel_bookings.xlsx, datasets/titanic_train.xlsx


# ==============================================================================
# WEEK 6 — SQL & DATABASES           (Folder: Week_6_SQL_Databases)
# ==============================================================================
# D1  W6_D1_SQL_Basics.ipynb             SQLite, SELECT, WHERE, ORDER BY
#                                        + ROYAL ROAD W6: parameterized queries
# D2  W6_D2_Database_Design.ipynb        Tables, keys, relationships, schema
#                                        + SMART SCHEMA AGENT Stage 1: schema introspection
# D3  W6_D3_Advanced_SQL.ipynb           JOINs, GROUP BY, subqueries
# D4  W6_D4_Python_SQL_Server.ipynb      pyodbc, SQL Server connection
# D5  W6_D5_Project_Database.ipynb       Mini-project: full database analysis
# D6  W6_D6_Project_Retail_Analytics     Weekly project


# ==============================================================================
# WEEK 7 — DATA ENGINEERING          (Folder: Week_7_Data_Engineering)
# ==============================================================================
# D1  W7_D1_ETL_Pipelines.ipynb          Extract, Transform, Load — design pattern
# D2  W7_D2_Data_Extraction.ipynb        Extract from files, APIs, databases
# D3  W7_D3_Data_Transformation.ipynb    Clean, map, validate, reshape
# D4  W7_D4_Data_Loading.ipynb           Load to DB, file, incremental loads
#                                        + SMART SCHEMA AGENT Stage 2: audit log
# D5  W7_D5_Pipeline_Automation.ipynb    Scheduling, logging, error recovery
# D6  W7_D6_Project_Tested_ETL.ipynb     Weekly project
#                                        + ROYAL ROAD W7: pytest-style test runner


# ==============================================================================
# WEEK 8 — PRODUCTION ENGINEERING    (Folder: Week_8_Production)
# Arch decision notes in every file header
# ==============================================================================
# D1  W8_D1_Cloud_Platforms.ipynb        AWS S3, GCP, Azure — concepts + boto3
# D2  W8_D2_Orchestration_Airflow.ipynb  Airflow DAG concepts, task dependencies
#                                        + GAP: semantic caching (SimpleCache, TTL)
# D3  W8_D3_Data_Quality.ipynb           Validation, monitoring, alerts
#                                        + SMART SCHEMA AGENT Stage 3: safety layer
# D4  W8_D4_Big_Data_Spark.ipynb         PySpark intro, when to use distributed compute
# D5  W8_D5_Final_Project.ipynb          Full end-to-end data pipeline project
#                                        + ROYAL ROAD W8: FastAPI /health endpoint
#                                        + GAP: health/readiness/metrics endpoints
# D6  W8_D6_Project_Mini_Pipeline        Weekly project
# D7  W8_D7_Automated_QA_Verification    QA patterns + pytest
#                                        + GAP: CI/CD simulation, developer productivity


# ==============================================================================
# WEEK 9 — MACHINE LEARNING          (Folder: Week_9_Machine_Learning)
# Arch decision notes in every file header
# ==============================================================================
# D1  W9_D1_ML_Concepts_ScikitLearn.ipynb   What is ML, supervised learning, train/test
#                                            + SMART SCHEMA AGENT Stage 4: query classifier
# D2  W9_D2_Linear_Regression.ipynb          Predict numbers, coefficients, R2, MAE
# D3  W9_D3_Classification.ipynb             Logistic Regression, Decision Tree, accuracy
# D4  W9_D4_Model_Evaluation.ipynb           Confusion matrix, precision, recall, F1, CV
#                                            + ROYAL ROAD W9: MLflow experiment tracking
#                                            + GAP: MLflow polynomial regression tracking
# D5  W9_D5_Project_Titanic_Survival.ipynb   Full ML project on Titanic dataset
# D6  W9_D6_Project_Full_ML_Workflow.ipynb   Weekly project
#                                            + GAP: DriftMonitor, data/prediction drift
#
# Datasets used: datasets/titanic_train.xlsx


# ==============================================================================
# WEEK 10 — AI ENGINEERING ESSENTIALS  (Folder: Week_10_AI_Engineering)
# Arch decision notes in every file header
# ==============================================================================
# D1  W10_D1_LLM_APIs.ipynb                 OpenAI / Anthropic API, streaming, async
#                                            + GAP: PromptCache with hit rate + cost
# D2  W10_D2_Prompt_Engineering.ipynb        Prompts, few-shot, Pydantic outputs
#                                            + GAP: PromptRegistry, versioning, A/B
# D3  W10_D3_LangChain_Basics.ipynb          PromptTemplate, chains, tool calling
#                                            + SMART SCHEMA AGENT Stage 5: NL->SQL
#                                            + ROYAL ROAD W10: LangSmith tracing
# D4  W10_D4_VectorDB_Embeddings.ipynb       Embeddings, cosine similarity, ChromaDB
# D5  W10_D5_Project_RAG_Pipeline.ipynb      Full RAG pipeline: index -> retrieve -> generate
#                                            + GAP: Vertex AI / LocalPipeline simulation
# D6  W10_D6_Project_RAG_Chatbot             Weekly project
#
# INSTALL: pip install openai anthropic langchain langchain-openai chromadb pydantic


# ==============================================================================
# WEEK 11 — ADVANCED AI & PRODUCTION  (Folder: Week_11_Advanced_AI)
# Arch decision notes in every file header
# ==============================================================================
# D1  W11_D1_LangGraph_Agents.ipynb          LangGraph agents, stateful graphs, routing
#                                            + SMART SCHEMA AGENT Stage 6: multi-agent
#                                            + ROYAL ROAD W11: GuardRail middleware chain
#                                            + GAP: ReAct loop, multi-agent orchestration
# D2  W11_D2_NLP_Basics.ipynb                Text cleaning, word frequency, sentiment
# D3  W11_D3_Speech_Recognition.ipynb        Whisper API, voice pipeline, transcription
# D4  W11_D4_AI_Ethics.ipynb                 Bias detection, fairness metrics, compliance
#                                            + GAP: ModelCard Pydantic schema, AuditLog
#                                            + GAP: Prompt injection and guardrails
# D5  W11_D5_Final_AI_Project.ipynb          Full AI-powered data assistant (capstone)
#                                            + GAP: run_ab_test(), LLM evaluation
# D6  W11_D6_Project_AI_Data_Assistant       Weekly project
#
# INSTALL: pip install langchain-openai langgraph textblob openai ragas pytest


# ==============================================================================
# WEEK 12 — CAPSTONE PIPELINE        (Folder: Week_12_Capstone)
# Arch decision notes in every file header
# Full data pipeline: API -> Kafka -> MinIO -> PostgreSQL -> Grafana
# (SIMULATION MODE: Python list -> local folder -> SQLite — no Docker needed)
# ==============================================================================
# OVERVIEW  W12_OVERVIEW                     Architecture map, tech stack decisions
# D1  W12_D1_Docker_Kafka_Setup.ipynb        Kafka concepts, producer/consumer pattern
# D2  W12_D2_Extract_API_Producer.ipynb      Fetch from data.gov.il, produce to Kafka
# D3  W12_D3_Store_MinIO.ipynb               Bronze layer: store raw JSON to object storage
# D4  W12_D4_Transform_Load_PostgreSQL.ipynb Silver layer: clean, validate, load to DB
# D5  W12_D5_Pipeline_Final_Run.ipynb        Full pipeline orchestration + run report
#                                            + ROYAL ROAD W12: PipelineObserver (full observability)
#                                            + SMART SCHEMA AGENT Stage 7: FastAPI wrapper


# ==============================================================================
# CAREER PATH
# ==============================================================================
#
# After Week 4:  Junior Data Analyst
#                  Skills: Python, Pandas, SQL, data cleaning, visualization
#
# After Week 6:  Mid-level Data Analyst
#                  Skills: + statistics, database design, parameterized SQL
#
# After Week 8:  Data Engineer
#                  Skills: + ETL pipelines, cloud, orchestration, production APIs
#                           Royal Road: dataclasses -> Pydantic -> retry -> assertions
#                                       logging -> SQL safety -> pytest -> FastAPI
#
# After Week 9:  ML Engineer
#                  Skills: + scikit-learn, regression, classification, MLflow tracking
#
# After Week 11: AI Engineer
#                  Skills: + LLM APIs, RAG, LangChain, LangGraph, NLP, ethics
#                           Smart Schema Agent: governed NL->SQL (W6->W11)
#                           Royal Road: observability, guardrails, tracing
#
# After Week 12: Principal AI Solutions Engineer
#                  Skills: + production pipelines, full observability stack
#                            FastAPI-wrapped agents, architecture decisions
#                            Reliability, Observability, Guardrails — end to end
#
# ==============================================================================

print("Curriculum loaded — 12 weeks, 76 lessons.")
print()
print("Start with: Week_1_Python_Basics / W1_D1_Variables_DataTypes.ipynb")
print()
print("Engineering thread (Royal Road Standards):")
print("  W1-W6   dataclasses, Pydantic, retry, assertions, logging, SQL safety")
print("  W7-W12  pytest, FastAPI, MLflow, LangSmith, guardrails, observability")
print()
print("Cumulative project (Smart Schema Agent, W6-W12):")
print("  Schema -> Audit -> Safety -> ML classifier -> NL->SQL -> Multi-agent -> FastAPI")
print()
print("Career milestones:")
print("  After Week 4   -> Junior Data Analyst")
print("  After Week 8   -> Data Engineer")
print("  After Week 11  -> AI Engineer")
print("  After Week 12  -> Principal AI Solutions Engineer")
print()
print("Good luck!")
