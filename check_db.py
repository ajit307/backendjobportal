import sqlite3

# Database connect
conn = sqlite3.connect("test.db")
cursor = conn.cursor()

# Tables list
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables:", tables)

# Example: Users table data
cursor.execute("SELECT * FROM Users;")
users = cursor.fetchall()
print("Users:")
for user in users:
    print(user)

# Jobs table data
cursor.execute("SELECT * FROM Jobs;")
jobs = cursor.fetchall()
print("Jobs:")
for job in jobs:
    print(job)

# Applications table data
cursor.execute("SELECT * FROM Applications;")
apps = cursor.fetchall()
print("Applications:")
for app in apps:
    print(app)

conn.close()
