import re

class JackTokenizer(object):

	_symbols = "{|}|\(|\)|\[|\]|\.|,|;|\+|-|\*|/|&|\||<|>|=|~"
	_operands = ['+', '-', '/', '&', '|', '<', '>', '=', '~', '*']

	def __init__(self, code):
		"""
		constructor for tokenizer
		"""

		self.index = 0
		self.tokens = self.extract_tokens(code)
		self.current_token = self.tokens[self.index]
		self.token_length = len(self.tokens) - 1

	def extract_tokens(self, jack_code):
		"""
		Method for extracting tokens from lines of jack code provided
		"""
		tmp = []

		for line in jack_code:
			if len(line) > 0:
					
				parts = line.split()

				for possible_token in parts:
					in_case_of_symbols = []
					in_case_of_symbols += re.split('(' + self._symbols + ')', possible_token)

					for token in in_case_of_symbols:
						if token != "":
							tmp.append(token)

		return tmp

	def get_token(self):
		"""
		Method returns the current token
		"""
		if self.has_more_tokens():
			return str(self.current_token)
		else:
			print('Out of Tokens. Insert more to play again :)')

	def has_more_tokens(self):
		"""
		Method returns a boolean value for wether or not any tokens remain
		"""

		if self.index < self.token_length:
			return True 
		else: 
			return False

	def advance(self):
		"""
		Method increments token index and updates current token
		"""

		self.index = self.index + 1
		self.current_token = self.tokens[self.index]

	def keyword(self):
		"""
		Method returns the xml for a keyword
		"""

		xml = "<keyword> " + str(self.current_token) + " </keyword>\n"
		self.advance()
		
		return xml

	def symbol(self):
		"""
		Method returns the xml for a symbol
		"""
		
		xml = "<symbol> " + str(self.current_token) + " </symbol>\n"
		self.advance()
		
		return xml

	def identifier(self):
		"""
		Method returns the xml for an identifier
		"""
		
		xml = "<identifier> " + str(self.current_token) + " </identifier>\n"
		self.advance()
		
		return xml

	def int_value(self):
		"""
		Method returns the xml for an integerConstant
		"""
		
		xml = "<integerConstant> " + str(self.current_token) + " </integerConstant>\n"
		self.advance()
		
		return xml

	def str_value(self):
		"""
		Method returns the xml for an stringConstant
		"""

		xml = '<stringConstant> '

		count = 0

		while(self.current_token != '"' and count < 2):
			if '"' in self.current_token:
				count = count + 1

			xml += self.current_token.replace('"', '') + " "
			self.advance()

		xml += ' </stringConstant>\n'
		
		if count != 2:
			self.advance()

		return xml

