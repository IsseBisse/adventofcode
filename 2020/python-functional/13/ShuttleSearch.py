from CheatModule import arrow_alignment, extended_gcd
from functools import reduce

def get_data(path):
	with open(path) as file:
		raw_data = file.read().split("\n")

	wait_time = int(raw_data[0])
	time_table = raw_data[1].split(",")

	return wait_time, time_table

def above_finder(target):
	def find_closest_above(bus_id):
		return (target // bus_id) * bus_id + bus_id if target % bus_id != 0 else target

	return find_closest_above

def part_one():
	wait_time, time_table = get_data("input.txt")
	relevant_time_table = tuple(map(int, filter(lambda bus_id: bus_id!="x", time_table)))	# Tuple to enable reuse

	finder = above_finder(wait_time)
	closest_above = tuple(map(finder, relevant_time_table))

	shortest_wait = min(closest_above)-wait_time
	bus_id = relevant_time_table[closest_above.index(min(closest_above))]
	print(shortest_wait, bus_id, shortest_wait*bus_id)


def parse_time_table(time_table):
	relevant_times = list()
	relevant_indicies = list()
	for i, time in enumerate(time_table):
		if time != "x":
			relevant_times.append(int(time))
			relevant_indicies.append(-i)

	return relevant_times, relevant_indicies

def gcd_wrapper(offsets):
	def offset_gcd(first, second):
		offset = next(offsets)
		print(first, second, offset)
		return arrow_alignment(first, second, offset)

	offsets = iter(offsets)
	return offset_gcd

def part_two():
	wait_time, time_table = get_data("smallInput.txt")
	relevant_time_table, offsets = parse_time_table(time_table)
	print(relevant_time_table, offsets)

	offset_gcd = gcd_wrapper(offsets[1:])
	first = relevant_time_table[0]
	offset = offsets[1]
	for second in relevant_time_table[1:]:
		first = offset_gcd(first, second)

	final_time = reduce(offset_gcd, relevant_time_table)
	print(final_time)

if __name__ == '__main__':
	#part_one()
	part_two()