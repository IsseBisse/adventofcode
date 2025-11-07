class Point:

	def __init__(self, position, velocity):
		self.position = position
		self.velocity = velocity

	def __str__(self):
		string = "Pos: (%d, %d), Vel: (%d, %d)" % (self.position[0], self.position[1], self.velocity[0], self.velocity[1])
		return string


	def updatePosition(self):
		for i in range(len(self.position)):
			self.position[i] += self.velocity[i]


	def getPosition(self):
		return self.position