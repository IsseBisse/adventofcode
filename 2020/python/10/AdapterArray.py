def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	for i, entry in enumerate(data):
		data[i] = int(entry)

	data.append(0)
	data.append(max(data) + 3)

	return data

def part_one():
	data = get_data("input.txt")
	print(data)

	data.sort()
	print(data)

	jolt_differences = [0, 0]
	for i, jolt in enumerate(data[:-1]):
		diff = data[i+1] - jolt

		if diff == 1:
			jolt_differences[0] += 1

		elif diff == 3:
			jolt_differences[1] += 1

	print(jolt_differences)
	print(jolt_differences[0] * jolt_differences[1])
	
class Node:
	def __init__(self, jolt):
		self.jolt = jolt
		self.children = list()
		
	def __str__(self):
		string = "%s: " % self.jolt
		string += "%s" % [child.jolt for child in self.children]
		
		return string

	def add_connections(self, available_jolts):
		for i in range(3):
			child_jolt = self.jolt + i + 1
			
			if child_jolt in list(available_jolts.keys()):
				self.children.append(available_jolts[child_jolt])

	def count_paths_to_end(self, end_jolt):
		paths_to_end = 0

		if self.children:
			for child in self.children:
				paths_to_end += child.count_paths_to_end(end_jolt)

		else:
			if self.jolt == end_jolt:
				return 1

			else:
				return 0

		return paths_to_end


def part_two():
	data = get_data("input.txt")
	data.sort()

	split_data = list()
	start_ind = 0
	for i in range(len(data) - 1):
		if data[i+1] - data[i] == 3:
			split_data.append(data[start_ind:i+1])
			start_ind = i+1

	total_num_configs = 1
	for sub_data in split_data:

		available_jolts = dict()
		for jolt in sub_data:
			available_jolts[jolt] = Node(jolt)
			root = available_jolts[sub_data[0]]

		for key in available_jolts:
			available_jolts[key].add_connections(available_jolts)

		num_configurations = root.count_paths_to_end(sub_data[-1])
		total_num_configs *= num_configurations

	print(total_num_configs)

if __name__ == '__main__':
	part_two()