from functools import lru_cache
from math import ceil
import re


def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	blueprints = [(idx+1, get_blueprint(row)) for idx, row in enumerate(data)]

	return blueprints


def get_cost(sentence):
	material_cost = {material: 0 for material in MATERIALS}
	output = re.findall(r"([a-z]+) robot", sentence)[0]
	materials = re.findall(r"[0-9]+ [a-z]+", sentence)

	for cost_string in materials:
		value = int(cost_string.split(" ")[0])
		material = cost_string.split(" ")[1]

		material_cost[material] = value

	return output, material_cost


def get_blueprint(row):
	sentences = row.split(":")[1].split(".")[:-1]
	blueprint = [get_cost(sentence) for sentence in sentences]
	blueprint = {robot: cost for robot, cost in blueprint}

	blueprint = tuple(tuple(recipe.values()) for recipe in blueprint.values())
	return blueprint

MATERIALS = ("ore", "clay", "obsidian", "geode")


@lru_cache
def time_to_buy(inventory, robots, recipe):
	minutes_to_buy = 1

	for material_idx in range(4):
		if recipe[material_idx] == 0:
			continue
		
		if robots[material_idx] == 0:
			return None

		additional_inventory = recipe[material_idx] - inventory[material_idx]
		minutes_to_buy = max(minutes_to_buy, ceil(additional_inventory / robots[material_idx]) + 1)

	# Add one minute for build time
	return minutes_to_buy


@lru_cache
def fastforward(inventory, robots, minutes, recipe=None):
	new_inventory = [0] * 4
	for material_idx in range(4):
		new_inventory[material_idx] += inventory[material_idx] + minutes * robots[material_idx]
		new_inventory[material_idx] -= recipe[material_idx] if recipe is not None else 0

	return tuple(new_inventory)


@lru_cache
def add_robot(robots, material_idx):
	new_robots = list(robots)
	new_robots[material_idx] += 1
	return tuple(new_robots)


@lru_cache
def theoretical_max_geodes(inventory, robots, minutes_left):
	max_geodes = inventory[3] + sum(range(robots[3], robots[3]+minutes_left))
	return max_geodes


def blueprint_tester(blueprint):
	max_robot_amount = [max(recipe[material_idx] for recipe in blueprint) for material_idx in range(4)]
	max_robot_amount[3] = -1
	max_robot_amount = tuple(max_robot_amount)
	
	def best_path(state, minutes_left):
		inventory, robots = state
		
		path_geodes = list()
		for material_idx in range(4):
			if robots[material_idx] == max_robot_amount[material_idx]:
				continue

			recipe = blueprint[material_idx]
			minutes_to_buy = time_to_buy(inventory, robots, recipe)
			if minutes_to_buy is None or minutes_to_buy > minutes_left:
				continue

			# print(state, minutes_left, material, minutes_to_buy)

			new_inventory = fastforward(inventory, robots, minutes_to_buy, recipe)
			new_robots = add_robot(robots, material_idx)
			new_state = (new_inventory, new_robots)
			new_minutes_left = minutes_left - minutes_to_buy

			if len(path_geodes) == 0 or theoretical_max_geodes(new_inventory, new_robots, new_minutes_left) > max(path_geodes):
				geodes = best_path(new_state, new_minutes_left)
				path_geodes.append(geodes)

		if len(path_geodes) == 0:
			# No possible robot purchases. Run until end
			inventory = fastforward(inventory, robots, minutes_left)
			return inventory[3]
		
		else:
			return max(path_geodes)

	return best_path


def part_one():
	blueprints = get_data("input.txt")
	
	quality_level = list()
	for idx, blueprint in blueprints:
		best_path = blueprint_tester(blueprint)
		inventory = (0, 0, 0, 0)
		robots = (1, 0, 0, 0)
		state = (inventory, robots)
		minutes_left = 24

		geodes = best_path(state, minutes_left)
		quality_level.append(idx * geodes)
		print(f"Blueprint {idx} done!")
		
	print(quality_level)
	print(sum(quality_level))


def part_two():
	# blueprints = get_data("smallInput.txt")
	blueprints = get_data("input.txt")[:3]

	num_geodes = list()
	for idx, blueprint in blueprints:
		best_path = blueprint_tester(blueprint)
		inventory = (0, 0, 0, 0)
		robots = (1, 0, 0, 0)
		state = (inventory, robots)
		minutes_left = 32

		geodes = best_path(state, minutes_left)
		num_geodes.append(geodes)
		print(f"Blueprint {idx} done!")
		
	print(num_geodes)


if __name__ == '__main__':
	# part_one()
	part_two()
