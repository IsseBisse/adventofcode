class Marble:

	def __init__(self, number):
		self.number = number

	def __str__(self):
		return "Marble #%d" % self.number

	def connectMarble(self, previous, following):
		if previous:
			self.previous = previous
		
		if following:
			self.next = following

	'''
	Setters and getters
	'''
	def getPrevious(self):
		return self.previous

	def getNext(self):
		return(self.next)

	def getNumber(self):
		return(self.number)