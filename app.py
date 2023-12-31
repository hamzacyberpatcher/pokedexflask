from api import Pokemon,listpokemon
from flask import Flask, render_template, request, redirect
from filters import name,weight,height
import random


app = Flask(__name__)
app.jinja_env.filters["name"] = name
app.jinja_env.filters["weight"] = weight
app.jinja_env.filters["height"] = height

bgcolor = [
	'#F7CEE2',
	'springgreen'
	'lightblue',
	'lightyellow',
	'#CCCAF0',
	'#CFDFEF',
	'#FEFBBE',
	'#9AE49E',
	'#76CBF0',
	'#FF6969'
]

pokelist = listpokemon()
pokenamelength = len(pokelist)

@app.route("/")
def index():
	n = random.randint(0,len(bgcolor) - 1)
	return render_template("index.html",pokelist=pokelist,bgcolor=bgcolor[n], maxlength = pokenamelength)

@app.route("/search")
def search():
	pokemon = request.args.get("pokemon")
	pokedata = Pokemon(pokemon)
	n = random.randint(0,len(bgcolor) - 1)
	if pokedata == None:
		return render_template("failure.html",pokemon=pokemon,pokelist=pokelist,bgcolor=bgcolor[n], maxlength = pokenamelength)

	return render_template("pokemon.html",pokedata=pokedata,pokelist=pokelist,bgcolor=bgcolor[n],maxlength=pokenamelength)
