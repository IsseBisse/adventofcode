def parseInput(filename):
	f = open(filename, "r")

	data = dict()
	data["table"] = [False] * 32 

	ind = 0
	for line in f:
		line = line.split("\n")
		line = line[0]

		if ind == 0:
			stateOld = line.split(": ")[1]
			
			stateNew = list()
			for state in stateOld:
				if state == "#":
					stateNew.append(True)
				else:
					stateNew.append(False)

			data["initial"] = list(stateNew)

		elif ind > 1:
			nextState = line.split(" => ")[1]
			if nextState == "#":
				nextState = True
			else:
				nextState = False

			currStateOld = line.split(" => ")[0]
			currState = ""
			for state in currStateOld:
				if state == "#":
					currState += '1'
				else:
					currState += '0'

			data["table"][int(currState, 2)] = nextState
			#print("In: " + currState)
			#print("Out: " + nextState)

		ind += 1

	return data

'''
Part 1
'''
from PotRow import PotRow

def partOne():
	data = parseInput("testInput.txt")

	potRow = PotRow(data)
	print(potRow)


'''
Part 2
'''


'''
Main
'''
if __name__ == '__main__':
	partOne()