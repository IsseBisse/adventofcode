from re import findall
from operator import lt, eq, gt

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	return data

def parse_data(data):
	sues = list()
	for line in data:
		attributes = findall(r"(\w+): (\d)", line)
		attributes = [(item[0], int(item[1])) for item in attributes]
		sues.append(dict(attributes))

	return sues

def match_correct_sue(sue):
	CORRECT_SUE = {"children": 3, "cats": 7, "samoyeds": 2, "pomeranians": 3, "akitas": 0, "vizslas": 0, "goldfish": 5, "trees": 3, "cars": 2, "perfumes": 1}
	return all([sue[key] == CORRECT_SUE[key] for key in sue])

def part_one():
	data = get_data("input.txt")
	sues = parse_data(data)
	
	for i, sue in enumerate(sues):
		if match_correct_sue(sue):
			print(sue, i+1)

def updated_match_correct_sue(sue):
	CORRECT_SUE = {"children": 3, "cats": 7, "samoyeds": 2, "pomeranians": 3, "akitas": 0, "vizslas": 0, "goldfish": 5, "trees": 3, "cars": 2, "perfumes": 1}
	
	for key in sue:
		if key in ["cats", "trees"]:
			op = gt
		elif key in ["pomeranians", "goldfish"]:
			op = lt
		else:
			op = eq

		if not op(sue[key], CORRECT_SUE[key]):
			return False

	return True

def part_two():
	data = get_data("input.txt")
	sues = parse_data(data)
	
	for i, sue in enumerate(sues):
		if updated_match_correct_sue(sue):
			print(sue, i+1)

if __name__ == '__main__':
	part_one()
	part_two()