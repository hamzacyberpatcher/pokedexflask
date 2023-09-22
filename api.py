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

	total = hp + atk + defense + spatk + spdef + speed

	types_resp = resp2.json()["types"]

	types = []

	for type_resp in types_resp:
		types.append(type_resp["type"]["name"])


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

	# imported the library here because elsewise it showed stupid debug data
	evolves_into = db.execute("SELECT name FROM evolutions WHERE evolves_from = ?",name)
	evolvesInto = []
	for evolve_into in evolves_into:
		evolvesInto.append(evolve_into["name"])

	if len(evolvesInto) == 0:
		evolvesInto.append("None")

	sprite = resp2.json()["sprites"]["other"]["official-artwork"]["front_default"]

	pokedata = {}
	pokedata["number"] = number
	pokedata["name"] = name
	pokedata["rank"] = pokerank
	pokedata["generation"] = generation
	pokedata["evolves_from"] = evolves_from
	pokedata["evolves_into"] = evolves_into
	pokedata["types"] = types
	pokedata["hp"] = hp
	pokedata["atk"] = atk
	pokedata["def"] = defense
	pokedata["spatk"] = spatk
	pokedata["spdef"] = spdef
	pokedata["speed"] = speed
	pokedata["total"] = total
	pokedata["desc"] = description
	pokedata["height"] = height
	pokedata["weight"] = weight
	pokedata["abilities"] = abilities
	pokedata["sprite"] = sprite
	return pokedata

def listpokemon():
	pokelist = db.execute("SELECT name FROM evolutions")
	return pokelist