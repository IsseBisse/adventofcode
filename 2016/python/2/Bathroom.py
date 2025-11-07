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
KEYPAD = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
DIRECTIONS = {"U": -1j, "D": 1j, "L": -1, "R": 1}

def partOne():
	# Get input
	data = parseInput("input.txt")
	
	# Parameters
	code = list()
	loc = 1 + 1j

	for line in data:
		for char in line:
			loc += DIRECTIONS[char]

			# Check if outside keypad
			loc = min(max(loc.real, 0), 2) + min(max(loc.imag, 0), 2) * 1j

		code.append(KEYPAD[int(loc.imag)][int(loc.real)])

	print(code)

'''
Part Two
'''
KEYPAD = [[-1, -1, -1, -1, -1, -1, -1],
	[-1, -1, -1, 1, -1, -1, -1],
	[-1, -1, 2, 3, 4, -1, -1],
	[-1, 5, 6, 7, 8, 9, -1],
	[-1, -1, "A", "B", "C", -1, -1],
	[-1, -1, -1, "D", -1, -1, -1],
	[-1, -1, -1, -1, -1, -1, -1]]
DIRECTIONS = {"U": -1j, "D": 1j, "L": -1, "R": 1}


def partTwo():
	# Get input
	data = parseInput("input.txt")
	
	# Parameters
	code = list()
	loc = 1 + 3j

	for line in data:
		for char in line:
			old_loc = loc
			loc += DIRECTIONS[char]

			# Check if outside keypad
			if KEYPAD[int(loc.imag)][int(loc.real)] == -1:
				loc = old_loc
			
		code.append(KEYPAD[int(loc.imag)][int(loc.real)])

	print(code)

'''
Main
'''
if __name__ == '__main__':
	partTwo()