def parseInput(filename, selectedRow):
	f = open(filename, "r")

	input = list()
	for line in f:
		parts = line.split("\n")

		if type(parts) == list:
			string = parts[0]

		input.append(string)

	# Select one row
	string = input[selectedRow]

	# Convert to dict
	input = dict()
	parts = string.split()

	input["numPlayers"] = int(parts[0])
	input["lastMarble"] = int(parts[6])
	if len(parts) == 12:
		input["highScore"] = int(parts[11])

	return input

'''
Part 1
'''
from Circle import Circle
from Marble import Marble

def playGame(gameInfo):
	numPlayers = gameInfo["numPlayers"]
	#numMarbles = 100 * gameInfo["lastMarble"] + 1 # Part two
	numMarble = gameInfo["lastMarble"] + 1 # Part one

	# Create circle
	circle = Circle(numPlayers)

	# Create unused marbles
	unusedMarbles = list()
	for i in range(numMarbles):
		unusedMarbles.append(Marble(i))

	# Play game
	for marble in unusedMarbles:
		circle.addMarble(marble)

	playerScores = circle.playerScores
	winningScore = max(playerScores)

	return winningScore


def partOne():
	gameInfo = parseInput("input.txt", 0)

	result = playGame(gameInfo)
	print("The winning score is: %d" % result)


'''
Part 2
'''
# See comment in playGame()

'''
Main
'''
if __name__ == '__main__':
	partOne()