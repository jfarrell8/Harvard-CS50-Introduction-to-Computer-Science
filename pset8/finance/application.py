import os
import datetime

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

#export API_KEY=pk_f5251c99facd4fe397f69b6091bdf1c3

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

    cash_total = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
    cash = usd(cash_total[0]["cash"])
    rows = db.execute("SELECT symbol, name, shares, price, total_value FROM portfolio WHERE id = :id", id=session["user_id"])
    stock_total = db.execute("SELECT SUM(total_value) FROM portfolio WHERE id = :id", id=session["user_id"])

    if stock_total[0]["SUM(total_value)"] is None:
        portfolio_total = usd(cash_total[0]["cash"])
    else:
        portfolio_total = usd(stock_total[0]["SUM(total_value)"] + cash_total[0]["cash"])

    return render_template("index.html", cash=cash, rows=rows, portfolio_total=portfolio_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))
        shares_to_buy = int(request.form.get("shares"))

        if not request.form.get("symbol"):
            return apology("Please enter a symbol")

        elif quote is None:
            return apology("Invalid symbol")

        elif shares_to_buy < 1:
            return apology("Enter positive # of shares")

        name = quote["name"]
        price = float("{0:.2f}".format(quote["price"]))
        symbol = quote["symbol"]

        #create list of symbols from key:value pairs in symbol_list_dict
        symbol_list_dict = db.execute("SELECT symbol FROM portfolio WHERE id = :id", id=session["user_id"])
        symbol_list =[d['symbol'] for d in symbol_list_dict]


        #determine cash from user with a given id
        cash_list = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
        cash = float(cash_list[0]['cash'])

        if cash > shares_to_buy * price:

            #check if the user already owns stock of this symbol: update their shares if they do, add to the portfolio if they don't
            if symbol in symbol_list:

                #calculate existing shares of a stock
                shares_list = db.execute("SELECT shares FROM portfolio WHERE symbol = :symbol AND id = :id", symbol=symbol, id=session["user_id"])
                shares = int(shares_list[0]['shares'])
                updated_shares = shares + shares_to_buy
                db.execute("UPDATE portfolio SET shares = :updated_shares, total_value = :total_value WHERE symbol = :symbol AND id = :id", updated_shares=updated_shares, total_value=updated_shares*price, symbol=symbol, id=session["user_id"])

            else:
                db.execute("INSERT INTO portfolio (id, name, symbol, price, shares, total_value) VALUES(:id, :name, :symbol, :price, :shares, :total_value)", id=session["user_id"], name=name, symbol=symbol, price=price, shares=shares_to_buy, total_value=shares_to_buy*price)

            #update cash
            db.execute("UPDATE users SET cash = :new_cash WHERE id = :id", id=session["user_id"], new_cash=cash - shares_to_buy*price)

            #update history with transaction
            transacted = datetime.datetime.now()
            db.execute("INSERT INTO history (id, symbol, shares, price, transacted) VALUES(:id, :symbol, :shares, :price, :transacted)", id=session["user_id"], symbol=symbol, shares=shares_to_buy, price=price, transacted=transacted)

            return redirect("/")

        else:
            return apology("You don't have enough cash for this stock purchase.")

    else:
        return render_template("buy.html")

@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    #need to use request.args.get for "GET" requests
    username = request.args.get("username")
    usernames = db.execute("SELECT username FROM users")
    if len(username) >= 1:
        if username in usernames:
            return jsonify(True)
    else:
        return jsonify(False)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    rows = db.execute("SELECT symbol, shares, price, transacted FROM history WHERE id = :id", id=session["user_id"])
    return render_template("history.html", rows=rows)


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

        quote = lookup(request.form.get("symbol"))

        if not request.form.get("symbol"):
            return apology("Please enter a symbol")

        elif quote is None:
            return apology("Invalid symbol")

        name = quote["name"]
        price = usd(quote["price"])
        symbol = quote["symbol"]

        return render_template("quoted.html", name=name, symbol=symbol, price=price)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        elif not request.form.get("confirmation"):
            return apology("must provide confirmation")

        if request.form.get("password") != request.form.get("confirmation"):
            return apology("password and confirmation must match")

        hash = generate_password_hash(request.form.get("password"))
        result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username=request.form.get("username"), hash=hash)
        if not result:
            return apology("You are already registered. Please login.")

        # Remember which user has logged in
        session["user_id"] = result

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":

        #make sure they enter a stock from the selector menu
        if not request.form.get("symbol"):
            return apology("Please select a symbol.")

        #lookup the quote of the stock they select and rip out information from IEX
        quote = lookup(request.form.get("symbol"))
        name = quote["name"]
        price = float("{0:.2f}".format(quote["price"]))
        symbol = quote["symbol"]

        #obtain shares from form, and available shares from 'portfolio' table
        shares_to_sell = int(request.form.get("shares"))
        shares_available_list = db.execute("SELECT shares FROM portfolio WHERE symbol = :symbol AND id = :id", symbol=symbol, id=session["user_id"])
        shares_available = int(shares_available_list[0]['shares'])

        #check ability to sell
        if shares_to_sell > shares_available:
            return apology("You don't have enough shares of that stock to sell.")

        #if shares to sell and available are the same, delete the entire stock record from the table
        elif shares_to_sell == shares_available:
            db.execute("DELETE FROM portfolio WHERE symbol = :symbol AND id = :id", symbol=symbol, id=session["user_id"])

        #else, if shares to sell is less than available, update the table to change the number of shares (don't delete from table)
        else:
            updated_shares = shares_available - shares_to_sell
            db.execute("UPDATE portfolio SET shares = :updated_shares, total_value = :total_value WHERE symbol = :symbol AND id = :id", updated_shares=updated_shares, total_value=updated_shares*price, symbol=symbol, id=session["user_id"])

        #update cash
        cash_list = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
        cash = float(cash_list[0]['cash'])
        db.execute("UPDATE users SET cash = :new_cash WHERE id = :id", id=session["user_id"], new_cash=cash + shares_to_sell*price)

        #update history table
        transacted = datetime.datetime.now()
        db.execute("INSERT INTO history (id, symbol, shares, price, transacted) VALUES(:id, :symbol, :shares, :price, :transacted)", id=session["user_id"], symbol=symbol, shares=shares_to_sell, price=price, transacted=transacted)

        return redirect("/")

    else:
        rows = db.execute("SELECT symbol FROM portfolio WHERE id = :id", id=session["user_id"])
        return render_template("sell.html", rows=rows)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
