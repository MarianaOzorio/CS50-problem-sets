import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    transactions = db.execute("SELECT symbol, SUM(shares) as total_shares FROM buy WHERE users_id = :user GROUP BY symbol HAVING total_shares > 0", user=session["user_id"])
    portfolio = []
    Grand_total = 0

    for transaction in transactions:
        stock = lookup(transaction["symbol"])
        portfolio.append({
            "symbol": stock["symbol"],
            "name": stock["name"],
            "shares": transaction["total_shares"],
            "price": usd(stock["price"]),
            "TOTAL": usd(stock["price"] * transaction["total_shares"])
        })

        Grand_total += stock["price"] * transaction["total_shares"]

    cash = db.execute("SELECT cash FROM users WHERE id = :user", user=session["user_id"])
    Total_cash = cash[0]["cash"]
    Grand_total += Total_cash

    return render_template("index.html", portfolio=portfolio, Total_cash=usd(Total_cash), Grand_total=usd(Grand_total))

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Add additional cash"""

    current_cash = db.execute("SELECT cash FROM users WHERE id = :user", user=session["user_id"])
    cash = current_cash[0]["cash"]

    if request.method == "POST":

        if not request.form.get("cash"):
            return apology("missing cash", 403)

        db.execute("UPDATE users SET cash = cash + :cash WHERE id = :user", cash=request.form.get("cash"), user=session["user_id"])

        flash("Success!")
        return redirect("/")

    else:
        return render_template("add.html", cash=usd(cash))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("must provide a valid symbol", 403)

        quote = lookup(request.form.get("symbol"))

        if quote == None:
            return apology("Invalid symbol", 403)

        if int(request.form.get("shares")) < 1:
            return apology("missing shares", 403)

        price = quote["price"] * float(request.form.get("shares"))
        user = session["user_id"]
        cash = db.execute("SELECT cash FROM users WHERE id = :user", user=user)

        if cash[0]["cash"] < price:
            return apology("you don't have enough cash", 403)

        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        db.execute("INSERT INTO buy (users_id, symbol, shares, price) VALUES (:users_id ,:symbol, :shares, :price)", users_id=user, symbol=symbol, shares=shares, price=price)
        db.execute("INSERT INTO history (users_id, symbol, shares, price) VALUES (:users_id ,:symbol, :shares, :price)", users_id=user, symbol=symbol, shares=shares, price=price)

        new_cash = cash[0]["cash"] - price
        db.execute("UPDATE users SET cash = :cash WHERE id = :user", cash=new_cash, user=user)

        flash("Success!")
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    transactions = db.execute("SELECT * FROM history WHERE users_id = :user", user=session["user_id"])
    history = []

    for transaction in transactions:
        history.append({
            "symbol": transaction["symbol"],
            "shares": transaction["shares"],
            "price": usd(transaction["price"]),
            "transacted": transaction["transacted"]
        })

    return render_template("history.html", history=history)


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
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
    """Get stock quote."""

    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("must provide a valid symbol", 403)

        quote = lookup(request.form.get("symbol"))

        if quote == None:
            return apology("Invalid symbol", 403)
        return render_template("quoted.html", name=quote["name"], symbol=quote["symbol"], price=usd(quote["price"]))

    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must provide username", 403)

        elif not request.form.get("password"):
            return apology("must provide password", 403)

        elif not request.form.get("confirmation") or request.form.get("confirmation") != request.form.get("password"):
            return apology("must provide the same password", 403)

        username = request.form.get("username")
        password = generate_password_hash(request.form.get("password"))

        try:
            name = db.execute("INSERT INTO users (username, hash) VALUES (:username, :password)", username=username, password=password)

        except:
            return apology("username already exist", 403)

        session["user_id"] = name

        flash("Success!")
        return redirect("/")

    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    stocks = db.execute("SELECT symbol, SUM(shares) FROM buy WHERE users_id = :user GROUP BY symbol HAVING SUM(shares) > 0", user=session["user_id"])
    companies = []
    for stock in stocks:
        stock = lookup(stock["symbol"])
        companies.append({"symbol": stock["symbol"]})

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))

        if not symbol or symbol == None:
            return apology("please select a stock", 403)

        for stock in stocks:
            if shares < 1 or shares > stock["SUM(shares)"]:
                return apology("invalid number of shares", 403)

        stock = lookup(symbol)
        price = stock["price"]

        db.execute("INSERT INTO history (users_id, symbol, shares, price) VALUES (:users_id, :symbol, :shares, :price)", users_id=session["user_id"], symbol=symbol, shares=-shares, price=price)

        cash = db.execute("SELECT cash FROM users WHERE id = :user", user=session["user_id"])
        current_cash = cash[0]["cash"]
        new_cash = current_cash + (price * shares)
        db.execute("UPDATE users SET cash = :cash WHERE id = :user", cash=new_cash, user=session["user_id"])

        db.execute("INSERT INTO buy (users_id, symbol, shares, price) VALUES (:users_id, :symbol, :shares, :price)", users_id=session["user_id"], symbol=symbol, shares=-1 * shares, price=price)

        flash("Success!")
        return redirect("/")

    else:
        return render_template("sell.html", companies=companies)

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
