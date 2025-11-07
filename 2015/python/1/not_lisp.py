def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	return data

def part_one():
	data = get_data("input.txt")

	floor = 0
	for char in data[0]:
		floor += 1 if char == "(" else -1

	print("End floor is: %d" % floor)
	
def part_two():
	data = get_data("input.txt")

	floor = 0
	for i, char in enumerate(data[0]):
		floor += 1 if char == "(" else -1

		if floor == -1:
			position = i+1
			break

	print("-1 floor position is: %d" % position)

if __name__ == '__main__':
	#part_one()
	part_two()