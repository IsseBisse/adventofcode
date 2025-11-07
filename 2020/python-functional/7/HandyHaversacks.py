import re

def parse_container(container):
	number = int(re.findall(r"[0-9]+", container)[0])
	color = re.findall(r" ([a-z ]+) bag", container)[0]

	return number, color

def parse_line(string):
	first = re.findall(r"^([a-z ]+) bags contain", string)[0]
	contains_string = re.findall(r"([0-9]+ [a-z ]+ bag)+", string)
	contents = tuple(map(parse_container, contains_string))

	return first, contents 

def get_data(path):
	with open(path) as file:
		raw_data = file.read().split("\n")

	data = map(parse_line, raw_data)

	return tuple(data)


def part_one():
	data = get_data("smallInput.txt")
	print(data)



def part_two():
	pass

if __name__ == '__main__':
	part_one()