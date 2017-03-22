import re

## Modified version for VM translator
class StripFile(object):

	def __init__(self,filename):
		self.filename = filename

	def strip_file(self):

		infile = open(self.filename, 'r')

		tmp = []
		for line in infile:
			no_comments = re.split(r"//", line)
			clear_white_space = re.sub("\t|\r|\n|", "", no_comments[0])

			if clear_white_space != '':
				tmp.append(clear_white_space)
		
		infile.close()

		return tmp