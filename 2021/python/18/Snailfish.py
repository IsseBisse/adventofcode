import ast
from dataclasses import dataclass

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	data = [ast.literal_eval(string) for string in data]

	return data

@dataclass
class SnailNumber:
	left: object
	right: object
	depth: int

# def replace(string, idx, replace_string)

def try_explode(snail_sum):
	snail_string = str(snail_sum)
	left_idx = None
	nest_counter = 0
	for idx, char in enumerate(snail_string):
		if char == "[":
			nest_counter += 1
		elif char == "]":
			nest_counter -= 1
		elif char.isdigit():
			left_idx = idx

		if nest_counter > 4 and char not in {"[", "]"}:

			print(char)


	

def try_split(snail_sum):
	pass

def snail_add(x, y):
	snail_sum = [x, y]

	# Reduce
	try_explode(snail_sum)

def test_operators():
	explode = get_data("explode_examples.txt")

	for example in explode:
		try_explode(example)

def part_one():
	data = get_data("smallInput.txt")

	print(data[1])

def part_two():
	data = get_data("smallInput.txt")

if __name__ == '__main__':
	test_operators()
	# part_one()
	# part_two()