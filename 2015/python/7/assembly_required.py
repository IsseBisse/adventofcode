import re

"""
Helpers
"""
def get_data(path):

	with open(path) as file:
		return file.read().split("\n")

def parse_line(string):
	expression, output = string.split(" -> ")

	op_matches = re.findall(r"[A-Z]+", expression)
	if len(op_matches) == 0:
		op = "NOP"

	else:
		op = op_matches[0]

	args = re.findall(r"[a-z]+", expression)
	int_args = [int(arg) for arg in re.findall(r"[0-9]+", expression)]

	return op, args + int_args, output

ops = {"NOP": lambda a: a,
	"NOT": lambda a: ~a & 0xFFFF,
	"AND": lambda a, b: a & b,
	"OR": lambda a, b: a | b,
	"LSHIFT": lambda a, b: a << b,
	"RSHIFT": lambda a, b: a >> b}

def only_numbers(string):
	return all([char.isdigit() for char in string])

def get_outputs(data):
	outputs = dict()
	num_outputs = len(data)

	while len(outputs) != num_outputs:
	# Loop over copy to allow removing lines
		for line in list(data):
			op, args, output_name = parse_line(line)

			if all([(arg in outputs.keys() or isinstance(arg, int)) for arg in args]):
				print(op, args)

				args = [key if isinstance(key, int) else outputs[key] for key in args]
				print(args)
				outputs[output_name] = ops[op](*args)
				data.remove(line)

	return outputs

"""
Part one
"""
def part_one():
	data = get_data("input.txt")
	print(data)

	outputs = get_outputs(data)
	for key, value in outputs.items():
		print(key, value)
	
"""
Part two
"""
def part_two():
	data = get_data("modifiedInput.txt")
	print(data)

	outputs = get_outputs(data)
	for key, value in outputs.items():
		print(key, value)

if __name__ == '__main__':
	part_one()
	part_two()