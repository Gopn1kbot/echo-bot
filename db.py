import sqlite3
from datetime import datetime

conn = sqlite3.connect("echo.db", check_same_thread=False)
cur = conn.cursor()

# 🧠 таблица памяти (контекст диалога)
cur.execute("""
CREATE TABLE IF NOT EXISTS memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    role TEXT,
    content TEXT,
    created_at TEXT
)
""")

conn.commit()


# 💾 сохранить сообщение
def save_message(user_id, role, content):
    cur.execute("""
    INSERT INTO memory (user_id, role, content, created_at)
    VALUES (?, ?, ?, ?)
    """, (user_id, role, content, datetime.now()))
    conn.commit()


# 📖 загрузить историю
def load_history(user_id, limit=10):
    cur.execute("""
    SELECT role, content FROM memory
    WHERE user_id=?
    ORDER BY id DESC
    LIMIT ?
    """, (user_id, limit))

    rows = cur.fetchall()

    # переворачиваем, чтобы было по порядку диалога
    return list(reversed(rows))
