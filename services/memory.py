import sqlite3
import os


os.makedirs("database", exist_ok=True)

DB_PATH = "database/chat_history.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS chat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            query TEXT,
            response TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_chat(user, query, response):
    init_db() 

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO chat (user, query, response) VALUES (?, ?, ?)",
        (user, query, response)
    )

    conn.commit()
    conn.close()


def get_history(user):
    init_db()  

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT id, query, response 
        FROM chat 
        WHERE user=? 
        ORDER BY id DESC
    """, (user,))

    data = cur.fetchall()
    conn.close()
    return data