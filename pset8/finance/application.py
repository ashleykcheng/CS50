import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
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

all_shares = []

@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    portfolio_symbols = db.execute("SELECT shares, symbol FROM transactions WHERE user_id = :id", id=session["user_id"])

    total_cash = 0

    for transaction_symbol in portfolio_symbols:
        symbol = transaction_symbol["symbol"]
        shares = transaction_symbol["shares"]
        stock = lookup(symbol)
        total = shares * stock["price"]
        total_cash += total
        name = stock["name"]
        db.execute("UPDATE transactions SET price=:price, total=:total WHERE user_id=:id AND symbol=:symbol", price=usd(stock["price"]), total=usd(total), id=session["user_id"], symbol=symbol)

    # update user's cash in portfolio
    updated_cash = db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])

    # update total cash -> cash + shares worth
    total_cash += updated_cash[0]["cash"]

    # print portfolio in index homepage
    updated_portfolio = db.execute("SELECT * from transactions WHERE user_id=:id", id=session["user_id"])

    return render_template("index.html", stocks=updated_portfolio, cash=usd(updated_cash[0]["cash"]), total= usd(total_cash) )

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))
        if quote == None:
            return apology("wrong symbol", 404)
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("shares must be a positive integer", 404)
        if shares <= 0:
            return apology("input correct number of shares", 404)

        rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])

        remaining_cash = rows[0]["cash"]
        share_price = quote["price"]
        name = (quote["name"])
        total = share_price * shares

        low_sym = request.form.get("symbol")
        upp_sym = low_sym.upper()

        now = datetime.now()
        current_time = now.strftime("%d/%m/%Y %H:%M:%S")

        if total > remaining_cash:
            return apology("not enough funds", 404)

        db.execute("UPDATE users SET cash = cash - :price WHERE id = :user_id", price=total, user_id=session["user_id"])

        user_shares = db.execute("SELECT shares FROM transactions WHERE user_id = :user_id AND symbol = :symbol", user_id=session["user_id"], symbol=upp_sym)

        db.execute("INSERT INTO history (symbol, shares, price, transacted, id) VALUES (:symbol, :shares, :price, :time, :id)", symbol = upp_sym, shares =shares, price = total, time = current_time, id = session["user_id"])


        if not user_shares:
            db.execute("INSERT INTO transactions (user_id, symbol, shares, price, total, name) VALUES(?, ?, ?, ?, ?, ?)",
             session["user_id"], upp_sym, shares, share_price, total, name);
        else:
            total_shares = user_shares[0]["shares"] + shares
            db.execute("UPDATE transactions SET shares = :shares WHERE user_id =:id AND symbol=:symbol", shares=total_shares, id = session["user_id"], symbol = upp_sym)

        return redirect("/")



@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    history = db.execute("SELECT * from history WHERE id=:id", id=session["user_id"])

    return render_template("history.html", histories = history)


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
    if request.method == "GET":
        return render_template("quote.html")
    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))
        if quote == None:
            return apology("wrong symbol", 403)

        return render_template("quoted.html", quote = quote)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        if not username:
            return apology("must provide username", 403)
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not password:
            return apology("must provide passowrd", 403)
        #elif not request.form.get("password") == request.form.get(confirmation):
            #return apology("passwords do not match", 403)
        hash = generate_password_hash(request.form.get("password"))
        new_user_id = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username = username, hash= hash)

        if not new_user_id:
            return apology("the username is taken", 403)

        session["user_id"] = new_user_id

    return redirect("/")




@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "GET":
        return render_template("sell.html")

    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))
        if quote == None:
            return apology("wrong symbol", 404)
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("shares must be a positive integer", 404)
        if shares <= 0:
            return apology("input correct number of shares", 404)

        rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])

        remaining_cash = rows[0]["cash"]
        share_price = quote["price"]
        name = (quote["name"])
        total = share_price * shares

        low_sym = request.form.get("symbol")
        upp_sym = low_sym.upper()


        db.execute("UPDATE users SET cash = cash + :price WHERE id = :user_id", price=total, user_id=session["user_id"])

        user_shares = db.execute("SELECT shares FROM transactions WHERE user_id = :user_id AND symbol = :symbol", user_id=session["user_id"], symbol=upp_sym)

        if not user_shares:
            return apology("do not own this stock")
        else:
            total_shares = user_shares[0]["shares"] - shares
            db.execute("UPDATE transactions SET shares = :shares WHERE user_id =:id AND symbol=:symbol", shares=total_shares, id = session["user_id"], symbol = upp_sym)

        if total_shares == 0:
            db.execute("DELETE FROM transactions WHERE user_id =:id AND shares = 0", id = session["user_id"])
        now = datetime.now()
        current_time = now.strftime("%d/%m/%Y %H:%M:%S")
        db.execute("INSERT INTO history (symbol, shares, price, transacted, id) VALUES (:symbol, :shares, :price, :time, :id)", symbol = upp_sym, shares =-shares, price = total, time = current_time, id = session["user_id"])



        return redirect("/")


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():

    if request.method =="POST":
        if not request.form.get("current_password"):
            return apology("must provide current password", 403)


        rows = db.execute("SELECT hash FROM users WHERE id = :user_id", user_id=session["user_id"])


        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("current_password")):
            return apology("invalid password", 403)


        if not request.form.get("new_password"):
            return apology("must provide new password", 403)


        if not request.form.get("new_password_confirmation"):
            return apology("must provide new password confirmation", 403)


        if request.form.get("new_password") != request.form.get("new_password_confirmation"):
            return apology("new password and confirmation must match", 403)


        hash = generate_password_hash(request.form.get("new_password"))
        rows = db.execute("UPDATE users SET hash = :hash WHERE id = :user_id", user_id=session["user_id"], hash=hash)
        return redirect("/")

    if request.method == "GET":
        return render_template("change_password.html")



def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
