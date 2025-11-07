import re
from functools import reduce

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	return data

def split_string(string):
	parts = string.split(" ")
	while "" in parts:
		parts.remove('')

	return parts

def parse_string(string):

	parenthesis_level = 0
	starts = list()
	ends = list()
	
	for i, char in enumerate(string):
		if char == "(":
			parenthesis_level += 1

			if parenthesis_level == 1:
				starts.append(i)

		elif char == ")":
			parenthesis_level -= 1

			if parenthesis_level == 0:
				ends.append(i+1)

	if len(starts) != 0:
		parts = list()
		for i, start in enumerate(starts):
			prev_end = 0 if i==0 else ends[i-1]
			end = ends[i]

			parts += split_string(string[prev_end:start])
			parts += parse_string(string[start+1:end-1])

		parts += split_string(string[end:])
		if "" in parts:
			parts.remove("")

		return [parts]

	else:
		return [split_string(string)] 

def my_eval(expression):
	value = expression[0]
	if isinstance(value, list):
		value = my_eval(value)

	else:
		value = int(value)

	for symbol_ind in range(1, len(expression), 2):
		symbol = expression[symbol_ind]
		next_term = expression[symbol_ind+1]

		if isinstance(next_term, list):
			next_term = my_eval(next_term)

		else:
			next_term = int(next_term)

		value = eval("%d%s%d" % (value, symbol, next_term))

	return value
 
def my_eval_two(expression):
	value = expression[0]
	if isinstance(value, list):
		value = my_eval(value)

	else:
		value = int(value)

	# Evaluate parenthesis
	for i, term in enumerate(expression):
		if isinstance(term, list):
			expression[i] = "%d" % my_eval_two(term)

	# Evaluate addition
	addition_string = "".join(expression)
	sum_parts = [[int(num) for num in part.split("+")] for part in addition_string.split("*")]
	factors = [sum(part) for part in sum_parts]
	
	product = reduce((lambda x, y: x*y), factors)

	return product

def evaluate_line(line, is_part_two=False):
	parsed_string = parse_string(line)[0]
	if is_part_two:
		value = my_eval_two(parsed_string)

	else:
		value = my_eval(parsed_string)

	return value
	
def part_one():
	data = get_data("input.txt")

	sum_values = 0
	for line in data:
		value = evaluate_line(line)	
		sum_values += value

	print("Sum is: %d" % sum_values)

def part_two():
	data = get_data("input.txt")

	sum_values = 0
	for line in data:
		value = evaluate_line(line, is_part_two=True)
		#print(line, value)
		sum_values += value

	print("Sum is: %d" % sum_values)


if __name__ == '__main__':
	#part_one()
	part_two()