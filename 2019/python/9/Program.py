class Program:

	def __init__(self, memory_size):
		
		self.code = [0] * memory_size
		self.p = 0
		self.done = False
		self.relative_base = 0
		
		self.input_ = []
		self.output = []

	'''
	Operations
	'''
	def add(self, a, b, res_pos):
		self.code[res_pos] = self.code[a] + self.code[b]

	def mult(self, a, b, res_pos):
		self.code[res_pos] = self.code[a] * self.code[b]

	def input_(self, pos):
		self.code[pos] = self.input_.pop()

	def output(self, pos):
		self.output.append(self.code[pos])

	def jt(self, pos, new_p):
		if self.code[pos] != 0:
			self.p = self.code[new_p] - (self.INSTRUCTIONS[5]["n_arg"] + 1)

	def jf(self, pos, new_p):
		if self.code[pos] == 0:
			self.p = self.code[new_p] - (self.INSTRUCTIONS[6]["n_arg"] + 1)

	def lt(self, a, b, pos):
		if self.code[a] < self.code[b]:
			self.code[pos] = 1
		else:
			self.code[pos] = 0

	def eq(self, a, b, pos):
		if self.code[a] == self.code[b]:
			self.code[pos] = 1
		else:
			self.code[pos] = 0

	def base(self, pos):
		self.relative_base = self.code[pos]

	INSTRUCTIONS = {1: {"func": add, "n_arg": 3},
	2: {"func": mult, 	"n_arg": 3},
	3: {"func": input_, "n_arg": 1},
	4: {"func": output, "n_arg": 1},
	5: {"func": jt, 	"n_arg": 2},
	6: {"func": jf, 	"n_arg": 2},
	7: {"func": lt, 	"n_arg": 3},
	8: {"func": eq, 	"n_arg": 3},
	9: {"func": base,	"n_arg": 1},
	99: {"func": "b", 	"n_arg": 0}}

	'''
	Main functions
	'''
	def interpret(self):
		# Extract opcode
		opcode = self.code[self.p]
		opcode_string = "%05d" % opcode
		is_positive = opcode > 0
		command = int(opcode_string[-2:])


		if command in self.INSTRUCTIONS:
			parameter_modes = [int(x) for x in reversed(opcode_string[:-2])]
			parameter_modes = parameter_modes[:self.INSTRUCTIONS[command]["n_arg"]]

		else:
			print("Invalid command: %d" % command)
			raise NotImplementedError

		return command, parameter_modes

	def execute(self, command, parameter_modes):
		# Get parameters
		params = []
		param_p = self.p + 1

		for i in range(self.INSTRUCTIONS[command]["n_arg"]):
			if parameter_modes[i] == 0:
				params.append(self.code[param_p])

			elif parameter_modes[i] == 1:
				params.append(param_p)

			else:
				params.append(self.code[param_p] + self.relative_base)

			param_p += 1

		func = self.INSTRUCTIONS[command]["func"]
		print(func, params, self.relative_base)

		func(self, *params)

	def load_code(self, path):

		f = open(path, "r")
		code = [int(x) for x in  f.read().split(",")]
		self.code[:len(code)] = code

	def load_input(self, input_):

		self.input_ = input_

	def get_output(self):
		
		return self.output

	def reset(self):

		self.p = 0

	def is_done(self):

		return self.done

	def run(self):

		if not self.code:
			print("No code loaded!")

		while True:	
			command, parameter_modes = self.interpret()
			print(command, parameter_modes)

			if command == 99:
				self.done = True
				break

			self.execute(command, parameter_modes)
			self.p += self.INSTRUCTIONS[command]["n_arg"] + 1