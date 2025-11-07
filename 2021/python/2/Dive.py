import re
from functools import reduce

def get_data(path):
	with open(path) as file:
		data = file.read()

	return data

def parse_data(data):
	commands = re.findall(r"([a-z]+) (\d+)", data, re.MULTILINE)
	commands = [(item[0], int(item[1])) for item in commands]
	return commands


COMMAND_TO_DIRECTION = {
	"forward": (1, 0),
	"down": (0, 1),
	"up": (0, -1),
}

def update_position(position, command):
	command, scaling = command

	direction = COMMAND_TO_DIRECTION[command]
	direction = [scaling*component for component in direction]
	position = [sum(x) for x in zip(position, direction)]

	return position

def part_one():
	data = get_data("input.txt")
	commands = parse_data(data)

	position = [0, 0]
	for command in commands:
		position = update_position(position, command)
		
	print(reduce(lambda x, y: x*y, position))


def update_position_with_aim(position, command):
	command, scaling = command

	if command == "forward":
		position[0] += scaling
		position[1] += scaling * position[2]

	else:
		aim_direction = 1 if command == "down" else -1
		position[2] += aim_direction * scaling

	return position 

def part_two():
	data = get_data("input.txt")
	commands = parse_data(data)

	position = [0, 0, 0]
	for command in commands:
		position = update_position_with_aim(position, command)
		
	print(reduce(lambda x, y: x*y, position[:-1]))

if __name__ == '__main__':
	part_one()
	part_two()