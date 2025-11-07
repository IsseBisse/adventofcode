import math

def parse_input(path):

	f = open(path, "r")

	data = [int(x) for x in  f.read().split("\n")]

	return data

def part_one():

	data = parse_input("input.txt")

	sum_of_fuel = sum([math.floor(x / 3) - 2 for x in data])
	print(sum_of_fuel)

def required_fuel(mass):

	fuel = math.floor(mass / 3) - 2

	if fuel <= 0:
		fuel = 0

	else:
		fuel += required_fuel(fuel)

	return fuel

def part_two():

	data = parse_input("input.txt")

	sum_of_fuel = sum([required_fuel(mass) for mass in data])
	print(sum_of_fuel)

if __name__ == '__main__':
	part_two()