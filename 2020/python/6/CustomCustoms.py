def get_data(path):
	with open(path) as file:
		data = file.read().split("\n\n")

	for i, entry in enumerate(data):
		data[i] = entry.split("\n")

	return data

def part_one():
	data = get_data("input.txt")
	
	total_sum = 0
	for i, entry in enumerate(data):
		temp = "".join(entry)
		temp = set(temp)

		total_sum += len(temp)

	print(total_sum)
	
def part_two():
	data = get_data("input.txt")
	
	total_sum = 0
	for i, group in enumerate(data):
		intersect = set(group[0])

		for entry in group:
			intersect &= set(entry)

		total_sum += len(intersect)

	print(total_sum)

if __name__ == '__main__':
	#part_one()
	part_two()