import sqlite3

conn = sqlite3.connect("healthmon.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS medications(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    time TEXT
)
""")

conn.commit()

def add_medication(name, time):
    cursor.execute("INSERT INTO medications(name,time) VALUES (?,?)",(name,time))
    conn.commit()

def get_medications():
    cursor.execute("SELECT name,time FROM medications")
    return cursor.fetchall()
