import numpy as np
import numpy.matlib

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	for i, entry in enumerate(data):
		data[i] = int(entry)

	return data

def part_one():

	data = np.array(get_data("input.txt"))
	data = np.matlib.repmat(data, len(data), 1)
	data_t = np.matrix.transpose(data)

	sum_data = data + data_t
	ind = np.where(sum_data == 2020)
	
	product = data[ind][0] * data[ind][1]
	print(product)

def part_two():
	data = np.array(get_data("input.txt"))
	
	data_x = data[:, None, None]
	data_y = data[None, :, None]
	data_z = data[None, None, :]

	data_x = np.tile(data_x, (1, len(data), len(data)))
	data_y = np.tile(data_y, (len(data), 1, len(data)))
	data_z = np.tile(data_z, (len(data), len(data), 1))
	
	data_sum = data_x + data_y + data_z

	print(data_x.shape, data_y.shape, data_z.shape, data_sum.shape)

	ind = np.where(data_sum == 2020)
	product = 1 
	for i in range(3):
		product *= data_y[ind][i]

	print(product)

if __name__ == '__main__':
	part_two()