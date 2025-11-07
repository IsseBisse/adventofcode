from re import findall, MULTILINE

def get_data(path):
	with open(path) as file:
		data = file.read()

	return data

def create_board(data):
	board = [int(string) for string in findall(r"\d+", data, MULTILINE)]
	board = (board, [False] * len(board))

	return board

def parse_data(data):
	parts = data.split("\n\n")
	numbers = [int(string) for string in findall(r"\d+", parts[0])]

	boards = list()
	for board_data in parts[1:]:
		boards.append(create_board(board_data))

	return numbers, boards 

def draw_number(numbers, boards):
	draw = numbers.pop(0)

	for board in boards:
		indices = [ind for ind, num in enumerate(board[0]) if num == draw]
		for ind in indices:
			board[1][ind] = True

	return numbers, boards, draw

def check_bingo(boards):
	for ind, board in enumerate(boards):
		# Check "rows"
		for i in range(5):
			if all(board[1][i*5:i*5+5]):
				return ind

		# Check "columns"
		for i in range(5):
			if all(board[1][i::5]):
				return ind

	return None

def get_score(board):
	return sum([num*(not is_checked) for num, is_checked in zip(board[0], board[1])])

def pretty_print(board):
	for row in range(5):
		for col in range(5):
			ind = row*5 + col
			suffix = "*" if board[1][ind] else ""
			string = f"{board[0][ind]}{suffix}"
			print(f"{string:>4}", end="")

		print("")
	print("")

def part_one():
	data = get_data("input.txt")
	numbers, boards = parse_data(data)

	ind = None
	while ind is None:
		numbers, boards, draw = draw_number(numbers, boards)
		ind = check_bingo(boards)
	
	pretty_print(boards[ind])
	print(get_score(boards[ind]) * draw)

def check_all_bingo(boards):
	indicies = list()

	for ind, board in enumerate(boards):
		# Check "rows"
		for i in range(5):
			if all(board[1][i*5:i*5+5]):
				indicies.append(ind)

		# Check "columns"
		for i in range(5):
			if all(board[1][i::5]):
				indicies.append(ind)

	return set(indicies)

def part_two():
	data = get_data("input.txt")
	numbers, boards = parse_data(data)

	ind = []
	old_ind = []
	while len(ind) < len(boards):
		old_ind = ind
		numbers, boards, draw = draw_number(numbers, boards)
		ind = check_all_bingo(boards)

		print(ind)

	last_bingo = set(ind).difference(set(old_ind))
	print(last_bingo)
	ind = list(last_bingo)[-1]
	print(get_score(boards[ind]) * draw)

if __name__ == '__main__':
	part_one()
	part_two()