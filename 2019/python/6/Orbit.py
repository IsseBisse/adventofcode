def parse_input(path):

	f = open(path, "r")
	data = [x.split(")") for x in  f.read().split("\n")]

	return data

class Planet:

	def __init__(self, name):

		self.name = name
		self.orbit_center = None

	def __str__(self):
		if self.orbit_center:
			return "Planet %s orbiting %s" % (self.name, self.orbit_center.name)

		else:
			return "Planet %s (center of universe)" % self.name

	def add_orbit(self, planet):

		self.orbit_center = planet

	def orbits_to_COM(self):

		orbits = list()

		if self.orbit_center:
			orbits.append(self.orbit_center)
			return orbits + self.orbit_center.orbits_to_COM()

		else:

			return []

	def get_num_orbits(self):

		if self.orbit_center:
			return self.orbit_center.get_num_orbits() + 1

		else:
			return 0

def arrange_orbits(data):
	planets = dict()
	for orbit in data:
		# Add planets if not already added
		for planet_name in orbit:
			if not planet_name in planets:
				planets[planet_name] = Planet(planet_name)

		center_planet = planets[orbit[0]]
		orbiting_planet = planets[orbit[1]]

		orbiting_planet.add_orbit(center_planet)

	return planets

def part_one():
	
	data = parse_input("input.txt")
	planets = arrange_orbits(data)

	total_num_orbits = 0
	for planet_name in planets:
		total_num_orbits += planets[planet_name].get_num_orbits()
		
	print("Total number of orbits: %d" % total_num_orbits)

def part_two():
	
	data = parse_input("input.txt")
	planets = arrange_orbits(data)

	your_orbits = planets["YOU"].orbits_to_COM()
	santas_orbits = planets["SAN"].orbits_to_COM()

	print("You orbit:")
	for planet in your_orbits:
		print(planet)
	print("")

	print("Santa orbits:")
	for planet in santas_orbits:
		print(planet)
	print("")

	# Find first common orbit
	print("First common orbit:")
	for your_steps, orbit in enumerate(your_orbits):
		if orbit in santas_orbits:

			first_common_orbit = orbit
			break

	for santas_steps, orbit in enumerate(santas_orbits):
		if orbit == first_common_orbit:

			break

	print("Total jumps needed: %d" % (santas_steps + your_steps))

if __name__ == '__main__':
	part_two()