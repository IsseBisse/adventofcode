import cmath
import math

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

		for i, entry in enumerate(data):
			data[i] = (entry[0], int(entry[1:]))

	return data

class Ship:
	DIRECTIONS = {"N": (0, 1),
		"E": (1, 0),
		"S": (0, -1),
		"W": (-1, 0)}

	DIRECTION_TO_IND = {"N": 0,
		"E": 1,
		"S": 2,
		"W": 3}

	TURN = {"R": 1,
		"L": -1}

	def __init__(self):
		self.pos = [0, 0]

		self.direction_ind = 1

	def __str__(self):
		keys_list = list(self.DIRECTIONS.keys())
		return "Ship @ (%d, %d) facing %s" % (self.pos[0], self.pos[1], keys_list[self.direction_ind])

	def move(self, direction_char, distance):

		# Turn		
		move = True
		if direction_char in self.TURN:
			self.direction_ind = int(self.direction_ind + self.TURN[direction_char] * distance/90) % 4
			move = False

		elif direction_char in self.DIRECTIONS:
			direction = self.DIRECTIONS[direction_char]

		else:
			keys_list = list(self.DIRECTIONS.keys())	
			direction = self.DIRECTIONS[keys_list[self.direction_ind]]

		# Move
		if move:
			for i in range(2):
				self.pos[i] += direction[i] * distance

	def get_distance(self):
		return sum([abs(coord) for coord in self.pos])

def part_one():
	data = get_data("input.txt")
	ship = Ship()
	print(data)
	print(ship)

	for entry in data:
		ship.move(entry[0], entry[1])
		print(ship)

	print("Ship is %d units away" % ship.get_distance())

class WaypointShip:
	TURN = {"R": -1,
		"L": 1}

	WAYPOINT_DIRECTIONS = {"N": 1j,
		"E": 1,
		"S": -1j,
		"W": -1}

	def __init__(self):
		self.pos = 0 + 0j
		self.waypoint = 10 + 1j
		self.direction_ind = 1

	def __str__(self):
		string = "Ship @ (%d, %d) " % (self.pos.real, self.pos.imag)
		string += "with waypoint (%d, %d)" % (self.waypoint.real, self.waypoint.imag)

		return string
		
	def move_command(self, command, value):
		if command in self.TURN:
			self.turn(command, value)

		elif command in self.WAYPOINT_DIRECTIONS:
			self.move_waypoint(command, value)

		else:
			self.move(value) 

	def turn(self, direction, angle):
		# Convert to polar and turn
		waypoint_pol = cmath.polar(self.waypoint)
		new_waypoint_pol = (waypoint_pol[0], waypoint_pol[1] + self.TURN[direction] * math.radians(angle))
		
		# Convert back and round
		new_waypoint = cmath.rect(new_waypoint_pol[0], new_waypoint_pol[1])
		self.waypoint = complex(round(new_waypoint.real), round(new_waypoint.imag))

	def move(self, distance):
		self.pos += self.waypoint * distance

	def move_waypoint(self, direction, distance):
		self.waypoint += self.WAYPOINT_DIRECTIONS[direction] * distance

	def get_distance(self):
		return abs(self.pos.real) + abs(self.pos.imag)

def part_two():
	data = get_data("input.txt")
	ship = WaypointShip()
	print(ship)

	for entry in data:
		ship.move_command(entry[0], entry[1])
		print(ship)

	print("Ship is %d units away" % ship.get_distance())

if __name__ == '__main__':
	#part_one()
	part_two()