import numpy as np

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	data = tuple(int(row) for row in data)

	return data

def has_depth_increase(current_depth, previous_depth):
	return current_depth - previous_depth > 0

def part_one():
	data = get_data("input.txt")

	depth_increases = map(has_depth_increase, data[1:], data[:-1])
	num_depth_increases = sum(depth_increases)

	print(num_depth_increases)

def part_two():
	data = get_data("input.txt")

	window_length = 3
	average_depth = np.convolve(data, np.ones(window_length), "valid")
	depth_increases = map(has_depth_increase, average_depth[1:], average_depth[:-1])
	num_depth_increases = sum(depth_increases)
	
	print(num_depth_increases)

if __name__ == '__main__':
	part_one()
	part_two()