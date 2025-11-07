def get_data(path):
	with open(path) as file:
		data = file.read()

	return data

def parse_data(data):
	return [int(string) for string in data.split(",")]

def one_day(school):
	reset_day = 6

	new_fish = list()
	for i, fish in enumerate(school):
		if fish == 0:
			school[i] = reset_day
			new_fish.append(8)

		else:
			school[i] = fish - 1

	return school + new_fish

def part_one():
	data = get_data("input.txt")
	school = parse_data(data)


	#print(f"Initial state: {school}")
	NUM_DAYS = 80
	for day in range(1, NUM_DAYS+1):
		school = one_day(school)
		#print(f"After {day:>4} days: {school}")

	print(len(school))


def get_school_dict(school):
	keys = range(9)
	values = map(school.count, keys)
	return dict(zip(keys, values))

def one_day_dict(school_dict):
	keys = range(9)
	values = [0] * len(keys)
	new_school_dict = dict(zip(keys, values))

	for key in new_school_dict:
		new_school_dict[key] = school_dict[(key + 1) % 9]

	new_school_dict[6] += school_dict[0]

	return new_school_dict

def part_two():
	data = get_data("input.txt")
	school = parse_data(data)
	school_dict = get_school_dict(school)

	# print(f"Initial state: {[value for _, value in school_dict.items()]}")
	NUM_DAYS = 256
	for day in range(1, NUM_DAYS+1):
		school_dict = one_day_dict(school_dict)
		# print(f"After {day:>4} days: {[value for _, value in school_dict.items()]}")

	print(sum([value for _, value in school_dict.items()]))

if __name__ == '__main__':
	part_one()
	part_two()