import numpy as np
from scipy.signal import convolve2d

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	return data

def parse_data(data, dim):
	lights = np.zeros(dim)

	for row, line in enumerate(data):
		for col, char in enumerate(line):
			lights[row, col] = char == "#"

	return lights

def pretty_printer(lights):
	string = ""
	for row in range(lights.shape[0]):
		for col in range(lights.shape[1]):
			char = "#" if lights[row, col] else "."
			string += char

		string += "\n"

	print(string)

def one_step(lights):
	neighbor_pattern = np.ones((3,3))
	neighbor_pattern[1,1] = 0

	neighbors = convolve2d(lights, neighbor_pattern, "same")
	on_condition = np.logical_or(neighbors==2, neighbors==3)
	off_condition = neighbors==3

	new_lights = np.zeros(lights.shape)
	new_lights[lights == 0] = off_condition[lights == 0]
	new_lights[lights == 1] = on_condition[lights == 1]

	return new_lights

def part_one():
	# data = get_data("smallInput.txt")
	# dim = (6, 6)
	data = get_data("input.txt")
	dim = (100, 100)

	lights = parse_data(data, dim)
	# print(f"Initial state:")
	# pretty_printer(lights)

	num_steps = 100
	for step in range(num_steps):
		lights = one_step(lights)
		# print(f"After {step+1} steps:")
		# pretty_printer(lights)

	print(np.sum(lights))

def add_stuck_lights(lights):
	lights[0, 0] = 1
	lights[0, -1] = 1
	lights[-1, 0] = 1
	lights[-1, -1] = 1

def part_two():
	# data = get_data("smallInput.txt")
	# dim = (6, 6)
	data = get_data("input.txt")
	dim = (100, 100)

	lights = parse_data(data, dim)
	add_stuck_lights(lights)
	# print(f"Initial state:")
	# pretty_printer(lights)

	# num_steps = 5
	num_steps = 100
	for step in range(num_steps):
		lights = one_step(lights)
		add_stuck_lights(lights)
		# print(f"After {step+1} steps:")
		# pretty_printer(lights)

	print(np.sum(lights))

if __name__ == '__main__':
	part_one()
	part_two()