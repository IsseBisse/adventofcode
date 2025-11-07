def parseFile(filename):
    f = open(filename, "r")

    # Read .txt file and parse into list of strings
    coordList = list()
    for line in f:
        lineSplit = line.split("\n")
        
        if type(lineSplit) == list:
            string = lineSplit[0]
        else:
            string = lineSplit

        coord = parseInputString(string)
        coordList.append(coord)

    return coordList


def parseInputString(string):
	coord = list()

	parts = string.split(",")
	for part in parts:
		coord.append(int(part))

	return coord


'''
Part 1
'''
import numpy as np
import matplotlib.pyplot as plt


def manhattanDistance(coord1, coord2):
	return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])


def placeCoords(coordList):
	mapDim = [-1, -1]

	# Get max dimensions
	for coord in coordList:
		# x max
		if coord[0]+1 > mapDim[0]:
			mapDim[0] = coord[0]+1

		# y max
		if coord[1]+1 > mapDim[1]:
			mapDim[1] = coord[1]+1

	coordMap = np.ones(mapDim, dtype = int)
	coordMap = coordMap * -2
	print(coordMap.shape)

	
	# Place coords
	for ind, coord in enumerate(coordList):
		coordMap[coord[0], coord[1]] = ind

	return coordMap

def fillMap(coordList, coordMap):
	mapDim = coordMap.shape

	# Fill map
	# Check every pixel of map
	for x in range(mapDim[0]):
		for y in range(mapDim[1]):
			# Find closest coordinate
			pixelCoord = [x, y]

			# Calculate distance to each pixel
			minDist = max(mapDim) + 1
			minInd = -1
			pixelDist = list()
			for ind, coord in enumerate(coordList):
				pixelDist.append(manhattanDistance(coord, pixelCoord))

			# Find min
			sortInd = sorted(range(len(pixelDist)), key=lambda k: pixelDist[k])
			pixelDist.sort()
			if pixelDist[0] == pixelDist[1]:
				coordMap[x,y] = -1
			else:
				coordMap[x,y] = sortInd[0]
	
	return coordMap 

def findLargestArea(coordList, coordMap):
	mapDim = coordMap.shape

	# Trace edge to remove infinite areas
	removeInd = list()
	# Trace x borders
	for x in [0, mapDim[0]-1]:
		for y in range(mapDim[1]):
			pixelInd = coordMap[x, y]
			#print("Coords: (%d, %d)" % (x, y))

			if pixelInd not in removeInd:
				removeInd.append(pixelInd)

	# Trace y borders
	for y in [0, mapDim[1]-1]:
		for x in range(mapDim[0]):
			pixelInd = coordMap[x, y]
			#print("Coords: (%d, %d)" % (x, y))

			if pixelInd not in removeInd:
				removeInd.append(pixelInd)
	#print(removeInd)

	# Add ok indicies
	okInds = list()
	for ind, coord in enumerate(coordList):
		if ind not in removeInd:
			okInds.append(ind)
	#print(okInds)

	# Calculate area
	areas = list()
	for ind in okInds:
		areaPixels = np.where(coordMap == ind)
		areas.append(len(areaPixels[0]))

	return max(areas)


def partOne():
	coordList = parseFile("input.txt")
	#print(coordList)

	coordMap = placeCoords(coordList)
	#print(np.transpose(coordMap))

	coordMap = fillMap(coordList, coordMap)
	#print(np.transpose(coordMap))
	plt.imshow(coordMap)
	plt.show()

	largestArea = findLargestArea(coordList, coordMap)
	print("Largest area: %d" % largestArea)

'''
Part 2
'''
def areaWithinDistance(coordList, coordMap, maxTotalDistance):
	mapDim = coordMap.shape

	# Fill map
	# Check every pixel of map
	for x in range(mapDim[0]):
		for y in range(mapDim[1]):
			# Find closest coordinate
			pixelCoord = [x, y]

			# Calculate distance to each pixel
			pixelDist = list()
			for ind, coord in enumerate(coordList):
				pixelDist.append(manhattanDistance(coord, pixelCoord))

			# Sum
			totalDistance = sum(pixelDist)
			if totalDistance < maxTotalDistance:
				coordMap[x,y] = 1
			else:
				coordMap[x,y] = 0
	
	return coordMap 


def partTwo():
	coordList = parseFile("input.txt")
	#print(coordList)

	coordMap = placeCoords(coordList)
	#print(np.transpose(coordMap))

	maxTotalDistance = 10000
	coordMap = areaWithinDistance(coordList, coordMap, maxTotalDistance)
	#print(np.transpose(coordMap))
	plt.imshow(coordMap)
	plt.show()

	# Calculate area
	areaPixels = np.where(coordMap == 1)
	totalArea = len(areaPixels[0])
	print("Largest area: %d" % totalArea)


'''
Main
'''
if __name__ == '__main__':
	partTwo()