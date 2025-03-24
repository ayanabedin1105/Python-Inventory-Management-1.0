from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import sqlite3
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
# define app name
app = Flask(__name__)
app.secret_key = '1105hotmail'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# create datasbase and table if doesn't exists
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS inventory
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 quantity INTEGER NOT NULL)''')
    conn.commit()
    conn.close()

init_db()

# User class for flask-Login
class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


# Home Page (Requires Login)
@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM inventory")
    items = c.fetchall()
    conn.close()
    return render_template('index.html', items=items)

# Add Item (AJAX)
@app.route('/add', methods=['POST'])
@login_required
# def add_item():
#     name = request.form['name']
#     quantity = request.form['quantity']
#     conn = sqlite3.connect('database.db')
#     c = conn.cursor()
#     c.execute("INSERT INTO inventory (name, quantity) VALUES (?,?)", (name, quantity))
#     conn.commit()
#     conn.close()
#     return jsonify({"name": name, "quantity": quantity})

# new AJAX add item code
def add_item():
    data = request.get_json()
    name = data.get("name")
    quantity = data.get("quantity")
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO inventory (name, quantity) VALUES (?,?)", (name, quantity))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "name": name, "quantity": quantity})

# Delete Item (AJAX)
@app.route('/delete/<int:item_id>', methods=["POST"])
@login_required
def delete_item(item_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM inventory WHERE id=?", (item_id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "item_id": item_id})

# Update Item (AJAX) (Note: this is not working as expected, it's probably a problem with the way we're getting the data)
@app.route('/update', methods=['POST'])
@login_required
def update_item(item_id):
    # item_id = request.form["id"]
    # quantity = request.form["quantity"]
    # conn = sqlite3.connect('database.db')
    # c = conn.cursor()
    # c.execute("UPDATE inventory SET quantity=? WHERE id=?", (quantity, item_id))
    # conn.commit()
    # conn.close()
    
    # return jsonify({"status": "success", "item_id": item_id, "quantity": quantity})

    data = request.get_json()
    item_id = data.get("id")
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("UPDATE inventory SET quantity=? WHERE id=?", (quantity, item_id))
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success", "item_id": item_id, "quantity": quantity})

# Authentication Routes
@app.route("/login", methods=["GET", "POST"])

def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        user = c.fetchone()
        conn.close()
        
        if user and bcrypt.check_password_hash(user[2], password):
            login_user(User(user[0]))
            return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__=="__main__":
    app.run(debug=True)
