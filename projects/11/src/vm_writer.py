class VMWriter(object):

	def __init__(self,output):
		self.outfile = open(output, 'w')

	def write_push(self, segment, index):
		self.outfile.write('push ' + segment + ' ' + str(index) + '\n')

	def write_pop(self, segment, index):
		self.outfile.write('pop ' + segment + ' ' + str(index) + '\n')

	def write_arithmetic(self, command):
		self.outfile.write(command + '\n')

	def write_label(self, label):
		self.outfile.write('label ' + label +'\n')

	def write_goto(self, label):
		self.outfile.write('goto ' + label + '\n')

	def write_if(self, label):
		self.outfile.write('if-goto ' + label + '\n')

	def write_call(self, name, nArgs):
		self.outfile.write('call ' + name + ' ' + str(nArgs) + '\n')

	def write_function(self, name, nLocals):
		self.outfile.write('function ' + name + ' ' + str(nLocals) + '\n')

	def write_return(self):
		self.outfile.write('return\n')

	def close(self):
		self.outfile.close()