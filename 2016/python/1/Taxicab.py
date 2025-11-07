'''
Input
'''
def parseInput(filename):
	f = open(filename, "r")
	data = f.read()

	data = data.split(", ")

	return data

'''
Part One
'''
from Mover import Mover

def partOne():
	# Read data
	data = parseInput("testInput2.txt")

	# Create mover
	mover = Mover()

	# Move for each command
	for command in data:
		mover.move(command)

	print(mover)

'''
Part Two
'''
def partTwo():
	# Read data
	data = parseInput("input.txt")

	# Create mover
	mover = Mover()

	# Move for each command
	continue_moving = True
	num_commands = len(data)
	i = 0

	print("%d commands loaded!" % num_commands)

	while continue_moving:
		command = data[i]
		i = (i + 1) % num_commands

		continue_moving = mover.move(command)

	print(mover)

'''
Main
'''
if __name__ == '__main__':
	partTwo()