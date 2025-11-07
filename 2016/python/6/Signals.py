'''
Input
'''
def parseInput(filename):
	f = open(filename, "r")
	data = f.read()

	data = data.split()

	return data

'''
Part One
'''
# List of characters
CHAR_START = 97
NUM_CHARS = 26

CHARS = list()
for i in range(NUM_CHARS):
	CHARS.append(chr(i+CHAR_START))

def partOne():
	data = parseInput("input.txt")

	# Split into column data
	column_strings = [""] * len(data[0])
	for line in data:
		for i in range(len(column_strings)):
			column_strings[i] += line[i]

	# Check number of occurance
	message = ""
	for string in column_strings:
		occurance = [0] * NUM_CHARS

		for i, char in enumerate(CHARS):
			occurance[i] = string.count(char)

		max_ind = occurance.index(max(occurance))
		message += CHARS[max_ind]

	print("The message is: %s" % message)


'''
Part Two
'''
def partTwo():
	data = parseInput("input.txt")

	# Split into column data
	column_strings = [""] * len(data[0])
	for line in data:
		for i in range(len(column_strings)):
			column_strings[i] += line[i]

	# Check number of occurance
	message = ""
	for string in column_strings:
		occurance = [0] * NUM_CHARS

		for i, char in enumerate(CHARS):
			count = string.count(char)
			if count == 0:
				occurance[i] = len(string)
			else:
				occurance[i] = count

		max_ind = occurance.index(min(occurance))
		message += CHARS[max_ind]

	print("The message is: %s" % message)

'''
Main
'''
if __name__ == '__main__':
	#partOne()
	partTwo()