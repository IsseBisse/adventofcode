class Pot:
	def __init__(self, number):
		self.number = number
		self.plant = False

	def __str__(self):
		if self.hasPlant():
			return "#"
		else:
			return "."

	'''
	Plant
	'''
	def setPlant(self, plant):
		self.plant = plant

	def hasPlant(self):
		return self.plant

	'''
	Getters
	'''
	def getNumber(self):
		return self.number