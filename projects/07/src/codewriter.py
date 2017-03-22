class CodeWriter():

	def __init__(self, filename):
		"""Initializes codywriter class with outfile's name as parameter"""
		""" Initalizes a count and jump-flag global vars"""

		self.outfile = open(filename, 'w')
		self.jmpFlag = 0
		self.count = 0

		filename_parts = filename.split("/")
		i = len(filename_parts)-1
		self.fname = filename_parts[i][:-4]

	def getArthTemplate(self, command, jmpType):
		""" Returns redundant machine language code for arithmetic commands"""
		""" Parameters: command and type of jump for logic commands"""

		if command in ["add","sub", "and","or"]:
			return "@SP\n" + "AM=M-1\n" + "D=M\n" + "A=A-1\n"

		elif command in ["gt","lt","eq"]:
			return "@SP\n" + "AM=M-1\n" + "D=M\n" + "A=A-1\n" + "D=M-D\n" + "@FALSE" + str(self.jmpFlag)+ "\n" + "D;" + jmpType + "\n" + "@SP\n" + "A=M-1\n" + "M=-1\n" + "@CONTINUE" + str(self.jmpFlag) + "\n" + "0;JMP\n" + "(FALSE" + str(self.jmpFlag) + ")\n" + "@SP\n" + "A=M-1\n" + "M=0\n" + "(CONTINUE" + str(self.jmpFlag) + ")\n"

	def getPushPopTemplate(self, command, segment, index, isPointer):
		""" Returns redundant machine language code for push/pop commands """
		""" Parameters: command, segment representing 1st argument, A register value, and boolean value representing whether command is a pointer"""

		if command == 'push':
			
			pushCode = ["@" + segment + "\n" + "D=M\n", "@SP\n" + "A=M\n" + "M=D\n" + "@SP\n" + "M=M+1\n"]
			
			if isPointer:
				pointerCode = ""
				return pushCode[0] + pointerCode + pushCode[1]
			elif not isPointer:
				pointerCode = "@" + str(index) + "\n" + "A=D+A\n" + "D=M\n"
				return pushCode[0] + pointerCode + pushCode[1]
			else: 
				print("Bad push")

		if command == 'pop':
			
			popCode = ["@" + segment + "\n", "@R13\n" + "M=D\n" + "@SP\n" + "AM=M-1\n" + "D=M\n" + "@R13\n" + "A=M\n" + "M=D\n"]
			
			if isPointer:
				pointerCode = "D=A\n"
				return popCode[0] + pointerCode + popCode[1]
			elif not isPointer:
				pointerCode = "D=M\n" + "@" + str(index) + "\n" + "D=D+A\n"
				return popCode[0] + pointerCode + popCode[1]
			else:
				print("Bad pop")



	def writeArithmetic(self, command):
		"""Method for writing machine language to outfile for arithmetic commands"""
		"""Parameters: the command """

		if command == "add": 
			self.outfile.write(self.getArthTemplate(command,None) + "M=M+D\n")

		elif command == 'sub':
			self.outfile.write(self.getArthTemplate(command,None) + "M=M-D\n")

		elif command == 'neg':
			self.outfile.write("D=0\n" + "@SP\n" + "A=M-1\n" + "M=D-M\n")

		elif command == 'and':
			self.outfile.write(self.getArthTemplate(command, None) + "M=M&D\n")

		elif command == 'or':
			self.outfile.write(self.getArthTemplate(command,None) + "M=M|D\n")

		elif command == 'not':
			self.outfile.write("@SP\n" + "A=M-1\n" + "M=!M\n")

		elif command == 'gt':
			self.outfile.write(self.getArthTemplate(command, "JLE"))			
			self.jmpFlag += 1

		elif command == 'lt':
			self.outfile.write(self.getArthTemplate(command, "JGE"))
			self.jmpFlag += 1

		elif command == 'eq':
			self.outfile.write(self.getArthTemplate(command, "JNE"))
			self.jmpFlag += 1


	def writePushPop(self, command, segment, index):
		"""Method for writing push/pop commands to maching language in outfile"""
		"""Parameters: the command, 1st argument, A register index"""
		
		cmd = ''

		if command == 'C_PUSH':
			cmd = 'push'

		if command == 'C_POP':
			cmd = 'pop'
			
		if segment == 'local':
			self.outfile.write(self.getPushPopTemplate(cmd,'LCL',index,False))
			
		elif segment == 'argument':
			self.outfile.write(self.getPushPopTemplate(cmd,'ARG',index,False))
			
		elif segment == 'this':
			self.outfile.write(self.getPushPopTemplate(cmd,'THIS',index,False))
			
		elif segment == 'that':
			self.outfile.write(self.getPushPopTemplate(cmd,'THAT',index,False))
			
		elif segment == 'temp':
			self.outfile.write(self.getPushPopTemplate(cmd,'R5',index + 5, False))
			
		elif segment == 'pointer':
			if index == 0:
				self.outfile.write(self.getPushPopTemplate(cmd,'THIS',index,True))
			if index == 1:
				self.outfile.write(self.getPushPopTemplate(cmd,'THAT',index,True))
			
		elif segment == 'constant':
			self.outfile.write("@" + str(index) + "\n" + "D=A\n" + "@SP\n" + "A=M\n" + "M=D\n" + "@SP\n" + "M=M+1\n")

		elif segment == 'static':
			if cmd == 'push':
				self.outfile.write(self.getPushPopTemplate(cmd,str(self.fname + "." + str(index)),index,True))
			elif cmd == 'pop':
				self.outfile.write("@SP\n" + "A=M-1\n" + "D=M\n" + "@SP\n" + "M=M-1\n")
				self.outfile.write("@" + str(self.fname) + "." + str(index) + "\n" + "M=D\n")






