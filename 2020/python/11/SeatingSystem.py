import copy

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	return data

class Seats:
	VAL_CHARS = {"#": 1, "L": 0, ".": -1}
	STR_CHARS = {v: k for k, v in VAL_CHARS.items()}

	def __init__(self, data):
		
		self.fill_seats(data)
		self.old_seats = None

	def fill_seats(self, data):
		
		self.seats = list()
		for row in data:
			row_values = [-1] + [self.VAL_CHARS[char] for char in row] + [-1]
			self.seats.append(row_values)

		fill_rows = [-1] * len(self.seats[0])
		self.seats.insert(0, fill_rows)
		self.seats.append(fill_rows)

	def __str__(self):

		string = ""
		for row in self.seats:
			string += "".join(self.STR_CHARS[val] for val in row) + "\n"

		return string

	def simulate_change(self, num_adjacent_func, max_num_adjacent):

		self.old_seats = copy.deepcopy(self.seats)

		for i, row in enumerate(self.old_seats):
			if i == 0 or i == len(self.old_seats) - 1:
				continue

			for j, num in enumerate(row):
				if j == 0 or j == len(row) - 1:
					continue

				if num == 0 and num_adjacent_func(i, j) == 0:
					self.seats[i][j] = 1

				elif num == 1 and num_adjacent_func(i, j) >= max_num_adjacent:
					self.seats[i][j] = 0

	def get_num_adjacent(self, i, j):

		num_adjacent = 0
		for row in self.old_seats[i-1:i+2]:
			for seat in row[j-1:j+2]:
				num_adjacent += int(seat > 0)

		num_adjacent -= self.old_seats[i][j]

		return num_adjacent

	def get_num_occupied(self):

		num_occupied = 0
		for row in self.seats:
			for seat in row:
				num_occupied += int(seat > 0)

		return num_occupied

	def get_num_visible_adjacent(self, i, j):
		
		DIRECTIONS = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
		
		max_row = len(self.old_seats)
		max_col = len(self.old_seats[0])

		
		num_adjacent = 0
		for dir_ in DIRECTIONS:
			pos = [i + dir_[0], j + dir_[1]]

			while (pos[0] >= 0 and pos[0] < max_row) and (pos[1] >= 0 and pos[1] < max_col):
				if self.old_seats[pos[0]][pos[1]] != -1:
					num_adjacent += 1 if self.old_seats[pos[0]][pos[1]] else 0
					break

				pos = [pos[k] + dir_[k] for k in range(2)]

				
		return num_adjacent

	def state_unchanged(self):

		if self.old_seats is None:
			return False

		for i, row in enumerate(self.seats):
			for j, seat in enumerate(row):
				if seat != self.old_seats[i][j]:
					return False

		return True 

def part_one():
	data = get_data("input.txt")
	seats = Seats(data)

	print(seats)
	while not seats.state_unchanged():
		seats.simulate_change(seats.get_num_adjacent, 4)
		print(seats)
		print("Num occ: %d" % seats.get_num_occupied())
	
def part_two():
	data = get_data("input.txt")
	seats = Seats(data)

	while not seats.state_unchanged():
		seats.simulate_change(seats.get_num_visible_adjacent, 5)
		#print(seats)
	
	print("Num occ: %d" % seats.get_num_occupied())

if __name__ == '__main__':
	part_two()