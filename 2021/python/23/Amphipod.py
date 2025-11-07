import numpy as np
import sys

CHAR_TO_VALUE = {chr(i+65): i+1 for i in range(5)} | {".": 0}
VALUE_TO_CHAR = {value: key for key, value in CHAR_TO_VALUE.items()} | {-1: "#"}

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	height, width = len(data), len(data[0])
	pod_map = np.zeros((height, width), dtype=int)

	
	for row_idx, row in enumerate(data):
		for col_idx, char in enumerate(row):
			if char in CHAR_TO_VALUE:
				value = CHAR_TO_VALUE[char]
			else:
				value = -1
				
			pod_map[row_idx, col_idx] = value 

	return pod_map[1:-1, 1:-1]

def to_string(pod_map):
	height, width = pod_map.shape

	string = ""
	for row_idx in range(height):
		for col_idx in range(width):
			string += VALUE_TO_CHAR[pod_map[row_idx, col_idx]]

		string += "\n"

	return string

def pretty_print(pod_map):
	print(to_string(pod_map), end="")

COST_PER_STEP = {i+1:10**i for i in range(4)}
def move(pod_map, from_coord, to_coord):
	if pod_map[to_coord] != 0:
		raise NotImplementedError("Already occupied space!")

	if pod_map[from_coord] in [0, -1]:
		raise NotImplementedError("Immovable object!")

	new_map = pod_map.copy()

	new_map[to_coord] = new_map[from_coord]
	new_map[from_coord] = 0

	steps = from_coord[0] + to_coord[0] + abs(from_coord[1] - to_coord[1])
	cost = steps * COST_PER_STEP[pod_map[from_coord]]

	return new_map, cost

ROOM_COL_COORDS = [2, 4, 6, 8]
def finished_moving(pod_map, coord):
	"""In correct room and no incorrect below"""
	# Incorrect room
	if not pod_map[coord] == (coord[1] // 2):
		return False

	for row in range(coord[0], pod_map.shape[0]):
		# Incorrect pods below
		if pod_map[(row, coord[1])] != pod_map[coord]:
			return False

	return True

def possible_from_coords(pod_map):
	from_coords = list()

	# Check "hallway"
	for col_idx in range(pod_map.shape[1]):
		if pod_map[0, col_idx] != 0:
			from_coords.append((0, col_idx))

	# Check rooms
	for col_idx in ROOM_COL_COORDS:
		for row_idx in range(1, pod_map.shape[0]):
			# If occupied and not "your" room
			if pod_map[row_idx, col_idx] != 0 and not finished_moving(pod_map, (row_idx, col_idx)):
				from_coords.append((row_idx, col_idx))
				break

	return from_coords

def possible_to_coords(pod_map, from_coord):
	# Check hallway collisions (left and right)
	left = from_coord[1] - 1
	while left >= 0 and pod_map[(0, left)] == 0:
		left -= 1
	left += 1

	right = from_coord[1] + 1
	while right < pod_map.shape[1] and pod_map[(0, right)] == 0:
		right += 1
	right -= 1

	if from_coord[0] > 0:
		# Can only move to hallway if in a room
		to_coords = [(0, col) for col in range(left, right+1) if col not in ROOM_COL_COORDS]
	else:
		to_coords = list()

	# Check room
	room_col = int(pod_map[from_coord] * 2)
	if room_col in range(left, right+1):
		# Possible to reach room from hallway
		row = pod_map.shape[0]-1
		while pod_map[row, room_col] == pod_map[from_coord]:
			row -= 1

		if row > 0 and pod_map[(row, room_col)] == 0:
			to_coords.append((row, room_col))

	return to_coords


# FINISHED_MAP = np.array([[1, 2, 3, 4], [1, 2, 3, 4]])
# def test_all_moves(pod_map, cost):
# 	if np.all(pod_map[1:, 2:10:2] == FINISHED_MAP):
# 		print(cost)
# 		return cost

# 	from_coords = possible_from_coords(pod_map)
# 	for from_co in from_coords:
# 		to_coords = possible_to_coords(pod_map, from_co)

# 		total_costs = list()
# 		for to_co in to_coords:
# 			new_map, move_cost = move(pod_map, from_co, to_co)
# 			ret = test_all_moves(new_map, cost+move_cost)

# 			if ret is not None:
# 				total_costs.append(ret)

# 	if total_costs:
# 		return min(total_costs)
	
# 	else:
# 		return None

FINISHED_MAP = get_data("finished_map.txt")
def explore_all_positions(pod_maps):
	next_maps = dict()

	print(len(pod_maps))
	for _, (pod_map, cost) in pod_maps.items():
		# Get all possible next positions (one move away)
		pods_next_maps = dict()

		from_coords = possible_from_coords(pod_map)
		for from_co in from_coords:
			to_coords = possible_to_coords(pod_map, from_co)

			total_costs = list()
			for to_co in to_coords:
				next_map, move_cost = move(pod_map, from_co, to_co)

				pods_next_maps[to_string(next_map)] = (next_map, cost + move_cost)

		# Add to complete list if cost is lower
		for key, (pod_map, cost) in pods_next_maps.items():
			if key in next_maps:
				if cost < next_maps[key][1]:
					next_maps[key] = (pod_map, cost)

			else:
				next_maps[key] = (pod_map, cost)


	if to_string(FINISHED_MAP) in next_maps:
		return next_maps[to_string(FINISHED_MAP)][1]	
	
	elif len(next_maps) == 0:
		for _, (pod_map, cost) in pod_maps.items():
			pretty_print(pod_map)
			print(cost)
		return None 

	else:
		return explore_all_positions(next_maps)

def part_one():
	pod_map = get_data("input.txt")
	minimum_cost = explore_all_positions({to_string(pod_map): (pod_map, 0)})
	print(minimum_cost)

def get_data_part_two(path):
	with open(path) as file:
		data = file.read().split("\n")

	# Add extra rows
	data.insert(3, "  #D#B#A#C#  ")
	data.insert(3, "  #D#C#B#A#  ")

	height, width = len(data), len(data[0])
	pod_map = np.zeros((height, width), dtype=int)

	
	for row_idx, row in enumerate(data):
		for col_idx, char in enumerate(row):
			if char in CHAR_TO_VALUE:
				value = CHAR_TO_VALUE[char]
			else:
				value = -1
				
			pod_map[row_idx, col_idx] = value 

	return pod_map[1:-1, 1:-1]

FINISHED_MAP = get_data("finished_map2.txt")
def part_two():
	pod_map = get_data_part_two("input.txt")
	pretty_print(pod_map)
	# sys.setrecursionlimit(2000)
	minimum_cost = explore_all_positions({to_string(pod_map): (pod_map, 0)})
	print(minimum_cost)

if __name__ == '__main__':
	# part_one()
	part_two()