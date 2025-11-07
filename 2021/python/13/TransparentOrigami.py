import numpy as np
import re

def get_data(path):
	with open(path) as file:
		data = file.read()

	return data

def parse_data(data):
	dots_string, folds_string = data.split("\n\n")

	max_dim = [0, 0]
	matches = re.findall(r"([0-9]+),([0-9]+)", dots_string, re.MULTILINE)
	coords = [tuple([int(elem) for elem in match]) for match in matches]
	max_coords = [max([coord[i] for coord in coords]) + 1 for i in range(2)]
	print(max_coords)

	matrix = np.zeros(tuple(max_coords), dtype=bool)
	for coord in coords:
		matrix[coord] = 1

	matches = re.findall(r"([x|y])=([0-9]+)", folds_string, re.MULTILINE)
	folds = [(match[0], int(match[1])) for match in matches]

	return matrix, folds

def fold(matrix, axis, value):
	if axis == "x":
		left_half = matrix[:value, :]
		right_half = matrix[value+1:, :]

		return np.logical_or(left_half, right_half[::-1, :])

	elif axis == "y":
		top_half = matrix[:, :value]
		bottom_half = matrix[:, value+1:]

		if top_half.shape[1] > bottom_half.shape[1]:
			bigger_bottom_half = np.zeros(top_half.shape)
			bigger_bottom_half[:, :bottom_half.shape[1]] = bottom_half
			bottom_half = bigger_bottom_half
			
		return  np.logical_or(top_half, bottom_half[:, ::-1])

def pretty_print(matrix):
	for row in range(matrix.shape[1]):
		for col in range(matrix.shape[0]):
			if matrix[col, row]:
				print("#", end="")

			else:
				print(".", end="")

		print("")

	print("")

def part_one():
	data = get_data("input.txt")
	matrix, folds = parse_data(data)

	#pretty_print(matrix)

	for axis, value in folds[:1]:
		matrix = fold(matrix, axis, value)
		#pretty_print(matrix)
		print(f"{np.sum(matrix)} visible dots")
	
def part_two():
	data = get_data("input.txt")
	matrix, folds = parse_data(data)

	for axis, value in folds:
		print(axis, value)
		matrix = fold(matrix, axis, value)
	
	pretty_print(matrix)
	
if __name__ == '__main__':
	part_one()
	part_two()