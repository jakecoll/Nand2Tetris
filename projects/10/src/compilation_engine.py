class CompilationEngine(object):

	_operands = {'<':'&lt;', '>':'&gt;', '"':'&quot;', '&':'&amp;'}

	def __init__(self, jack_tokenizer, output):
		"""
		constructor for compilation engine
		"""

		self.tokenizer = jack_tokenizer
		self.outfile = open(output, 'w')

	def compile(self):
		"""
		Method for compiling jack files. Assumes all files are classes
		"""

		while(self.tokenizer.has_more_tokens()):

			if self.tokenizer.get_token() == 'class':
				self.compile_class()
			elif self.tokenizer.get_token() in ['field','static']:
				self.compile_class_var_dec()
			elif self.tokenizer.get_token() in ['function', 'method', 'constructor']:
				self.compile_subroutine()

		self.outfile.write('<symbol> } </symbol>\n' + '</class>')
		self.outfile.close()

				
	def compile_class(self):
		"""
		Method for compiling initial class tokens
		"""
		
		xml = '<class>\n' + self.tokenizer.keyword() + self.tokenizer.identifier() + self.tokenizer.symbol()

		self.outfile.write(xml)

	def compile_class_var_dec(self):
		"""
		Method for compiling variables with class level scope
		"""
		
		xml = "<classVarDec>\n" + self.tokenizer.keyword()

		if self.tokenizer.get_token() in ['int', 'boolean', 'char']:
			xml += self.tokenizer.keyword()
		else:
			xml += self.tokenizer.identifier()

		xml += self.tokenizer.identifier()

		self.outfile.write(xml)

		while(self.tokenizer.get_token() == ','):
			xml = self.tokenizer.symbol() + self.tokenizer.identifier()

			self.outfile.write(xml)

		xml = self.tokenizer.symbol() + '</classVarDec>\n'
		self.outfile.write(xml)

		if self.tokenizer.get_token() == 'field' or self.tokenizer.get_token() == 'static':
			self.compile_class_var_dec()

	def compile_subroutine(self):
		"""
		method for compiling subroutines
		"""

		xml = '<subroutineDec>\n' 

		if self.tokenizer.get_token() == 'constructor':
			xml +=  self.tokenizer.keyword() + self.tokenizer.identifier()
		else: 
			xml += self.tokenizer.keyword() + self.tokenizer.keyword()

		xml += self.tokenizer.identifier() + self.tokenizer.symbol()

		self.outfile.write(xml)

		if self.tokenizer.get_token() != ')':
			self.outfile.write('<parameterList>\n')
			self.compile_parameter_list()
			self.outfile.write('</parameterList>\n')
		else:
			self.outfile.write('<parameterList>\n </parameterList>\n')
		
		xml = self.tokenizer.symbol() + '<subroutineBody>\n' + self.tokenizer.symbol()

		self.outfile.write(xml)

		if self.tokenizer.get_token() == 'var':
			self.compile_var_dec()

		self.outfile.write('<statements>\n')

		while(self.tokenizer.get_token() != "}"):
			self.compile_statements()
			if self.tokenizer.get_token() == None:
				break

		xml = '</statements>\n' + self.tokenizer.symbol() + '</subroutineBody>\n</subroutineDec>\n'
		self.outfile.write(xml)

		if self.tokenizer.get_token() in ['function', 'method', 'constructor']:
			self.compile_subroutine()

	def compile_parameter_list(self):
		"""
		Method for compiling parameter lists
		"""

		xml = self.tokenizer.keyword() + self.tokenizer.identifier()

		self.outfile.write(xml)

		if self.tokenizer.get_token() == ',':
			self.outfile.write(self.tokenizer.symbol())
			self.compile_parameter_list()


	def compile_var_dec(self):
		"""
		Method for compiling local variables
		"""

		xml = '<varDec>\n' + self.tokenizer.keyword()
		
		if self.tokenizer.get_token() in ['int', 'boolean', 'char']:
			xml += self.tokenizer.keyword()	
		else: 
			xml += self.tokenizer.identifier()

		xml += self.tokenizer.identifier()

		self.outfile.write(xml)

		while self.tokenizer.get_token() == ',':
			xml = self.tokenizer.symbol() + self.tokenizer.identifier()
			self.outfile.write(xml)

		self.outfile.write(self.tokenizer.symbol() + '</varDec>\n')

		if self.tokenizer.get_token() == 'var':
			self.compile_var_dec()


	def compile_statements(self):
		"""
		Method for distinguishing among statements and executing appropriate compilation methods
		"""
	
		if self.tokenizer.get_token() == 'do':
			self.compile_do()
		elif self.tokenizer.get_token() == 'let':
			self.compile_let()
		elif self.tokenizer.get_token() == 'while':
			self.compile_while()
		elif self.tokenizer.get_token() == 'return':
			self.compile_return()
		elif self.tokenizer.get_token() == 'if':
			self.compile_if()

	def compile_do(self):
		"""
		Method for compiling do statements
		"""

		xml = '<doStatement>\n' + self.tokenizer.keyword() + self.tokenizer.identifier()

		if self.tokenizer.get_token() == '.':
			xml += self.tokenizer.symbol() + self.tokenizer.identifier() + self.tokenizer.symbol() + '<expressionList>\n'
		else:
			xml += self.tokenizer.symbol() + '<expressionList>\n'

		self.outfile.write(xml)

		xml = ''

		if self.tokenizer.get_token() != ')':
			self.compile_expression_list()

		xml = '</expressionList>\n' + self.tokenizer.symbol() + self.tokenizer.symbol() + '</doStatement>\n'
		self.outfile.write(xml)

	def compile_let(self):
		"""
		Method for compiling let statements
		"""

		xml = "<letStatement>\n" + self.tokenizer.keyword() + self.tokenizer.identifier()

		self.outfile.write(xml)

		if self.tokenizer.get_token() == '[':
			xml = self.tokenizer.symbol()
			self.outfile.write(xml)

			self.compile_expression()

			xml = self.tokenizer.symbol()
			self.outfile.write(xml)

		xml = self.tokenizer.symbol()
		self.outfile.write(xml)

		self.compile_expression()

		xml = self.tokenizer.symbol() + '</letStatement>\n'
		self.outfile.write(xml)

	def compile_while(self):
		"""
		Method for compiling while statements
		"""

		xml = "<whileStatement>\n" + self.tokenizer.keyword() + self.tokenizer.symbol()
		self.outfile.write(xml)

		self.compile_expression()

		xml = self.tokenizer.symbol() + self.tokenizer.symbol() + '<statements>\n'
		self.outfile.write(xml)

		while self.tokenizer.get_token() != '}':
			self.compile_statements()

		xml = '</statements>\n' + self.tokenizer.symbol() + '</whileStatement>\n'
		self.outfile.write(xml)

	def compile_return(self):
		"""
		Method for compiling return statements
		"""

		xml = '<returnStatement>\n' + self.tokenizer.keyword()
		self.outfile.write(xml)

		if self.tokenizer.get_token() != ';':
			self.compile_expression()

		xml = self.tokenizer.symbol() + '</returnStatement>\n'
		self.outfile.write(xml)

	def compile_if(self):
		"""
		Method for compiling if statements
		"""

		xml = '<ifStatement>\n' + self.tokenizer.keyword() + self.tokenizer.symbol()
		self.outfile.write(xml)

		self.compile_expression()

		xml = self.tokenizer.symbol() + self.tokenizer.symbol() + '<statements>\n'
		self.outfile.write(xml)

		while self.tokenizer.get_token() != '}':
			self.compile_statements()

		self.outfile.write('</statements>\n' + self.tokenizer.symbol())

		if self.tokenizer.get_token() == 'else':
			self.compile_else()

		self.outfile.write('</ifStatement>\n')

	def compile_else(self):
		"""
		Method for compiling else option for if statemetns
		"""

		xml = self.tokenizer.keyword() + self.tokenizer.symbol() + '<statements>\n'
		self.outfile.write(xml)

		while self.tokenizer.get_token() != '}':
			self.compile_statements()

		xml = '</statements>\n' + self.tokenizer.symbol()
		self.outfile.write(xml)

	def compile_expression(self):
		"""
		Method provides expression xml wrapper for terms
		"""
		
		self.outfile.write('<expression>\n')
		self.compile_term()
		self.outfile.write('</expression>\n')

	def compile_term(self):
		"""
		Method for compiling terms. 
		"""

		self.outfile.write('<term>\n')

		count = 0

		while(self.tokenizer.get_token() not in [')',']',';',',', '/', '|', '<', '>', '=', '*', '+', '&']):
			if self.tokenizer.get_token().isdigit():
				self.outfile.write(self.tokenizer.int_value())
			elif '"' in self.tokenizer.get_token():
				self.outfile.write(self.tokenizer.str_value())
			elif self.tokenizer.get_token() in ['true', 'false', 'null', 'this']:
				self.outfile.write(self.tokenizer.keyword())
			elif self.tokenizer.get_token() == '-' and count == 0:
				self.outfile.write(self.tokenizer.symbol())
				self.compile_term()
			elif self.tokenizer.get_token() == '-' and count > 0:
				break
			elif self.tokenizer.get_token() == '~':
				self.outfile.write(self.tokenizer.symbol())

				if self.tokenizer.get_token() != '(':
					self.compile_term()

				else:
					self.outfile.write('<term>\n' + self.tokenizer.symbol())
					self.compile_expression()
					xml = self.tokenizer.symbol() + '</term>\n'
					self.outfile.write(xml)

			elif self.tokenizer.get_token() == '(':

				self.outfile.write(self.tokenizer.symbol())
				self.compile_expression()
				self.outfile.write(self.tokenizer.symbol())

			elif self.tokenizer.get_token() == '[':
				xml = self.tokenizer.symbol()
				self.outfile.write(xml)

				self.compile_expression()

				self.outfile.write(self.tokenizer.symbol())

			elif self.tokenizer.get_token() == '.':
				xml = self.tokenizer.symbol() + self.tokenizer.identifier() + self.tokenizer.symbol() + '<expressionList>\n'
				self.outfile.write(xml)

				if self.tokenizer.get_token() != ')':
					self.compile_expression_list()

				self.outfile.write('</expressionList>\n' + self.tokenizer.symbol())
		
			else:
				self.outfile.write(self.tokenizer.identifier())

			count = count + 1

		self.outfile.write('</term>\n')

		if self.tokenizer.get_token() in self.tokenizer._operands:
			if self.tokenizer.get_token() in ['<', '>', '"', '&']:
				xml = '<symbol> ' + CompilationEngine._operands.get(self.tokenizer.get_token()) + ' </symbol>\n'
				self.tokenizer.advance()
			else:
				xml = self.tokenizer.symbol()

			self.outfile.write(xml)
			self.compile_term()

	def compile_expression_list(self):
		"""
		Method for compiling expression list
		"""

		self.compile_expression()

		while(self.tokenizer.get_token() == ','):
			self.outfile.write(self.tokenizer.symbol())
			self.compile_expression()





