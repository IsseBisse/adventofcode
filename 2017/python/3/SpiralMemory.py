'''
Part one
'''
def addCoords(coord1, coord2):
	return [coord1[0] + coord2[0], coord1[1] + coord2[1]]

def manhattanDistance(coord):
	return abs(coord[0]) + abs(coord[1])

def partOne(data):
	coords = [0, 0]

	directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]
	directions_index = 0

	distance_current = 0
	distance_turn = 1
	distance_increase = False

	i = 1
	while i < data:
		# Update
		coords = addCoords(coords, directions[directions_index])
		distance_current += 1
		i += 1

		# Check if turn
		if distance_current == distance_turn:
			# Turn
			distance_current = 0
			directions_index = (directions_index + 1) % 4

			# Check if increase distance
			if distance_increase:
				# Increase every other turn
				distance_turn += 1
				distance_increase = False
			else:
				distance_increase = True 

		#print(coords)

	print("Distance: %d" % manhattanDistance(coords))

'''
Part two
'''
#def partTwo():


if __name__ == '__main__':
	partOne(368078)