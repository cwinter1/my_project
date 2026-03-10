"""
W11 Multi-Agent Contract tests — Supervisor, SQL Writer, Safety Guard.

Run with:
    MOCK_LLM=true pytest Week_11_Advanced_AI/tests/test_agent.py -v

What is tested:
  - Supervisor routes READ query to SQL Writer
  - Safety Guard blocks DROP TABLE
  - Safety Guard blocks DELETE without WHERE
  - Full pipeline: NL input -> Supervisor -> SQL Writer -> Safety Guard -> output
"""

import re

import pytest


# ── Agent implementations ──────────────────────────────────────────────────────

class SafetyGuard:
    """Blocks dangerous SQL: DROP, TRUNCATE, DELETE without WHERE."""

    BLOCKED_PATTERNS = [
        (re.compile(r"\bDROP\b",     re.IGNORECASE), "DROP not allowed"),
        (re.compile(r"\bTRUNCATE\b", re.IGNORECASE), "TRUNCATE not allowed"),
    ]

    def check(self, sql):
        """Returns (safe: bool, reason: str)."""
        for pattern, reason in self.BLOCKED_PATTERNS:
            if pattern.search(sql):
                return (False, reason)
        # DELETE without WHERE
        if re.search(r"\bDELETE\b", sql, re.IGNORECASE):
            if not re.search(r"\bWHERE\b", sql, re.IGNORECASE):
                return (False, "DELETE without WHERE not allowed")
        return (True, "")


class SQLWriter:
    """Generates or validates SELECT queries. Mocked when MOCK_LLM=true."""

    def write(self, sql_or_nl):
        """
        If input is already a SELECT, return it unchanged.
        Otherwise, mock an NL->SQL conversion.
        """
        if sql_or_nl.strip().upper().startswith("SELECT"):
            return sql_or_nl
        # Mocked NL->SQL (no LLM call needed in CI)
        return "SELECT * FROM employees"


class Supervisor:
    """
    Routes user input through the multi-agent pipeline:
      1. Safety Guard pre-check
      2. SQL Writer (generates SELECT)
      3. Safety Guard post-check on generated SQL
    """

    def __init__(self):
        self.sql_writer   = SQLWriter()
        self.safety_guard = SafetyGuard()

    def route(self, user_input):
        """
        Returns:
          {"agent": "sql_writer",   "result": sql,      "safe": True}
          {"agent": "safety_guard", "result": reason,   "safe": False}
        """
        # Pre-check: block known-dangerous inputs before calling SQL Writer
        safe, reason = self.safety_guard.check(user_input)
        if not safe:
            return {"agent": "safety_guard", "result": reason, "safe": False}

        # SQL Writer: generate or pass through SQL
        sql = self.sql_writer.write(user_input)

        # Post-check: validate generated SQL before returning
        safe2, reason2 = self.safety_guard.check(sql)
        if not safe2:
            return {"agent": "safety_guard", "result": reason2, "safe": False}

        return {"agent": "sql_writer", "result": sql, "safe": True}


# ── Fixtures ───────────────────────────────────────────────────────────────────

@pytest.fixture
def supervisor():
    return Supervisor()


# ── Safety Guard contract ─────────────────────────────────────────────────────

def test_safety_guard_blocks_drop():
    guard = SafetyGuard()
    safe, reason = guard.check("DROP TABLE employees")
    assert not safe
    assert "DROP" in reason


def test_safety_guard_blocks_delete_without_where():
    guard = SafetyGuard()
    safe, reason = guard.check("DELETE FROM employees")
    assert not safe
    assert "DELETE" in reason


def test_safety_guard_allows_delete_with_where():
    guard = SafetyGuard()
    safe, _ = guard.check("DELETE FROM employees WHERE id = 999")
    assert safe


def test_safety_guard_allows_select():
    guard = SafetyGuard()
    safe, _ = guard.check("SELECT * FROM employees WHERE dept = 'Engineering'")
    assert safe


# ── Supervisor routing contract ───────────────────────────────────────────────

def test_supervisor_routes_select_to_sql_writer(supervisor):
    result = supervisor.route("SELECT name, salary FROM employees")
    assert result["agent"] == "sql_writer"
    assert result["safe"] is True


def test_supervisor_routes_drop_to_safety_guard(supervisor):
    result = supervisor.route("DROP TABLE employees")
    assert result["agent"] == "safety_guard"
    assert result["safe"] is False


def test_supervisor_routes_delete_without_where_to_safety_guard(supervisor):
    result = supervisor.route("DELETE FROM employees")
    assert result["agent"] == "safety_guard"
    assert result["safe"] is False


# ── Full pipeline: NL -> Supervisor -> SQL Writer -> Safety Guard ──────────────

def test_full_pipeline_nl_returns_select(supervisor):
    """NL question flows through full pipeline and returns a safe SELECT."""
    result = supervisor.route("Show me all employees in Engineering")
    assert result["safe"] is True
    assert result["agent"] == "sql_writer"
    assert result["result"].strip().upper().startswith("SELECT")


def test_full_pipeline_dangerous_nl_is_blocked(supervisor):
    """A dangerous SQL string passed as NL is caught by pre-check."""
    result = supervisor.route("DROP TABLE employees")
    assert result["safe"] is False
    assert result["agent"] == "safety_guard"
