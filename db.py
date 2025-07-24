import sqlite3

# Shared DB connection
conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()

def get_db():
    return conn, cursor
