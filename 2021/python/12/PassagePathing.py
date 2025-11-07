import copy
import re

def get_data(path):
	with open(path) as file:
		data = file.read()

	return data

def parse_data(data):
	caves = set(re.findall(r"[a-zA-Z]+", data, re.MULTILINE))
	
	paths = dict()
	for path in data.split("\n"):
		origin, destination = path.split("-")

		if origin in paths:
			paths[origin].append(destination)

		else:
			paths[origin] = [destination]

		# Add return path
		if destination in paths:
			paths[destination].append(origin)

		else:
			paths[destination] = [origin]

	return paths

def find_possible_route(origin, route, paths, possible_routes):
	possible_destinations = paths[origin]
	route.append(origin)

	if origin == "end":
		possible_routes.append(route)
		return

	for dest in possible_destinations:
		if not (re.findall(r"[a-z]+", dest) and dest in route):
			find_possible_route(dest, copy.deepcopy(route), paths, possible_routes)

def part_one():
	data = get_data("input.txt")
	paths = parse_data(data)

	possible_routes = list()
	find_possible_route("start", [], paths, possible_routes)

	print(len(possible_routes))


def is_small_cave_visited_twice(route):
	small_caves_visited = list()
	for dest in route:
		if re.findall(r"[a-z]+", dest):
			if dest in small_caves_visited:
				return True

			else:
				small_caves_visited.append(dest)

	return False

def updated_find_possible_route(origin, route, paths, possible_routes):
	possible_destinations = paths[origin]
	route.append(origin)

	if origin == "end":
		possible_routes.append(route)
		return

	for dest in possible_destinations:
		if re.findall(r"[a-z]+", dest):
			if not (dest in route and is_small_cave_visited_twice(route) or 
				dest == "start"):
				updated_find_possible_route(dest, copy.deepcopy(route), paths, possible_routes)

		else:
			updated_find_possible_route(dest, copy.deepcopy(route), paths, possible_routes)
	
def part_two():
	data = get_data("input.txt")
	paths = parse_data(data)

	possible_routes = list()
	updated_find_possible_route("start", [], paths, possible_routes)

	print(len(possible_routes))

if __name__ == '__main__':
	part_one()
	part_two()