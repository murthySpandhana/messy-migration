import sqlite3
from werkzeug.security import generate_password_hash

# Connect to SQLite DB
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

# Insert sample users with hashed passwords
users = [
    ('John Doe', 'john@example.com', 'password123'),
    ('Jane Smith', 'jane@example.com', 'secret456'),
    ('Bob Johnson', 'bob@example.com', 'qwerty789')
]

for name, email, plain_password in users:
    hashed_password = generate_password_hash(plain_password)
    cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                   (name, email, hashed_password))

conn.commit()
conn.close()

print("Database initialized with sample users (hashed passwords)")
