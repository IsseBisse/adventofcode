from re import findall
from json import loads

def get_data(path):
	with open(path) as file:
		data = file.read()

	return data

def part_one():
	data = get_data("input.txt")

	numbers = [int(match) for match in findall(r"[\-0-9]+", data)]
	print(sum(numbers))
	
def parse_object(obj, included_objects):
	if isinstance(obj, list):
		for item in obj:
			parse_object(item, included_objects)

	elif isinstance(obj, dict):
		if not any(item == "red" for item in obj.values()):
			for item in obj.values():
				parse_object(item, included_objects)

	else:
		# Value
		included_objects.append(obj)

def part_two():
	json_data = loads(get_data("input.txt"))

	included_objects = list()
	parse_object(json_data, included_objects)

	# Sort out ints
	int_objects = [item for item in included_objects if isinstance(item, int)]
	print(sum(int_objects))

	"""
	for data_string in get_data("smallInput2.txt").split("\n"):
		json_data = loads(data_string)

		included_objects = list()
		parse_object(json_data, included_objects)

		# Sort out ints
		int_objects = [item for item in included_objects if isinstance(item, int)]

		print(json_data)
		print(included_objects)
		print(int_objects)
		print(sum(int_objects))
		print("")
	"""



if __name__ == '__main__':
	# part_one()
	part_two()