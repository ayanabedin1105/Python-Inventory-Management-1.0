import sqlite3
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
username = "admin"
password = "admin123"
hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

conn = sqlite3.connect("database.db")
c = conn.cursor()
c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
conn.commit()
conn.close()

print("User added successfully!")
