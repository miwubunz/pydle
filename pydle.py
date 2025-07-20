import argparse
from pathlib import Path
import wordlist_parser
import random
from prompt_toolkit import prompt, print_formatted_text, HTML
import data_manager
import sys

parser = argparse.ArgumentParser(prog="pydle")
parser.add_argument("path", help="path for the \".wordlist\" file to load.")

data: dict[str, str] = vars(parser.parse_args())
wordlist = []

game_data: dict = {}

def plural_or_singular(amount: int, forms: list) -> str:
	return forms[0] if ((amount <= 1) and (amount > 0)) else forms[1]

def start_game():
	data_manager.setup_data()
	if not data_manager.data_exists():
		data_manager.save_data(data_manager.get_default_dictionary())
	if data_manager.is_data_correct(data_manager.data):
		if len(wordlist) > 0:
			random_index = random.randint(0, len(wordlist) - 1)
			random_word = wordlist[random_index]
			tries = data_manager.data.get("tries", 5)
			game_data["word"] = random_word
			game_data["current_try"] = 0
			game_data["max_tries"] = tries if tries > 0 else 5
			if tries <= 0:
				print_formatted_text(HTML(f"<error>tries is less than/equals to 0.\nusing default value (5).\n</error>"), style=data_manager.get_style())
				data_manager.data["tries"] = 5
				data_manager.save_data()
			print_formatted_text(HTML(f"the length of the word is <b><i>{len(random_word)} characters.</i></b>\nyou have {game_data['max_tries']} {plural_or_singular(tries, ("try", "tries"))}.\n<b>-- PYDLE --</b>\n"))
			input_guess()

def show_result(user_word: str):
	string_to_display = ""
	game_word: str = game_data.get("word", "")
	word_array = list(game_word)

	index = 0

	for i in user_word:
		if i == game_word[index]:
			string_to_display += f"<right_place>{i}</right_place>"
		elif i in word_array:
			string_to_display += f"<wrong_place>{i}</wrong_place>"
			word_array.remove(i)
		else:
			string_to_display += f"<wrong_word>{i}</wrong_word>"
		index += 1
	
	print_formatted_text(HTML(string_to_display), style=data_manager.get_style())

def input_guess():
	user_input = prompt("guess: ")
	sys.stdout.write("\033[K")
	user_word = user_input.strip().upper()
	game_word = game_data.get("word", "")
	current_try = game_data.get("current_try", 0) + 1
	max_tries = game_data.get("max_tries", 0)

	if user_word in wordlist and len(user_word) == len(game_word):
		show_result(user_word)
		if user_word == game_word:
			print_formatted_text(HTML(f"<win>you won!</win>\nword guessed in <win>{current_try}/{max_tries}</win>."), style=data_manager.get_style())
		else:
			if current_try < max_tries:
				game_data["current_try"] += 1
				input_guess()
			else:
				print_formatted_text(HTML(f"<lose>you lost.</lose>\nthe word was <b>{game_word}</b>"), style=data_manager.get_style())
	else:
		sys.stdout.write("\033[F\033[K")
		input_guess()

file_path = data.get("path", "") if Path(data.get("path", "")).suffix != "" else data.get("path", "") + ".wordlist"

if Path(file_path).exists():
	with open(file_path, 'r') as file:
		wordlist = wordlist_parser.get_words_from_wordlist(file.read())
		start_game()
else:
	print_formatted_text(HTML(f"<error>file \"{file_path}\" does not exist.</error>"), style=data_manager.get_style())
