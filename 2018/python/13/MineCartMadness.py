
from TrainSystem import TrainSystem

def parseInput(filename):
	f = open(filename, "r")

	fileData = list()
	for line in f:
		lineSplit = line.split("\n")
		if type(lineSplit) == list:
			row = lineSplit[0]
		else:
			row = lineSplit

		fileData.append(row)

	trainSystem = TrainSystem(fileData)

	return trainSystem

'''
Part 1
'''
def partOne():
	mapOfTracks = parseInput("testInput.txt")
	print(mapOfTracks)

'''
Part 2
'''


'''
Main
'''
if __name__ == '__main__':
	partOne()
