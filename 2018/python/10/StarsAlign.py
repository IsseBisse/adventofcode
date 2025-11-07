def parseInput(filename):
	f = open(filename, "r")

	input = list()
	for line in f:
		lineSplit = line.split("\n")
		if type(lineSplit) == list:
			string = lineSplit[0]
		else:
			string = lineSplit

		# Split string
		parts = string.split("<")
		#print(parts)

		posParts = parts[1].split(">")
		posParts = posParts[0].split(",")

		velParts = parts[2].split(">")
		velParts = velParts[0].split(",")

		update = dict()
		update["position"] = [int(posParts[0]), int(posParts[1])]
		update["velocity"] = [int(velParts[0]), int(velParts[1])]
	
		input.append(update)
		

	return input

'''
Part 1
'''
from Point import Point
import numpy as np

def printPoints(points, time):
	# Dimension
	xPos = list()
	yPos = list()

	for point in points:
		position = point.getPosition()
		xPos.append(position[0])
		yPos.append(position[1])

	dim = dict()
	dim["X"] = min(xPos)						# X start corner
	dim["Y"] = min(yPos)						# Y start corner
	dim["width"] = max(xPos) - min(xPos) + 1	# X width
	dim["height"] = max(yPos) - min(yPos) + 1	# Y width

	#print(dim)
	maxDim = 100
	printed = False

	if dim["width"] < maxDim and dim["height"] < maxDim:
		# Create pixel matrix
		pixels = np.zeros((dim["width"], dim["height"]))

		for point in points:
			position = point.getPosition()
			x = position[0] - dim["X"]
			y = position[1] - dim["Y"]

			pixels[x][y] = 1

		# Print pixels
		print("After %d seconds:" % time) # Part two
		for row in range(dim["height"]):
			for col in range(dim["width"]):
				if pixels[col, row] == 0:
					print(".", end = "")
				else:
					print("#", end = "")
			print("")

		print("\n\n")
		printed = True

	return printed 


def partOne():
	movement = parseInput("input.txt")

	points = list()
	for coords in movement:
		newPoint = Point(coords["position"], coords["velocity"])
		points.append(newPoint)
		#print(newPoint)

	printed = False
	oldPrinted = False
	time = 1
	while not (oldPrinted and not printed):
		for ind, point in enumerate(points):
			points[ind].updatePosition()

		oldPrinted = printed
		printed = printPoints(points, time)
		time += 1




'''
Part 2
'''
# See comment in printPoints()

'''
Main
'''
if __name__ == '__main__':
	partOne()