class CodeWriter():

	def __init__(self, filename):
		"""Initializes codywriter class with outfile's name as parameter"""
		""" Initalizes a count and jump-flag global vars"""

		self.outfile = open(filename, 'w')
		self.jmpFlag = 0
		self.functionCount = 0

		filename_parts = filename.split("/")
		i = len(filename_parts)-1
		self.fname = filename_parts[i][:-4]

	def setFileName(self, filename):
		self.fname = str(filename)

	def getArthTemplate(self, command, jmpType):
		""" Returns redundant machine language code for arithmetic commands"""
		""" Parameters: command and type of jump for logic commands"""

		if command in ["add","sub", "and","or"]:
			return "@SP\n" + "AM=M-1\n" + "D=M\n" + "A=A-1\n"

		if command in ["gt","lt","eq"]:
			return "@SP\n" + "AM=M-1\n" + "D=M\n" + "A=A-1\n" + "D=M-D\n" + "@FALSE" + str(self.jmpFlag)+ "\n" + "D;" + jmpType + "\n" + "@SP\n" + "A=M-1\n" + "M=-1\n" + "@CONTINUE" + str(self.jmpFlag) + "\n" + "0;JMP\n" + "(FALSE" + str(self.jmpFlag) + ")\n" + "@SP\n" + "A=M-1\n" + "M=0\n" + "(CONTINUE" + str(self.jmpFlag) + ")\n"

	def getPushPopTemplate(self, command, segment, index, isPointer):
		""" Returns redundant machine language code for push/pop commands """
		""" Parameters: command, segment representing 1st argument, A register value, and boolean value representing whether command is a pointer"""

		if 'push' in command:
			
			pushCode = ["@" + segment + "\n" + "D=M\n", "@SP\n" + "A=M\n" + "M=D\n" + "@SP\n" + "M=M+1\n"]
		
			if isPointer:
				pointerCode = ""
				return pushCode[0] + pointerCode + pushCode[1]
			elif not isPointer:
				pointerCode = "@" + str(index) + "\n" + "A=D+A\n" + "D=M\n"
				return pushCode[0] + pointerCode + pushCode[1]
			else: 
				print("Bad push")

		if 'pop' in command:
			
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


		if 'add' in command: 
			self.outfile.write(self.getArthTemplate('add',None) + "M=M+D\n")

		elif 'sub' in command:
			self.outfile.write(self.getArthTemplate('sub',None) + "M=M-D\n")

		elif 'neg' in command:
			self.outfile.write("D=0\n" + "@SP\n" + "A=M-1\n" + "M=D-M\n")

		elif 'and' in command:
			self.outfile.write(self.getArthTemplate('and', None) + "M=M&D\n")

		elif 'or' in command:
			self.outfile.write(self.getArthTemplate('or',None) + "M=M|D\n")

		elif 'not' in command:
			self.outfile.write("@SP\n" + "A=M-1\n" + "M=!M\n")

		elif 'gt' in command:
			
			self.outfile.write(self.getArthTemplate('gt', "JLE"))			
			self.jmpFlag += 1

		elif 'lt' in command:
	
			self.outfile.write(self.getArthTemplate('lt', "JGE"))
			self.jmpFlag += 1

		elif 'eq' in command:
	
			self.outfile.write(self.getArthTemplate('eq', "JNE"))
			self.jmpFlag += 1


	def writePushPop(self, command, segment, index):
		"""Method for writing push/pop commands to maching language in outfile"""
		"""Parameters: the command, 1st argument, A register index"""
		
		cmd = ''

		if command == 'C_PUSH':
			cmd = 'push'
	
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
				#elif cmd == 'pop':
				#	self.outfile.write("@SP\n" + "A=M-1\n" + "D=M\n" + "@SP\n" + "M=M-1\n")
				#	self.outfile.write("@" + str(self.fname) + "." + str(index) + "\n" + "M=D\n")
		
		else:
			cmd = 'pop'

			if segment == 'static':
				self.outfile.write("@SP\n" + "A=M-1\n" + "D=M\n" + "@SP\n" + "M=M-1\n")
				self.outfile.write("@" + str(self.fname) + "." + str(index) + "\n" + "M=D\n")

			elif segment == 'local':
				self.outfile.write(self.getPushPopTemplate(cmd,'LCL',index,False))
			elif segment == 'argument':
				self.outfile.write(self.getPushPopTemplate(cmd, 'ARG', index, False))
			elif segment == 'this':
				self.outfile.write(self.getPushPopTemplate(cmd, 'THIS', index, False))
			elif segment == 'that':
				self.outfile.write(self.getPushPopTemplate(cmd, 'THAT', index, False))
			elif segment == 'temp':
				self.outfile.write(self.getPushPopTemplate(cmd, 'R5', index + 5, False))
			elif segment == 'pointer':
				if index == 0:
					self.outfile.write(self.getPushPopTemplate(cmd, 'THIS', index, True))
				if index == 1:
					self.outfile.write(self.getPushPopTemplate(cmd, 'THAT', index, True))


	def writeInit(self):
		"""
		Writes the bootstrap code to file
		"""
		
		self.outfile.write("@256\n" + "D=A\n" + "@SP\n" + "M=D\n")
		self.writeCall("Sys.init",0)


	def writeLabel(self, label):
		"""
		Write labels to the vm code
		"""

		self.outfile.write("(" + label + ")\n")

	def writeGoto(self, label):
		"""
		Writes assembly code for goto command
		"""
		
		self.outfile.write("@" + label + "\n" + "0;JMP\n")

	def writeIf(self, label):
		"""
		Writes assembly code for if-goto command
		"""
		
		self.outfile.write("@SP\n" + "AM=M-1\n" + "D=M\n" + "A=A-1\n" + "@" + label + "\n" + "D;JNE\n")

	def writeCall(self, strFunction, nArgs):
		"""
		Writes assembly code for call command
		"""
		
		self.functionCount += 1
		callCode = "@RETURN" + str(self.functionCount) + "\n" + "D=A\n"
		callCode += "D=A\n" + "@SP\n" + "A=M\n" + "M=D\n" +"@SP\n" + "M=M+1\n"

		for pointer in ["LCL", "ARG", "THIS", "THAT"]:
			callCode += "@" + pointer + "\n" + "D=M\n" + "@SP\n" + "A=M\n" + "M=D\n" + "@SP\n" + "M=M+1\n"

		callCode += "@SP\n" + "D=M\n" + "@5\n" + "D=D-A\n" + "@" + str(nArgs) + "\n" + "D=D-A\n" + "@ARG\n" + "M=D\n" + "@SP\n" + "D=M\n" + "@LCL\n" + "M=D\n"
		self.outfile.write(callCode)
		self.writeGoto(strFunction)
		self.writeLabel("RETURN" + str(self.functionCount))

	def writeReturn(self):
		"""
		Write assembly code for return command
		"""

		code = "@LCL\n" + "D=M\n" + "@R14\n" + "M=D\n" + "@5\n" + "D=A\n" + "@R14\n" + "D=M-D\n" + "A=D\n" + "D=M\n" "@R15\n" + "M=D\n" 
		code += self.getPushPopTemplate('pop','ARG', '0',False) + "@ARG\n" + "D=M\n" + "@SP\n" + "M=D+1\n"		

		for pointer in ["THAT", "THIS", "ARG", "LCL"]:
			code += "@R14\n" + "M=M-1\n" + "A=M\n" + "D=M\n" + "@" + pointer + "\n" + "M=D\n"

		code += "@R15\n" + "A=M\n" + "0;JMP\n"

		self.outfile.write(code)

	def writeFunction(self, strFunction, nLocal):
		"""
		Writes function 
		"""

		self.writeLabel(strFunction)
		for i in range(int(nLocal)):

			self.writePushPop('push','constant','0')




