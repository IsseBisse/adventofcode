from re import findall
import matplotlib.pyplot as plt

from math import sqrt

def get_data(path):
	with open(path) as file:
		data = file.read()

	return data

def parse_data(data):
	return [int(string) for string in findall(r"\d+", data)]

def get_score(positions, point):
	score = 0
	for pos in positions:
		score += abs(pos - point)

	return score

def plot_points(positions):
	X = list(range(3000))
	Y = list()
	for x in X:
		Y.append(get_score(positions, x))

	plt.plot(X, Y)
	plt.show()

def get_closest_point(positions, scoring_func=get_score):
	scores = list()
	for point in range(min(positions), max(positions) + 1):
		score = scoring_func(positions, point)

		scores.append((point, score))

	scores.sort(key=lambda x: x[1])

	return scores[0]

def part_one():
	data = get_data("input.txt")
	positions = parse_data(data)

	closest_point = get_closest_point(positions)
	print(closest_point)

def new_get_score(positions, point):
	score = 0
	for pos in positions:
		score += sum(range(abs(pos - point) + 1))

	return score

def part_two():
	data = get_data("input.txt")
	positions = parse_data(data)

	closest_point = get_closest_point(positions, scoring_func=new_get_score)
	print(closest_point)

if __name__ == '__main__':
	part_one()
	part_two()