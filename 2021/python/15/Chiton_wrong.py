import numpy as np

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	data = [[int(char) for char in row] for row in data]
	data = np.array(data)

	return data

# def cost_of_square(risk_matrix, x, y):
# 	from_left_cost = cost_matrix[x-1, y] + risk_matrix[x, y] if x > 0 else 1e9
# 	from_top_cost = cost_matrix[x, y-1] + risk_matrix[x, y] if y > 0 else 1e9

# 	return min(from_left_cost, from_top_cost)

def get_next_positions(prev_positions, matrix_dim):
	next_positions = set()
	for pos in prev_positions:
		pos = np.array(pos)
		for move in [np.array([0, 1]), np.array([1, 0])]:
			next_pos = pos + move

			if all(next_pos < matrix_dim):
				next_positions.add(tuple(next_pos))

	return next_positions

def get_cost_matrix(risk_matrix):
	cost_matrix = np.zeros_like(risk_matrix)

	cost_matrix[0, 0] = risk_matrix[0, 0] 
	next_positions = get_next_positions([(0, 0)], risk_matrix.shape)
	while next_positions:
		for pos in next_positions:
			x, y = pos
			from_left_cost = cost_matrix[x-1, y] + risk_matrix[x, y] if x > 0 else 1e9
			from_top_cost = cost_matrix[x, y-1] + risk_matrix[x, y] if y > 0 else 1e9
			cost_matrix[x, y] = min(from_left_cost, from_top_cost)
		
		next_positions = get_next_positions(next_positions, risk_matrix.shape)
		
	return cost_matrix

def part_one():
	risk_matrix = get_data("input.txt")
	cost_matrix = get_cost_matrix(risk_matrix)

	print(f"Total risk is {cost_matrix[-1, -1] - risk_matrix[-1, -1]}")

def part_two():
	data = get_data("smallInput.txt")

if __name__ == '__main__':
	part_one()
	# part_two()