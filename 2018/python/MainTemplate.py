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

'''
Part 1
'''


'''
Part 2
'''


'''
Main
'''
if __name__ == '__main__':
	main()