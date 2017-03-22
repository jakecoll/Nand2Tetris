import sys
import re
from sys import argv

def stripWhiteSpace():

	readFilename = argv[1]
	readFile = open(readFilename, "r")
	outFilename = readFilename.replace(".in",".out")

	with open(outFilename,"w") as f:
		for line in readFile:
			editLine = line
			for char in [" ", "	"]:
				editLine = editLine.replace(char, "")
			if len(editLine) > 1:
				f.write(editLine)

	f.close()

def no_comments():

	outFilename = argv[2].replace(".in",".out")
	tmp = []
	
	with open(outFilename,"r") as r2:
		for line in r2:
			#edit = re.sub('//.*?\n','\n', line, flags=re.DOTALL)
			edit = re.split(r"//", line)
			cleaned = re.sub("\n|\r|\t ", "", edit[0])
			if cleaned != "\n":
				tmp.append(cleaned+ "\n")
	
	r2.close()

	with open(outFilename, "w") as w:
		for i in range(len(tmp)):
			if len(tmp[i]) > 1:
				w.write(tmp[i])

	w.close()

def main():
	if len(sys.argv) < 3:
		stripWhiteSpace()

	elif len(sys.argv) == 3:
		if sys.argv[1] == "no-comments":
			no_comments()


if __name__ == "__main__":
	main()
