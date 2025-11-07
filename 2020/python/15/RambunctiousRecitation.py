def get_data(path):
	with open(path) as file:
		data = file.read().split(",")

	for i, entry in enumerate(data):
		data[i] = int(entry)

	return data

class MemoryGame():
	def __init__(self, starting_numbers):
		self.turn = 0
		self.starting_numbers = starting_numbers
		
		self.last_turn_spoken = dict()
		self.previous = None
		self.current = None

		print("MemoryGame. Starting numbers: %s" % self.starting_numbers)

	def execute_turn(self):
		self.previous = self.current

		if self.turn < len(self.starting_numbers):
			self.current = self.starting_numbers[self.turn]

		else:
			if self.previous in self.last_turn_spoken.keys():
				self.current = self.turn - self.last_turn_spoken[self.previous]

			else:
				self.current = 0
		
		self.last_turn_spoken[self.previous] = self.turn
		self.turn += 1
		#print("Turn %d: %d" % (self.turn, self.current))

def part_one():
	starting_numbers = get_data("input.txt")
	game = MemoryGame(starting_numbers)

	for i in range(500000):
		game.execute_turn()

	print("Turn %d: %d" % (game.turn, game.current))

def part_two():
	starting_numbers = get_data("input.txt")
	game = MemoryGame(starting_numbers)

	for i in range(30e6):
		game.execute_turn()

	print("Turn %d: %d" % (game.turn, game.current))

if __name__ == '__main__':
	part_one()