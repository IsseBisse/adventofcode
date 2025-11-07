import numpy as np
from scipy.signal import convolve2d

def get_data(path):
	with open(path) as file:
		data = file.read()

	return data

def parse_data(data):
	matrix = [[int(item) for item in row] for row in data.split("\n")]
	return np.array(matrix)

def one_step(matrix):
	matrix = matrix + np.ones(matrix.shape)

	flashes = np.zeros(matrix.shape, dtype=bool)
	while (np.multiply(matrix, ~flashes) > 9).any():
		new_flashes = np.multiply(matrix, ~flashes) > 9
		flash_addition = convolve2d(new_flashes, np.ones((3,3)), "same")
		matrix = matrix + flash_addition

		flashes = flashes + new_flashes
		
	matrix = np.multiply(matrix, matrix < 10)

	return matrix, np.sum(flashes)

def part_one():
	data = get_data("input.txt")
	matrix = parse_data(data)

	num_steps = 100
	num_flashes = 0
	for i in range(num_steps):
		matrix, flashes = one_step(matrix)
		num_flashes += flashes

	print(f"{num_flashes} flashes after {num_steps} steps")

def part_two():
	data = get_data("input.txt")
	matrix = parse_data(data)

	max_num_flashes = 0
	num_sync_flashes = matrix.size
	steps = 0
	while max_num_flashes < num_sync_flashes:
		matrix, flashes = one_step(matrix)

		if flashes > max_num_flashes:
			max_num_flashes = flashes

		steps += 1

	print(f"Synchronized after {steps} steps")

if __name__ == '__main__':
	part_one()
	part_two()