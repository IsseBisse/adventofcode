import numpy as np
import operator
import matplotlib.pyplot as plt

def parse_input(path):

	f = open(path, "r")

	data = [[(x[0], int(x[1:])) for x in row.split(",")] for row in f.read().split("\n")]

	return data

DIRECTIONS = {"R": (1,0),
	"L": (-1, 0),
	"U": (0, 1),
	"D": (0, -1)}

# line segment intersection using vectors
# see Computer Graphics by F.S. Hill
#
def perp( a ) :
    b = empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b

# line segment a given by endpoints a1, a2
# line segment b given by endpoints b1, b2
# return 
def seg_intersect(a1,a2, b1,b2) :
    da = a2-a1
    db = b2-b1
    dp = a1-b1
    dap = perp(da)
    denom = dot( dap, db)
    num = dot( dap, dp )
    return (num / denom.astype(float))*db + b1

def part_one():
	data = parse_input("input.txt")

	max_position = [0, 0]
	min_position = [0, 0]

	for row in data:
		current_position = [0, 0]

		for movement in row:
			change = tuple(i * movement[1] for i in DIRECTIONS[movement[0]])
			next_position = tuple(map(operator.add, current_position, change))

			for i in range(2):
				if next_position[i] > max_position[i]:
					max_position[i] = next_position[i]

				if next_position[i] < min_position[i]:
					min_position[i] = next_position[i] 

			current_position = next_position

	size = tuple(max_position[i] - min_position[i] + 1 for i in range(2))
	center = tuple(-min_position[i] for i in range(2))

	area = np.zeros((size[0], size[1], 2), dtype=np.uint8)

	for i, row in enumerate(data):
		current_position = center

		for movement in row:
			steps = 0

			while steps < movement[1]:
				current_position = tuple(map(operator.add, current_position, DIRECTIONS[movement[0]]))
				area[current_position[0], current_position[1], i] = 1
		
				steps += 1

	area = np.sum(area, axis=2)

	crossings = np.where(area > 1)

	min_distance = 1e9
	for i in range(len(crossings[0])):
		distance =  abs(crossings[0][i] - center[0]) + abs(crossings[1][i] - center[1])

		if distance > 0 and distance < min_distance:
			min_distance = distance

	return (area, center), data

def part_two():
	(area, center), data = part_one()

	crossing_array = np.where(area > 1)
	crossings = list()
	for i in range(len(crossing_array[0])):
		crossings.append((crossing_array[0][i], crossing_array[1][i]))

	min_steps = 1e9
	length_to_crossing = np.zeros((len(crossings), 2))
	for i, row in enumerate(data):
		current_position = center
		total_steps = 0

		for movement in row:
			steps = 0

			while steps < movement[1]:
				current_position = tuple(map(operator.add, current_position, DIRECTIONS[movement[0]]))
				steps += 1
				total_steps += 1

				if current_position in crossings:
					length_to_crossing[crossings.index(current_position), i] = total_steps

	min_distance = 1e9
	for distance in length_to_crossing:
		if np.sum(distance) < min_distance:
			min_distance = int(np.sum(distance))

	print(min_distance)


if __name__ == '__main__':
	part_two()