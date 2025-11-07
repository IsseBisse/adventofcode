'''
Part 1
'''

def parseInput(filename):
	f = open(filename, "r")

	input = list()
	for line in f:
		lineSplit = line.split("\n")
		if type(lineSplit) == list:
			lineInt = int(lineSplit[0])
		else:
			lineInt = int(lineSplit)

		input.append(lineInt)

	return input

def partOne():
	input = parseInput("input.txt")
	print("Part 1: resulting frequency is %d" % sum(input))

'''
Part 2
'''

def findDuplicateFrequency(input):
	currInd = 0
	currLap = 1

	allFreq = list()
	duplicate = False
	currFreq = 0

	# Loop through list
	while ~duplicate:
		currFreq += input[currInd]

		#print("Lap: %d, Index: %d, Update: %d, Frequency: %d" % (currLap, currInd, input[currInd], currFreq))

		# Check if duplicate
		if currFreq in allFreq:
			return currFreq
		else:
			allFreq.append(currFreq)

		# Update index
		if currInd < len(input)-1:
			currInd += 1
		else:
			currInd = 0
			currLap += 1
			print("Lap: %d" % currLap)

def partTwo():
	input = parseInput("input.txt")
	print('First duplicate frequency: %d' % findDuplicateFrequency(input))

'''
Main
'''
if __name__ == '__main__':
	partOne()
	partTwo()