def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	return data

def move_to_loc(move):
	if move == ">":
		return [1,0]

	elif move == "<":
		return [-1,0]
	
	elif move == "^":
		return [0,1]
	
	elif move == "v":
		return [0,-1]

	else:
		print("Got unexpected char: %s" % move)
		return -1

def add_loc(loc1, loc2):
	if len(loc1) != len(loc2):
		return -1

	new_loc = list()
	for dim in range(len(loc1)):
		new_loc.append(loc1[dim] + loc2[dim])

	return new_loc

def add_house(visited_houses, loc):

	loc_string = "%s" % loc
	if loc_string in visited_houses:
		visited_houses[loc_string] += 1

	else:
		visited_houses[loc_string] = 1

def part_one():
	data = get_data("input.txt")

	visited_houses = dict()
	loc = [0,0]
	add_house(visited_houses, loc)

	for move in data[0]:
		loc_diff = move_to_loc(move)
		loc = add_loc(loc, loc_diff)

		add_house(visited_houses, loc)

	print(len(visited_houses))
	
def part_two():
	data = get_data("input.txt")

	visited_houses = dict()
	santa_loc = [0,0]
	robo_loc = [0,0]
	add_house(visited_houses, santa_loc)

	santas_turn = True
	for move in data[0]:
		loc_diff = move_to_loc(move)
		
		if santas_turn:
			santa_loc = add_loc(santa_loc, loc_diff)
			add_house(visited_houses, santa_loc)

		else:
			robo_loc = add_loc(robo_loc, loc_diff)
			add_house(visited_houses, robo_loc)

		santas_turn = not santas_turn

	print(len(visited_houses))

if __name__ == '__main__':
	part_one()
	part_two()