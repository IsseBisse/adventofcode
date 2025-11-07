import numpy as np

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	binary_data = tuple(tuple(int(char) for char in row) for row in data)

	return binary_data

def binary_vector_to_int(binary_vector):
	return sum(value * 2**index for index, value in enumerate(binary_vector[::-1]))

def part_one():
	binary_data = get_data("input.txt")
	data = np.array(binary_data)
	
	num_rows = data.shape[0]
	row_sums = np.sum(data, axis=0)
	gamma_rate_binary = row_sums > (num_rows / 2)
	epsilon_rate_binary = ~gamma_rate_binary

	gamma_rate = binary_vector_to_int(gamma_rate_binary)
	epsilon_rate = binary_vector_to_int(epsilon_rate_binary)

	print(gamma_rate * epsilon_rate)

def filter_ratings(data, index, is_most_common=True):
	filter_digit = int(sum([digits[index] for digits in data]) >= len(data)/2)	
	if not is_most_common:
		filter_digit = 1 - filter_digit
	filtered_data = tuple(digits for digits in data if digits[index] == filter_digit)

	if len(filtered_data) > 1:
		return filter_ratings(filtered_data, index+1, is_most_common)

	else:
		return filtered_data

def part_two():
	data = get_data("input.txt")

	oxygen_rating_binary = filter_ratings(data, 0)[0]
	co2_rating_binary = filter_ratings(data, 0, is_most_common=False)[0]

	oxygen_rating = binary_vector_to_int(oxygen_rating_binary)
	co2_rating = binary_vector_to_int(co2_rating_binary)
	print(oxygen_rating * co2_rating)

if __name__ == '__main__':
	# part_one()
	part_two()