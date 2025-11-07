from Marble import Marble

class Circle:

	def __init__(self, numPlayers):
		# Add marble handling
		self.currentMarble = None
		self.numMarbles = 0

		# Add player scores
		self.playerScores = list()
		for player in range(numPlayers):
			self.playerScores.append(0)
		self.currentPlayer = 0

	def __str__(self):
		string =  "==================\n"
		string += "=== Scoreboard ===\n"
		string += "==================\n"

		for ind, player in enumerate(self.playerScores):
			if ind == self.currentPlayer:
				string += "(Player %d): %d points \n" % (ind, player)
			else:
				string += "Player %d: %d points \n" % (ind, player)

		string += "\n"
		string += "===============\n"
		string += "=== Marbles ===\n"
		string += "===============\n"

		if self.currentMarble:
			# Always start from 0
			firstMarble = self.currentMarble
			while firstMarble.getNumber() != 0:
				firstMarble = firstMarble.getNext()

			# Print marble order
			firstID = firstMarble.getNumber()
			currentID = None
			currentMarble = firstMarble
			orderString = ''
			while firstID != currentID:
				if currentMarble == self.currentMarble:
					orderString += "(%d) " % currentMarble.getNumber()
				else:
					orderString += "%d " % currentMarble.getNumber()
				
				currentMarble = currentMarble.getNext()
				currentID = currentMarble.getNumber()

			string += orderString + "\n"

		return string


	def addMarble(self, marble):
		if marble.getNumber() % 23 == 0 and not marble.getNumber() == 0:
			# Remove every 23rd marble
			self.playerScores[self.currentPlayer] += marble.getNumber()

			# Selct 7th marble previous
			removeMarble = self.currentMarble
			for i in range(7):
				removeMarble = removeMarble.getPrevious()

			# Add to score...
			self.playerScores[self.currentPlayer] += removeMarble.getNumber()

			# ...and remove
			previousMarble = removeMarble.getPrevious()
			nextMarble = removeMarble.getNext()

			previousMarble.connectMarble(None, nextMarble)
			nextMarble.connectMarble(previousMarble, None)

			# Make previous marble current marble
			self.currentMarble = nextMarble
		else:
			# Add first marble
			if not self.currentMarble:
				marble.connectMarble(marble, marble)
				self.currentMarble = marble

			# Add not first marble
			else:
				# Get 1st and 2nd marble clockwise from current
				previousMarble = self.currentMarble.getNext()
				nextMarble = self.currentMarble.getNext().getNext()
				
				# Reconnect them
				previousMarble.connectMarble(None, marble)
				nextMarble.connectMarble(marble, None)

				# Connect new marble
				marble.connectMarble(previousMarble, nextMarble)
				self.currentMarble = marble

		#print(self)

		# Update current player
		self.currentPlayer += 1
		if self.currentPlayer == len(self.playerScores):
			self.currentPlayer = 0

		