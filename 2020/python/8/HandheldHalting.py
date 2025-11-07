import copy

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	code = list()
	for entry in data:
		command = entry.split(" ")[0]
		value = int(entry.split(" ")[1])
		
		code.append((command, value))

	return code

class Program:
	def __init__(self, code):
		self.code = code
		self.accumulator = 0
		self.instruction_p = 0
		self.executed_instructions = list()

	def run(self):
		while self.instruction_p < len(self.code):
			if self.instruction_p in self.executed_instructions:
				return 1	# exit code == infinite loop

			self.executed_instructions.append(self.instruction_p)
			command, value = self.code[self.instruction_p]

			#print("%d: %s %d" % (self.instruction_p, command, value))
			function = getattr(self, command)
			function(value)

			self.instruction_p += 1

		return 0	# exit code == success

	def get_acc(self):
		return self.accumulator

	def nop(self, value):
		pass

	def jmp(self, value):
		self.instruction_p += value-1

	def acc(self, value):
		self.accumulator += value

def part_one():
	code = get_data("input.txt")
	program = Program(code)

	res = program.run()
	print("Acc: %d" % program.get_acc())

def change_command(line):
	command, value = line

	if command == "nop":
		return ("jmp", value)
	elif command == "jmp":
		return ("nop", value)		

def part_two():
	ORIGINAL_CODE = get_data("input.txt")
	
	possible_error_indicies = list()
	for i, line in enumerate(ORIGINAL_CODE):
		command = line[0]
		if command == "nop" or command == "jmp":
			possible_error_indicies.append(i)

	for i in possible_error_indicies:
		code = copy.deepcopy(ORIGINAL_CODE)
		code[i] = change_command(code[i])
		program = Program(code)

		res = program.run()
		if res == 0:
			print("Acc: %d" % program.get_acc())
			break

if __name__ == '__main__':
	#part_one()
	part_two()