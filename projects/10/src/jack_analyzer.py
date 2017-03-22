import sys
import os
from jack_tokenizer import JackTokenizer
from compilation_engine import CompilationEngine
from strip_file import StripFile

class JackAnalyzer(object):

	def __init__(self, inFileOrFolder, outputFolder):
		""" 
		constructor for jack analyzer
		"""

		self.input = inFileOrFolder
		self.output = outputFolder

	def main(self):

		#checks for directory in order to process multiple jack files
		if os.path.isdir(self.input):

			directory = os.path.basename(self.input)

			for file in os.listdir(self.input):
				if ".jack" in file.lower():
					jack_code = StripFile(self.input + "/" + file).strip_file()

					outfile = self.output + "/" + file.split('.')[0] + ".xml"
					self.tokenize(jack_code,outfile)

		#used for just one jack file
		else: 
			index = len(self.input.split('/')) - 1
			filename = self.input.split('/')[index]
			outfile = self.output + filename.replace('.jack', '.xml')
			
			jack_code = StripFile(self.input + "/" + file).strip_file() 
			self.tokenize(jack_code,outfile)

	def tokenize(self, code, outfile):

		tokenizer = JackTokenizer(code)		
		CompilationEngine(tokenizer,outfile).compile()



if __name__ == "__main__":

	args = sys.argv

	inFileOrFolder = args[1]
	outputFolder = args[2]

	analyzer = JackAnalyzer(inFileOrFolder, outputFolder)

	analyzer.main()


