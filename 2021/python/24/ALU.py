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
	def __init__(self, code):
		self.code = code
		self.code_ptr = 0
		self.next_input = None
		self.finished = False
		
		self.register = {"w": 0, "x": 0, "y": 0, "z": 0}

	def __str__(self):
		return str(self.register)

	def __get_value(self, a):
		if isinstance(a, int):
			return a
		elif isinstance(a, str):
			return self.register[a]

	def add_input(self, input_):
		self.next_input = input_

	def inp(self, a):
		self.register[a] = self.next_input
		self.next_input = None

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

	def copy(self):
		alu = ALU(self.code[self.code_ptr:])
		alu.next_input = self.next_input
		alu.register = self.register.copy()

		return alu

	def is_finished(self):
		return self.code_ptr == len(self.code)

	def run(self, input_):
		decreasing_chunk = False
		z_decreased = False
		
		self.next_input = input_
		for idx in range(18):
			command, args = self.code[self.code_ptr]
			# Decreasing chunk (x should equal w at line 6)
			if idx == 5 and args[1] < 0:
				decreasing_chunk = True
			func = getattr(self, f"{command}")
			func(*args)
			if decreasing_chunk and idx == 6:
				z_decreased = self.register["x"] == 1
			self.code_ptr += 1 

		if decreasing_chunk == z_decreased:
			return self
		else:
			return None


def find_largest_digit(alu):
	digit = 9
	while True:
		new_alu = alu.copy()
		new_alu = new_alu.run(digit)

		if new_alu is not None:
			if new_alu.is_finished():
				return [digit]

			else:
				digits = find_largest_digit(new_alu)
				if digits is not None:
					digits = [digit] + digits
					return digits

		digit -= 1
		if digit == 0:
			return None

def part_one():
	code = get_data("input.txt")
	alu = ALU(code)

	digits = find_largest_digit(alu)
	print("".join([str(digit) for digit in digits]))

def find_smallest_digit(alu):
	digit = 1
	while True:
		new_alu = alu.copy()
		new_alu = new_alu.run(digit)

		if new_alu is not None:
			if new_alu.is_finished():
				return [digit]

			else:
				digits = find_smallest_digit(new_alu)
				if digits is not None:
					digits = [digit] + digits
					return digits

		digit += 1
		if digit == 10:
			return None

def part_two():
	code = get_data("input.txt")
	alu = ALU(code)

	digits = find_smallest_digit(alu)
	print("".join([str(digit) for digit in digits]))

if __name__ == '__main__':
	part_one()
	part_two()