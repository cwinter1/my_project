# CLAUDE.md — Session Guide for python-gstat Curriculum

## Installation

A `requirements.txt` file is in the repo root.

**Install all packages:**
```bash
pip install -r requirements.txt
```

**Install core only (for G-Lesson notebooks 1-8):**
```bash
pip install numpy pandas matplotlib seaborn openpyxl
```

---

## What This Project Is

A Python data science curriculum built as `.ipynb` notebook files for VS Code.
Path: `C:\Users\crist\Documents\GitHub\python-gstat\Curriculum\`

Goal: Senior BI Developer / Data Analyst → **Principal AI Solutions Engineer**
Focus: Reliability, Observability, and Guardrails (not just syntax).

This is an Engineering Implementation curriculum — every week has a Royal Road Standard
(a non-negotiable engineering practice that carries forward into every later week).

---

## File Format — STRICT RULES

Every lesson file follows this interleaved structure (concept → example → exercise, repeated):

```
# ══════════════════════════════════════════════════════════════
#  WEEK X  |  DAY Y  |  LESSON TITLE
# ══════════════════════════════════════════════════════════════
#
#  LEARNING OBJECTIVES
#  ───────────────────
#  1. ...
#
#  TIME:  ~30 minutes
#
#  YOUTUBE
#  ───────
#  Search: "..."
#
# ══════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════
#  CONCEPT 1 — NAME
# ══════════════════════════════════════════════════════════════
# (theory as comments only)
# EXAMPLE ──────────────────────────────────────────────────────
[working runnable code]

# ══════════════════════════════════════════════════════════════
#  EXERCISE 1
# ══════════════════════════════════════════════════════════════
# (instructions as comments)
# Expected output:
#     ...
# --- starting data ---
[actual variable assignments as code]




[4-6 blank lines — student writes here]

# CONCEPT 2 ... etc.
```

### Section marker names
| File type | Section marker | Example marker |
|-----------|---------------|----------------|
| Regular lesson (D1-D5) | `EXERCISE N` | `EXAMPLE` |
| Weekly project (D6, D7) | `TASK N` | no EXAMPLE needed |
| Capstone (Week 12 D1-D5) | `EXERCISE N` | `EXAMPLE` + `# REAL MODE (commented)` |
| Overview/README | no markers required | — |

---

## Style Rules (non-negotiable)

- NO emojis anywhere
- NO `input()` calls
- NO progress tracking variables
- Plain English comments
- Real-world scenarios: employees, sales, pipelines, API data
- Expected output always shown in exercise comments
- Exercise area = 4-6 blank lines ONLY — no code hints
- Starting data given as actual variable assignments above the blank lines
- 3-4 exercises per lesson file, each ~5-10 min

---

## Curriculum Structure

```
Curriculum/
├── README.py                          # Full curriculum map
├── verify_curriculum.py               # QA checker — run: python verify_curriculum.py
├── datasets/
│   ├── titanic_train.xlsx
│   ├── police.xlsx
│   └── hotel_bookings.xlsx
├── Week_1_Python_Basics/              # D1-D5 + D6 project
├── Week_2_Functions/                  # D1-D5 + D6 OOP + D7 project
├── Week_3_External_Data/              # D1-D5 + D6 project
├── Week_4_Pandas_NumPy/               # D1-D5 + D6 project
├── Week_5_Visualization/              # D1-D5 + D6 project
├── Week_6_SQL_Databases/              # D1-D5 + D6 project
├── Week_7_Data_Engineering/           # D1-D5 + D6 project
├── Week_8_Production/                 # D1-D5 + D6 project + D7 QA lesson
├── Week_9_Machine_Learning/           # D1-D5 + D6 project
├── Week_10_AI_Engineering/            # D1-D5 + D6 project
├── Week_11_Advanced_AI/               # D1-D5 + D6 project
└── Week_12_Capstone/                  # OVERVIEW + D1-D5 pipeline project
```

### Week content map
| Week | Topic | Key tools |
|------|-------|-----------|
| 1 | Python basics (variables, lists, dicts, conditionals, loops) | built-in |
| 2 | Functions, error handling, list comprehensions, modules, OOP/classes | built-in |
| 3 | File handling, CSV, JSON, REST APIs, web scraping | requests, BeautifulSoup |
| 4 | NumPy, Pandas basics, data cleaning, groupby | numpy, pandas |
| 5 | Matplotlib, Seaborn, time series, statistics | matplotlib, seaborn |
| 6 | SQL basics, database design, advanced SQL, Python+SQL Server | sqlite3, pyodbc |
| 7 | ETL pipelines, extraction, transformation, loading, automation | pandas, sqlite3 |
| 8 | Cloud platforms, Airflow (conceptual), data quality, Spark (conceptual), FastAPI, pytest, QA | logging, pytest |
| 9 | ML concepts, linear regression, classification, model evaluation | scikit-learn |
| 10 | LLM APIs, prompt engineering (+structured outputs), LangChain (+tool calling +memory +observability), vector DBs, RAG | openai, langchain, chromadb, pydantic |
| 11 | LangGraph agents (+ReAct +multi-agent), NLP basics, speech (Whisper), AI ethics, final project (+LLM evaluation) | langgraph, nltk, whisper, ragas, pytest |
| 12 | Capstone: Gov API → Kafka → MinIO → PostgreSQL → Grafana | kafka, boto3, psycopg2 |

---

## Week 12 Capstone Architecture

```
data.gov.il API
      │
      ▼
  Kafka topic (SIMULATION: Python list)
      │
      ▼
  MinIO Bronze layer (SIMULATION: local folder)
      │
      ▼
  PostgreSQL (SIMULATION: SQLite)
      │
      ▼
  Grafana dashboard (described in comments)
```

Each capstone file has SIMULATION MODE (works without Docker) and REAL MODE (commented out).

---

## QA Workflow

Run anytime:
```bash
cd C:\Users\crist\Documents\GitHub\python-gstat\Curriculum
python verify_curriculum.py
```

Checks per file:
1. `══` border present (new format)
2. No `input(` calls
3. No emojis
4. At least 3 EXERCISE or TASK sections
5. At least 3 EXAMPLE/PART blocks (non-project files only)
6. Blank workspace (4+ blank lines after an EXERCISE/TASK section)
7. Python syntax valid (ast.parse)

---

## Dataset Reference

```python
# Standard path pattern used throughout the curriculum:
import os
path = os.path.join(os.path.dirname(__file__), "..", "datasets", "titanic_train.xlsx")
```

Datasets available: `titanic_train.xlsx`, `police.xlsx`, `hotel_bookings.xlsx`

---

## Past Content Additions (ALL DONE — do not re-add)

All 13 Gen AI topics from Rounds 1-3 have been appended to existing W10-W11 files.
Full list in MEMORY.md. Do not duplicate any of these.

| Done | Topic | File |
|------|-------|------|
| 1-3 | Tool calling, Pydantic outputs, Conversation memory | W10_D3, W10_D2, W10_D3 |
| 4-7 | LLM eval, Streaming, Cost/model, Vision | W11_D5, W10_D1, W10_D2, W10_D4 |
| 8-10 | Fine-tuning, Async, Prompt injection | W10_D5, W10_D1, W11_D4 |
| 11-13 | ReAct, Multi-agent, LangSmith tracing | W11_D1, W11_D1, W10_D3 |

---

## Engineering Refactor Plan (Principal AI Solutions Engineer Track)

### Pillar 1 — Royal Road Standards (one per week, cumulative)

Each week introduces one non-negotiable engineering practice. It is carried forward into every later week.
New blocks are added as CONCEPT + EXERCISE at the end of the target file.

| Week | Standard | Target file | Status |
|------|----------|-------------|--------|
| W1 | `dataclasses` for structured data contracts | W1_D3 (Dictionaries) | DONE |
| W2 | Pydantic for function I/O validation | W2_D2 (Function Parameters) | DONE |
| W3 | Retry logic + structured error logging for APIs | W3_D4 (API Requests) | DONE |
| W4 | Data quality assertions before any analysis | W4_D3 (Data Cleaning) | DONE |
| W5 | `logging` module (not print) in every pipeline | W5_D5 (Project Sales Analysis) | DONE |
| W6 | Parameterized queries only — no string interpolation in SQL | W6_D1 (SQL Basics) | DONE |
| W7 | pytest-style test runner | W7_D6 (Project Tested ETL) | DONE |
| W8 | FastAPI + `/health` endpoint + structured logs | W8_D5 (Final Project) | DONE |
| W9 | MLflow experiment tracking — every model run is logged | W9_D4 (Model Evaluation) | DONE |
| W10 | LangSmith tracing wired into every LLM call | W10_D3 (LangChain Basics) | DONE |
| W11 | Guardrails as middleware (input + output validation) | W11_D1 (LangGraph Agents) | DONE |
| W12 | Full observability: logs + traces + cost dashboard | W12_D5 (Pipeline Final Run) | DONE |

### Pillar 2 — Smart Schema Agent (cumulative project, W6→W12)

One agent grows across 7 weeks. Each stage = new CONCEPT + EXERCISE block in an existing file.
Simulates BigQuery-style governance using SQLite (already in the course).

| Week | Agent gains | Target file | Status |
|------|-------------|-------------|--------|
| W6 | Schema introspection — reads `sqlite_master`, returns metadata dict | W6_D2 (Database Design) | DONE |
| W7 | Audit log — writes every query to an `audit_log` table | W7_D4 (Data Loading) | DONE |
| W8 | Safety layer — rejects DROP/DELETE without WHERE, logs blocked queries | W8_D3 (Data Quality) | DONE |
| W9 | Query classifier — scikit-learn labels queries READ/WRITE/ADMIN | W9_D1 (ML Concepts) | DONE |
| W10 | LLM-powered — LangChain tool calling replaces manual NL→SQL | W10_D3 (LangChain Basics) | DONE |
| W11 | Multi-agent review — Supervisor + SQL Writer + Safety Guard | W11_D1 (LangGraph Agents) | DONE |
| W12 | Production integration — agent exposed via FastAPI on top of pipeline | W12_D5 | DONE |

### Pillar 3 — Gap Modules (new CONCEPT + EXERCISE blocks in W8-W11)

#### Week 8 (ALL DONE)
| Gap | Target file | Status |
|-----|-------------|--------|
| Developer productivity tooling (pre-commit, CI/CD pattern, ruff) | W8_D7 (Automated QA) | DONE |
| Semantic caching — cache key design, TTL, when not to cache | W8_D2 (Orchestration) | DONE |
| Health check + readiness endpoint (FastAPI `/health`) | W8_D5 (Final Project) | DONE |

#### Week 9 (ALL DONE)
| Gap | Target file | Status |
|-----|-------------|--------|
| MLflow experiment tracking (Royal Road Standard for W9) | W9_D4 (Model Evaluation) | DONE |
| Model monitoring — data drift, prediction drift, threshold alerts | W9_D6 (Full ML Workflow) | DONE |

#### Week 10 (ALL DONE)
| Gap | Target file | Status |
|-----|-------------|--------|
| Semantic caching for LLMs (hash-based, cost impact) | W10_D1 (LLM APIs) | DONE |
| Vertex AI orchestration concept + local code skeleton | W10_D5 (RAG Pipeline) | DONE |
| Prompt versioning — prompts as versioned artifacts | W10_D2 (Prompt Engineering) | DONE |

#### Week 11 (ALL DONE)
| Gap | Target file | Status |
|-----|-------------|--------|
| Guardrails as middleware (Royal Road Standard for W11) | W11_D1 (LangGraph Agents) | DONE |
| AI compliance framework — model card as Pydantic schema, audit logging | W11_D4 (AI Ethics) | DONE |
| A/B testing for LLMs — side-by-side prompt comparison with scoring | W11_D5 (Final AI Project) | DONE |

### Pillar 4 — Architecture Decision Notes — ALL DONE

30 lesson files in W8-W12 each have a 5-line ARCHITECTURE DECISION block appended to the header cell.
Format:
```
 ─────────────────────────────────────────────────────────────
 ARCHITECTURE DECISION
 ─────────────────────
 Choosing between: [option A] vs [option B] vs [option C].
 Rule of thumb: use [X] when [condition]. Move to [Y] when [condition].
```

### Refactor Status: ALL PILLARS COMPLETE

All 4 pillars fully implemented. 77/77 QA PASS. QA check 8 (ARCHITECTURE DECISION) active for W8-W12.

---

## Bonus Capstone Projects

Two bonus projects in `Week_12_Capstone/`. The curriculum teaches all prerequisite skills; the student builds the app files themselves.

### Bonus 1 — NL-SQL App (`W12_Bonus_NL_SQL_Project.ipynb`)
User types plain English → FastAPI → LangChain (Groq) → SQLite → Streamlit display.

Student builds: `nl_sql_app/backend.py`, `nl_sql_app/app.py`, `nl_sql_app/seed_data.py`
Provided: `nl_sql_app/.env.example` only.

Teaches: Python decorators, context managers, type hints, LangChain AgentExecutor with Groq.

### Bonus 2 — Self-Healing ETL Pipeline (`W12_Bonus_ETL_Self_Healing_Project.ipynb`)
Raw data → LLM Pre-Validation → MinIO (Bronze) → Python ETL + Schema Mapping → Parquet (Silver) → DuckDB queries + NL Audit Log.

| AWS service | Local simulation |
|---|---|
| S3 | MinIO (already in W12) |
| Glue ETL | Python + pandas |
| Athena | DuckDB (SQL on Parquet) |
| Bedrock | LangChain + Groq |
| DynamoDB | JSON log file |

4 LLM integration points:
1. Pre-Validation — inspect data sample, flag anomalies in natural language
2. Schema Mapping — detect column drift (user_id→customer_id), map semantically
3. Error Remediation — send traceback to LLM, get explanation + fix in plain English
4. NL Audit Logging — human-readable pipeline run summary instead of raw system logs

---

## Prerequisite Lessons for Bonus Projects

New CONCEPT + EXERCISE blocks appended to existing files (do not re-add):

| File | Concept added | Needed for |
|------|--------------|------------|
| W3_D4 API Requests | CONCEPT 5: python-dotenv (.env management) | both |
| W4_D3 Data Cleaning | CONCEPT 5: Parquet format (pyarrow) | ETL |
| W6_D3 Advanced SQL | CONCEPT 4: DuckDB (SQL on files) | ETL |
| W7_D3 Data Transformation | CONCEPT 4: Schema drift detection | ETL |
| W8_D7 Automated QA | CONCEPT 5: Docker + GitHub Actions | both |
| W10_D1 LLM APIs | CONCEPT 8: Groq API | both |
| W10_D2 Prompt Engineering | CONCEPT 7: LLM as data validator | ETL Stage 1 |
| W11_D4 AI Ethics | CONCEPT 6: LLM error remediation + NL audit logging | ETL Stages 3-4 |
| W12_Bonus_NL_SQL | CONCEPT 5: Streamlit basics | NL-SQL app |

---

## User Profile

- Background: Senior BI Developer / Data Analyst (strong SQL, data modeling, reporting)
- Target role: Principal AI Solutions Engineer (Reliability, Observability, Guardrails)
- IDE: VS Code on Windows 11
- Language: English
- Prefers: simple, clear, gstat-style visual separation
- Dislikes: emojis, `input()`, progress tracking, too many hints in exercises
