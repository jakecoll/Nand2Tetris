import StripFile

class Parser():

	def __init__(self, vmCode):
		""" Initializes parser with vm code as parameter and sets index to -1 (will be incremented before called)"""

		self.code = vmCode
		self.index = -1
	
	def hasMoreCommands(self):
		""" returns boolean value for whether there are more commands in line"""

		if self.index < (len(self.code)-1):
			return True
		else:
			return False

	def advance(self):
		""" function increase index for array of code"""

		self.index += 1

	def getCommandType(self):
		""" Returns the command type of a given command """

		#The Book lists all argument types in its implementation section, but only C_PUSH and C_POP will ever returned from parser in Project 7
		argTypes = {'push':'C_PUSH','pop':'C_POP','label':'C_LABEL','goto':'C_GOTO','if-goto':'C_IF','function':'C_FUNCTION','return':'C_RETURN','call':'C_CALL'}
		arithmetic = {'add','sub','neg','eq','gt','lt', 'and', 'or', 'not'}
		
		cmd = self.code[self.index].split(' ')
		if cmd[0] in arithmetic:
			return 'C_ARITHMETIC'
		elif cmd[0] in argTypes.keys():
			return argTypes.get(cmd[0])

	def getArg1(self):
		""" Returns first argument for command in vm language line. 
		If its arithmetic (e.g. add, sub, etc.) then it will return that versus argument that follow push pop command"""

		cmd = self.code[self.index].split(' ')

		if self.getCommandType() == 'C_ARITHMETIC':
			return cmd[0]
		else:
			return cmd[1]

	def getArg2(self):
		""" Returns value from push pop argument """

		return int(self.code[self.index].split(' ')[2])

	def getCommand(self):
		""" Returns current commond (e.g. line of vm language) """

		return self.code[self.index]
