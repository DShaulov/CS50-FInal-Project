from flask import Flask, redirect, render_template, request, session
from cs50 import SQL
from flask_session import Session
from datetime import datetime
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import lookup
import random


app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["DEBUG"] = False

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///users.db")


definitions = []
word = ""

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "GET":
        line_count = 0
        with open("easy.txt", "r") as file:
            for line in file:
                line_count += 1

        with open("easy.txt", "r") as file:
            rand_line = random.randint(0, line_count)
            for line in enumerate(file):
                if line[0] == rand_line:
                    global word
                    word = line[1]


        word = word.replace("\n", "")
        letter_count = len(word)
        global definitions
        definitions = lookup(word)
        first_letter = word[0].upper()
        second_letter = word[1].upper()
        last_letter = word[len(word)-1].upper()
        return render_template("easy.html", definitions=definitions, letter_count=letter_count, word=word.capitalize(), first_letter=first_letter, last_letter=last_letter, second_letter=second_letter)

    if request.method == "POST":
        if session != {}:
            exists = db.execute("SELECT word FROM words WHERE word= :word", word=word)
            if exists == []:
                db.execute("INSERT INTO words (id, word, definitions, times) VALUES (:ids, :word, :definitions, :times)", ids=session["user_id"], word=word.capitalize(), definitions=definitions, times=1)

            else:
                previous_times = db.execute("SELECT times FROM words WHERE word=:word", word=word)
                print(previous_times)
                new_times = previous_times[0]["times"] + 1
                db.execute("UPDATE words SET times=:times WHERE word=:word", times=new_times, word=word)

            definitions = []
            word = ""
        return ("", 204)

@app.route("/medium", methods=["POST", "GET"])
def medium():
    if request.method == "GET":
        line_count = 0
        with open("medium.txt", "r") as file:
            for line in file:
                line_count += 1

        with open("medium.txt", "r") as file:
            rand_line = random.randint(0, line_count)
            for line in enumerate(file):
                if line[0] == rand_line:
                    global word
                    word = line[1]


        word = word.replace("\n", "")
        letter_count = len(word)
        global definitions
        definitions = lookup(word)
        first_letter = word[0].upper()
        second_letter = word[1].upper()
        last_letter = word[len(word)-1].upper()
        return render_template("medium.html", definitions=definitions, letter_count=letter_count, word=word.capitalize(), first_letter=first_letter, last_letter=last_letter, second_letter=second_letter)

    if request.method == "POST":
        if session != {}:
            exists = db.execute("SELECT word FROM words WHERE word= :word", word=word)
            if exists == []:
                db.execute("INSERT INTO words (id, word, definitions, times) VALUES (:ids, :word, :definitions, :times)", ids=session["user_id"], word=word.capitalize(), definitions=definitions, times=1)

            else:
                previous_times = db.execute("SELECT times FROM words WHERE word=:word", word=word)
                print(previous_times)
                new_times = previous_times[0]["times"] + 1
                db.execute("UPDATE words SET times=:times WHERE word=:word", times=new_times, word=word)

            definitions = []
            word = ""
        return ("", 204)


@app.route("/hard", methods=["POST", "GET"])
def hard():
    if request.method == "GET":
        line_count = 0
        with open("hard.txt", "r") as file:
            for line in file:
                line_count += 1

        with open("hard.txt", "r") as file:
            rand_line = random.randint(0, line_count)
            for line in enumerate(file):
                if line[0] == rand_line:
                    global word
                    word = line[1]


        word = word.replace("\n", "")
        letter_count = len(word)
        global definitions
        definitions = lookup(word)
        first_letter = word[0].upper()
        second_letter = word[1].upper()
        last_letter = word[len(word)-1].upper()
        second_letter = word[1].upper()
        return render_template("hard.html", definitions=definitions, letter_count=letter_count, word=word.capitalize(), first_letter=first_letter, last_letter=last_letter, second_letter=second_letter)

    if request.method == "POST":
        if session != {}:
            exists = db.execute("SELECT word FROM words WHERE word= :word", word=word)
            if exists == []:
                db.execute("INSERT INTO words (id, word, definitions, times) VALUES (:ids, :word, :definitions, :times)", ids=session["user_id"], word=word.capitalize(), definitions=definitions, times=1)

            else:
                previous_times = db.execute("SELECT times FROM words WHERE word=:word", word=word)
                print(previous_times)
                new_times = previous_times[0]["times"] + 1
                db.execute("UPDATE words SET times=:times WHERE word=:word", times=new_times, word=word)

            definitions = []
            word = ""
        return ("", 204)


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        ##########CHECK THAT USERNAME DOESNT ALREADY EXIST#########
        user_check = db.execute("SELECT * FROM users WHERE username= :username", username=request.form.get("username"))
        print(user_check)
        if user_check != []:
            exists = "*Username already exists"
            return render_template("register.html", exists=exists)

        #########GENERATE PASSWORD HASH###########################
        user_pass = request.form.get("password")
        hashed_pass = generate_password_hash(user_pass)
        username = request.form.get("username")
        ########ADD TO DATABASE##################
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hashed)", username=username, hashed=hashed_pass)

        return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        #########CHECK THAT USERNAME EXISTS############
        valid_check_name = db.execute("SELECT username FROM users WHERE username = :username", username = request.form.get("username"))
        print(valid_check_name)
        if valid_check_name == []:
            error = "*username or password are incorrect"
            return render_template("login.html", error=error)

        ########CHECK PASSWORD#########################
        db_hash = db.execute("SELECT hash FROM users WHERE username= :username", username= request.form.get("username"))
        if not check_password_hash(db_hash[0]["hash"], request.form.get("password")):
            error = "*username or password are incorrect"
            return render_template("login.html", error=error)

        ########LOG USER IN############################
        current_id = db.execute("SELECT id FROM users WHERE username = :username", username = request.form.get("username"))
        session["user_id"] = current_id[0]["id"]
        return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/history")
def history():
    print(session)
    if session == {}:
        return redirect("/login")

    history = db.execute("SELECT * FROM words WHERE id= :ids", ids=session["user_id"])
    print(history)
    return render_template("history.html", history=history)

