'''
Part 1
'''
def parseInput(filename):
	f = open(filename, "r")

	# Read .txt file and parse into list of strings
	input = list()
	for line in f:
		lineSplit = line.split("\n")
		if type(lineSplit) == list:
			lineStr = lineSplit[0]
		else:
			lineStr = lineSplit

		input.append(lineStr)

	return input

def countLetters(string):
	letterCount = dict()

	# Loop through char in strings and count occurence
	for char in string:
		if char in letterCount:
			letterCount[char] += 1
		else:
			letterCount[char] = 1

	return letterCount

def partOne():
	input = parseInput("input.txt")

	# Count number of duplicates and triplets
	numDup = 0
	numTri = 0
	for string in input:
		#print(string)
		letterCount = countLetters(string) 
		#print(letterCount)

		foundDup = False
		foundTri = False
		for key, value in letterCount.items():
			# Add if duplicate
			if value == 2 and not foundDup:
				numDup += 1
				foundDup = True
				#print('Duplicate found!')

			# Add if triplet
			if value == 3 and not foundTri:
				numTri += 1
				foundTri = True
				#print('Triplet found!')

	print('Duplicates: %d, Triplets: %d' % (numDup, numTri))
	print('Checksum: %d' % (numDup * numTri))


'''
Part 2
'''
import numpy as np

def stringDistance(string1, string2):
	distance = 0

	for ind, char in enumerate(string1):
		if char != string2[ind]:
			distance += 1
	
	return distance

def findSameChars(string1, string2):
	sameChars = list()

	for ind, char in enumerate(string1):
		if char == string2[ind]:
			sameChars.append(char)
	
	return ''.join(sameChars)

def partTwo():
	input = parseInput("input.txt")

	dim = (len(input), len(input))
	dist = np.zeros(dim, dtype=np.int)
	#print(dist)
	for ind, string in enumerate(input):
		for compInd, compString in enumerate(input):
			dist[ind, compInd] = stringDistance(string, compString)
	
	#print(dist)
	sameCharsInd = np.where(dist==1)
	string1 = input[sameCharsInd[0][0]]
	string2 = input[sameCharsInd[0][1]]
	print(findSameChars(string1, string2))

'''
Main
'''
if __name__ == '__main__':
	partTwo()