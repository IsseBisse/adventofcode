import re

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	return data

def part_one():
	data = get_data("input.txt")
	
	length_diff = sum([len(line) - len(eval(line)) for line in data])
	print(length_diff)

def calculate_length_diff(data):
	diffs = list()
	encoded_data = [line.encode("unicode_escape") for line in data]
	
	for i, line in enumerate(encoded_data):
		quote_matches = re.findall(r"\"", str(line))
		encoded_length = len(line) + len(quote_matches) + 2

		diffs.append(encoded_length - len(data[i]))

	return diffs

def part_two():
	data = get_data("input.txt")

	diffs = calculate_length_diff(data)
	print(diffs)
	print(sum(diffs))


if __name__ == '__main__':
	#part_one()
	part_two()