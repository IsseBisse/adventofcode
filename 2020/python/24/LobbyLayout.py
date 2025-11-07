import matplotlib.pyplot as plt
from tqdm import tqdm 


DIRECTION_TO_COORDS = {"e": (1, 0), "w": (-1, 0), "ne": (0.5, 0.5),
					   "nw": (-0.5, 0.5), "se": (0.5, -0.5), "sw": (-0.5, -0.5)}
def parse(line):
	group = ""
	moves = list()
	for char in line:
		group += char
		if group in DIRECTION_TO_COORDS:
			moves.append(DIRECTION_TO_COORDS[group])
			group = ""

	return moves


def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	moves = [parse(line) for line in data]

	return moves


def part_one():
	moves = get_data("input.txt")
	blacks = set()
	for move in moves:
		coords = (sum(x for x, _ in move), sum(y for _, y in move))
		if coords not in blacks:
			blacks.add(coords)
		else:
			blacks.remove(coords)

	print(len(blacks))


def get_adjacent(coord):
	adjacent = set()
	for direction_coord in DIRECTION_TO_COORDS.values():
		adjacent.add(tuple(coord[axis]+direction_coord[axis] for axis in range(2)))

	return adjacent


def check_white(blacks):
	def checker(coord):
		adjacent = get_adjacent(coord)
		num_adjacent_blacks = len(adjacent.intersection(blacks))

		return num_adjacent_blacks == 2

	return checker


def check_black(blacks):
	def checker(coord):
		adjacent = get_adjacent(coord)
		num_adjacent_blacks = len(adjacent.intersection(blacks))

		return not (num_adjacent_blacks == 0 or num_adjacent_blacks > 2)

	return checker


def one_day(blacks):
	adjacent = set()
	for coord in blacks:
		adjacent = adjacent.union(get_adjacent(coord))
		
	adjacent_whites = adjacent.difference(blacks)

	blacks_to_blacks = set(filter(check_black(blacks), blacks))
	whites_to_blacks = set(filter(check_white(blacks), adjacent_whites))

	new_blacks = blacks_to_blacks.union(whites_to_blacks)
	
	# x, y = zip(*blacks)
	# plt.plot(x, y, 'bo')
	# x, y = zip(*adjacent_whites)
	# plt.plot(x, y, 'ro')
	# x, y = zip(*new_blacks)
	# plt.plot(x, y, 'g*')
	# plt.show()

	return new_blacks


def part_two():
	moves = get_data("input.txt")
	blacks = set()
	for move in moves:
		coords = (sum(x for x, _ in move), sum(y for _, y in move))
		if coords not in blacks:
			blacks.add(coords)
		else:
			blacks.remove(coords)

	num_days = 100
	for day in tqdm(range(num_days)):
		blacks = one_day(blacks)
		
	print(f"Day {day+1}: {len(blacks)}")


if __name__ == '__main__':
	# part_one()
	part_two()
