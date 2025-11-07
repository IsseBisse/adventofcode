'''
Input
'''
def parseInput(filename):
	f = open(filename, "r")
	data = f.read()

	data = data.split()

	return data

'''
Helpers
'''
def findPossibleTriangles(data):
	# Find possible triangles	
	possible_triangles = 0
	for line in data:
		line = sorted(line)

		possible_triangles += int(sum(line[0:2]) > line[2])

	return possible_triangles

'''
Part One
'''
def partOne():
	data = parseInput("input.txt")

	# Sort data in groups of 3 
	sorted_data = list()
	for i in range(int(len(data) / 3)):
		sorted_data.append((int(data[i*3]), int(data[i*3 + 1]), int(data[i*3 + 2])))

	print("%d possible triangles found!" % findPossibleTriangles(sorted_data))


'''
Part Two
'''
def partTwo():
	data = parseInput("input.txt")

	# Sort data (column-wise) in groups of 3
	i = 0
	jump = 0
	sorted_data = list()

	while i < len(data) - 6:
		sorted_data.append((int(data[i]), int(data[i+3]), int(data[i+6])))

		if jump == 2:
			i += 7
		else:
			i += 1
		jump = (jump + 1) % 3

	print("%d possible triangles found!" % findPossibleTriangles(sorted_data))

'''
Main
'''
if __name__ == '__main__':
	partTwo()