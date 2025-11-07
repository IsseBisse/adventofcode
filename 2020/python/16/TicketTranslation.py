import re
import copy

def get_data(path):
	with open(path) as file:
		data_parts = file.read().split("\n\n")

		pattern_string = data_parts[0].split("\n")
		my_ticket_string = data_parts[1].split("\n")[1]
		tickets_string = data_parts[2].split("\n")[1:]

		# Get pattern
		patterns = dict()
		for line in pattern_string:
			category = re.findall(r"^[a-z ]+:", line)[0][:-1]
			ranges_string = re.findall(r"[0-9]+-[0-9]+", line)

			ranges = list()
			for range_string in ranges_string:
				[start, stop] = re.findall(r"[0-9]+", range_string)
				ranges.append(range(int(start), int(stop)+1))
			
			patterns[category] = ranges
			
		# Get my ticket
		my_ticket = [int(num) for num in re.findall(r"[0-9]+", my_ticket_string)]

		# Get other tickets
		nearby_tickets = list()
		for line in tickets_string:
			nearby_tickets.append([int(num) for num in re.findall(r"[0-9]+", line)])

	return patterns, my_ticket, nearby_tickets

"""
ONE
"""
def is_value_in_field(field, value):
	for range_ in field:
		if value in range_:
			return True

	return False

def is_value_in_pattern(pattern, value):
	for key in pattern:
		if is_value_in_field(pattern[key], value):
			return True

	return False

def part_one(path):
	patterns, _, nearby_tickets = get_data(path)

	incorrect_values = list()
	correct_tickets = list()
	for ticket in nearby_tickets:
		ticket_is_valid = True

		for value in ticket:
			if not is_value_in_pattern(patterns, value):
				incorrect_values.append(value)
				ticket_is_valid = False

		if ticket_is_valid:
			correct_tickets.append(ticket)

	print("Error rate is: %d" % sum(incorrect_values))
	return correct_tickets

"""
TWO
"""
# def get_remaining_values(values):
# 	if len(values) == 1:
# 		return None

# 	else:
# 		return copy.deepcopy(values[1:])

# def find_possible_combination(patterns, values, used_keys):
# 	if values is None:
# 		return [tuple(used_keys)]

# 	next_value = values[0]

# 	valid_key_combinations = list()
# 	valid_key_found = False
# 	for key in patterns:
# 		if key in used_keys:
# 			continue

# 		if is_value_in_field(patterns[key], next_value):
# 			next_used_keys = copy.deepcopy(used_keys)
# 			next_used_keys.append(key)
# 			valid_key_combinations += find_possible_combination(patterns, get_remaining_values(values), next_used_keys)

# 	return valid_key_combinations

# def part_two():
# 	path = "input.txt"

# 	patterns, my_ticket, _ = get_data(path)
# 	correct_tickets = part_one(path)

# 	print(len(correct_tickets))
# 	print(len(correct_tickets[0]))

# 	tickets_valid_combinations = None
# 	for i, ticket in enumerate(correct_tickets):
# 		valid_key_combinations = find_possible_combination(patterns, ticket, [])

# 		if tickets_valid_combinations is None:
# 			tickets_valid_combinations = set(valid_key_combinations)

# 		else:
# 			tickets_valid_combinations = tickets_valid_combinations.intersection(set(valid_key_combinations))

# 		print(tickets_valid_combinations)
		
# 	if len(tickets_valid_combinations) == 1:
# 		print("Correct combination found!")
# 		correct_combination = tuple(tickets_valid_combinations)[0]
	
# 	my_ticket_dict = dict()
# 	for i, category in enumerate(correct_combination):
# 		my_ticket_dict[category] = my_ticket[i]

# 	print(my_ticket_dict)

def part_two():
	path = "input.txt"

	patterns, my_ticket, _ = get_data(path)
	num_field = len(patterns)
	correct_tickets = part_one(path)

	keys = list(patterns.keys())
	possible_fields_for_ind = [copy.deepcopy(keys) for i in range(num_field)] 
	
	# Get all possible fields for each value index
	for ticket in correct_tickets:
		for i, value in enumerate(ticket):
			for possible_fields in possible_fields_for_ind[i]:
				if not is_value_in_field(patterns[possible_fields], value):
					possible_fields_for_ind[i].remove(possible_fields)
		
	# Find correct combination by removing fields
	correct_combination = [None] * num_field
	i = 0
	while None in correct_combination:
		if len(possible_fields_for_ind[i]) == 1:
			correct_field = possible_fields_for_ind[i][0]
			correct_combination[i] = correct_field

			for possible_fields in possible_fields_for_ind:
				if correct_field in possible_fields:
					possible_fields.remove(correct_field)

		i = (i+1) % num_field

	print(correct_combination)

	# Get answer
	departure_product = 1
	for i, field in enumerate(correct_combination):
		if "departure" in field:
			departure_product *= my_ticket[i]

	print("Product is %d" % departure_product)

if __name__ == '__main__':
	#part_one("input.txt")
	part_two()