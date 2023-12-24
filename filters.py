def name(value):
	value = value.title()
	value = value.replace("-"," ")
	return value

def weight(value):
	value = value / 10
	return f"{value:,.1f}kg"

def height(value):
	value = value / 10
	f = value * 3.281
	return f"{f:.1f}ft"
