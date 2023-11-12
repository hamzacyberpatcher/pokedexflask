import requests
from cs50 import SQL
db = SQL("sqlite:///evolutions.db")

def internet_connection():
    try:
        response = requests.get("https://www.pokeapi.co", timeout=5)
        return True
    except requests.ConnectionError:
        return False 

def Pokemon(pokemon):

	if not internet_connection():
		return None
	pokemon = pokemon.lower()

	pokemon = pokemon.replace(" ","-")

	baseURL1 = "https://pokeapi.co/api/v2/pokemon-species/"

	baseURL2 = "https://pokeapi.co/api/v2/pokemon/"

	resp1 = requests.get(baseURL1 + pokemon)

	if resp1.status_code != 200:
		return None

	number = resp1.json()["id"]

	name = resp1.json()["name"]

	resp2 = requests.get(baseURL2 + str(number))

	if resp1.json()["evolves_from_species"] != None:
		evolves_from = resp1.json()["evolves_from_species"]["name"]
	else:
		evolves_from = "nothing"

	stats = resp2.json()["stats"]
	hp = int(stats[0]["base_stat"])
	atk = int(stats[1]["base_stat"])
	defense = int(stats[2]["base_stat"])
	spatk = int(stats[3]["base_stat"])
	spdef = int(stats[4]["base_stat"])
	speed = int(stats[5]["base_stat"])

	types_resp = resp2.json()["types"]

	types = []

	for type_resp in types_resp:
		typename = type_resp["type"]["name"]
		typename = typename.capitalize()
		types.append(typename)


	flavor_text_entries = resp1.json()["flavor_text_entries"]
	i = 0
	if len(flavor_text_entries) != 0:
		while True:
			if flavor_text_entries[i]["language"]["name"] == "en":
				description = flavor_text_entries[i]["flavor_text"]
				description = description.replace("\n\n"," ")
				description = description.replace("\n"," ")
				description = description.replace("\x0c"," ")
				description = description.replace("  "," ")
				break
			i = i + 1
	else:
		description = "Not Available"

	height = resp2.json()["height"]
	weight = resp2.json()["weight"]

	abilities_resp = resp2.json()["abilities"]

	abilities = []

	for ability_resp in abilities_resp:
		ability = {"name":[],"is_hidden":[],"desc":[]}
		url = ability_resp["ability"]["url"]
		ability_resps = requests.get(url)
		effect_entries = ability_resps.json()["effect_entries"]
		if len(effect_entries) !=0:
			for effect_entry in effect_entries:
				if effect_entry["language"]["name"] == "en":
					ability_desc = effect_entry["effect"]
					ability_desc = ability_desc.replace("\n"," ")
					ability_desc = ability_desc.replace("\n\n"," ")
					ability_desc = ability_desc.replace("\x0c"," ")
					ability_desc = ability_desc.replace("  "," ")
					break
		else:
			ability_desc = "Not available"
		ability["name"] = ability_resp["ability"]["name"]
		ability["is_hidden"] = ability_resp["is_hidden"]
		ability["desc"] = ability_desc
		abilities.append(ability)

	generation = resp1.json()["generation"]["name"]

	if resp1.json()["is_mythical"]:
		pokerank = "mythical"
	elif resp1.json()["is_legendary"]:
		pokerank = "legendary"
	elif resp1.json()["is_baby"]:
		pokerank = "baby"
	else:
		pokerank = "ordinary"

	evolves_into = db.execute("SELECT name FROM evolutions WHERE evolves_from = ?",name)
	evolvesInto = []
	for evolve_into in evolves_into:
		evolvesInto.append(evolve_into["name"])

	sprite = resp2.json()["sprites"]["other"]["official-artwork"]["front_default"]

	types = ', '.join(types)

	pokedata = {}
	pokedata["number"] = int(number)
	pokedata["name"] = name
	pokedata["rank"] = pokerank
	pokedata["generation"] = generation
	pokedata["evolves_from"] = evolves_from
	pokedata["evolves_into"] = evolvesInto
	pokedata["types"] = types
	pokedata["hp"] = int(hp)
	pokedata["atk"] = int(atk)
	pokedata["def"] = int(defense)
	pokedata["spatk"] = int(spatk)
	pokedata["spdef"] = int(spdef)
	pokedata["speed"] = int(speed)
	pokedata["desc"] = description
	pokedata["height"] = int(height)
	pokedata["weight"] = int(weight)
	pokedata["abilities"] = abilities
	pokedata["sprite"] = sprite
	pokedata["favicon"] = resp2.json()["sprites"]["front_default"]
	return pokedata

def listpokemon():
	pokelist = db.execute("SELECT name FROM evolutions")
	return pokelist

def name(value):
	value = value.capitalize()
	value = value.replace("-"," ")
	return value

def weight(value):
	value = value / 10
	return f"{value:,.1f}kg"

def height(value):
	value = value / 10
	f = value * 3.281
	return f"{f:.1f}ft"
