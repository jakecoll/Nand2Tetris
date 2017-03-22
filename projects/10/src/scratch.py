import re

_symbols = "{|}|\(|\)|\[|\]|\.|,|;|\+|-|\*|/|&|\||<|>|=|~"

def get_tokens(jack_code):
	tmp = []

	for line in jack_code:
		if len(line) > 0:
				
			parts = line.split()

			for possible_token in parts:
				in_case_of_symbols = []
				in_case_of_symbols += re.split('(' + _symbols + ')', possible_token)

				for token in in_case_of_symbols:
					if token != "":
						tmp.append(token)
	return tmp

test = ["Main{ method"]

print(get_tokens(test))