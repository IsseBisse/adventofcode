from re import findall

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	return data

def parse_data(data):
	vectors = list()
	for line in data:
		vector = [int(string) for string in findall(r"\d+", line)]
		vector = list(zip(vector[::2], vector[1::2]))
		vectors.append(vector)

	return vectors

def get_points(horz_vert_vector):
	points = list()
	for col in range(horz_vert_vector[0][0], horz_vert_vector[1][0]+1):
		for row in range(horz_vert_vector[0][1], horz_vert_vector[1][1]+1):
			points.append((col, row))

	return points

def get_horz_vert_vectors(vectors):
	horz_vert_vectors = list()
	for vector in vectors: 
		if vector[0][0] == vector[1][0] or \
			vector[0][1] == vector[1][1]:
			horz_vert_vectors.append(vector)

	return horz_vert_vectors

def part_one():
	data = get_data("input.txt")
	vectors = parse_data(data)

	horz_vert_vectors = get_horz_vert_vectors(vectors)

	vents = dict()
	for vector in horz_vert_vectors:
		points = get_points(sorted(vector))

		for point in points:
			if point in vents:
				vents[point] += 1

			else:
				vents[point] = 1

	num_overlaps = 0
	for _, value in vents.items():
		num_overlaps += 1 if value >= 2 else 0  

	print(num_overlaps)

def get_diag_vectors(vectors):
	diag_vectors = list()
	for vector in vectors:
		horz_diff = abs(vector[0][0] - vector[1][0])
		vert_diff = abs(vector[0][1] - vector[1][1])

		if horz_diff==vert_diff:
			diag_vectors.append(vector)

	return diag_vectors
	
def get_diag_points(diag_vector):
	row_diff = int((diag_vector[1][1] - diag_vector[0][1]) / 
		abs(diag_vector[1][1] - diag_vector[0][1]))

	points = list()
	row = diag_vector[0][1]
	for col in range(diag_vector[0][0], diag_vector[1][0]+1):
		points.append((col, row))
		row += row_diff

	return points

def part_two():
	data = get_data("input.txt")
	vectors = parse_data(data)

	horz_vert_vectors = get_horz_vert_vectors(vectors)
	diag_vectors = get_diag_vectors(vectors)

	vents = dict()
	for vector in horz_vert_vectors:
		points = get_points(sorted(vector))

		for point in points:
			if point in vents:
				vents[point] += 1

			else:
				vents[point] = 1

	for vector in diag_vectors:
		points = get_diag_points(sorted(vector))

		for point in points:
			if point in vents:
				vents[point] += 1

			else:
				vents[point] = 1
		
	num_overlaps = 0
	for key, value in vents.items():
		num_overlaps += 1 if value >= 2 else 0 

	print(num_overlaps)

if __name__ == '__main__':
	part_one()
	part_two()