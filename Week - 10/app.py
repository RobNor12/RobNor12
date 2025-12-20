#made use of chatgpt to help me with my code
import os
import sqlite3
from flask import Flask, render_template, request, redirect, session, flash
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import requests
import time
from datetime import datetime

app = Flask(__name__)

DATABASE = os.path.join(os.path.dirname(__file__), "wall.db")
db_initialized = False
AUTO_STOCKS = ["AAPL"]
COMPANY_NAMES = {
    "AAPL": "Apple Inc.",
    "AMZN": "Amazon.com, Inc.",
}

#configure session 
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#intilized db
def lookup(symbol):
    symbol = symbol.upper().strip()
    api_key = "D5AQ9FSAIVLLA37G"

    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()

    if "Global Quote" not in data or not data["Global Quote"]:
        return None

    try:
        return float(data["Global Quote"]["05. price"])
    except:
        return None
    
def db_connect():
    return sqlite3.connect(DATABASE, check_same_thread=False)

def init_db():
    con = db_connect()
    cur = con.cursor()

    cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                hash TEXT NOT NULL
            );
        """)
    
    cur.execute("""
            CREATE TABLE IF NOT EXISTS stocks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                price REAL
            );
        """)
    
    cur.execute("""
            CREATE TABLE IF NOT EXISTS watchlist (
                user_id INTEGER NOT NULL,
                stock_id INTEGER NOT NULL,
                PRIMARY KEY (user_id, stock_id),
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (stock_id) REFERENCES stocks(id)
            );
        """)

    con.commit()
    con.close()

def auto_update_stocks():
    con = db_connect()
    cur = con.cursor()

    cur.execute("SELECT COUNT(*) FROM stocks")
    count = cur.fetchone()[0]

    if count == 0:
        print("📈 Inserting default stocks...")
        for sym in AUTO_STOCKS:
            cur.execute(
            "INSERT INTO stocks (symbol, name) VALUES (?, ?)",
            (sym, COMPANY_NAMES.get(sym, sym))
            )
        con.commit()
        print("✅ All default stocks inserted")

    con.close()

def update_stock_prices():
    con = db_connect()
    cur = con.cursor()

    cur.execute("SELECT symbol FROM stocks")
    symbols = cur.fetchall()

    for (sym,) in symbols:
        price = lookup(sym)
        if price is None:
            continue

        cur.execute(
            "UPDATE stocks SET price = ? WHERE symbol = ?",
            (price, sym)
        )

    con.commit()
    con.close()

def update_stock_prices():
    con = db_connect()
    cur = con.cursor()

    cur.execute("SELECT symbol FROM stocks")
    symbols = cur.fetchall()

    for (sym,) in symbols:
        price = lookup(sym)
        if price is None:
            continue  # keep old price

        cur.execute("""
            UPDATE stocks
            SET price = ?
            WHERE symbol = ?
        """, (price, sym))

    con.commit()
    con.close()

    return price

@app.before_request
def startup():
    global db_initialized
    if not db_initialized:
        init_db()
        auto_update_stocks()
        update_stock_prices()
        db_initialized = True

def migrate_stocks_table():
    con = db_connect()
    cur = con.cursor()

    try:
        cur.execute("ALTER TABLE stocks ADD COLUMN price REAL")
    except sqlite3.OperationalError:
        pass

    try:
        cur.execute("ALTER TABLE stocks ADD COLUMN updated_at TEXT")
    except sqlite3.OperationalError:
        pass

    con.commit()
    con.close()

@app.route("/add", methods=["POST"])
def add_stock():
    symbol = request.form.get("symbol")
    stock = lookup(symbol)

    if stock is None:
        flash("Invalid stock symbol")
        return redirect("/")

    con = db_connect()
    cur = con.cursor()

    # Insert the stock if it doesn’t exist
    cur.execute("""
        INSERT OR IGNORE INTO stocks (symbol, name)
        VALUES (?, ?)
    """, (stock["symbol"], stock["name"]))

    con.commit()
    con.close()

    flash(f"{stock['symbol']} added!")
    return redirect("/")

#HOMEPAGE 
@app.route("/")
def index():
    con = db_connect()
    cur = con.cursor()

    cur.execute("""
        SELECT symbol, name, price
        FROM stocks
        ORDER BY symbol
    """)
    rows = cur.fetchall()
    con.close()

    stocks = []

    for symbol, name, price in rows:
        stocks.append({
            "symbol": symbol,
            "name": name if name != symbol else None,
            "price": price if price is not None else 0.0
        })

    return render_template("index.html", stocks=stocks)
    

#REGISTER
@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        con = db_connect()
        cur = con.cursor()

        #check existing username 

        cur.execute("SELECT * FROM users WHERE username =?", (username, ))
        if cur.fetchone():
            flash("username already taken")
            return redirect("/register")
        
        #Insert new user 
        hashed = generate_password_hash(password)
        cur.execute("INSERT INTO users (username, hash) VALUES (?, ?);", (username, hashed))
        con.commit()
        con.close()

        flash("Registered Successfully.")
        return redirect("/login")
    
    return render_template("register.html")

#LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        con = db_connect()
        cur = con.cursor()

        cur.execute("SELECT id, hash FROM users WHERE username = ?", (username,))
        user = cur.fetchone()

        if user is None or not check_password_hash(user[1], password):
            flash("Invalid username or password.")
            return redirect("/login")
        
        session["user_id"] = user[0]
        flash("Welcome back!")
        return redirect("/")
    
    return render_template("login.html")

#LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out.")
    return redirect("/")

#WALL List bookmark
@app.route("/bookmark/<symbol>")
def bookmark(symbol):
    if "user_id" not in session:
        flash("You must be logged in to bookmark")
        return redirect("/login")
    
    user_id = session["user_id"]
    con = db_connect()
    cur = con.cursor()

    #get stock id
    cur.execute("SELECT id FROM stocks WHERE symbol = ?", (symbol, ))
    stock = cur.fetchone()
    if stock is None: 
        flash("stock not found")
        return redirect("/")
    
    stock_id = stock[0]

    #check if stock is bookmarked 
    cur.execute("SELECT * FROM watchlist WHERE user_id = ? and stock_id = ?", (user_id, stock_id))
    exists = cur.fetchone()

    if exists:
        cur.execute("DELETE FROM watchlist WHERE user_id = ? and stock_id = ?", (user_id, stock_id))
        flash(f"Removed {symbol} from wall list.")
    else:
        cur.execute("INSERT INTO watchlist (user_id, stock_id) VALUES (?, ?)", (user_id, stock_id))
        flash(f"Added {symbol} to wall list.")

    con.commit()
    con.close()

    return redirect("/")

#user account deletion
@app.route("/delete", methods=["GET", "POST"])
def delete_account():
    # Must be logged in
    if "user_id" not in session:
        flash("You must login first")
        return redirect("/login")
    
    if request.method == "POST":
        username_input = request.form.get("username")  # optional verification
        password = request.form.get("password")
        
        con = db_connect()
        cur = con.cursor()

        # Verify user by session id and optionally username
        cur.execute("SELECT id, hash, username FROM users WHERE id = ?", (session["user_id"],))
        user = cur.fetchone()
        
        if user is None:
            con.close()
            flash("User not found.")
            return redirect("/delete")
        
        # Check password
        if not check_password_hash(user[1], password):
            con.close()
            flash("Incorrect password.")
            return redirect("/delete")
        
        # Optional: verify username matches input
        if username_input and username_input != user[2]:
            con.close()
            flash("Username does not match logged-in user.")
            return redirect("/delete")
        
        # Delete watchlist entries
        cur.execute("DELETE FROM watchlist WHERE user_id = ?", (session["user_id"],))
        # Delete user
        cur.execute("DELETE FROM users WHERE id = ?", (session["user_id"],))

        con.commit()
        con.close()

        # Clear session
        session.clear()
        flash("Account deleted successfully.")
        return redirect("/")
    
    return render_template("delete.html")

#users wall list
@app.route("/wall")
def wall():
    if "user_id" not in session:
        flash("You must log in to view your Wall List.")
        return redirect("/login")

    user_id = session["user_id"]

    con = db_connect()
    cur = con.cursor()

    # Get the user's bookmarked stocks
    cur.execute("""
        SELECT stocks.symbol, stocks.name
        FROM watchlist
        JOIN stocks ON watchlist.stock_id = stocks.id
        WHERE watchlist.user_id = ?
        ORDER BY stocks.symbol;
    """, (user_id,))

    wall_list = cur.fetchall()
    con.close()

    return render_template("wall.html", stocks=wall_list)

# search
@app.route("/search", methods=["POST"])
def search():
    con = db_connect()
    cur = con.cursor()
    symbol = request.form.get("symbol", "").upper().strip()

    if not symbol:
        flash("Please enter a stock symbol.")
        return redirect("/")

    price = lookup(symbol)
    if price is None:
        flash("Stock not found.")
        return redirect("/")

    name = COMPANY_NAMES.get(symbol, symbol)

    cur.execute("""
    INSERT INTO stocks (symbol, name, price)
    VALUES (?, ?, ?)
    ON CONFLICT(symbol) DO UPDATE SET
        name = excluded.name,
        price = excluded.price
""", (symbol, name, price))

    con.commit()
    con.close()

    flash(f"{symbol} added to Wall Watcher!")
    return redirect("/")

#Start app
if __name__ == "__main__":
    app.run(debug=True)
