import numpy as np
import re

def string_to_board(board_string):
	return np.array([[int(chars) for chars in re.findall(r"[0-9]+", row)] for row in board_string.split("\n")])

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n\n")

	numbers = tuple(int(chars) for chars in data[0].split(","))
	boards = tuple(string_to_board(part) for part in data[1:])

	return numbers, boards

def board_has_bingo(board):
	board_size = 5
	diagonals = [np.eye(board_size), np.eye(board_size)[:,::-1]]

	print(rows)

	# print(checks, checks.shape)

def play_game(numbers, boards):
	board_has_bingo(boards[0])


def part_one():
	numbers, boards = get_data("smallInput.txt")

	play_game(numbers, boards)

def part_two():
	data = get_data("smallInput.txt")

if __name__ == '__main__':
	part_one()
	part_two()