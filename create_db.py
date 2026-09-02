# create_db.py
import sqlite3

conn = sqlite3.connect("audit_log.db")
cursor = conn.cursor()

cursor.execute("""
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

print("audit_log.db created with audit_log table.")