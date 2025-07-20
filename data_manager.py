import json
from pathlib import Path
from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.styles import Style

DEFAULT_SAVE_PATH = "data.json"
DEFAULT_STYLE = {
	"wrong_word": "#54411a",
	"right_place": "#98f98b",
	"wrong_place": "#f9f88b",
	"error": "#fc4737",
	"win": "#5cf990",
	"lose": "#f9645c"
}

data: dict = {}

def setup_data() -> dict:
	if data_exists():
		with open(DEFAULT_SAVE_PATH, 'r') as file:
			global data
			data = json.loads(file.read())
			return data
	else:
		with open(DEFAULT_SAVE_PATH, 'w') as file:
			data = get_default_dictionary()
			file.write(json.dumps(data, indent="\t"))
			return data

def save_data():
	with open(DEFAULT_SAVE_PATH, 'w') as file:
		file.write(json.dumps(data, indent="\t"))

def data_exists() -> bool:
	return Path(DEFAULT_SAVE_PATH).exists()

def get_default_dictionary() -> dict:
	return {
		"tries": 5,
		"style": DEFAULT_STYLE
	}

def get_default_style() -> Style:
	return Style.from_dict(DEFAULT_STYLE)

def is_data_correct(dictionary: dict, reference: dict = get_default_dictionary()) -> bool:
	for i in reference:
		if i in dictionary.keys():
			types = (type(reference.get(i)), type(dictionary.get(i)))
			if types[0] == types[1]:
				if types[0] == dict:
					if is_data_correct(dictionary.get(i, {}), reference.get(i, {})):
						continue
				else:
					continue
			else:
				raise TypeError(f"type of key \"{i}\" is not correct.\nexpected \"{types[0].__name__}\", got \"{types[1].__name__}\".")
		else:
			raise TypeError(f"key \"{i}\" is missing.")
		return False
	return True

def get_style() -> dict:
	return Style.from_dict(data.get("style", DEFAULT_STYLE))