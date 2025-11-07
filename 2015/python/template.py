def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	for i, entry in enumerate(data):
		data[i] = int(entry)

	return data

def part_one():
	pass
	
def part_two():
	pass

if __name__ == '__main__':
	part_one()