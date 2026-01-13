import sqlite3

def connect():
    return sqlite3.connect("data.db")

def create_table():
    con = connect()
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tappal(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        text TEXT,
        category TEXT,
        status TEXT
    )
    """)
    con.commit()
    con.close()
