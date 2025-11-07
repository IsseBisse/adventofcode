def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	return data


def parse(stream):
	groups = list()
	garbage = list()

	open_group_starts = list()
	garbage_start = None

	garbage_level = 1
	skip_next = False
	for idx, char in enumerate(stream):
		if skip_next:
			skip_next = False
			continue



		if char == "!":
			skip_next = True

		elif char == ">":
			garbage.append(stream[garbage_start:idx+1])
			garbage_start = None

		if garbage_start is None:
			if char == "{":
				open_group_starts.append((garbage_level, idx))
				garbage_level += 1

			elif char == "}":
				level, start_idx = open_group_starts.pop()
				groups.append((level, stream[start_idx:idx+1]))
				garbage_level -= 1

			elif char == "<":
				garbage_start = idx

	return groups, garbage


def part_one():
	data = get_data("smallInputs.txt")
	# data = get_data("input.txt")
	for stream in data:
		groups, garbage = parse(stream)

		# print(stream)
		# print(groups)
		print(garbage)
		print(sum([score for score, _ in groups]))
		# print()


def count_characters(garbage):
	count = 0
	skip_next = False

	garbage = garbage[1:-1]
	for char in garbage:
		if skip_next:
			skip_next = False
			continue

		if char == "!":
			skip_next = True

		else:
			count += 1

	return count


def part_two():
	# data = get_data("smallGarbageInputs.txt")
	data = get_data("input.txt")
	for stream in data:
		groups, garbage = parse(stream)

		print(garbage)
		print(sum([count_characters(pile) for pile in garbage]))


if __name__ == '__main__':
	# part_one()
	part_two()