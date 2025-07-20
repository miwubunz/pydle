def get_words_from_wordlist(list: str) -> list[str]:
	word_list = []
	lines = list.split("\n")
	for line in lines:
		if len(line) > 0 or line != "":
			word_list.append(line.strip().upper())
	
	return word_list	
