import numpy as np
import math

def parse_input(path):

	f = open(path, "r")

	data = [x for x in  f.read().split("\n")]
	grid = np.zeros((len(data), len(data[0])))

	for row, line in enumerate(data):
		for col, char in enumerate(line):
			if char == "#":
				grid[row, col] = 1

	return grid

def cart2pol(x, y):

	rho = np.sqrt(x**2 + y**2)
	phi = np.arctan2(y, x)
	return (rho, phi)

def part_one(path):
	
	grid = parse_input(path)

	asteroid_coords = np.where(grid == 1)
	num_asteroids = len(asteroid_coords[0])
	max_seen_asteroids = 0
	max_seen_asteroids_ind = -1 
	for i in range(num_asteroids):
		# Monitoring station candidate
		x0 = asteroid_coords[1][i]
		y0 = asteroid_coords[0][i]

		seen_asteroids = list()

		for j in range(num_asteroids):
			x = asteroid_coords[1][j]
			y = asteroid_coords[0][j]

			if not (x0 == x and y0 == y):
				(_, phi) = cart2pol(x-x0, y-y0)

				if not phi in seen_asteroids:
					seen_asteroids.append(phi)

		num_seen_asteroids = len(seen_asteroids) 
		if num_seen_asteroids > max_seen_asteroids:
			max_seen_asteroids = num_seen_asteroids
			max_seen_asteroids_ind = i

	print("Maximum seen asteroids: %d from (%d, %d)" % (max_seen_asteroids, asteroid_coords[1][max_seen_asteroids_ind], asteroid_coords[0][max_seen_asteroids_ind]))
	return (asteroid_coords[1][max_seen_asteroids_ind], asteroid_coords[0][max_seen_asteroids_ind])

def part_two(station_coords, path):
	
	grid = parse_input(path)
	
	# Station coords
	x0 = station_coords[0]
	y0 = station_coords[1]
	grid[y0, x0] = 2

	# Sort asteroids
	asteroid_coords = np.where(grid == 1)
	num_asteroids = len(asteroid_coords[0])
	asteroids_by_angle = dict()
	for i in range(num_asteroids):
		
		x = asteroid_coords[1][i]
		y = asteroid_coords[0][i]

		if not (x0 == x and y0 == y):
			(rho, phi) = cart2pol(x-x0, -(y-y0))


			# Parallell to y-axis pointing up should be phi=0
			phi -= math.pi/2
			if phi > 0:
				phi -= 2*math.pi

			# Add to dict
			asteroid = {"cart": (x, y), "pol": (rho, phi)}			
			if phi not in asteroids_by_angle:
				asteroids_by_angle[phi] = list()

			asteroids_by_angle[phi].append(asteroid)

	# Sort each angle by distance to station
	for phi in asteroids_by_angle:

		asteroids_by_angle[phi] = sorted(asteroids_by_angle[phi], key = lambda asteroid: asteroid["pol"][0])

	# Get kill order
	angles = sorted(list(asteroids_by_angle), reverse=True)
	kill_order = list()
	i = 0
	while len(kill_order) < num_asteroids:
		
		phi = angles[i]
		if len(asteroids_by_angle[phi]) > 0:
			asteroid = asteroids_by_angle[phi][0]
			del asteroids_by_angle[phi][0]
			kill_order.append(asteroid)

		i = (i + 1) % len(angles)

	return kill_order

if __name__ == '__main__':
	
	path = "input.txt"
	station_coords = part_one(path)
	print("(%d, %d) best station pos for %s" % (station_coords[0], station_coords[1], path))

	#station_coords = (8, 3)
	kill_order = part_two(station_coords, path)
	for i, asteroid in enumerate(kill_order):
		print("#%d at (%d, %d)" % (i+1, asteroid["cart"][0], asteroid["cart"][1]))
	