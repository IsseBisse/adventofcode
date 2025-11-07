import re

def parse_data(line):
	times = tuple(map(int, re.findall(r"[0-9]+", line)))
	letter = re.findall(r"[ ][a-z]{1}[:]", line)[0][1]
	password = re.findall(r"[a-z]{2,}", line)[0]

	return times, letter, password

def get_data(path):
	with open(path) as file:
		raw_data = file.read().split("\n")

	data = zip(*map(parse_data, raw_data))

	return tuple(data)

def password_ok(times, letter, password):
	min_times, max_times = times
	matches = re.findall(f"[{letter}]", password)
	return min_times <= len(matches) <= max_times

def part_one():
	times, letter, password = get_data("input.txt")
	results = map(password_ok, times, letter, password)
	print(sum(results))

def new_password_ok(times, letter, password):
	needs_letter, needs_not_letter = times
	return (password[needs_letter-1] == letter) != \
		(password[needs_not_letter-1] == letter)

def part_two():
	times, letter, password = get_data("input.txt")
	results = map(new_password_ok, times, letter, password)
	print(sum(results))

if __name__ == '__main__':
	part_one()
	part_two()