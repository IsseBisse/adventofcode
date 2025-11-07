def get_data(path):
	with open(path) as file:
		raw_data = file.read().split("\n")

	data = map(int, raw_data)

	return tuple(data)

def part_one():
	pass
	
def part_two():
	pass

if __name__ == '__main__':
	part_one()