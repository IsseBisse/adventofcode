import re

from functools import reduce

def parse_line(line):
	return tuple(re.findall(r"[FB]+|[LR]+", line))

def get_data(path):
	with open(path) as file:
		raw_data = file.read().split("\n")
	
	data = map(parse_line, raw_data)

	return tuple(data)

UPPER = {"B", "R"}

def consume_line(line, limits):
	lower, upper = limits
	if line == "":
		return lower

	elif line[0] in UPPER:
		lower += (upper - lower)//2 + 1

	else:
		upper -= (upper - lower)//2 + 1

	return consume_line(line[1:], (lower, upper))

def get_limit(line):
	return 0, 2**len(line)-1

def get_seat_id(entry):
	limits = map(get_limit, entry)
	row, column = tuple(map(consume_line, entry, limits))
	seat_id = row*8 + column

	return row, column, seat_id

def part_one():
	data = get_data("input.txt")
	seat_data = map(get_seat_id, data)
	seat_ids = map(lambda x: x[2], seat_data)

	print(max(seat_ids))
	return seat_ids

def part_two():
	data = get_data("input.txt")
	seat_data = map(get_seat_id, data)
	seat_ids = map(lambda x: x[2], seat_data)
	sorted_seat_ids = sorted(seat_ids)
	available_seat_ids = set(range(sorted_seat_ids[0], sorted_seat_ids[-1]))
	
	print(available_seat_ids - set(sorted_seat_ids))

if __name__ == '__main__':
	part_one()
	part_two()