import sqlite3

conn = sqlite3.connect("echo.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS memory (
    user_id INTEGER PRIMARY KEY,
    last_text TEXT
)
""")

conn.commit()


def save(user_id, text):
    cur.execute("""
    INSERT OR REPLACE INTO memory (user_id, last_text)
    VALUES (?, ?)
    """, (user_id, text))
    conn.commit()


def load(user_id):
    cur.execute("SELECT last_text FROM memory WHERE user_id=?", (user_id,))
    row = cur.fetchone()
    return row[0] if row else ""
