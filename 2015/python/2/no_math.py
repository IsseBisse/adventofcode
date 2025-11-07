def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	for i, entry in enumerate(data[:-1]):
		parsed_entry = entry.split("x")
		data[i] = tuple([int(num) for num in parsed_entry])

	return data[:-1]

def calculate_paper(dim):

	[w, h, l] = dim
	sorted_dim = sorted(dim)

	return 2*l*w + 2*w*h + 2*h*l + sorted_dim[0]*sorted_dim[1]

def part_one():
	data = get_data("input.txt")

	paper = [calculate_paper(dim) for dim in data]
	print("Total amount of paper: %d" % sum(paper))
	

def calculate_ribbon(dim):

	[w, h, l] = dim
	sorted_dim = sorted(dim)

	return l*w*h + 2*sorted_dim[0] + 2*sorted_dim[1]

def part_two():
	data = get_data("input.txt")

	paper = [calculate_ribbon(dim) for dim in data]
	print("Total amount of ribbon: %d" % sum(paper))

if __name__ == '__main__':
	#part_one()
	part_two()