import sqlite3

# ---------------- DATABASE CONNECTION ---------------- #

conn = sqlite3.connect("healthmon.db", check_same_thread=False)
cursor = conn.cursor()

# ---------------- MEDICATION TABLE ---------------- #

cursor.execute("""
CREATE TABLE IF NOT EXISTS medications(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    time TEXT NOT NULL
)
""")

# ---------------- HEALTH GOALS TABLE ---------------- #

cursor.execute("""
CREATE TABLE IF NOT EXISTS health_goals(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    goal TEXT,
    target_weight REAL,
    current_weight REAL
)
""")

conn.commit()

# =====================================================
# MEDICATION FUNCTIONS
# =====================================================

def add_medication(name, time):
    cursor.execute(
        "INSERT INTO medications(name, time) VALUES (?, ?)",
        (name, time)
    )
    conn.commit()


def get_medications():
    cursor.execute(
        "SELECT name, time FROM medications"
    )
    return cursor.fetchall()


def delete_medication(name):
    cursor.execute(
        "DELETE FROM medications WHERE name=?",
        (name,)
    )
    conn.commit()

# =====================================================
# HEALTH GOALS
# =====================================================

def save_goal(goal, target_weight, current_weight):
    cursor.execute(
        """
        INSERT INTO health_goals
        (goal, target_weight, current_weight)
        VALUES (?, ?, ?)
        """,
        (goal, target_weight, current_weight)
    )

    conn.commit()


def get_goals():
    cursor.execute(
        """
        SELECT
        goal,
        target_weight,
        current_weight
        FROM health_goals
        """
    )

    return cursor.fetchall()

# =====================================================
# DATABASE CLOSE
# =====================================================

def close_database():
    conn.close()
