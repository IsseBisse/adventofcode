import numpy as np

class Mover:
	DIRECTIONS = ((1, 0), (0, 1), (-1, 0), (0, -1)) # north, east, south, west

	def __init__(self):
		self.position = 0 + 0j
		self.heading = 1

		self.visited_positions = set()
		self.visited_positions.add(self.position)

	def __str__(self):
		string = "Current position (x,y) is (%d, %d).\n" % (self.position.real, self.position.imag)
		string += "Distance is %d blocks away." % (abs(self.position.real) + abs(self.position.imag))

		return string

	'''
	Movement
	'''
	def move(self, command):
		turn = command[0]
		distance = int(command[1:])

		if turn == "R":
			self.heading *= 1j
		else:
			self.heading *= -1j

		for i in range(distance):
			self.position += self.heading

			continue_moving = not(self.position in self.visited_positions)
			if continue_moving:
				self.visited_positions.add(self.position)
			else:
				break
		
		return continue_moving
		