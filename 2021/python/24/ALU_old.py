import pandas as pd

def parse(row):
	parts = row.split(" ")
	
	command = parts[0]
	args = tuple([int(part) if part.lstrip("-").isdigit() else part for part in parts[1:]])

	return command, args

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	code = list(map(parse, data))

	return code

class ALU:
	def __init__(self, code, input_=None):
		self.code = code
		self.code_ptr = 0
		self.input = input_
		
		self.register = {"w": 0, "x": 0, "y": 0, "z": 0}

	def __str__(self):
		return str(self.register)

	def __get_value(self, a):
		if isinstance(a, int):
			return a
		elif isinstance(a, str):
			return self.register[a]

	def inp(self, a):
		self.register[a] = self.input.pop(0)

	def add(self, a, b):
		self.register[a] = self.register[a] + self.__get_value(b)

	def mul(self, a, b):
		self.register[a] = self.register[a] * self.__get_value(b)

	def div(self, a, b):
		if self.__get_value(b) == 0:
			raise NotImplementedError("Cannot divide by 0!")
		self.register[a] = self.register[a] // self.__get_value(b)

	def mod(self, a, b):
		if self.register[a] < 0 or self.__get_value(b) <= 0:
			raise NotImplementedError("Invalid modulus!")
		self.register[a] = self.register[a] % self.__get_value(b)

	def eql(self, a, b):
		self.register[a] = 1 if self.register[a] == self.__get_value(b) else 0

	# def run(self):
	# 	for command, args in self.code:
	# 		func = getattr(self, f"{command}")
	# 		func(*args)

	# def run_lines(self, start, end):
	# 	for command, args in self.code[start:end]:
	# 		func = getattr(self, f"{command}")
	# 		func(*args)
	# 		# print(command, args)
	# 		# print(self)

	def copy(self):
		pass	# TODO:

	def run(self, num_lines):
		for _ in range(num_lines):
			command, args = self.code[self.code_ptr]
			func = getattr(self, f"{command}")
			func(*args)
			self.code_ptr += 1

# def one_run(code, digits):
# 	alu = ALU(code, [])
# 	# x_adds = [item[1][1] for item in alu.code[5::18]]

# 	for i in range(14):
# 		start = 18*i
# 		end = 18*(i+1)

# 		next_digit = digits.pop(-1)

# 		# Replace if better value is available
# 		next_chunk = alu.code[start:end]
# 		next_x_add = next_chunk[5][1][1]
# 		if next_x_add < 0:
# 		alu.input.append(next_digit)
# 		alu.run_lines(start, end)

# 	return alu.register["z"]

def run_until_negative_add(code, digits):
	alu = ALU(code, digits)
	num_lines = 18*len(digits)
	alu.run(num_lines)

	next_chunk = alu.code[num_lines:num_lines+18]
	next_x_add = next_chunk[5][1][1]
	best_w = alu.register["z"] % 26 + next_x_add
	
	if 1 <= best_w <= 9:
		return best_w

	else:
		return None
		
def find_digits(alu):
	
	while:
		digit = 9
		alu = alu.run_chunk(digit)
		if alu is not None:
			if alu.finished:
				return [digit] 

			else:
				digits = find_digits(alu.copy())

		digit -= 1
		if digit == 0:
			# Done trying for this digit, move up one step
			return None



def part_one():
	code = get_data("input.txt")
	
	# x_adds = [item[1][1] for item in alu.code[5::18]]
	num_digits = 3
	digit_chunk = 10**(3+1)-1

	chunk_found = False
	while not chunk_found:
		best_w = run_until_negative_add(code, [int(char) for char in str(digit_chunk)])
		if best_w is not None:
			break

		digit_chunk -= 1

	print(digit_chunk, best_w)

	alu = ALU(code, [9, 9, 3, 9])
	alu.run(18*4)
	print(alu)
	return


def part_two():
	code = get_data("input.txt")

if __name__ == '__main__':
	part_one()
	# part_two()

	# # NOTE: Code repeats every 18 rows with slight variations
	# # NOTE: Lots of div/mod 26. Alphabet-related? 
	# code = get_data("input.txt")
	# row_types = list()
	# for start in range(18):
	# 	lines = code[start::18]
	# 	lines = list(set(lines)) if len(set(lines)) == 1 else lines
	# 	row_types.append(lines)

	# for row in row_types:
	# 	print(row)