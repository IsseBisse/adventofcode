from itertools import permutations
import re


def to_acronym(item_string):
	acronym = item_string[0].upper()
	acronym += "M" if "microchip" in item_string else "G"

	return acronym


def parse(floor):
	items = re.findall(r"[a-z\-]+ (?:microchip|generator)", floor)
	floor = tuple(to_acronym(item) for item in items)

	return floor


def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	floors = tuple(parse(row) for row in data)

	return floors


def one_step_all(states):
	new_states_all = set()
	for state in states:
		new_states = one_step(state)
		new_states_all = new_states_all.union(new_states)

	return new_states_all


def one_step(state):
	elevator, steps, floors = state

	next_elevator = list()
	if elevator < 3:
		next_elevator.append(elevator+1)
	if elevator > 0:
		next_elevator.append(elevator-1)

	same_floor_items = floors[elevator]
	next_floor_items = set([tuple(sorted(item)) for item in permutations(same_floor_items, 1)] +
						   [tuple(sorted(item)) for item in permutations(same_floor_items, 2)])

	steps += 1

	new_states = set()
	for new_elevator in next_elevator:
		for new_items in next_floor_items:
			new_floors = list(list(item) for item in floors)
			for item in new_items:
				new_floors[elevator].remove(item)

			new_floors[new_elevator] += new_items
			new_floors = tuple(tuple(item) for item in new_floors)

			new_state = (new_elevator, steps, new_floors)
			if is_valid_floor(new_floors):
				new_states.add(new_state)

	return new_states


def is_valid_floor(floors):
	check_floors = list(list(item) for item in floors)

	no_pairs_floors = list()
	for floor in check_floors:
		for item in floor:



def part_one():
	floors = get_data("smallInput.txt")
	states = {(0, 0, floors)}

	steps = 0
	final_state = (3, steps, ((), (), (), tuple(item for sublist in floors for item in sublist)))
	while final_state not in states:
		states = one_step_all(states)

		steps += 1
		final_state = (3, steps, ((), (), (), tuple(item for sublist in floors for item in sublist)))

	print(steps)

def part_two():
	floors = get_data("smallInput.txt")

if __name__ == '__main__':
	part_one()
	# part_two()