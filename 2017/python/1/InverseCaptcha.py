def readInput(filename):
	f = open(filename, "r")

	data = list()
	for line in f:
		data = line

	return data

def partOne():
	data = readInput("input.txt")

	cumSum = 0
	for ind, char in enumerate(data):
		nextInd = (ind + 1) % len(data)

		if char == data[nextInd]:
				cumSum += int(char)

	print(cumSum)

def partTwo():
	data = readInput("input.txt")

	cumSum = 0
	increment = int(len(data) / 2)
	for ind, char in enumerate(data):
		nextInd = (ind + increment) % len(data)

		if char == data[nextInd]:
				cumSum += int(char)

	print(cumSum)


if __name__ == '__main__':
	partTwo()