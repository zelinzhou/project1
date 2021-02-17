

import os

from flask import Flask, session, render_template,request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker








app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))







@app.route("/")
def index():
    return render_template("index.html")



@app.route("/login",methods=["POST"])
def login():
    username_temp = request.form.get("username")
    password_temp = request.form.get("password")



    #check if the user input the correct username or password
    if db.execute("SELECT * FROM user WHERE username = :username OR password =: password", {"username":username_temp},{"password": password_temp}).rowcount == 0:
        return render_template("error.html",message="wrong username or password")
    return render_template("success.html")


@app.route("/signup")
def signup():
    username=request.form.get("username")
    password=request.form.get("password")

    if db.execute("SELECT * FROM user WHERE username =: username",{"username":username_temp}).rowcount > 0:
        return render_template("error.html", message="Username already exists!")
    db.execute("INSERT INTO user (username, password) VALUES (:username, :password)"),{"username":username, "password":password}
    db.commit()
    return render_template("success.html")


@app.route("/search")
def search():
    bookname=request.form.get("bookname")
    b=db.execute("SELECT * FROM books WHERE title = :title",{"title": bookname})
    if db.execute("SELECT * FROM books WHERE title = :bookname",{"bookname":bookname}).rowcounnt > 0:
        return render_template("{{url_for('book',isbn=b.isbn)}}")
    return render_template("error.html")




@app.route("/search/<int:isbn>")
def book(isbn):

    book=db.execute("SELECT * FROM books WHERE isbn=:isbn",{"isbn": isbn})
    if book is None:
        return render_template("error.html")


    comment=db.execute("SELECT comment FROM reviews WHERE isbn= :isbn",{"isbn":isbn}).fetchall()
    rate=db.execute("SELECT rating FROM reviews WHERE isbn= :isbn",{"isbn":isbn}).fetchall()
    return render_template("book.html",comment=comment,rate=rate)
