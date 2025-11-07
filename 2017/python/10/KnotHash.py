from itertools import cycle


def get_data(path):
	with open(path) as file:
		data = [int(length) for length in file.read().split(",")]

	return data


class CircularList():
	def __init__(self, values):
		self.values = cycle(values)
		self.len = len(values)
		self.current_position = 0
		self.skip_size = 0

	def reverse(self, length):
		first = list()
		for _ in range(length):
			first.append(next(self.values))

		second = list()
		for _ in range(self.len - length):
			second.append(next(self.values))

		print(first, second)

	def move(self, length):
		self.current_position = (self.current_position + length + self.skip_size) % len(self.values)


def part_one():
	circular_list = CircularList([x for x in range(5)])
	lengths = get_data("smallInput.txt")

	circular_list.reverse(lengths[0])

def part_two():
	data = get_data("smallInput.txt")


if __name__ == '__main__':
	part_one()
	part_two()