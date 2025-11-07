import numpy as np
from MineCart import MineCart

class TrainSystem:

	CONT_SYMBOLS = {" ": 0, 
	"|": 3,
	"-": 4}

	EVENT_SYMBOLS = {"/" : 1,
	"\\": 2,
	"+": 5}

	TRAIN_SYMBOLS = {"^": -1,
	">": -2,
	"<": -3,
	"v": -4}

	MAP_SYMBOLS = {**CONT_SYMBOLS,
	**EVENT_SYMBOLS,
	**TRAIN_SYMBOLS}

	INV_MAP_SYMBOLS = {v: k for k, v in MAP_SYMBOLS.items()}

	def __init__(self, fileData):
		self.mapOfTracks, self.carts = self.createMapAndCarts(fileData)

	def __str__(self):
		string = ""

		# Print map
		height = self.mapOfTracks.shape[0]
		width = self.mapOfTracks.shape[1]

		for row in range(height):
			for col in range(width):
				string += self.INV_MAP_SYMBOLS[self.mapOfTracks[row, col]]
			string += "\n"

		string += "\n=== Carts ===\n"

		# Print list of carts
		for cart in self.carts:
			string += str(cart)

		return string

	'''
	Map handling
	'''
	def createMapAndCarts(self, fileData):
		# Create map of train tracks
		width = len(fileData[0])
		height = len(fileData)

		mapOfTracks = np.zeros((height, width))
		scarts = list()
		for row, line in enumerate(fileData):
			for col, char in enumerate(line):
				mapOfTracks[row, col] = self.MAP_SYMBOLS[char]

				# Add cart to list
				symbolIndex = self.MAP_SYMBOLS[char]
				if symbolIndex < 0:
					position = [row, col]
					velocity = abs(symbolIndex)
					carts.append(MineCart(position, velocity))

		# Remove carts from map of train tracks

		return mapOfTracks, carts

	def getSurroundingPixels(self, position):
		surroundingPixels = 

	def tick(self):
		