import numpy as np

CHAR_VALUE = {".": 0, ">": 1, "v": 2}
def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	floor_map = np.array([[CHAR_VALUE[char] for char in row] for row in data])

	return floor_map

def move(line, mover_value):
	new_line = np.zeros_like(line)

	idx = 0
	while idx < len(line):
		value = line[idx]
		next_idx = idx + 1 if idx < len(line)-1 else 0
		
		if value == mover_value and line[next_idx] == 0:
			new_line[next_idx] = value
			idx += 2

		else:
			new_line[idx] = value
			idx += 1

	return new_line

def one_step(floor_map):
	new_floor_map = np.zeros_like(floor_map)

	for row in range(floor_map.shape[0]):
		new_floor_map[row, :] = move(floor_map[row, :], 1)

	for col in range(floor_map.shape[1]):
		new_floor_map[:, col] = move(new_floor_map[:, col], 2)

	return new_floor_map

VALUE_CHAR = {value: key for key, value in CHAR_VALUE.items()}
def pretty_print(floor_map):
	for row in floor_map:
		print("".join([VALUE_CHAR[value] for value in row]))

	print()

def part_one():
	floor_map = get_data("input.txt")

	laps = 0
	while True:
		new_floor_map = one_step(floor_map)
		laps += 1

		if np.array_equal(new_floor_map, floor_map):
			break

		floor_map = new_floor_map		
		
	print(laps)

def part_two():
	data = get_data("smallInput.txt")

if __name__ == '__main__':
	part_one()
	# part_two()