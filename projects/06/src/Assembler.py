import sys
import re
import SymbolConverter
import StripFile


class Assembler():

	def __init__(self):

		self.symbols = SymbolConverter.SymbolConverter()
		self.next_address = 16;

	def num_to_bin(self, num):
		#strip '0b' from bin function
		binary = bin(num)[2:]

		#determine number of preceding 0s
		zeroes = 16-min(15,len(binary))
		instruction = '0'*zeroes + binary

		return instruction

	def is_var(self, str):

		#checks if string is predefinied variables
		if str in self.symbols._var.keys():
			return True

	def a_instruction(self, line):

		a = line[1:]

		# Check if A set to a digit
		if a.isdigit():
			num = int(a)
			binary = self.num_to_bin(num)

		#If not a digit then check for a predefined variable
		elif self.is_var(a):
			a_reg = self.symbols._var[a]
			binary = self.num_to_bin(a_reg)

		#If not at digit or predefinied variable then a new variable that needs to be stored and indexed
		else:
			binary = self.num_to_bin(self.next_address)
			self.symbols._var[a] = self.next_address
			self.next_address += 1

		return binary

	def c_instruction(self, line):

		#dest
		if '=' in line:
			parts = line.split('=')
			comp = parts[1]
			dest = parts[0]
			jump = ''

		#jmps
		if ';' in line:
			parts = line.split(';')
			comp = parts[0]
			dest = ''
			jump = parts[1]

		#get binary stored in dictionaries of SymbolConverter
		try:
			comp_cmd = self.symbols._comp[comp]
			dest_cmd = self.symbols._dest[dest]
			jump_cmd = self.symbols._jump[jump]
		except:
			print("Error on line: " + line)

		binary = '111' + comp_cmd + dest_cmd + jump_cmd
		return binary


	# Indexes and removes labels
	def first_pass(self, code):

		tmp = []
		index = 0

		for line in code:
			if line[0] == '(' and line[-1] == ')':
				var = line[1:-1]
				self.symbols._var[var] = index
				
			else:
				index += 1
				tmp.append(line)
			
		return tmp


if __name__ == "__main__":

	args = sys.argv

	infile = args[1]
	outfile = args[2]

	assembler = Assembler()

	machineCode = StripFile.StripFile(infile).strip_file()
	machineCode = assembler.first_pass(machineCode)

	binaryCMDs = []
	for line in machineCode:
		#check if a instruction
		if line[0] == '@':
			command = assembler.a_instruction(line)
			binaryCMDs.append(command)
		
		#o/w a c instruction
		else:
			command = assembler.c_instruction(line)
			binaryCMDs.append(command)
			

	outfile = open(outfile, 'w')
	for command in binaryCMDs:
		outfile.write(command + '\n')
	outfile.close()








