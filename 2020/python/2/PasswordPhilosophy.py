import re

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	for i, entry in enumerate(data):
		char = re.findall(r"[a-z]:", entry)[0][0]
		password = re.findall(r"[a-z]+", entry)[1]
		
		limits = re.findall(r"[0-9]+", entry) 
		char_min = int(limits[0])
		char_max = int(limits[1])
		
		data[i] = {"password": password, "char": char, "min": char_min, "max": char_max}

	return data

def part_one():
	data = get_data("input.txt")

	num_valid_passwords = 0
	for entry in data:
		occurances = entry["password"].count(entry["char"])
		valid = occurances <= entry["max"] and occurances >= entry["min"]

		num_valid_passwords += 1 if valid else 0
		
	print(num_valid_passwords)

def part_two():
	data = get_data("input.txt")

	num_valid_passwords = 0
	for entry in data:
		valid = False
		
		match = entry["password"][entry["min"]-1] == entry["char"]
		valid = valid != match
		match = entry["password"][entry["max"]-1] == entry["char"]
		valid = valid != match

		num_valid_passwords += 1 if valid else 0

	print(num_valid_passwords)

if __name__ == '__main__':
	part_two()