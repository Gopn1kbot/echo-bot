import sqlite3
import time

conn = sqlite3.connect("echo.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    text TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    last_seen REAL DEFAULT 0
)
""")

conn.commit()

def save(user_id, text):
    cursor.execute(
        "INSERT INTO memory (user_id, text) VALUES (?, ?)",
        (user_id, text)
    )
    conn.commit()

def get_last(user_id):
    cursor.execute("""
        SELECT text FROM memory
        WHERE user_id=?
        ORDER BY id DESC
        LIMIT 10
    """, (user_id,))

    return [r[0] for r in reversed(cursor.fetchall())]

def update_seen(user_id):
    cursor.execute("""
    INSERT INTO users (user_id, last_seen)
    VALUES (?, ?)
    ON CONFLICT(user_id)
    DO UPDATE SET last_seen=excluded.last_seen
    """, (user_id, time.time()))
    conn.commit()
