def readInput(filename):
	f = open(filename, "r")

	data = list()
	for line in f:
		row = line.split("\n")[0]
		row = row.split("\t")
		
		for i, element in enumerate(row):
			row[i] = int(element)

		data.append(row)

	return data

'''
Part one
'''
def maxDiff(row):
	return max(row) - min(row)
	
def partOne():
	data = readInput("input.txt")

	checksum = 0
	for row in data:
		checksum += maxDiff(row)

	print(checksum)


'''
Part two
'''
def evenDivisible(row):
	for first_number in row:
		for second_number in row:
			if (first_number % second_number == 0) & (first_number != second_number):
				#print("First: %d. Second: %d" % (first_number, second_number))

				return int(first_number / second_number)

def partTwo():
	data = readInput("input.txt")

	checksum = 0
	for row in data:
		checksum += evenDivisible(row)

	print(checksum)


if __name__ == '__main__':
	partTwo()