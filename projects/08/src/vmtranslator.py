import sys
import os
import parser
import codewriter
import StripFile

class VMTranslator():

	def __init__(self, inputFileOrFolder, outfolder):
		"""
		Constructor for VMTranslator
		Parameters: path/filename for outfile, parsed VM code in array
		"""

		self.cwriter = None
		self.input = inputFileOrFolder
		self.outFolder = outfolder

	def main(self):
		"""Main method parses vm code and passes arguments to codewriter """

		#checks for directory in order to process multiple vms
		if os.path.isdir(self.input):

			directory = os.path.basename(self.input)
			outfile = self.outFolder + "/" + directory + ".asm"
			self.cwriter = codewriter.CodeWriter(outfile)
			self.cwriter.writeInit()

			for file in os.listdir(self.input):
				if ".vm" in file.lower():
					vmCode = StripFile.StripFile(self.input + "/" + file).strip_file()
				
					self.vmtranslate(file, vmCode)

		#used for just one vm
		else: 
			outfile = self.input.split('.')[0] + ".asm"
			print(outfile)
			self.cwriter = codewriter.CodeWriter(outfile)
			vmCode = vmCode = StripFile.StripFile(self.input).strip_file()
			self.vmtranslate(self.input,vmCode)

	def vmtranslate(self, file, code):
		"""
		called from main function to translate vm code
		"""

		parsed_lines = parser.Parser(code)

		while parsed_lines.hasMoreCommands():
			
			parsed_lines.advance()
			command_type = parsed_lines.getCommandType()
	

			if command_type == 'C_ARITHMETIC':
				self.cwriter.writeArithmetic(parsed_lines.getCommand())
			elif command_type == 'C_PUSH' or command_type == 'C_POP':
				segment = parsed_lines.getArg1()
				value = parsed_lines.getArg2()
				self.cwriter.writePushPop(command_type,segment,value)
			elif command_type == "C_GOTO":
				self.cwriter.writeGoto(parsed_lines.getArg1())
			elif command_type == "C_IF":
				self.cwriter.writeIf(parsed_lines.getArg1())
			elif command_type == "C_LABEL":
				self.cwriter.writeLabel(parsed_lines.getArg1())
			elif command_type == "C_RETURN":
				self.cwriter.writeReturn()
			elif command_type == "C_FUNCTION":
				self.cwriter.writeFunction(parsed_lines.getArg1(), parsed_lines.getArg2())
			elif command_type == "C_CALL":
				self.cwriter.writeCall(parsed_lines.getArg1(), parsed_lines.getArg2())



if __name__ == "__main__":
	
	args = sys.argv

	inFileOrFolder = args[1]
	outfolder = args[2]

	translator = VMTranslator(inFileOrFolder,outfolder)

	translator.main()