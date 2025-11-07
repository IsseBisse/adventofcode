'''
Part 1
'''
import numpy as np

def calculatePowerLevel(X, Y, serial):
	rackID = X + 10
	powerLevel = rackID * Y
	powerLevel = powerLevel + serial
	powerLevel = powerLevel * rackID
	powerLevelString = "%03d" % powerLevel
	powerLevel = int(powerLevelString[-3])
	powerLevel -= 5

	return powerLevel


def partOne(serial):
	gridSize = 300
	grid = np.zeros((gridSize, gridSize))

	for x in range(gridSize):
		for y in range(gridSize):
			grid[x, y] = calculatePowerLevel(x+1, y+1, serial)

	maxFuel = -5 * 9
	maxCoords = [0, 0]
	maxSize = 0

	for subSize in range(gridSize):
		subSize += 1

		for x in range(gridSize - subSize + 1):
			for y in range(gridSize - subSize + 1):
				fuel = grid[x:x+subSize, y:y+subSize].sum()

				if fuel > maxFuel:
					maxCoords = [x + 1, y + 1]
					maxFuel = fuel
					maxSize = subSize

	print("Maximum fuel: %d" % maxFuel)
	print("At position: (%d, %d, %d)" % (maxCoords[0], maxCoords[1], maxSize))

'''
Part 2
'''


'''
Main
'''
if __name__ == '__main__':
	partOne(8772)