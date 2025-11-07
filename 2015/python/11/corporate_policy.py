from re import findall

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	for i, entry in enumerate(data):
		data[i] = int(entry)

	return data

def increment_string(string):
	offset = 97
	base = 26
	num_string = [ord(char) - offset for char in string]

	carry = 0
	for i, num in reversed(list(enumerate(num_string))):
		num_string[i] = (num + 1) % base
		carry = (num + 1) // base

		if carry == 0:
			break

	return "".join([chr(num + offset) for num in num_string])


def has_incrementing_characters(string):
	incrementing_characters = ["".join([chr(i+97), chr(i+98), chr(i+99)]) for i in range(24)]
	return any(substring in string for substring in incrementing_characters)

def has_only_allowed_characters(string):
	not_allowed_characters = ["i", "o", "l"]
	return not any(char in string for char in not_allowed_characters)

def has_two_character_pairs(string):
	paired_characters = findall(r"([a-z]+)\1", string)
	return len(paired_characters) >= 2

def part_one(original_password):
	new_password = original_password

	new_password_ok = False
	while not new_password_ok:
		new_password = increment_string(new_password)

		new_password_ok = has_incrementing_characters(new_password) & \
			has_only_allowed_characters(new_password) & \
			has_two_character_pairs(new_password)

	return new_password
	
def part_two(original_password):
	return part_one(original_password)

if __name__ == '__main__':
	original_password = "cqjxjnds"
	new_password = part_one(original_password)
	print(f"Part one: {new_password}")

	new_password = part_two(new_password)
	print(f"Part two: {new_password}")