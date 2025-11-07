from dataclasses import dataclass
from typing import List

import math

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	return data

@dataclass
class Snaildigit:
	value: int
	depth: int

@dataclass
class Snailnumber:
	digits: List[Snaildigit]

	def __str__(self):
		return " ".join([str((digit.value, digit.depth)) for digit in self.digits])

	def add(self, snailnumber):
		for idx, _ in enumerate(self.digits):
			self.digits[idx].depth += 1

		for idx, _ in enumerate(snailnumber.digits):
			snailnumber.digits[idx].depth += 1

		self.digits += snailnumber.digits

	def reduce(self):
		while self.try_explode() or self.try_split():
			pass

	def magnitude(self):
		max_depth = max([digit.depth for digit in self.digits])
		magnitude_digits = self.digits.copy()

		for depth in reversed(range(max_depth + 1)):
			idx = len(magnitude_digits) - 1
			right = None
			while idx >= 0:
				digit = magnitude_digits[idx] 
				if digit.depth == depth:
					if right is None:
						right = digit

					else:
						magnitude_digits.pop(idx)
						magnitude_digits.pop(idx)
						new_digit = Snaildigit(3*digit.value+2*right.value, depth-1)
						magnitude_digits.insert(idx, new_digit)
						right = None

				idx -= 1

		return magnitude_digits[0].value

	def try_explode(self):
		for idx, left_digit in enumerate(self.digits):
			if left_digit.depth > 4:
				right_digit = self.digits[idx+1]

				if idx != 0:
					self.digits[idx-1].value += left_digit.value

				if idx+2 < len(self.digits):
					self.digits[idx+2].value += right_digit.value

				self.digits.pop(idx)
				self.digits.pop(idx)
				self.digits.insert(idx, Snaildigit(0, left_digit.depth-1))
				return True

		return False

	def try_split(self):
		for idx, digit in enumerate(self.digits):
			# print(digit)
			if digit.value >= 10:
				left_digit = Snaildigit(math.floor(digit.value / 2), digit.depth+1)
				right_digit = Snaildigit(math.ceil(digit.value / 2), digit.depth+1)

				self.digits.pop(idx)
				self.digits.insert(idx, right_digit)
				self.digits.insert(idx, left_digit)
				return True

		return False

def to_snaildigits(string):
	snaildigits = list()
	
	depth = 0
	last_number_string = ""
	for char in string:
		if char.isdigit():
			last_number_string += char
		else:
			if last_number_string:
				snaildigits.append(Snaildigit(int(last_number_string), depth))
				last_number_string = ""

		if char == "[":
			depth += 1
		elif char == "]":
			depth -= 1
	
	return snaildigits

def test_operators():
	pass
	# explode = get_data("explode_examples.txt")
	# for string in explode:
	# 	snaildigits = to_snaildigits(string)
	# 	snailnumber = Snailnumber(snaildigits)
	# 	print(snailnumber)
	# 	snailnumber.try_explode()
	# 	print(snailnumber)
	# 	print()

	# split = get_data("split_examples.txt")
	# for string in split:
	# 	snaildigits = to_snaildigits(string)
	# 	snailnumber = Snailnumber(snaildigits)
	# 	print(string)
	# 	print(snailnumber)
	# 	snailnumber.try_split()
	# 	print(snailnumber)

	# sums = get_data("sum_examples.txt")
	# for string in sums:
	# 	snaildigits = to_snaildigits(string)
	# 	snailnumber = Snailnumber(snaildigits)
	# 	print(snailnumber)
	# 	while snailnumber.try_explode() or snailnumber.try_split():
	# 		pass
	# 	print(snailnumber)
	# 	print()

	# a = Snailnumber(to_snaildigits("[[[[4,3],4],4],[7,[[8,4],9]]]"))
	# b = Snailnumber(to_snaildigits("[1,1]"))

	# print(a)
	# print(b)
	# a.add(b)
	# print(a)
	# a.reduce()
	# print(a)

	# mags = get_data("magnitude_examples.txt")
	# for string in mags:
	# 	snailnumber = Snailnumber(to_snaildigits(string))
	# 	print(string)
	# 	print(snailnumber.magnitude())

def part_one():
	data = get_data("input.txt")
	snailnumber = Snailnumber(to_snaildigits(data[0]))
	for string in data:
		new = Snailnumber(to_snaildigits(string))
		snailnumber.add(new)
		snailnumber.reduce()

	print(snailnumber)
	print(snailnumber.magnitude())

def part_two():
	data = get_data("input.txt")
	max_magnitude = 0

	for first_string in data:
		for second_string in data:
			if first_string != second_string:
				first = Snailnumber(to_snaildigits(first_string))
				second = Snailnumber(to_snaildigits(second_string))

				first.add(second)
				first.reduce()
				max_magnitude = max(max_magnitude, first.magnitude())

				first = Snailnumber(to_snaildigits(first_string))
				second = Snailnumber(to_snaildigits(second_string))

				second.add(first)
				second.reduce()
				max_magnitude = max(max_magnitude, second.magnitude())

	print(max_magnitude)

if __name__ == '__main__':
	# test_operators()
	# part_one()
	part_two()