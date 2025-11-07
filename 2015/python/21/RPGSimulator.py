import re
import copy

def get_data(path):
	with open(path) as file:
		data = file.read()

	return data

def parse_data(data):
	return [int(match) for match in re.findall(r"(\d+)", data, re.MULTILINE)]

def get_items():
	with open("items.txt") as file:
		sections = file.read().split("\n\n")

	items = dict()
	for section in sections:
		for i, line in enumerate(section.split("\n")):
			if i == 0:
				item_type = line.split(":")[0]
				items[item_type] = list()

			else:
				items[item_type].append([int(match) for match in re.findall(r"( \d+)", line)])

	return items

def create_player(*args):
	player = [100, sum([item[1] for item in args]), sum([item[2] for item in args])]
	cost = sum([item[0] for item in args])

	return player, cost

def fight(player, boss):
	player_dmg = max(player[1] - boss[2], 1)
	boss_dmg = max(boss[1] - player[2], 1)

	while True:
		boss[0] -= player_dmg
		if boss[0] <= 0:
			return True

		# print(f"Boss: {boss[0]} hp")

		player[0] -= boss_dmg
		if player[0] <= 0:
			return False

		# print(f"Player: {player[0]} hp")

def part_one():
	items = get_items()
	data = get_data("input.txt")
	boss = parse_data(data)

	items["Armor"].append([0, 0, 0]) 	# No armor
	items["Rings"].append([0, 0, 0])	# Only 1 ring
	items["Rings"].append([0, 0, 0])	# No rings

	lowest_cost = 1e8
	for weapon in items["Weapons"]:
		for armor in items["Armor"]:
			for i, first_ring in enumerate(items["Rings"]):
				for second_ring in items["Rings"][:i] + items["Rings"][i+1:]:
					player, cost = create_player(weapon, armor, first_ring, second_ring)
					player_wins = fight(player, copy.deepcopy(boss))

					if player_wins and cost < lowest_cost:
						lowest_cost = cost

	print(lowest_cost)


def part_two():
	items = get_items()
	data = get_data("input.txt")
	boss = parse_data(data)

	items["Armor"].append([0, 0, 0]) 	# No armor
	items["Rings"].append([0, 0, 0])	# Only 1 ring
	items["Rings"].append([0, 0, 0])	# No rings

	highest_cost = 0
	for weapon in items["Weapons"]:
		for armor in items["Armor"]:
			for i, first_ring in enumerate(items["Rings"]):
				for second_ring in items["Rings"][:i] + items["Rings"][i+1:]:
					player, cost = create_player(weapon, armor, first_ring, second_ring)
					player_wins = fight(player, copy.deepcopy(boss))

					if not player_wins and cost > highest_cost:
						highest_cost = cost

	print(highest_cost)

if __name__ == '__main__':
	part_one()
	part_two()