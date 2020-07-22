import os
import yagmail
import requests
import urllib.parse

from cs50 import SQL, eprint
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Login required
def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///mailing.db")


@app.route("/")
@login_required
def index():
    """Homepage"""

    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username exists and password is correct
        if not request.form.get("password"):
            return render_template("denied.html")
        if not check_password_hash(generate_password_hash("12345"), request.form.get("password")):
            return render_template("denied.html")
        else:
            session["user_id"] = 1

            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/compose", methods=["GET", "POST"])
@login_required
def compose():
    """Compose an email and send it"""
    if request.method == "POST":
        subject = request.form.get("subject")
        if subject == "":
            subject = "No Subject"
        content = request.form.get("hiddenEmail")
        db.execute("INSERT INTO history (subject, content) VALUES (:subject, :content)", subject=subject, content=content)
        yag = yagmail.SMTP("$EMAIL$", "$PASSWORD$")
        emailinfo = db.execute("SELECT email, hash FROM 'mailing-list'")
        for user in range(len(emailinfo)):
            email = content + "<p><i>Want off the mailing list? <a href=\"http://ide50-chamath-wijesekera.cs50.io:8080/unsubscribe?id=" + \
                emailinfo[user]["hash"] + "\">Unsubscribe Here</a></i></p>"
            yag.send(emailinfo[user]["email"], subject, email)
        return render_template("compose.html", vis="visible")
    else:
        return render_template("compose.html", vis="hidden")


@app.route("/mailing-list")
@login_required
def mailinglist():
    """Show list of users on the mailing list"""
    users = history = db.execute("SELECT * FROM 'mailing-list' ORDER BY name_last ASC")
    id = request.args.get('id')
    if id:
        db.execute("DELETE FROM 'mailing-list' WHERE id=:id", id=id)
        users = history = db.execute("SELECT * FROM 'mailing-list' ORDER BY name_last ASC")
    return render_template("mailing-list.html", users=users)


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Add a user to the mailing list"""

    if request.method == "POST":
        salutation = request.form.get("salutation")
        name_first = request.form.get("name_first")
        name_last = request.form.get("name_last")
        email = request.form.get("email")
        userhash = generate_password_hash(email)

        result = db.execute("INSERT INTO 'mailing-list' (salutation, name_first, name_last, email, hash) VALUES (:salutation, :name_first, :name_last, :email, :hash)",
                            salutation=salutation, name_first=name_first, name_last=name_last, email=email, hash=userhash)
        if not result:
            return render_template("add.html", vis="visible")
        return redirect("/mailing-list")
    else:
        return render_template("add.html", vis="hidden")


@app.route("/history")
@login_required
def history():
    """Show history of emails sent"""
    history = db.execute("SELECT * FROM history ORDER BY timestamp DESC")
    return render_template("history.html", histories=history)


@app.route("/view")
@login_required
def view():
    """View an email from history"""
    id = request.args.get('id')
    view = db.execute("SELECT content, subject FROM history WHERE id=:id", id=id)
    contentreal = view[0]["content"]
    subjectreal = view[0]["subject"]
    return render_template("view.html", view=contentreal, subject=subjectreal)


@app.route("/unsubscribe")
def unsubscribe():
    """Unsubscribe user based on hash"""
    hash = request.args.get('id')
    userinfo = db.execute("SELECT * FROM 'mailing-list' WHERE hash=:hash", hash=hash)
    db.execute("DELETE FROM 'mailing-list' WHERE hash=:hash", hash=hash)
    if userinfo[0]["salutation"] and userinfo[0]["name_first"] and userinfo[0]["name_last"]:
        farewell = "A hearty farewell to you, " + userinfo[0]["salutation"] + \
            " " + userinfo[0]["name_first"] + " " + userinfo[0]["name_last"] + "!"
    elif userinfo[0]["salutation"] and userinfo[0]["name_last"]:
        farewell = "I hope to talk with you again, " + userinfo[0]["salutation"] + " " + userinfo[0]["name_first"] + "!"
    else:
        farewell = "Goodbye, " + userinfo[0]["name_first"] + ", I'll miss you!"
    return render_template("unsubscribe.html", farewell=farewell)


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

