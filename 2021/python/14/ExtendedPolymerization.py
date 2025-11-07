from collections import Counter
import itertools

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	start = data[0]
	inserts = {row.split(" -> ")[0]: row.split(" -> ")[1] for row in data[2:]}

	return start, inserts

def polymer_extender(inserts):
	def extend(polymer):
		"""Extend polymer (string) into new polymer (string) using "inserts" dict""" 
		pairs = [polymer[i:i+2] for i in range(len(polymer)-1)]
		new_elements = map(lambda x: inserts[x], pairs)
		new_polymer = ''.join(map(''.join, zip(polymer, new_elements))) + polymer[-1]
		return new_polymer

	return extend

def count_elements(polymer):
	"""Count occurence of each element in polymer (string)"""
	elements = set(polymer)
	counts = map(lambda x: polymer.count(x), elements)	
	element_counts = sorted(tuple(zip(elements, counts)), key=lambda item: item[1])

	return element_counts

def part_one():
	start, inserts = get_data("input.txt")
	extender = polymer_extender(inserts)

	polymer = start
	num_laps = 10
	for _ in range(num_laps):
		polymer = extender(polymer)

	element_counts = count_elements(polymer)
	print(element_counts[-1][1] - element_counts[0][1])

def dictize_polymer(polymer):
	"""Convert polymer (string) into polymer_dict (Counter)"""
	pairs = [polymer[i:i+2] for i in range(len(polymer)-1)]
	polymer_dict = Counter(pairs)
	return polymer_dict

def dictize_inserts(inserts):
	"""Convert inserts ({pair: insert}) into insert_dict ({pair: (first_new_pair, second_new_pair)})"""
	inserts_dict = {key:(key[0] + value, value + key[1]) for key, value in inserts.items()}
	return inserts_dict

def polymer_dict_extender(inserts_dict):
	def extend(polymer_dict):
		def extend_pair(pair, number):
			return {new_pair: number for new_pair in inserts_dict[pair]}

		new_pairs = map(extend_pair, polymer_dict.keys(), polymer_dict.values())
		new_polymer_dict = sum(map(Counter, new_pairs), Counter())
		return new_polymer_dict

	return extend
		
def count_dict_elements(polymer_dict):
	def count_pair_elements(key, value):
		return ({key[0]: value}, {key[1]: value})
	element_count_for_pair = map(count_pair_elements, polymer_dict.keys(), polymer_dict.values())
	merged_element_counts = list(itertools.chain.from_iterable(element_count_for_pair))
	summed_element_counts = sum(map(Counter, merged_element_counts), Counter())
	halved_element_counts = ((key, (value+1)//2) for key, value in summed_element_counts.items())
	element_counts = sorted(halved_element_counts, key=lambda item: item[1])
	return element_counts

def part_two():
	start, inserts = get_data("input.txt")

	insert_dict = dictize_inserts(inserts)
	extender = polymer_dict_extender(insert_dict)
	polymer_dict = dictize_polymer(start)

	num_laps = 40
	for _ in range(num_laps):
		polymer_dict = extender(polymer_dict)

	element_counts = count_dict_elements(polymer_dict)
	print(element_counts[-1][1] - element_counts[0][1])
	
if __name__ == '__main__':
	part_one()
	part_two()