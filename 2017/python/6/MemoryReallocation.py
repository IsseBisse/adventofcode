def readInput(filename):
	f = open(filename, "r")

	data = list()
	for line in f:
		row = line.split("\t")

		for string in row:
			data.append(int(string))

	return data

'''
Part one
'''	
def maxInd(values):
	return values.index(max(values))

def redistribute(values):
	redist_index = maxInd(values)
	redist_value = values[redist_index]

	values[redist_index] = 0
	for i in range(redist_value):
		index = (redist_index + i + 1) % len(values)
		values[index] += 1

	return values

def partOne():
	data = readInput("input.txt")
	#data = [0, 2, 7, 0]

	seen = set()
	laps = 0
	while str(data) not in seen:
		# Add old permutation...
		seen.add(str(data))

		# ...and redistribute
		data = redistribute(data)
		
		laps += 1

	seen = set()
	laps = 0
	while str(data) not in seen:
		# Add old permutation...
		seen.add(str(data))

		# ...and redistribute
		data = redistribute(data)
		
		laps += 1

	print("Number of redistributions needed: %d" % laps)

'''
Part two
'''
def partTwo():
	data = readInput("input.txt")


if __name__ == '__main__':
	partOne()
	