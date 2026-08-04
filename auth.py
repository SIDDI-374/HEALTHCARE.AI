"""
HealthMonAI authentication module.

Stores users in a local SQLite database (healthmonai_users.db, created
automatically on first run). Passwords are never stored in plain text —
each password is hashed with PBKDF2-HMAC-SHA256 using a random per-user
salt.
"""

import sqlite3
import hashlib
import secrets

DB_PATH = "healthmonai_users.db"


def init_db():
    """Create the users table if it doesn't already exist. Call once at app startup."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            salt TEXT NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def _hash_password(password: str, salt: str) -> str:
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100_000
    ).hex()


def user_exists(username: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM users WHERE username = ?", (username,))
    result = cur.fetchone()
    conn.close()
    return result is not None


def create_user(username: str, password: str) -> bool:
    """Create a new user. Returns False if the username is already taken."""
    if user_exists(username):
        return False

    salt = secrets.token_hex(16)
    password_hash = _hash_password(password, salt)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (username, salt, password_hash) VALUES (?, ?, ?)",
        (username, salt, password_hash)
    )
    conn.commit()
    conn.close()
    return True


def verify_user(username: str, password: str) -> bool:
    """Check a username/password combination. Returns True if valid."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT salt, password_hash FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()

    if row is None:
        return False

    salt, stored_hash = row
    return _hash_password(password, salt) == stored_hash