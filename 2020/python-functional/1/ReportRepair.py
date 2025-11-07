from itertools import permutations
from functools import reduce

def get_data(path):
	with open(path) as file:
		raw_data = file.read().split("\n")

	data = map(int, raw_data)

	return tuple(data)

def get_2020_combination(data, r):
	sets = permutations(data, r)
	# Next gets first correct set (there will be r correct sets, because permutations)
	correct_set = next(filter(lambda x: sum(x)==2020, sets))
	# "Sum" but with multiplication
	pair_prod = reduce((lambda x, y: x * y), correct_set)

	return correct_set, pair_prod

def part_one():
	data = get_data("input.txt")
	correct_pair, prod = get_2020_combination(data, 2)

	print(correct_pair, prod)
	

def part_two():
	data = get_data("input.txt")
	correct_pair, prod = get_2020_combination(data, 3)

	print(correct_pair, prod)

if __name__ == '__main__':
	part_one()
	part_two()