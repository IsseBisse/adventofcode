from functools import reduce

def get_data(path):
	with open(path) as file:
		raw_data = file.read().split("\n\n")

	return tuple(raw_data)

def get_positive_answers(lines):
	return len(set(lines.replace("\n", "")))

def part_one():
	data = get_data("input.txt")
	positive_answers = map(get_positive_answers, data)
	print(sum(positive_answers))
	
def get_positive_union(answer, new_answers):
	return set(answer).intersection(new_answers)

def get_all_positive_answers(lines):
	answers = lines.split("\n")
	return set(reduce(get_positive_union, answers))

def part_two():
	data = get_data("input.txt")
	all_positives = map(get_all_positive_answers, data)
	num_positives = map(len, all_positives)

	print(sum(num_positives))

if __name__ == '__main__':
	part_one()
	part_two()