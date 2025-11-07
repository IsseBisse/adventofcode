import copy

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")
		data = [[char for char in line] for line in data]

	return data

class Universe:
	def __init__(self, initial_state):
		self.active_cubes = dict()	# dict[z] of dict[y] of dict[x]
		
		z = 0
		for y, line in enumerate(initial_state):
			for x, char in enumerate(line):
				if char == "#":
					self.set_state((x, y, z), True)


	def __str__(self):
		string = "{num_active} active cubes at (x, y, z):\n".format(num_active=len(self.get_active_cube_coords()))
		for coords in self.get_active_cube_coords():
			string += "{coords}\n".format(coords=coords)

		return string

	def set_state(self, coords, is_active):
		(x, y, z) = coords

		if not z in self.active_cubes:
			self.active_cubes[z] = dict()

		if not y in self.active_cubes[z]:
			self.active_cubes[z][y] = dict()

		self.active_cubes[z][y][x] = is_active

	def get_state(self, coords):
		(x, y, z) = coords

		if z in self.active_cubes:
			if y in self.active_cubes[z]:
				if x in self.active_cubes[z][y]:
					return self.active_cubes[z][y][x]

		return False

	def get_active_cube_coords(self):
		active_cube_coords = list()

		for z in self.active_cubes:
			for y in self.active_cubes[z]:
				for x in self.active_cubes[z][y]:
					if self.active_cubes[z][y][x]:
						active_cube_coords.append((x, y, z))

		return active_cube_coords

	@staticmethod
	def get_nearby_coords(coords):
		(x, y, z) = coords
		nearby_coords = list()

		for xd in range(-1, 2):
			for yd in range(-1, 2):
				for zd in range(-1, 2):
					nearby_coords.append((x+xd, y+yd, z+zd))

		nearby_coords.remove((x, y, z))
		
		return nearby_coords

	def change_state(self, coords, active_coords):
		is_active = coords in active_coords

		nearby_coords = set(Universe.get_nearby_coords(coords))
		nearby_active_coords = nearby_coords.intersection(set(active_coords))

		if is_active and (len(nearby_active_coords)==2 or len(nearby_active_coords)==3):
			# Remain active cube
			self.set_state(coords, True)

		elif not is_active and len(nearby_active_coords)==3:
			# Activate cube
			self.set_state(coords, True)

		else:
			# Deactivate cube
			self.set_state(coords, False)

	def next_state(self):
		old_active_cube_coords = self.get_active_cube_coords()

		for active_coords in old_active_cube_coords:
			self.change_state(active_coords, old_active_cube_coords)

			nearby_coords = Universe.get_nearby_coords(active_coords)
			for coords in nearby_coords:
				self.change_state(coords, old_active_cube_coords)


def part_one():
	initial_state = get_data("input.txt")
	universe = Universe(initial_state)
	
	for i in range(6):
		universe.next_state()
		#print(universe)
		print("{num_active} active cubes after {num_cycles} cycles.".format(num_active=len(universe.get_active_cube_coords()), num_cycles=i+1))
	
# class Universe4D:
# 	def __init__(self, initial_state):
# 		self.active_cubes = dict()	# dict[z] of dict[y] of dict[x]
		
# 		z = 0
# 		w = 0
# 		for y, line in enumerate(initial_state):
# 			for x, char in enumerate(line):
# 				if char == "#":
# 					self.set_state((x, y, z, w), True)


# 	def __str__(self):
# 		string = "{num_active} active cubes at (x, y, z, w):\n".format(num_active=len(self.get_active_cube_coords()))
# 		for coords in self.get_active_cube_coords():
# 			string += "{coords}\n".format(coords=coords)

# 		return string

# 	def set_state(self, coords, is_active):
# 		(x, y, z, w) = coords

# 		if not w in self.active_cubes:
# 			self.active_cubes[w] = dict()

# 		if not z in self.active_cubes[w]:
# 			self.active_cubes[w][z] = dict()

# 		if not y in self.active_cubes[w][z]:
# 			self.active_cubes[w][z][y] = dict()

# 		self.active_cubes[w][z][y][x] = is_active

# 	def get_state(self, coords):
# 		(x, y, z, w) = coords

# 		if w in self.active_cubes:
# 			if z in self.active_cubes[w]:
# 				if y in self.active_cubes[w][z]:
# 					if x in self.active_cubes[w][z][y]:
# 						return self.active_cubes[w][z][y][x]

# 		return False

# 	def get_active_cube_coords(self):
# 		active_cube_coords = list()

# 		for w in self.active_cubes:
# 			for z in self.active_cubes[w]:
# 				for y in self.active_cubes[w][z]:
# 					for x in self.active_cubes[w][z][y]:
# 						if self.active_cubes[w][z][y][x]:
# 							active_cube_coords.append((x, y, z, w))

# 		return active_cube_coords

# 	@staticmethod
# 	def get_nearby_coords(coords):
# 		(x, y, z, w) = coords
# 		nearby_coords = list()

# 		for xd in range(-1, 2):
# 			for yd in range(-1, 2):
# 				for zd in range(-1, 2):
# 					for wd in range(-1, 2):
# 						nearby_coords.append((x+xd, y+yd, z+zd, w+wd))

# 		nearby_coords.remove((x, y, z, w))
		
# 		return nearby_coords

# 	def change_state(self, coords, active_coords):
# 		is_active = coords in active_coords

# 		nearby_coords = set(Universe4D.get_nearby_coords(coords))
# 		nearby_active_coords = nearby_coords.intersection(set(active_coords))

# 		if is_active and (len(nearby_active_coords)==2 or len(nearby_active_coords)==3):
# 			# Remain active cube
# 			self.set_state(coords, True)

# 		elif not is_active and len(nearby_active_coords)==3:
# 			# Activate cube
# 			self.set_state(coords, True)

# 		else:
# 			# Deactivate cube
# 			self.set_state(coords, False)

# 	def next_state(self):
# 		old_active_cube_coords = self.get_active_cube_coords()

# 		for active_coords in old_active_cube_coords:
# 			self.change_state(active_coords, old_active_cube_coords)

# 			nearby_coords = Universe4D.get_nearby_coords(active_coords)
# 			for coords in nearby_coords:
# 				self.change_state(coords, old_active_cube_coords)

class Universe4D:
	def __init__(self, initial_state):
		self.active_coords = dict()	# dict[coords] of all passed cubes (i.e. once active or inactive)
		
		z = 0
		w = 0
		for y, line in enumerate(initial_state):
			for x, char in enumerate(line):
				if char == "#":
					self.set_state((x, y, z, w), True)


	def __str__(self):
		string = "{num_active} active cubes at (x, y, z, w):\n".format(num_active=len(self.get_active_cube_coords()))
		for coords in self.get_active_cube_coords():
			string += "{coords}\n".format(coords=coords)

		return string

	def set_state(self, coords, is_active):
		if is_active:
			self.active_coords[coords] = is_active

		else:
			self.active_coords.pop(coords, None)

	def get_active_cube_coords(self):
		return list(self.active_coords.keys())


	@staticmethod
	def get_nearby_coords(coords):
		(x, y, z, w) = coords
		nearby_coords = list()

		for xd in range(-1, 2):
			for yd in range(-1, 2):
				for zd in range(-1, 2):
					for wd in range(-1, 2):
						nearby_coords.append((x+xd, y+yd, z+zd, w+wd))

		nearby_coords.remove((x, y, z, w))
		
		return nearby_coords

	def change_state(self, coords, active_coords):
		is_active = coords in active_coords

		nearby_coords = set(Universe4D.get_nearby_coords(coords))
		nearby_active_coords = nearby_coords.intersection(set(active_coords))

		if is_active and (len(nearby_active_coords)==2 or len(nearby_active_coords)==3):
			# Remain active cube
			self.set_state(coords, True)

		elif not is_active and len(nearby_active_coords)==3:
			# Activate cube
			self.set_state(coords, True)

		else:
			# Deactivate cube
			self.set_state(coords, False)

	def next_state(self):
		old_active_cube_coords = self.get_active_cube_coords()

		for active_coords in old_active_cube_coords:
			self.change_state(active_coords, old_active_cube_coords)

			nearby_coords = Universe4D.get_nearby_coords(active_coords)
			for coords in nearby_coords:
				self.change_state(coords, old_active_cube_coords)

def part_two():
	initial_state = get_data("input.txt")
	universe = Universe4D(initial_state)
	
	for i in range(6):
		universe.next_state()
		#print(universe)
		print("{num_active} active cubes after {num_cycles}.".format(num_active=len(universe.get_active_cube_coords()), num_cycles=i+1))

if __name__ == '__main__':
	#part_one()
	part_two()