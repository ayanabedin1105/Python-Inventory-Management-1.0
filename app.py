from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = "ae414aaa83baaa4c2b0f7272a1f84810"  # Change this in production
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# Initialize Database
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # Create users table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Create inventory table
    c.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()

init_db()

# User Class for Flask-Login
class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Home Page (Requires Login)
@app.route("/")
@login_required
def index():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM inventory")
    items = c.fetchall()
    conn.close()
    return render_template("index.html", items=items)

# Add Item (AJAX)
@app.route("/add", methods=["POST"])
@login_required
def add():
    data = request.get_json()
    name = data.get("name")
    quantity = data.get("quantity")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO inventory (name, quantity) VALUES (?, ?)", (name, quantity))
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "name": name, "quantity": quantity})

# Delete Item (AJAX)
@app.route("/delete/<int:item_id>", methods=["POST"])
@login_required
def delete(item_id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("DELETE FROM inventory WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "item_id": item_id})

# Update Item (AJAX)
@app.route("/update", methods=["POST"])
@login_required
def update():
    data = request.get_json()
    item_id = data.get("id")
    quantity = data.get("quantity")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("UPDATE inventory SET quantity = ? WHERE id = ?", (quantity, item_id))
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "item_id": item_id, "quantity": quantity})

# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        conn.close()

        if user and bcrypt.check_password_hash(user[2], password):
            login_user(User(user[0]))
            return redirect(url_for("index"))
    
    return render_template("login.html")

# Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# Run Flask App
if __name__ == "__main__":
    app.run(debug=True)
