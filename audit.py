# audit.py
import sqlite3
from datetime import datetime, timezone

DB_PATH = "audit_log.db"


def log_action(action, user_id=None, user_email=None, detail=None, status="SUCCESS"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO audit_log (timestamp, action, user_id, user_email, detail, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        datetime.now(timezone.utc).isoformat(),
        action,
        user_id,
        user_email,
        detail,
        status
    ))

    conn.commit()
    conn.close()