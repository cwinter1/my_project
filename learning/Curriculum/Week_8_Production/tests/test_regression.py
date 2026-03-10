"""
W8 Regression Gate — Smart Schema Agent, all 6 stages.

Runs on every PR to main to ensure no prior Agent stage regresses.
Run with:
    pytest Week_8_Production/tests/test_regression.py -v

Stages tested:
  Stage 1 (W6): schema introspection returns a metadata dict
  Stage 2 (W7): every query is written to audit_log
  Stage 3 (W8): DROP / DELETE-without-WHERE are blocked with ValueError
  Stage 4 (W9): query classifier returns READ / WRITE / ADMIN
  Stage 5 (W10): NL->SQL returns a SELECT (mocked, MOCK_LLM=true)
  Stage 6 (W11): Supervisor routes to sql_writer or safety_guard correctly
"""

import os
import re
import sqlite3

import pytest


# ── Complete Smart Schema Agent ────────────────────────────────────────────────

class SmartSchemaAgent:
    """
    Cumulative agent built across W6-W11.
    Self-contained reference implementation for regression testing.
    """

    def __init__(self, conn):
        self._conn = conn
        self._setup_audit()

    # Stage 1 — Schema introspection (W6)
    def schema(self):
        cur = self._conn.cursor()
        cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name != 'audit_log'"
        )
        tables = [r[0] for r in cur.fetchall()]
        result = {}
        for t in tables:
            cur.execute(f"PRAGMA table_info({t})")
            result[t] = [{"col": r[1], "type": r[2]} for r in cur.fetchall()]
        return result

    # Stage 2 — Audit log (W7)
    def _setup_audit(self):
        self._conn.execute(
            "CREATE TABLE IF NOT EXISTS audit_log "
            "(id INTEGER PRIMARY KEY AUTOINCREMENT, sql TEXT, "
            "ts DATETIME DEFAULT CURRENT_TIMESTAMP)"
        )
        self._conn.commit()

    def _log(self, sql):
        self._conn.execute("INSERT INTO audit_log (sql) VALUES (?)", (sql,))
        self._conn.commit()

    # Stage 3 — Safety layer (W8)
    def _check_safety(self, sql):
        upper = sql.strip().upper()
        if re.search(r"\bDROP\b", upper):
            raise ValueError(f"Blocked: DROP is not allowed")
        if re.search(r"\bDELETE\b", upper) and not re.search(r"\bWHERE\b", upper):
            raise ValueError(f"Blocked: DELETE without WHERE is not allowed")

    # Stage 4 — Query classifier (W9)
    def classify(self, sql):
        upper = sql.strip().upper()
        if upper.startswith("SELECT"):
            return "READ"
        if any(upper.startswith(k) for k in ("INSERT", "UPDATE", "DELETE")):
            return "WRITE"
        return "ADMIN"

    # Stage 5 — NL->SQL (W10, mocked)
    def nl_to_sql(self, question):
        if os.environ.get("MOCK_LLM") == "true":
            if "salary" in question.lower():
                return "SELECT name, salary FROM employees ORDER BY salary DESC"
            return "SELECT * FROM employees"
        raise RuntimeError("Set MOCK_LLM=true in CI or provide an API key")

    # Stage 6 — Multi-agent routing (W11)
    def route(self, sql):
        """Returns ("sql_writer", sql) or ("safety_guard", error_msg)."""
        try:
            self._check_safety(sql)
        except ValueError as e:
            return ("safety_guard", str(e))
        if not sql.strip().upper().startswith("SELECT"):
            return ("safety_guard", "Only SELECT queries allowed")
        return ("sql_writer", sql)

    # Run (used by Stage 2 tests)
    def run(self, sql):
        self._check_safety(sql)
        self._log(sql)
        cur = self._conn.cursor()
        cur.execute(sql)
        return cur.fetchall()


# ── Fixture ────────────────────────────────────────────────────────────────────

@pytest.fixture
def agent():
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE employees "
        "(id INTEGER PRIMARY KEY, name TEXT, dept TEXT, salary REAL)"
    )
    conn.executemany("INSERT INTO employees VALUES (?,?,?,?)", [
        (1, "Alice", "Engineering", 95000),
        (2, "Bob",   "Sales",       72000),
        (3, "Carol", "Finance",     81000),
    ])
    conn.commit()
    return SmartSchemaAgent(conn)


# ── Stage 1 — Schema introspection ────────────────────────────────────────────

def test_stage1_schema_returns_dict(agent):
    schema = agent.schema()
    assert isinstance(schema, dict)
    assert len(schema) >= 1


def test_stage1_schema_has_employees_columns(agent):
    schema = agent.schema()
    assert "employees" in schema
    cols = [c["col"] for c in schema["employees"]]
    assert "name" in cols
    assert "salary" in cols


# ── Stage 2 — Audit log ────────────────────────────────────────────────────────

def test_stage2_query_written_to_audit_log(agent):
    before = agent._conn.execute(
        "SELECT COUNT(*) FROM audit_log"
    ).fetchone()[0]
    agent.run("SELECT * FROM employees")
    after = agent._conn.execute(
        "SELECT COUNT(*) FROM audit_log"
    ).fetchone()[0]
    assert after == before + 1


# ── Stage 3 — Safety layer ─────────────────────────────────────────────────────

def test_stage3_blocks_drop(agent):
    with pytest.raises(ValueError, match="DROP"):
        agent.run("DROP TABLE employees")


def test_stage3_blocks_delete_without_where(agent):
    with pytest.raises(ValueError, match="DELETE"):
        agent.run("DELETE FROM employees")


def test_stage3_allows_select(agent):
    rows = agent.run("SELECT * FROM employees")
    assert len(rows) == 3


# ── Stage 4 — Query classifier ────────────────────────────────────────────────

def test_stage4_classifies_select_as_read(agent):
    assert agent.classify("SELECT * FROM employees") == "READ"


def test_stage4_classifies_insert_as_write(agent):
    assert agent.classify("INSERT INTO employees VALUES (4,'Dan','HR',60000)") == "WRITE"


def test_stage4_classifies_drop_as_admin(agent):
    assert agent.classify("DROP TABLE employees") == "ADMIN"


# ── Stage 5 — NL->SQL (mocked) ────────────────────────────────────────────────

def test_stage5_nl_to_sql_returns_select(agent, monkeypatch):
    monkeypatch.setenv("MOCK_LLM", "true")
    sql = agent.nl_to_sql("Show me all employees ordered by salary")
    assert sql.strip().upper().startswith("SELECT")


# ── Stage 6 — Multi-agent routing ─────────────────────────────────────────────

def test_stage6_routes_select_to_sql_writer(agent):
    target, result = agent.route("SELECT * FROM employees")
    assert target == "sql_writer"


def test_stage6_routes_drop_to_safety_guard(agent):
    target, result = agent.route("DROP TABLE employees")
    assert target == "safety_guard"


def test_stage6_routes_delete_to_safety_guard(agent):
    target, result = agent.route("DELETE FROM employees")
    assert target == "safety_guard"
