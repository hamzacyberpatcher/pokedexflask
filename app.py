from api import Pokemon
from flask import Flask, render_template
from cs50 import SQL

db = SQL("sqlite:///evolutions.db")
pokelist = db.execute("SELECT name FROM evolutions")

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html",pokelist=pokelist)