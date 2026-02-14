import sqlite3

# connect to database (it will create a file automatically)
conn = sqlite3.connect("bookings.db")

# create a cursor (used to run commands)
cursor = conn.cursor()

# create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    truck TEXT,
    container_type TEXT,
    date TEXT,
    time TEXT
)
""")
# create users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

# save changes
conn.commit()

# close connection
conn.close()

print("Database and table created successfully!")
