from collections import deque
from Pot import Pot

class PotRow:
	def __init__(self, data):
		self.generation = 0

		# Create row of pots
		self.pots = deque()
		for ind, state in enumerate(data["initial"]):
			pot = Pot(ind)
			pot.setPlant(state)

			self.pots.append(pot)

		# Save evolution table
		self.evolution = data["table"]

	def __str__(self):
		string = "%3d: " % self.generation

		for pot in self.pots:
			string += str(pot)

		return string

	def addEgdePots(self):
		edgeLength = 3 # Minimum number of empty pots on each side
