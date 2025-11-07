def parseFile(filename):
	f = open(filename, "r")

	# Read .txt file and parse into list of strings
	input = list()
	for line in f:
		lineSplit = line.split("\n")
		
		if type(lineSplit) == list:
			string = lineSplit[0]
		else:
			string = lineSplit

		order = parseInputString(string)

		input.append(order)

	return input

def parseInputString(string):
	# Split string
	parts = string.split()
	coordinates = parts[2][:-1]
	coordinates = coordinates.split(',')
	x = coordinates[0]
	y = coordinates[1]

	dimensions = parts[3]
	dimensions = dimensions.split('x')
	xDim = dimensions[0]
	yDim = dimensions[1]

	# Create dict
	order = dict()
	order["ID"] = parts[0][1:]
	order["x"] = x
	order["y"] = y
	order["xDim"] = xDim
	order["yDim"] = yDim

	return order

'''
Part 1
'''
import numpy as np

def partOne():
	input = parseFile("input.txt")
	#print(input)

	fabric = np.zeros((1000, 1000), dtype=int)
	for order in input:
		x = int(order["x"])
		y = int(order["y"])
		xDim = int(order["xDim"])
		yDim = int(order["yDim"])

		fabric[x:x+xDim, y:y+yDim] += 1

	print(fabric)
	overlaps = np.where(fabric > 1)
	numOverlaps = len(overlaps[0])
	print(overlaps)
	print('Overlapping square inches: %d' % numOverlaps)


'''
Part 2
'''
def partTwo():
	input = parseFile("input.txt")

	fabric = np.zeros((1000, 1000), dtype=int)
	for order in input:
		x = int(order["x"])
		y = int(order["y"])
		xDim = int(order["xDim"])
		yDim = int(order["yDim"])

		fabric[x:x+xDim, y:y+yDim] += 1

	nonOverlapOrders = list()
	for order in input:
		x = int(order["x"])
		y = int(order["y"])
		xDim = int(order["xDim"])
		yDim = int(order["yDim"])

		overlapping = False
		for xInd in range(x, x+xDim):
			for yInd in range(y, y+yDim):
				if fabric[xInd, yInd] > 1:
					overlapping = True

		if not overlapping:
			nonOverlapOrders.append(order)

	print('Non-overlapping orders are:')
	for order in nonOverlapOrders:
		print('ID: %d' % int(order["ID"]))


'''
Main
'''
if __name__ == '__main__':
	partTwo()