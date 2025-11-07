import re
from ResevoirMap import ResevoirMap 

def parseInput(filename):
	f = open(filename, "r")

	map_data = list()
	for line in f:
		# Split x- and y-coord
		coord_strings = line.split(", ")
		
		# Parse out integers
		coord_values = list()
		for string in coord_strings:
			coord_values.append([int(s) for s in re.findall("(\d+)", string)])

		# Store arrange to (x,y) format
		coord = [None] * 2
		for i in range(2):
			if i == 0:
				value = coord_values[i]
			else:
				value = list(range(coord_values[i][0], coord_values[i][1] + 1))

			if coord_strings[i][0] == "x":
				coord[0] = value
			else:
				coord[1] = value

		map_data.append(coord)

	return map_data

'''
Part 1
'''
def partOne(map_data):
	resevoir_map = ResevoirMap(map_data)

'''
Part 2
'''


'''
Main
'''
if __name__ == '__main__':
	map_data = parseInput("testinput.txt")
	partOne(map_data)