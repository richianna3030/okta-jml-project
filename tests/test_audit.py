# tests/test_audit.py
import sqlite3
import os
import pytest
from audit import log_action

TEST_DB = "test_audit_log.db"


@pytest.fixture
def test_db(monkeypatch):
    monkeypatch.setattr("audit.DB_PATH", TEST_DB)

    conn = sqlite3.connect(TEST_DB)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            action TEXT NOT NULL,
            user_id TEXT,
            user_email TEXT,
            detail TEXT,
            status TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

    yield TEST_DB

    os.remove(TEST_DB)


def test_log_action_writes_success_row(test_db):
    log_action("CREATE", user_id="abc123", user_email="test@example.com", detail="Test detail")

    conn = sqlite3.connect(test_db)
    rows = conn.execute("SELECT * FROM audit_log").fetchall()
    conn.close()

    assert len(rows) == 1
    assert rows[0][2] == "CREATE"
    assert rows[0][6] == "SUCCESS"


def test_log_action_defaults_to_success(test_db):
    log_action("DEACTIVATE", user_id="abc123", user_email="test@example.com", detail="No status passed")

    conn = sqlite3.connect(test_db)
    row = conn.execute("SELECT status FROM audit_log").fetchone()
    conn.close()

    assert row[0] == "SUCCESS"


def test_log_action_records_failure_status(test_db):
    log_action("GROUP_ASSIGN", user_id="abc123", user_email="test@example.com", detail="Failed call", status="FAILURE")

    conn = sqlite3.connect(test_db)
    row = conn.execute("SELECT status FROM audit_log").fetchone()
    conn.close()

    assert row[0] == "FAILURE"