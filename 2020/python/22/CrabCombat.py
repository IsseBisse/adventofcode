def get_data(path):
	with open(path) as file:
		data = file.read().split("\n\n")

	players = [[int(row) for row in player_data.split("\n")[1:]] for player_data in data]

	return players


def one_round(players):
	player_one = players[0]
	player_two = players[1]
	card_one = player_one.pop(0)
	card_two = player_two.pop(0)

	if card_one > card_two:
		player_one.append(card_one)
		player_one.append(card_two)
	else:
		player_two.append(card_two)
		player_two.append(card_one)


def part_one():
	players = get_data("input.txt")
	# print(players)
	while len(players[0]) > 0 and len(players[1]) > 0:
		one_round(players)
		# print(players)

	winner = players[0] if len(players[0]) > 0 else players[1]
	score = sum(card*(multiplier+1) for card, multiplier in zip(reversed(winner), range(len(winner))))
	print(score)


def one_recursive_game(players):
	turn = 1
	previous_players = set()
	while len(players[0]) > 0 and len(players[1]) > 0:
		# print(f"Round {turn}: {players}")

		players_tuple = tuple(tuple(player) for player in players)
		if players_tuple in previous_players:
			return True, players
		previous_players.add(players_tuple)

		one_recursive_round(players)
		turn += 1

	one_is_winner = len(players[0]) > 0
	return one_is_winner, players


def one_recursive_round(players):
	player_one = players[0]
	player_two = players[1]
	card_one = player_one.pop(0)
	card_two = player_two.pop(0)

	if len(player_one) >= card_one and len(player_two) >= card_two:
		# print("Recursive game")
		players_copy = [player_one[:card_one], player_two[:card_two]]
		one_is_winner, _ = one_recursive_game(players_copy)

	else:
		one_is_winner = card_one > card_two

	if one_is_winner:
		player_one.append(card_one)
		player_one.append(card_two)

	else:
		player_two.append(card_two)
		player_two.append(card_one)


def part_two():
	players = get_data("input.txt")
	one_is_winner, players = one_recursive_game(players)
	winner = players[0] if one_is_winner else players[1]
	score = sum(card * (multiplier + 1) for card, multiplier in zip(reversed(winner), range(len(winner))))
	print(score)


if __name__ == '__main__':
	# part_one()
	part_two()