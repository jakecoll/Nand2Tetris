import vm_writer
import symbol_table

class CompilationEngine(object):

	_operands = {'<':'&lt;', '>':'&gt;', '"':'&quot;', '&':'&amp;'}

	def __init__(self, jack_tokenizer, output):
		"""
		constructor for compilation engine
		"""

		self.tokenizer = jack_tokenizer
		self.writer = vm_writer.VMWriter(output)
		self.symbol_table = symbol_table.SymbolTable()
		self.class_name = ""
		self.function_name = ""

	def compile(self):
		"""
		Method for compiling jack files. Assumes all files are classes
		"""
		self.tokenizer.advance() # advance over class
		self.class_name = self.tokenizer.get_token()
		self.tokenizer.advance() # advance over {

		while(self.tokenizer.check_token() in ['field','static']):
			self.compile_var_dec()
		while(self.tokenizer.check_token() in ['function', 'method', 'constructor']):
			self.compile_subroutine()

		#print(self.tokenizer.check_token())
		#self.tokenizer.advance()
		self.writer.close()

	# No longer need separate compile_var_dec and compile_class_var_dec
	def compile_var_dec(self):
		"""
		Method for compiling variables with class level scope
		"""

		kind = self.tokenizer.get_token() # static or field
		type = self.tokenizer.get_token() # var type
		name = self.tokenizer.get_token() # var name

		self.symbol_table.define(name, type, kind)
		while("," in self.tokenizer.check_token()):
			self.tokenizer.advance()
			name = self.tokenizer.get_token()
			self.symbol_table.define(name,type,kind)

		self.tokenizer.advance() # advance over ;

	def compile_subroutine(self):
		"""
		method for compiling subroutines
		"""

		_type = self.tokenizer.get_token() #constructor, method or function keyword

		self.tokenizer.advance() # advance over return type
		self.function_name = self.class_name + '.' + self.tokenizer.get_token()
		self.symbol_table.start_subroutine(self.function_name)
		self.symbol_table.set_scope(self.function_name)
		self.tokenizer.advance() # pass over (

		self.compile_parameter_list(_type)
		self.tokenizer.advance() # pass over )

		self.tokenizer.advance() # pass over {

		while(self.tokenizer.check_token() == 'var'):
			self.compile_var_dec()

		var_count = self.symbol_table._var_count
		self.writer.write_function(self.function_name,var_count)
		
		if _type == 'method':
			self.writer.write_push('argument', 0)
			self.writer.write_pop('pointer', 0)
		if _type == 'constructor':
			field_count = self.symbol_table._field_count
			self.writer.write_push('constant', field_count)
			self.writer.write_call('Memory.alloc', 1)
			self.writer.write_pop('pointer', 0)

		self.compile_statements()
		self
		self.tokenizer.advance()
		self.symbol_table.set_scope('global')


	def compile_parameter_list(self, function_type):
		"""
		Method for compiling parameter lists
		"""

		if function_type == 'method':
			self.symbol_table.define('this', 'self', 'arg')

		while(self.tokenizer.check_token() != ')'):
			type = self.tokenizer.get_token()
			name = self.tokenizer.get_token()
			self.symbol_table.define(name, type, 'arg')
			
			if self.tokenizer.check_token() == ',':
				self.tokenizer.advance()

	
	def compile_statements(self):
		"""
		Method for distinguishing among statements and executing appropriate compilation methods
		"""
		
		statements = ['do', 'let', 'while', 'return', 'if']

		while(self.tokenizer.check_token() in statements):

			if self.tokenizer.check_token() == 'do':
				self.compile_do()
			elif self.tokenizer.check_token() == 'let':
				self.compile_let()
			elif self.tokenizer.check_token() == 'while':
				self.compile_while()
			elif self.tokenizer.check_token() == 'return':
				self.compile_return()
			elif self.tokenizer.check_token() == 'if':
				self.compile_if()

	def compile_do(self):
		"""
		Method for compiling do statements
		"""

		num_locals = 0
		call_name = ''

		self.tokenizer.advance() # pass over 'do'
		
		name = self.tokenizer.get_token()

		if self.tokenizer.check_token() == '.':
			self.tokenizer.advance()
			subroutine = self.tokenizer.get_token()
			if name in self.symbol_table._scope or name in self.symbol_table._global:
				self.filter_push(name)
				call_name = self.symbol_table.type_of(name) + '.' + subroutine
				num_locals = num_locals + 1
			else:
				call_name = name + '.' + subroutine
		else:
			self.writer.write_push('pointer', 0)
			num_locals = num_locals + 1
			call_name = self.class_name + '.' + name

		self.tokenizer.advance()
		num_locals = num_locals + self.compile_expression_list()
		self.writer.write_call(call_name, num_locals)
		self.tokenizer.advance()

		self.writer.write_pop('temp', 0)

		if self.tokenizer.check_token() == ';':
			self.tokenizer.advance()
	

	def compile_let(self):
		"""
		Method for compiling let statements
		"""
	
		self.tokenizer.advance() # pass over 'let'
		name = self.tokenizer.get_token()

		if self.tokenizer.check_token() == '[':
			
			self.tokenizer.advance()
			self.compile_expression()
			self.tokenizer.advance()

			if name in self.symbol_table._scope:
				if self.symbol_table.kind_of(name) == 'var':
					self.writer.write_push('local', self.symbol_table.index_of(name))
				if self.symbol_table.kind_of(name) == 'arg':
					self.writer.write_push('argument', self.symbol_table.index_of(name))

			else:
				if symbol_table.kind_of(name) == 'static':
					self.writer.write_push('static', self.symbol_table.index_of(name))
				else:
					self.writer.write_push('this', self.symbol_table.index_of(name))

			self.writer.write_arithmetic('add')

			self.tokenizer.advance()
			self.compile_expression()

			self.writer.write_pop('temp', 0)
			self.writer.write_pop('pointer', 1)
			self.writer.write_push('temp', 0)
			self.writer.write_pop('that', 0)

		else:
			self.tokenizer.advance()
			self.compile_expression()
			self.filter_pop(name)

		if self.tokenizer.check_token() == ';':	
			self.tokenizer.advance() # pass over ;


	def compile_while(self):
		"""
		Method for compiling while statements
		"""
		count = str(self.symbol_table._while_count)
		self.symbol_table._while_count = self.symbol_table._while_count + 1

		self.writer.write_label('WHILE_EXP' + count)
		self.tokenizer.advance() # pass over while
		self.tokenizer.advance() # pass over (

		self.compile_expression()
		self.writer.write_arithmetic('not')
		self.writer.write_if('WHILE_END' + count)

		self.tokenizer.advance()
		self.tokenizer.advance()
		self.compile_statements()
		self.writer.write_goto('WHILE_EXP' + count)
		self.writer.write_label('WHILE_END' + count)

		self.tokenizer.advance()

	def compile_return(self):
		"""
		Method for compiling return statements
		"""

		self.tokenizer.advance() 

		if ';' in self.tokenizer.check_token():
			self.writer.write_push('constant', 0)

		else:
			while(';' not in self.tokenizer.check_token()):
				self.compile_expression()

		self.writer.write_return()
		self.tokenizer.advance()


	def compile_if(self):
		"""
		Method for compiling if statements
		"""

		self.tokenizer.advance() # pass over 'if'
		self.tokenizer.advance() # pass over (
		
		self.compile_expression()

		self.tokenizer.advance() # pass over )

		count = self.symbol_table._if_count
		self.symbol_table._if_count = self.symbol_table._if_count + 1
		self.writer.write_if('IF_TRUE' + str(count))
		self.writer.write_goto('IF_FALSE' + str(count))
		self.writer.write_label('IF_TRUE' + str(count))
		self.tokenizer.advance() # pass over {
		self.compile_statements()
		self.tokenizer.advance() # pass over }

		if self.tokenizer.check_token() == 'else':
			self.writer.write_goto('IF_END' + str(count))
			self.writer.write_label('IF_FALSE' + str(count))
			self.tokenizer.advance() # pass else
			self.tokenizer.advance() # pass {
			self.compile_statements()
			self.tokenizer.advance()
			self.writer.write_label('IF_END' + str(count))
		else:
			self.writer.write_label('IF_FALSE' + str(count))

	def compile_expression(self):
		"""
		Method provides expression xml wrapper for terms
		"""
		
		self.compile_term()

		operands = ['+', '-', '*', '/', '|', '&', '=', '<', '>']

		while(self.tokenizer.check_token() in operands):
			operand = self.tokenizer.get_token()
			self.compile_term()
			if operand == '+':
				self.writer.write_arithmetic('add')
			elif operand == '-':
				self.writer.write_arithmetic('sub')
			elif operand == '*':
				self.writer.write_call('Math.multiply', 2)
			elif operand == '/':
				self.writer.write_call('Math.divide', 2)
			elif operand == '|':
				self.writer.write_arithmetic('or')
			elif operand == '&':
				self.writer.write_arithmetic('and')
			elif operand == '=':
				self.writer.write_arithmetic('eq')
			elif operand == '<':
				self.writer.write_arithmetic('lt')
			elif operand == '>':
				self.writer.write_arithmetic('gt')


	def compile_term(self):
		"""
		Method for compiling terms. 
		"""

		count = 0
		isArray = False

		if self.tokenizer.check_token().isdigit():
			self.writer.write_push('constant', self.tokenizer.get_token())
		elif self.tokenizer.check_token() == '"':
			
			stringConstant = ''

			self.tokenizer.advance() # pass over "

			while(self.tokenizer.check_token() != '"'):

				if self.tokenizer.check_token() == ';':
					stringConstant = stringConstant[:-1]
					stringConstant += self.tokenizer.get_token() + ' '

				else:
					stringConstant += self.tokenizer.get_token() + ' '

			stringConstant = stringConstant[:-1]

			if stringConstant[len(stringConstant)-1] == ':':
				stringConstant += ' '

			self.writer.write_push('constant', len(stringConstant))
			self.writer.write_call('String.new', 1)
			for char in stringConstant:
				self.writer.write_push('constant', ord(char))	
				self.writer.write_call('String.appendChar', 2)


			self.tokenizer.advance()
			
			if self.tokenizer.check_token == ')':
				self.tokenizer.advance()

		elif self.tokenizer.check_token() in ['true', 'false', 'null', 'this']:
			if self.tokenizer.check_token() == 'true':
				self.writer.write_push('constant', 0)
				self.writer.write_arithmetic('not')
			elif self.tokenizer.check_token() == 'this':
				self.writer.write_push('pointer', 0)
			else:
				self.writer.write_push('constant', 0)

			self.tokenizer.advance()

		elif self.tokenizer.check_token() in ['-', '~']:
			operand = self.tokenizer.get_token() # get operand
			self.compile_term()
			if operand == '-':
				self.writer.write_arithmetic('neg')
			if operand == '~':
				self.writer.write_arithmetic('not')
		elif self.tokenizer.check_token() == '(':
			self.tokenizer.advance()
			self.compile_expression()
			self.tokenizer.advance()
		# Compile Identifier
		else:
			num_locals = 0
			name = self.tokenizer.get_token()
			
			if self.tokenizer.check_token() == '[': 
				isArray = True 
				self.tokenizer.advance()
				self.compile_expression()
				self.tokenizer.advance()
		
				if name in self.symbol_table._scope:
					if self.symbol_table.kind_of(name) == 'var':
						self.writer.write_push('local', self.symbol_table.index_of(name))
					if self.symbol_table.kind_of(name) == 'arg':
						self.writer.write_push('argument', self.symbol_table.index_of(name))

				else:
					if symbol_table.kind_of(name) == 'static':
						self.writer.write_push('static', self.symbol_table.index_of(name))
					else:
						self.writer.write_push('this', self.symbol_table.index_of(name))

				self.writer.write_arithmetic('add')
				

			if self.tokenizer.check_token() == '(':
				num_locals = num_locals + 1
				self.writer.write_push('pointer', 0)
				self.tokenizer.advance()
				num_locals = num_locals + self.compile_expression_list() 
				self.tokenizer.advance()
				self.writer.write_call(self.class_name + '.' + name, num_locals)

			elif self.tokenizer.check_token() == '.':
	
				self.tokenizer.advance()
				subroutine = self.tokenizer.get_token()
			
				if name in self.symbol_table._scope or name in self.symbol_table._global:
				
					self.filter_push(name)
					name = self.symbol_table.type_of(name) + '.' + subroutine
					num_locals = num_locals + 1
				else:
				
					name = name + '.' + subroutine

				self.tokenizer.advance() # pass symbol (

				notString = True

				if self.tokenizer.check_token() == '"':
					wasString = False
					self.compile_term()
					num_locals = num_locals + 1

				else:
					num_locals = num_locals + self.compile_expression_list()
				
				if notString: 
					self.tokenizer.advance() # pass symbol )

				self.writer.write_call(name, num_locals)

			else:
			
				if isArray:
					self.writer.write_pop('pointer', 1)
					self.writer.write_push('that', 0)
				elif name in self.symbol_table._scope:

					if self.symbol_table.kind_of(name) == 'var':
						self.writer.write_push('local', self.symbol_table.index_of(name))
					elif self.symbol_table.kind_of(name) == 'arg':
						self.writer.write_push('argument', self.symbol_table.index_of(name))
				else:		
					if self.symbol_table.kind_of(name) == 'static':
						self.writer.write_push('static', self.symbol_table.index_of(name))
					else:
						self.writer.write_push('this', self.symbol_table.index_of(name))

	def compile_expression_list(self):
		"""
		Method for compiling expression list
		"""

		count = 0

		if self.tokenizer.check_token() != ')':
			self.compile_expression()
			count = count + 1

			while(self.tokenizer.check_token() == ','):
				self.tokenizer.advance()
				self.compile_expression()
				count = count + 1

		return count


	def filter_push(self, name):
		if name in self.symbol_table._scope:
			if self.symbol_table.kind_of(name) == 'var':
				self.writer.write_push('local', self.symbol_table.index_of(name))
			elif self.symbol_table.kind_of(name) == 'arg':
				self.writer.write_push('argument', self.symbol_table.index_of(name))
		else:
			if self.symbol_table.kind_of(name) == 'static':
				self.writer.write_push('static', self.symbol_table.index_of(name))
			else:
				self.writer.write_push('this', self.symbol_table.index_of(name))

	def filter_pop(self, name):
		if name in self.symbol_table._scope:
			if self.symbol_table.kind_of(name) == 'var':
				self.writer.write_pop('local', self.symbol_table.index_of(name))
			elif self.symbol_table.kind_of(name) == 'arg':
				self.writer.write_pop('argument', self.symbol_table.index_of(name))
		else:
			if self.symbol_table.kind_of(name) == 'static':
				self.writer.write_pop('static', self.symbol_table.index_of(name))
			else:
				self.writer.write_pop('this', self.symbol_table.index_of(name))



