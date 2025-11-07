import numpy as np

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	dim = (len(data), len(data[0]))
	data_matrix = np.zeros(dim)
	
	for i, line in enumerate(data):
		for j, char in enumerate(line):
			data_matrix[i, j] = 1 if char == "#" else 0

	return data_matrix

def part_one():
	data = get_data("input.txt")
	dim = data.shape

	traj = (1, 3)	# row, col
	row = col = 0
	num_trees = 0

	while(row < dim[0]):
		num_trees += data[row, col]

		row = row + traj[0]
		col = (col + traj[1]) % dim[1]

	print(num_trees)
	
def part_two():
	data = get_data("input.txt")
	dim = data.shape

	trajs = [(1, 1),
		(1, 3),
		(1, 5),
		(1, 7),
		(2, 1)]

	num_trees_list = list()
	for traj in trajs:
		row = col = 0
		num_trees = 0

		while(row < dim[0]):
			num_trees += data[row, col]

			row = row + traj[0]
			col = (col + traj[1]) % dim[1]

		num_trees_list.append(num_trees)

	result = 1
	for num in num_trees_list:
		result *= num

	print(result)

if __name__ == '__main__':
	part_two()