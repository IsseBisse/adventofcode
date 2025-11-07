import math
from CheatModule import arrow_alignment, extended_gcd, combine_phased_rotations

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	departure_time = int(data[0])
	buses = data[1].split(",")
	
	return departure_time, buses

def part_one():
	departure_time, buses = get_data("input.txt")
	buses = [int(id_) for id_ in buses if id_ != "x"]

	print(departure_time, buses)

	shortest_wait = departure_time + 1
	bus_id = -1
	for bus in buses:
		last_missed_bus_diff = departure_time % bus
		depart_diff = bus - last_missed_bus_diff if last_missed_bus_diff != 0 else 0

		if depart_diff < shortest_wait:
			shortest_wait = depart_diff
			bus_id = bus

	print("Bus: %d, wait: %d, answer: %d" % (bus_id, shortest_wait, bus_id * shortest_wait))

def get_next_offset(first, second, offset):
	return arrow_alignment(first, second, offset)

def get_next_step(first, second):
    return abs(first*second) // math.gcd(first, second)

def part_two():
	# Get and parse data
	_, buses = get_data("input.txt")
	relevant_buses = list()
	offsets = list()
	for i, bus_id in enumerate(buses):
		if bus_id != "x":
			offsets.append(-i)
			relevant_buses.append(int(bus_id))
	print(relevant_buses, offsets)

	for i in range(1000):
		if (i % 3 == 0 and
			(i+1) % 5 == 0 and
			(i+2) % 4 == 0):
			break

	print(i)


	first_period = relevant_buses[0]
	first_phase = offsets[0]
	for i in range(1, len(relevant_buses)):
		second_period = relevant_buses[i]
		second_phase = offsets[i]
		
		first_period, first_phase = combine_phased_rotations(first_period, first_phase,
			second_period, second_phase)

	print(first_phase)


if __name__ == '__main__':
	#part_one()
	part_two()