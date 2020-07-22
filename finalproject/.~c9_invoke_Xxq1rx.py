import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
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


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # Retrieve user stock symbols from portfolio
    symbols = db.execute("SELECT quantity, symbol FROM portfolio WHERE id=:id", id=session["user_id"])
    grand_total = 0
    # Update symbol prices
    for symbolea in symbols:
        symbol = symbolea["symbol"]
        quantity = symbolea["quantity"]
        stock = lookup(symbol)
        total = quantity * stock["price"]
        grand_total += total
        db.execute("UPDATE portfolio SET priceea=:priceea, total=:total WHERE id=:id AND symbol=:symbol",
                   priceea=usd(stock["price"]), total=usd(total), id=session["user_id"], symbol=symbol)

    # Update user cash and total cash
    cash = db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])
    grand_total += cash[0]["cash"]

    # Set portfolio to index page
    portfolio = db.execute("SELECT * FROM portfolio WHERE id=:id", id=session["user_id"])

    return render_template("index.html", portfolio=portfolio, avail_cash=cash[0]["cash"], grand_total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    if request.method == "POST":
        # ensure proper symbol
        stock = lookup(request.form.get("symbol"))
        if not stock:
            return apology("Invalid Symbol")

        # ensure proper number of shares
        try:
            quantity = int(request.form.get("shares"))
            if quantity < 0:
                return apology("Please enter a valid quantity")
        except:
            return apology("Please enter a valid quantity")

        # select user's cash
        money = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])

        # check if enough money to buy
        if not money or float(money[0]["cash"]) < stock["price"] * quantity:
            return apology("Not enough money")

        # update history
        db.execute("INSERT INTO history (id, symbol, quantity, priceea) VALUES(:id, :symbol, :quantity, :priceea)", id=session["user_id"],
                   symbol=stock["symbol"], quantity=quantity, priceea=stock["price"])

        # update user cash
        db.execute("UPDATE users SET cash = cash - :total_price WHERE id = :id",
                   id=session["user_id"], total_price=stock["price"] * float(quantity))

        # Select user shares of that symbol
        user_shares = db.execute("SELECT quantity FROM portfolio WHERE id = :id AND symbol=:symbol",
                                 id=session["user_id"], symbol=stock["symbol"])

        # if user doesn't has shares of that symbol, create new stock object
        if not user_shares:
            db.execute("INSERT INTO portfolio (id, symbol, name, quantity, priceea, total) VALUES(:id, :symbol, :name, :quantity, :priceea, :total)",
                       id=session["user_id"],  symbol=stock["symbol"], name=stock["name"], quantity=quantity, priceea=stock["price"], total=quantity * stock["price"])

        # Else increment the shares count
        else:
            quantity_total = user_shares[0]["quantity"] + quantity
            db.execute("UPDATE portfolio SET quantity=:quantity WHERE id=:id AND symbol=:symbol",
                       quantity=quantity_total, id=session["user_id"], symbol=stock["symbol"])

        # return to index
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Update history
    histories = db.execute("SELECT * FROM history WHERE id=:id", id=session["user_id"])

    return render_template("history.html", histories=histories)


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

        # Get stock information
        quote = lookup(request.form.get("symbol"))

        # Check if stock valid
        if quote == None:
            return apology("Invalid stock symbol")

        return render_template("quoted.html", stock=quote)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        # Check for username
        if not request.form.get("username"):
            return apology("Please provide a username")

        # Check for password
        elif not request.form.get("password"):
            return apology("Please provide a password")

        # Check for password match
        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("Passwords must match")

        # Put user into database with hashed password
        passhash = generate_password_hash(request.form.get("password"))
        result = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                            username=request.form.get("username"), hash=passhash)

        # Check if username valid
        if not result:
            return apology("Username taken")

        # Create session and redirect
        session["user_id"] = result
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        # Check for valid symbol
        stock = lookup(request.form.get("symbol"))
        if not stock:
            return apology("Invalid symbol")

        # Check for valid quantity
        try:
            quantity = int(request.form.get("shares"))

        except:
            return apology("Invalid quantity")

        if quantity < 0:
            return apology("Invalid quantity")

        # Retrieve share symbols from user
        symbols = db.execute("SELECT quantity FROM portfolio WHERE id=:id AND symbol=:symbol", id=session["user_id"],
                             symbol=stock["symbol"])

        # Check if there are enough shares to sell
        if not symbols:
            return apology("You don't have any of these shares")
        elif int(symbols[0]["quantity"]) < quantity:
            return apology("Insufficient shares")

        # Update cash
        db.execute("UPDATE users SET cash = cash + :sold WHERE id=:id", sold=stock["price"] * int(quantity), id=session["user_id"])

        # Update history
        db.execute("INSERT INTO history (id, symbol, quantity, priceea) VALUES (:id, :symbol, :quantity, :priceea)",
                   id=session["user_id"], symbol=stock["symbol"],  quantity=-quantity, priceea=stock["price"])

        # Update shares
        total_shares = symbols[0]["quantity"] - quantity
        if total_shares == 0:
            db.execute("DELETE FROM portfolio WHERE id=:id AND symbol=:symbol", id=session["user_id"], symbol=stock["symbol"])

        else:
            db.execute("UPDATE portfolio SET quantity=:total_shares WHERE id=:id AND symbol=:symbol",
                       total_shares=total_shares, id=session["user_id"], symbol=stock["symbol"])
        # Redirect
        return redirect("/")

    else:
        # Populate list of stocks in portfolio
        portfolio_stocks = db.execute("SELECT symbol FROM portfolio WHERE id=:id", id=session["user_id"])

        return render_template("sell.html", portfolio_stocks=portfolio_stocks)




# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
