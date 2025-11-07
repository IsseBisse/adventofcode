class MineCart:

	LEFT = 3
	RIGHT = 2
	UP = 1
	DOWN = 4


	def __init__(self, position, velocity):
		self.position = position
		self.velocity = velocity

	def __str__(self):
		return "Cart at (%d, %d) with velocity (%d, %d).\n" % (self.position[0], self.position[1], self.velocity[0], self.velocity[1])

	def updatePosition(self):
		if self.velocity == self.LEFT:
			self.position[1] -= 1
		elif self.velocity == self.RIGHT:
			self.position[1] += 1
		elif self.velocity == self.UP:
			self.position[0] -= 1
		elif self.velocity == self.DOWN:
			self.position[0] += 1