import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime


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


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///users.db")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        print(name)
    if request.method == "GET":
        return render_template ("index.html")


@app.route("/resume")
def resume():
    return render_template ("resume.html")

@app.route("/awards")
def awards():
    return render_template ("awards.html")

@app.route("/leadership")
def leadership():
    return render_template ("leadership.html")

@app.route("/interests")
def compsci():
    return render_template ("compsci.html")

@app.route("/volunteering")
def volunteering():
    return render_template ("volunteering.html")

@app.route("/other")
def other():
    return render_template("other.html")

@app.route("/survey", methods=["GET", "POST"])
def survey():

    if request.method == "POST":
        fname = request.form.get("firstname")
        howknow = request.form.get("howknow")
        country = request.form.get("country")
        enjoy = request.form.get("enjoy")
        subject = request.form.get("subject")



        db.execute("INSERT INTO survey (fname, howknow, country, enjoy, subject) VALUES (:fname, :howknow, :country, :enjoy, :subject)", fname = fname, howknow = howknow, country = country, enjoy= enjoy, subject = subject)
        return redirect("/")



    if request.method == "GET":
        return render_template("survey.html")
@app.route("/psurvey")
def psurvey():
    return render_template("psurvey.html")