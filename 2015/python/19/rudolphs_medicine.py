import re

def get_data(path):
	with open(path) as file:
		data = file.read()

	return data

def parse_data(data):
	replacements_string, start_molecule = data.split("\n\n")

	replacements = dict()
	for line in replacements_string.split("\n"):
		key, value = line.split(" => ")
		if key in replacements:
			replacements[key].append(value)
		else:
			replacements[key] = [value]

	return replacements, start_molecule

def one_step(molecule, replacements):
	groups = re.findall(r"([A-Z][a-z]?)", molecule)

	possible_new_molecules = list()
	for i, group in enumerate(groups):
		if group in replacements:
			for replacement_group in replacements[group]:
				new_molecule = "".join(groups[:i] + [replacement_group] + groups[i+1:])
				possible_new_molecules.append(new_molecule)
	
	return possible_new_molecules

def part_one():
	data = get_data("input.txt")
	replacements, start_molecule = parse_data(data)
	
	possible_new_molecules = one_step(start_molecule, replacements)
	print(len(set(possible_new_molecules)))

def generate_inverse_replacements(replacements):
	inverse_replacements = dict()
	for entry, exits in replacements.items():
		for exit in exits:
			inverse_replacements[exit] = entry

	return inverse_replacements

def replace_molecule_group(molecule, group, replacement_group):
	molecule_split = re.split(f"({group})", molecule)

	new_molecules = list()
	for i, part in enumerate(molecule_split):
		if part == group:
			new_molecule = "".join(molecule_split[:i] + [replacement_group] + molecule_split[i+1:])
			new_molecules.append(new_molecule)

	return new_molecules

def collapser(replacements, num_iterations_list):
	
	def collapse_to_e(molecule, iterations):
		print(f"Molecule: {molecule}, iterations: {iterations}")
		
		if iterations >= min(num_iterations_list):
			return

		if molecule == "e":
			num_iterations_list.append(iterations)
			return

		for group, replacement_group in replacements.items():
			new_molecules = replace_molecule_group(molecule, group, replacement_group)
			
			for new_molecule in new_molecules:
				collapse_to_e(new_molecule, iterations+1)

	return collapse_to_e

def expander(replacements, target_molecule):
	pass 

def part_two():
	data = get_data("input.txt")
	replacements, end_molecule = parse_data(data)
	inverse_replacements = generate_inverse_replacements(replacements)

	num_iterations_list = [1e3]
	collapse_function = collapser(inverse_replacements, num_iterations_list)
	collapse_function(end_molecule, 0)

	print(min(num_iterations_list))
	
if __name__ == '__main__':
	# part_one()
	part_two()