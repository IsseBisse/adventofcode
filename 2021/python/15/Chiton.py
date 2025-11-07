import numpy as np

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	data = [[int(char) for char in row] for row in data]
	data = np.array(data)

	return data

def get_connected_unvisited_nodes(node, dim, visited):
	next_pos = list()
	for move in [(1,0), (0,1), (-1,0), (0, -1)]:
		new_pos = np.array(node) + np.array(move)
		if all(new_pos >= (0, 0)) and all(new_pos < dim) and tuple(new_pos) not in visited:
			next_pos.append(tuple(new_pos))

	return next_pos

def dijkstra(risk_matrix):
	cost_matrix = np.full(risk_matrix.shape, np.inf)
	cost_matrix[0, 0] = 0

	start = (0, 0)
	finish = tuple([dim-1 for dim in risk_matrix.shape])

	unvisited_non_infinite = [(0, start)]
	visited = set()

	while unvisited_non_infinite:
		# Hugely inefficient but works for now
		unvisited_non_infinite.sort(key=lambda x: x[0])

		currend_node = unvisited_non_infinite[0]
		current_score, current_pos = currend_node
		connected_nodes = get_connected_unvisited_nodes(current_pos, risk_matrix.shape, visited)

		# print(currend_node, connected_nodes)

		for next_node in connected_nodes:
			x, y = next_node
			next_cost = current_score+risk_matrix[x, y]
			if next_cost < cost_matrix[x, y]:
				cost_matrix[x, y] = next_cost
				unvisited_non_infinite.append((next_cost, next_node))

		# print(cost_matrix)

		unvisited_non_infinite.remove(currend_node)
		visited.add(current_pos)

	return cost_matrix

def part_one():
	risk_matrix = get_data("input.txt")
	cost_matrix = dijkstra(risk_matrix)
	print(cost_matrix[-1, -1])

def generate_full_matrix(risk_matrix):
	num_tiles = 5

	row_matrix = risk_matrix.copy()
	for incr in range(1, num_tiles):
		new_matrix = risk_matrix + incr
		new_matrix[new_matrix==10] = 1
		row_matrix = np.concatenate((row_matrix, new_matrix))

	full_matrix = row_matrix.copy()
	for incr in range(1, num_tiles):
		new_matrix = row_matrix + incr
		new_matrix[new_matrix>9] = (new_matrix[new_matrix>9] % 10) + 1
		full_matrix = np.concatenate((full_matrix, new_matrix), axis=1)

	return full_matrix

def part_two():
	risk_matrix = get_data("input.txt")
	full_matrix = generate_full_matrix(risk_matrix)
	cost_matrix = dijkstra(full_matrix)
	print(cost_matrix[-1, -1])

if __name__ == '__main__':
	# part_one()
	part_two()