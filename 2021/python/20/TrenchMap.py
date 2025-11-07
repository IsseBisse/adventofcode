import numpy as np
import scipy.signal as sig

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n\n")

	enhancement = data[0]
	enhancement_map = {idx: 0 if value == "." else 1 for idx, value in enumerate(enhancement)}
	image = [[0 if char == "." else 1 for char in row] for row in data[1].split("\n")]
	image = np.array(image)

	return enhancement_map, image

def pretty_print(image):
	for row in image.tolist():
		print("".join(["." if num==0 else "#" for num in row]))

def pixel_enhancer(enhancement_map):
	def enhance(pixel_value):
		return enhancement_map[pixel_value]

	return enhance

def enhance(image, enhancement_map, border=0):
	offset = 6
	output_image = np.ones((image.shape[0] + 2*offset, image.shape[1] + 2*offset)) * border
	output_image[offset:-offset, offset:-offset] = image

	bin_kernel = np.reshape(np.array([2**i for i in range(9)]), (3,3))
	output_conv = sig.convolve2d(output_image, bin_kernel,"same")

	enhance_pixel = pixel_enhancer(enhancement_map)
	enhance_pixel_vectorized = np.vectorize(enhance_pixel)
	output_image = enhance_pixel_vectorized(output_conv)
	border = output_image[1, 1] 	# Simulate infinite border
	output_image = output_image[(offset-3):-(offset-3), (offset-3):-(offset-3)] 	# Remove border to compensate convolution artefacts

	return output_image, border

def part_one():
	enhancement_map, image = get_data("smallInput.txt")
	
	pretty_print(image)
	border = 0
	for _ in range(2):
		image, border = enhance(image, enhancement_map, border)
		pretty_print(image)

	print(np.sum(image))

def part_two():
	enhancement_map, image = get_data("input.txt")
	border = 0
	for _ in range(50):
		image, border = enhance(image, enhancement_map, border)
	
	print(np.sum(image))

if __name__ == '__main__':
	# part_one()
	part_two()