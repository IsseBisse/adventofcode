import numpy as np
from scipy.signal import convolve2d
from functools import reduce

def get_data(path):
	with open(path) as file:
		data = file.read()

	return data

def parse_data(data):
	parsed_data = list()
	for line in data.split("\n"):
		parsed_data.append([int(num) for num in list(line)])

	return np.array(parsed_data)

def get_low_points(height_map):
	x_grad = convolve2d(height_map, np.array([[1, -1, 0]]), mode="full", fillvalue=10)
	x_grad = np.sign(x_grad)
	
	x_low = convolve2d(x_grad, np.array([[1, -1]]), mode="same")
	x_low = x_low[:,1:-1] == 2

	y_grad = convolve2d(height_map, np.array([[1], [-1], [0]]), mode="full", fillvalue=10)
	y_grad = np.sign(y_grad)
	
	y_low = convolve2d(y_grad, np.array([[1], [-1]]), mode="same")
	y_low = y_low[1:-1,:] == 2
	
	low_points = x_low & y_low

	return low_points

def part_one():
	data = get_data("input.txt")
	height_map = parse_data(data)

	low_points = get_low_points(height_map)
	risk = height_map[low_points]
	print(sum(risk) + len(risk))

def get_basin_size(height_map, low_points):

	low_point_indicies = np.where(low_points == 1)
	num_low_points = len(low_point_indicies[0])
	basins = np.zeros((*low_points.shape, num_low_points), dtype=int)
	
	for i, ind in enumerate(zip(*low_point_indicies)): 
		basins[ind[0], ind[1], i] = 1

	basin_size = [0] * num_low_points 
	while True:

		new_basin_size = [0] * num_low_points 
		for ind in range(num_low_points):
			basins[:,:,ind] = convolve2d(basins[:,:,ind], np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]]), "same")
			basins[:,:,ind] = basins[:,:,ind] > 0
			basins[:,:,ind] *= height_map != 9
			
			new_basin_size[ind] = np.sum(basins[:,:,ind])

		if new_basin_size == basin_size:
			break 

		basin_size = new_basin_size

	return sorted(basin_size)
	
def part_two():
	data = get_data("input.txt")
	height_map = parse_data(data)

	low_points = get_low_points(height_map)

	basin_size = get_basin_size(height_map, low_points)
	print(reduce(lambda x,y: x*y, basin_size[-3:]))

if __name__ == '__main__':
	part_one()
	part_two()