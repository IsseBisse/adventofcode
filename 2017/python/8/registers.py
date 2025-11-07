import operator

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	data = [tuple(row.split(" ")) for row in data]

	return data

class Register:
	ops = {
		">": operator.gt,
		"<": operator.lt,
		">=": operator.ge,
		"<=": operator.le,
		"==": operator.eq,
		"!=": operator.ne,
	}

	def __init__(self):
		self.registers = dict()
		self.highest_register_ever = 0

	def __str__(self):
		return str(self.registers)

	def max_register(self):
		return max([value for _, value in self.registers.items()])

	def max_ever_register(self):
		return self.highest_register_ever

	def execute(self, command):
		incr_reg, incr, incr_value, _, comp_reg, comp_op, comp_value = command

		for reg in (incr_reg, comp_reg):
			if reg not in self.registers:
				self.registers[reg] = 0

		incr_value = int(incr_value)
		comp_value = int(comp_value)
		incr_factor = 1 if incr == "inc" else -1

		if self.ops[comp_op](self.registers[comp_reg], comp_value):
			self.registers[incr_reg] += incr_factor*incr_value

		max_register = self.max_register()
		self.highest_register_ever = max_register if max_register > self.highest_register_ever else self.highest_register_ever

def part_one():
	data = get_data("input.txt")
	
	register = Register()
	for command in data:
		register.execute(command)
	
	print(register.max_register())
	
def part_two():
	data = get_data("input.txt")
	register = Register()
	for command in data:
		register.execute(command)
	
	print(register.max_ever_register())

if __name__ == '__main__':
	part_one()
	part_two()