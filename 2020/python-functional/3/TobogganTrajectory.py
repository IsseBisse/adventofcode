from functools import reduce

def get_data(path):
	with open(path) as file:
		raw_data = file.read().split("\n")

	return tuple(raw_data)

def position_generator(width, slope):
	def position(index):
		return (index * slope) % width
	
	return position

def check_position(pos, line):
	return line[pos] == "#"

def part_one(direction):
	data = get_data("input.txt")
	slope_width = len(data[0])
	slope, fall = direction

	pos_gen = position_generator(slope_width, slope)
	positions = map(pos_gen, range(len(data) // fall)) 
	results = map(check_position, positions, data[::fall])
	trees_met = sum(results)

	print("Num trees met: %d" % trees_met)

	return trees_met
	
def part_two():
	slopes = ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2))
	trees = map(part_one, slopes)
	answer = reduce((lambda x, y: x * y), trees)

	print(answer)

if __name__ == '__main__':
	part_one((3, 1))
	part_two()