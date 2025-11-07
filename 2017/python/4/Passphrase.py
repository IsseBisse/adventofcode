def readInput(filename):
	f = open(filename, "r")

	data = list()
	for line in f:
		row = line.split("\n")[0]
		#row = row.split("\t")

		data.append(row)

	return data

'''
Part one
'''	
def partOne():
	data = readInput("input.txt")

	number_of_valid = 0
	# For each pass phrase
	for phrase in data:
		# Split into each word
		words = phrase.split(" ")

		valid = True
		seen = set()
		for word in words:
			if word in seen:
				valid = False
				break

			seen.add(word)

		if valid:
			number_of_valid += 1

	print("Number of valid phrases: %d" % number_of_valid)

'''
Part two
'''
def partTwo():
	data = readInput("input.txt")

	number_of_valid = 0
	# For each pass phrase
	for phrase in data:
		# Split into each word
		words = phrase.split(" ")

		valid = True
		seen = set()
		for word in words:
			sorted_word = "".join(sorted(word))

			if sorted_word in seen:
				valid = False
				break

			seen.add(sorted_word)

		if valid:
			number_of_valid += 1

	print("Number of valid phrases: %d" % number_of_valid)


if __name__ == '__main__':
	partTwo()