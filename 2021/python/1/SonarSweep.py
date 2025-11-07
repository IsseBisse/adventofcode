def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	return data

def parse_data(data):
	return [int(line) for line in data]

def check_num_increases(depths):
	prev_depth = None
	num_increases = 0
	for curr_depth in depths:
		if prev_depth is not None:
			num_increases += 1 if curr_depth > prev_depth else 0

		prev_depth = curr_depth

	return num_increases

def part_one():
	data = get_data("input.txt")
	depths = parse_data(data)

	num_increases = check_num_increases(depths)
	print(num_increases)
	
def check_sliding_sum_increase(depths):
	prev_sum = None
	num_increases = 0
	for i in range(len(depths) - 2):
		curr_sum = sum(depths[i:i+3])
		if prev_sum is not None:
			num_increases += 1 if curr_sum > prev_sum else 0

		prev_sum = curr_sum

	return num_increases

def part_two():
	data = get_data("input.txt")
	depths = parse_data(data)

	num_increases = check_sliding_sum_increase(depths)
	print(num_increases)

if __name__ == '__main__':
	part_one()
	part_two()