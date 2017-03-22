class SymbolTable(object):

	def __init__(self):
		self._global = {}
		self._local = {}
		self._scope = self._global
		self._global_var_count = 0
		self._var_count = 0
		self._arg_count = 0
		self._field_count = 0
		self._static_count = 0
		self._if_count = 0
		self._while_count = 0

	def start_subroutine(self, name):
		"""
		Method reseting variable counts for new subrouting
		"""
		self._local[name] = {}
		self._var_count = 0
		self._arg_count = 0
		self._if_count = 0
		self._while_count =0

	def set_scope(self, name):
		"""
		Method for setting current scope
		"""
		if name == 'global':
			self._scope = self._global
		else:
			self._scope = self._local

	def define(self, name, type, kind):
		"""
		Method for defining variables and storing in scope 
		"""
		if kind == 'static':
			self._global[name] = (type, kind, self._static_count)
			self._static_count = self._static_count + 1
		elif kind == 'field':
			self._global[name] = (type, kind, self._field_count)
			self._field_count = self._field_count + 1
		elif kind == 'arg':
			self._scope[name] = (type, kind, self._arg_count)
			self._arg_count = self._arg_count + 1
		elif kind == 'var':
			self._scope[name] = (type, kind, self._var_count)
			self._var_count = self._var_count + 1


	def kind_of(self, name):
		"""
		Method returns variable kind
		"""
		if name in self._scope:
			return self._scope[name][1]
		elif name in self._global:
			return self._global[name][1]
		else:
			return 'NO KIND RECORDED'

	def type_of(self, name):
		"""
		Method returns variable type
		"""
		if name in self._scope:
			return self._scope[name][0]
		elif name in self._global:
			return self._global[name][0]
		else:
			return 'NO TYPE RECORDED'

	def index_of(self,name):
		"""
		Method returns variable index
		"""
		if name in self._scope:
			return self._scope[name][2]
		elif name in self._global:
			return self._global[name][2]
		else:
		
			return 'NOT INDEXED'
