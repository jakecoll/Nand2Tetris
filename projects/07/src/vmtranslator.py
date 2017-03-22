import sys
import parser
import codewriter
import StripFile

class VMTranslator():

	def __init__(self, outfile, vmCode):
		"""
		Constructor for VMTranslator
		Parameters: path/filename for outfile, parsed VM code in array
		"""

		self.cwriter = codewriter.CodeWriter(outfile)
		self.parsed_lines = parser.Parser(vmCode)

	def main(self):
		"""Main method parses vm code and passes arguments to codewriter """

		tracker = -1

		while self.parsed_lines.hasMoreCommands():
			tracker += 1

			self.parsed_lines.advance()
			command_type = self.parsed_lines.getCommandType()

			if command_type == 'C_ARITHMETIC':
				self.cwriter.writeArithmetic(self.parsed_lines.getCommand())
			elif command_type == 'C_PUSH' or command_type == 'C_POP':
				segment = self.parsed_lines.getArg1()
				value = self.parsed_lines.getArg2()
				self.cwriter.writePushPop(command_type,segment,value)


if __name__ == "__main__":

	args = sys.argv

	infile = args[1]
	outfile = args[2]

	vmCode = StripFile.StripFile(infile).strip_file()
	translator = VMTranslator(outfile,vmCode)

	translator.main()
