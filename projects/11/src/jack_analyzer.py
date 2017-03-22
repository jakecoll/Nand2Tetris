import sys
import os
from jack_tokenizer import JackTokenizer
from compilation_engine import CompilationEngine
from strip_file import StripFile

class JackAnalyzer(object):

	def __init__(self, inFolder):
		""" 
		constructor for jack analyzer
		"""

		self.input = inFolder
		self.output = inFolder

	def main(self):

		#checks for directory in order to process multiple jack files
		if os.path.isdir(self.input):

			directory = os.path.basename(self.input)

			for file in os.listdir(self.input):
				if ".jack" in file.lower():
					jack_code = StripFile(self.input + "/" + file).strip_file()

					outfile = self.output + "/" + file.split('.')[0] + ".vm"
					print(outfile)
					self.tokenize(jack_code,outfile)

	def tokenize(self, code, outfile):

		tokenizer = JackTokenizer(code)		
		CompilationEngine(tokenizer,outfile).compile()



if __name__ == "__main__":

	args = sys.argv

	inFolder = args[1]

	analyzer = JackAnalyzer(inFolder)

	analyzer.main()


