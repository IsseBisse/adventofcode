def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	return data

class Bag:
	def __init__(self, color):
		self.color = color
		self.children = list()
		self.parents = list()

	def __str__(self):
		string = "%s bags contain " % self.color
		
		if self.children:
			for child in self.children:
				string += "%d %s bags, " % (child[0], child[1].color)

			string = string[:-2] + "."

		else:
			string += "no other bags."

		return string

	def add_children(self, ALL_BAGS, children_info):
		for info in children_info:
			num = info[0]
			color = info[1]
			self.children.append((num, ALL_BAGS[color]))

			# Add as parent
			ALL_BAGS[color].add_parent(self)

	def add_parent(self, parent):
		self.parents.append(parent)

	def get_all_parents(self):
		all_parents = list()
		all_parents += self.parents

		for parent in self.parents:
			all_parents += parent.get_all_parents()

		return list(set(all_parents))

	def get_num_children(self):
		num_children = 0

		for child in self.children:
			num_children += child[0] + child[0]*child[1].get_num_children()

		return num_children

def parse_bag_description(line):
	parts = line.split(" bags contain ")
	color = parts[0]

	if "no other bags." == parts[1]:
		children = list()
	else:
		child_parts = parts[1].split(", ")
		child_parts[-1] = child_parts[-1][:-1]
		
		children = list()
		for child in child_parts:
			info_parts = child.split(" ")
			info = (int(info_parts[0]), " ".join(info_parts[1:-1]))
			children.append(info)

	return color, children

def part_one():
	data = get_data("input.txt")

	ALL_BAGS = dict()
	for line in data:
		color, _ = parse_bag_description(line)
		ALL_BAGS[color] = Bag(color)

	for line in data:
		color, children_info = parse_bag_description(line)
		ALL_BAGS[color].add_children(ALL_BAGS, children_info)

	contains_shiny_gold = ALL_BAGS["shiny gold"].get_all_parents()
	print("Shiny gold found in %d bags:" % len(contains_shiny_gold))
	for bag in contains_shiny_gold:
		print(bag.color)

def part_two():
	data = get_data("input.txt")

	ALL_BAGS = dict()
	for line in data:
		color, _ = parse_bag_description(line)
		ALL_BAGS[color] = Bag(color)

	for line in data:
		color, children_info = parse_bag_description(line)
		ALL_BAGS[color].add_children(ALL_BAGS, children_info)

	print(ALL_BAGS["shiny gold"].get_num_children())

if __name__ == '__main__':
	#part_one()
	part_two()