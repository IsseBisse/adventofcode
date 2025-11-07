from itertools import accumulate

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

		parts = tuple(row.split(" ") for row in data)
		course = tuple((part[0], int(part[1])) for part in parts)

	return course

def changes(course, scale_dict):
	changes = tuple(scale_dict[direction] * distance for direction, distance in course)
	return changes

def part_one():
	course = get_data("input.txt")
	depth_scaling = {"forward": 0, "up": -1, "down": 1}
	forward_scaling = {"forward": 1, "up": 0, "down": 0}

	depth_change = sum(changes(course, depth_scaling))
	forward_change = sum(changes(course, forward_scaling))

	print(forward_change  * depth_change)

def part_two():
	course = get_data("input.txt")

	aim_scaling = {"forward": 0, "up": -1, "down": 1}
	aim_changes = changes(course, aim_scaling)
	aim = accumulate(aim_changes)

	forward_scaling = {"forward": 1, "up": 0, "down": 0}
	forward_change = changes(course, forward_scaling)
	forward = sum(forward_change)

	depth_change = map(lambda aim, distance: aim*distance, aim, forward_change)
	depth = sum(depth_change)

	print(forward * depth)

if __name__ == '__main__':
	part_one()
	part_two()