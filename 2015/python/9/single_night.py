from itertools import permutations

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	return data

def parse_data(data):
	routes = list()
	for entry in data:
		route_string, distance_string = entry.split(" = ")
		origin, destination = route_string.split(" to ")

		routes.append((origin, destination, int(distance_string)))

	destinations = set([route[0] for route in routes] + 
		[route[1] for route in routes])

	return routes, destinations

def get_route_dict(routes, destinations):
	# Get dict of possible destinations
	route_dict = {dest: dict() for dest in destinations}

	for route in routes:
		route_dict[route[0]][route[1]] = route_dict[route[1]][route[0]] = route[2]

	return route_dict

def calculate_distance(journey, route_dict):
	distance = 0
	for i, destination in enumerate(journey[1:]):
		origin = journey[i]

		distance += route_dict[origin][destination]

	return distance

def part_one():
	data = get_data("input.txt")
	
	routes, destinations = parse_data(data)
	# route_dict, start_point = get_route_dict(routes, destinations)
	route_dict = get_route_dict(routes, destinations)

	print(route_dict)

	destinations = set(route_dict.keys())
	journeys = permutations(destinations)

	valid_journeys = list()
	for journey in journeys:
		distance = calculate_distance(journey, route_dict)
		
		if distance is not None:
			valid_journeys.append((distance, journey))

	valid_journeys.sort(key=lambda x:x[0])
	print(valid_journeys[-1])
	
def part_two():
	pass

if __name__ == '__main__':
	part_one()