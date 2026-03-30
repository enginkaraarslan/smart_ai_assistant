import sqlite3
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")


def create_user(username, password):
    conn = sqlite3.connect("database/users.db")
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
    finally:
        conn.close()


def login(username, password):
    conn = sqlite3.connect("database/users.db")
    cur = conn.cursor()

    cur.execute("SELECT password FROM users WHERE username=?", (username,))
    data = cur.fetchone()

    conn.close()

    if data:
        return pwd_context.verify(password, data[0])

    return False