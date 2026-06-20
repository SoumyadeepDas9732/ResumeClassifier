import sqlite3

conn = sqlite3.connect("database.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS candidates(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT,

    email TEXT,

    phone TEXT,

    education TEXT,

    role TEXT,

    score INTEGER,

    skills TEXT,

    resume_path TEXT,

    confidence REAL,

    second_role TEXT,

    second_confidence REAL

)
""")

conn.commit()
conn.close()

print("Database Ready")