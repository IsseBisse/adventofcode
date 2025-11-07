def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	return data

chunk_pairs = {"(": ")", "[": "]", "{": "}", "<": ">"}
score = {")": 3, "]": 57, "}": 1197, ">": 25137}

def is_line_corrupt(line):
	expected_closers = list()

	for i, char in enumerate(line):
		if char in chunk_pairs:
			# Chunk "opener"
			expected_closers.append(chunk_pairs[char])

		else:
			# Chuck "closer"
			expected = expected_closers.pop(-1)
			if expected != char:
				return True, char

	return False, expected_closers

def part_one():
	data = get_data("input.txt")
	
	syntax_score = 0
	for line in data:
		is_corrupt, incorrect_char = is_line_corrupt(line)
		if is_corrupt:
			syntax_score += score[incorrect_char]

	print(syntax_score)

autocomplete_score = {")": 1, "]": 2, "}": 3, ">": 4}

def get_autocomplete_score(expected_closers):
	score = 0
	for char in expected_closers[::-1]:
		score *= 5
		score += autocomplete_score[char]

	return score

def part_two():
	data = get_data("input.txt")

	completion_scores = list()
	for line in data:
		is_corrupt, expected_closers = is_line_corrupt(line)
		if not is_corrupt:
			completion_scores.append(get_autocomplete_score(expected_closers))

	completion_scores.sort()
	print(completion_scores[int(len(completion_scores) / 2)])

if __name__ == '__main__':
	part_one()
	part_two()