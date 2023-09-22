from api import Pokemon,listpokemon
from flask import Flask, render_template, request, redirect
from cs50 import SQL

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html",pokelist=listpokemon())

@app.route("/search")
def search():
	pokemon = request.args.get("pokemon")
	pokedata = Pokemon(pokemon)
	if pokedata == None:
		return render_template("failure.html")