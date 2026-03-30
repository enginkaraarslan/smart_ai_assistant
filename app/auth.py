import sqlite3
import os
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")

DB_PATH = "database/users.db"


os.makedirs("database", exist_ok=True)

def create_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    """)

    hashed_password = pwd_context.hash(password)

    try:
        cur.execute("INSERT INTO users VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        return True
    except:
        return False


def login(username, password):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cur.fetchone()

    if result and pwd_context.verify(password, result[0]):
        return True

    return False