import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # 1. Get the current user's stock holdings (sum of shares purchased/sold)
    # Filter out holdings where shares sum up to 0 (i.e., the user sold all of it)
    holdings = db.execute(
        """
        SELECT symbol, SUM(shares) as total_shares
        FROM transactions
        WHERE user_id = ?
        GROUP BY symbol
        HAVING total_shares > 0;
        """,
        session["user_id"]
    )

    # Initialize a list to hold the final portfolio data and a variable for grand total value
    portfolio = []
    grand_total = 0

    # 2. Iterate over holdings to get current price and calculate value
    for row in holdings:
        symbol = row["symbol"]
        total_shares = row["total_shares"]

        # Use the lookup helper to get current price and name
        stock_info = lookup(symbol)

        if stock_info:
            current_price = stock_info["price"]
            stock_name = stock_info["name"]
            total_value = current_price * total_shares
            grand_total += total_value

            portfolio.append({
                "symbol": symbol,
                "name": stock_name,
                "shares": total_shares,
                "price": usd(current_price),
                "total": usd(total_value)
            })

    # 3. Retrieve user's current cash balance
    user_data = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    cash_balance = user_data[0]["cash"] if user_data else 0

    # 4. Calculate the total net worth (stocks + cash)
    grand_total += cash_balance

    # 5. Render the portfolio page
    return render_template(
        "index.html",
        portfolio=portfolio,
        cash=usd(cash_balance),
        grand_total=usd(grand_total)
    )

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        shares_input = request.form.get("shares")

        # 1. Input Validation: Symbol
        if not symbol:
            return apology("must provide stock symbol")

        # 2. Stock Lookup
        stock = lookup(symbol)
        if stock is None:
            return apology("invalid stock symbol")

        # 3. Input Validation: Shares
        shares_input = request.form.get("shares")

        if not shares_input or not shares_input.isdigit():
            return apology("shares must be a positive integer", 400)

        shares = int(shares_input)

        if shares <= 0:
            return apology("shares must be a positive integer", 400)

        # Get current price and calculate total cost
        price = stock["price"]
        total_cost = price * shares
        user_id = session["user_id"]

        # 4. Cash Check
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

        if user_cash < total_cost:
            return apology("can't afford that many shares")

        # 5. Execute Transaction (Atomic updates)

        # Update user's cash
        db.execute(
            "UPDATE users SET cash = cash - ? WHERE id = ?",
            total_cost,
            user_id
        )

        # Record the purchase in transactions table. Shares are positive.
        db.execute(
            """
            INSERT INTO transactions (user_id, symbol, shares, price, transacted_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            """,
            user_id,
            symbol,
            shares,
            price
        )

        # Confirmation
        flash(f"Bought {shares} share(s) of {stock['name']} ({symbol}) for {usd(total_cost)}!")
        return redirect("/")

    else: # User reached route via GET, render buy form
        return render_template("buy.html")



@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]

    # FIX: Removed the non-existent 'type' column from the SELECT statement.
    # We will derive the type (BUY/SELL) from the 'shares' column in the template.
    transactions = db.execute(
        "SELECT symbol, shares, price, transacted_at FROM transactions WHERE user_id = ? ORDER BY transacted_at DESC",
        user_id
    )

    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("Must provide stock symbol", 400)

        quote = lookup(symbol)

        if quote is None:
            return apology("Invalid stock symbol", 400)

        # ------------------------------------------------------------------
        # FIX: Convert the price value to a float before passing it to usd()
        # ------------------------------------------------------------------
        try:
            # Safely cast the price from the dictionary (which is a string) to a float
            price_float = float(quote["price"])
        except ValueError:
            # Handle unexpected data if the 'price' string cannot be converted
            return apology("Error parsing stock price data", 500)

        # Call the usd function with the corrected data type (float)
        quoted_price = usd(price_float)

        return render_template(
            "quoted.html",
            name=quote["name"],
            symbol=quote["symbol"],
            price=quoted_price
        )

    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # 1. Ensure username was submitted
        if not username:
            return apology("must provide username")

        # 2. Check if username already exists
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) > 0:
            return apology("username already exists")

        # 3. Ensure password was submitted
        if not password:
            return apology("must provide password")

        # 4. Ensure confirmation was submitted
        if not confirmation:
            return apology("must confirm password")

        # 5. Ensure password and confirmation match
        if password != confirmation:
            return apology("passwords do not match")

        # 6. Hash the password
        # Use werkzeug's generate_password_hash function
        hashed_password = generate_password_hash(password)

        # 7. Insert the new user into the database
        db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)",
            username,
            hashed_password
        )

        # Log the user in automatically after registration
        # Retrieve the newly created user's ID
        new_user = db.execute("SELECT id FROM users WHERE username = ?", username)
        session["user_id"] = new_user[0]["id"]

        # Flash a success message
        flash(f"Account for {username} registered and logged in!")

        # Redirect user to home page
        return redirect("/")

    else:
        # User reached route via GET, so render the registration form
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]

    # Retrieve all symbols the user currently owns (where total shares > 0)
    owned_symbols = db.execute(
        """
        SELECT symbol
        FROM transactions
        WHERE user_id = ?
        GROUP BY symbol
        HAVING SUM(shares) > 0;
        """,
        user_id
    )
    # Convert list of dicts to list of strings for easier use in template/logic
    symbols = [row["symbol"] for row in owned_symbols]

    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        shares_input = request.form.get("shares")

        # 1. Input Validation: Symbol
        if not symbol or symbol not in symbols:
            return apology("must select a valid stock to sell")

        # 2. Input Validation: Shares
        if not shares_input or not shares_input.isdigit():
            return apology("shares must be a positive integer", 400)

        shares_to_sell = int(shares_input)

        if shares_to_sell <= 0:
            return apology("shares must be a positive integer", 400)

        # 3. Check current ownership
        current_shares = db.execute(
            "SELECT SUM(shares) as total_shares FROM transactions WHERE user_id = ? AND symbol = ?",
            user_id,
            symbol
        )[0]["total_shares"]

        if shares_to_sell > current_shares:
            return apology("you do not own that many shares")

        # 4. Get current stock price
        stock = lookup(symbol)
        if stock is None:
             # Should not happen if validation passed, but good to check
            return apology("stock lookup failed")

        price = stock["price"]
        revenue = price * shares_to_sell

        # 5. Execute Transaction (Atomic updates)

        # Update user's cash (cash increases)
        db.execute(
            "UPDATE users SET cash = cash + ? WHERE id = ?",
            revenue,
            user_id
        )

        # Record the sale in transactions table. Shares are negative for a sale.
        db.execute(
            """
            INSERT INTO transactions (user_id, symbol, shares, price, transacted_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            """,
            user_id,
            symbol,
            -shares_to_sell, # Keep the negative shares value for selling
            price
        )

        # Confirmation
        flash(f"Sold {shares_to_sell} share(s) of {symbol} for {usd(revenue)}!")
        return redirect("/")

    else:
        # User reached route via GET, render sell form with dropdown of owned stocks
        return render_template("sell.html", symbols=symbols)

@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    """Allow user to add additional cash to their account."""
    if request.method == "POST":
        amount_input = request.form.get("amount")

        # 1. Validation
        if not amount_input:
            return apology("Must provide an amount to add", 400)

        try:
            amount = float(amount_input)
            # Cash amount must be positive
            if amount <= 0:
                return apology("Amount must be a positive value", 400)
        except ValueError:
            return apology("Invalid amount format", 400)

        user_id = session["user_id"]

        # 2. Database Update
        # Add the amount to the user's cash balance
        db.execute(
            "UPDATE users SET cash = cash + ? WHERE id = ?",
            amount,
            user_id
        )

        # 3. Confirmation and Redirect
        flash(f"Successfully added {usd(amount)} to your account!")
        return redirect("/")

    else:
        # User reached route via GET, display the form
        return render_template("cash.html")

@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """Allow user to change their password."""
    if request.method == "POST":
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirmation = request.form.get("confirmation")
        user_id = session["user_id"]

        # 1. Basic Validation
        if not current_password or not new_password or not confirmation:
            return apology("Must fill all fields", 400)

        if new_password != confirmation:
            return apology("New passwords do not match", 400)

        # 2. Check Current Password
        # Retrieve the user's hash from the database
        user = db.execute("SELECT hash FROM users WHERE id = ?", user_id)
        if not user:
             # Should not happen if @login_required works, but good practice
            return apology("User not found", 403)

        # Check if the submitted current password matches the stored hash
        if not check_password_hash(user[0]["hash"], current_password):
            return apology("Incorrect current password", 403)

        # 3. Hash New Password
        new_hash = generate_password_hash(new_password)

        # 4. Update Database
        db.execute(
            "UPDATE users SET hash = ? WHERE id = ?",
            new_hash,
            user_id
        )

        # 5. Success
        flash("Password successfully changed!")
        return redirect("/")

    else:
        # User reached route via GET, display the form
        return render_template("change_password.html")

@app.route("/manage_cash", methods=["GET", "POST"])
@login_required
def manage_cash():
    """Allows user to view cash balance and withdraw funds."""
    user_id = session["user_id"]

    # Retrieve user's current cash balance
    user_data = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    current_cash = user_data[0]["cash"] if user_data else 0

    if request.method == "POST":
        withdrawal_input = request.form.get("withdrawal_amount")

        # 1. Validation
        if not withdrawal_input:
            return apology("Must provide an amount to withdraw", 400)

        try:
            withdrawal_amount = float(withdrawal_input)
            # Withdrawal must be positive
            if withdrawal_amount <= 0:
                return apology("Withdrawal amount must be a positive value", 400)
        except ValueError:
            return apology("Invalid amount format", 400)

        # 2. Check Sufficient Funds
        if withdrawal_amount > current_cash:
            return apology(f"Insufficient funds. Your balance is {usd(current_cash)}", 403)

        # 3. Database Update
        # Deduct the amount from the user's cash balance
        db.execute(
            "UPDATE users SET cash = cash - ? WHERE id = ?",
            withdrawal_amount,
            user_id
        )

        # 4. Confirmation and Redirect
        flash(f"Successfully withdrew {usd(withdrawal_amount)}. New balance: {usd(current_cash - withdrawal_amount)}.")
        return redirect("/")

    else:
        # User reached route via GET, display the form and current cash
        return render_template("manage_cash.html", current_cash=usd(current_cash))

@app.route("/delete_account", methods=["GET", "POST"])
@login_required
def delete_account():
    """Allows user to permanently delete their account."""
    user_id = session["user_id"]

    if request.method == "POST":
        # 1. Get Password for Confirmation
        password = request.form.get("password")
        if not password:
            return apology("Must provide password for confirmation", 400)

        # 2. Check Password
        user = db.execute("SELECT hash FROM users WHERE id = ?", user_id)
        if not user or not check_password_hash(user[0]["hash"], password):
            return apology("Invalid password", 403)

        # 3. Database Deletion (Crucial Step!)
        # Delete user's transactions first (FK constraint safety)
        db.execute("DELETE FROM transactions WHERE user_id = ?", user_id)

        # Delete the user record itself
        db.execute("DELETE FROM users WHERE id = ?", user_id)

        # 4. Cleanup and Redirect
        session.clear()
        flash("Your account has been permanently deleted.")
        # Redirect to the login page
        return redirect("/login")

    else:
        # User reached route via GET, display the confirmation form
        return render_template("delete_account.html")
