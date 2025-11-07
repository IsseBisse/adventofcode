def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	return data

def parse_data(data):
	parsed_data = list()
	for line in data:
		combinations, output = line.split(" | ")
		combinations = ["".join(sorted(comb)) for comb in combinations.split(" ")]
		output = ["".join(sorted(out)) for out in output.split(" ")]
		
		parsed_data.append((combinations, output))

	return parsed_data

def count_uniquie_segment_numbers(output):
	unique_number_occurances = 0
	for item in output:
		unique_number_occurances += len([segment for segment in item if len(segment) in [2, 3, 4, 7]])

	return unique_number_occurances

def part_one():
	data = get_data("input.txt")
	parsed_data = parse_data(data)

	print(count_uniquie_segment_numbers([output for _, output in parsed_data]))

def find_segment_mapping(combination):
	mapping = {}

	# Add unique length ones
	unique_lengths = {2: 1, 3: 7, 4: 4, 7: 8}
	for expected_length, value in unique_lengths.items():
		match = "".join([item for item in combination if len(item) == expected_length][0])
		mapping[value] = match

	# Add 0, 6, 9 (six segments)
	candidates = [item for item in combination if len(item) == 6]
	for cand in candidates:
		if set(cand).union(set(mapping[1])) == set(mapping[8]):
			mapping[6] = cand
			candidates.remove(cand)

	for cand in candidates:
		if set(cand).union(set(mapping[4])) == set(mapping[8]):
			mapping[0] = cand
			candidates.remove(cand)

	mapping[9] = candidates[0]

	# Add 2, 3, 5 (five segmenst)
	candidates = [item for item in combination if len(item) == 5]
	for cand in candidates:
		if set(cand).union(set(mapping[1])) == set(mapping[9]):
			mapping[5] = cand

		elif set(cand).union(set(mapping[4])) == set(mapping[9]):
			mapping[3] = cand

		else:
			mapping[2] = cand

	inverse_mapping = {value: key for key, value in mapping.items()}

	return inverse_mapping

	print(mapping)

def part_two():
	data = get_data("input.txt")
	parsed_data = parse_data(data)

	output_sum = 0
	for combination, output in parsed_data:
		mapping = find_segment_mapping(combination)

		output_string = ""
		for segments in output:
			output_string += str(mapping[segments])
		output_val = int(output_string)

		output_sum += output_val

	print(output_sum)

if __name__ == '__main__':
	part_one()
	part_two()