import re

## Modified version for VM translator
class StripFile(object):

	def __init__(self,filename):
		self.filename = filename

	def strip_file(self):

		skip_line = False

		infile = open(self.filename, 'r')

		tmp = []
		for line in infile:

			if "/*" in line and "*/" not in line:
				skip_line = True
				continue

			elif "/*" not in line and "*/" in line:
				skip_line = False
				continue

			elif skip_line:
				continue 

			elif "//" in line:
				find_comments = re.split(r"//", line)
				no_comments = re.sub("\t|\r|\n|", "", find_comments[0])

				if no_comments != '':
					tmp.append(no_comments)

			elif "/*" in line and "*/" in line:
	
				left = line.index("/*")
				right = line.index("*/", left) + 2

				no_comments = line.replace(line[left:right], "")
				no_comments = re.sub("\t|\r|\n|", "", no_comments)

				if no_comments != '':
					tmp.append(no_comments)

			else:
				clean = no_comments = re.sub("\t|\r|\n|", "", line)

				if clean != '':
					tmp.append(clean)
			
		infile.close()

		return tmp