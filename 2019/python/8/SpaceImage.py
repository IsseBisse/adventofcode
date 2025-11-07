import numpy as np
import matplotlib.pyplot as plt

def parse_input(path):

	f = open(path, "r")

	data = [int(x) for x in  f.read()]

	return data

def part_one():

	data = parse_input("input.txt")
	
	# Create image
	width = 25
	height = 6
	layers = int(len(data) / (width * height)) 	

	im = np.array(data)
	im = np.split(im, layers)

#	for i in range(layers): 
#		im[i] = np.reshape(im[i], (height, width))

	min_num_zeros = 1e9
	ind_min_zeros = -1
	for i in range(layers):

		num_zeros = len(im[i][im[i] == 0])

		if num_zeros < min_num_zeros:

			min_num_zeros = num_zeros
			ind_min_zeros = i

	num_ones = len(im[ind_min_zeros][im[ind_min_zeros] == 1])
	num_twos = len(im[ind_min_zeros][im[ind_min_zeros] == 2])

	print("Number is: %d" % (num_ones * num_twos))

def part_two():
	
	data = parse_input("input.txt")
	
	# Create image
	width = 25
	height = 6
	layers = int(len(data) / (width * height)) 	

	im = np.array(data)
	im = np.split(im, layers)

#	for i in range(layers): 
#		im[i] = np.reshape(im[i], (height, width))
	
	im_final = np.zeros((im[0].shape), dtype=int)
	for i in range(width * height):

		layer = 0
		while im[layer][i] == 2:
			layer += 1

		im_final[i] = im[layer][i]
	
	im_final = np.reshape(im_final, (height, width))
	plt.imshow(im_final)
	plt.show()

if __name__ == '__main__':
	
	part_two()