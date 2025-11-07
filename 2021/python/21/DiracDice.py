from collections import Counter
from dataclasses import dataclass, field, replace
from itertools import permutations
import re
from typing import Tuple

def get_data(path):
	with open(path) as file:
		data = file.read()

	matches = re.findall(r"position: ([0-9]+)", data)
	start = [int(pos) for pos in matches]

	return start

@dataclass
class Player:
	num: int
	position: int
	score: int = 0

	def __str__(self):
		return f"Player {self.num} at {self.position+1} with score: {self.score}"

	def take_turn(self, dice):
		steps = 0
		for _ in range(3):
			steps += dice.roll()
		
		self.position = (self.position + steps) % 10
		self.score += self.position + 1
			
class DeterministicDice:
	value: int = -1
	rolls: int = 0

	def __str__(self):
		return f"Dice with last value {self.value+1} and {self.rolls} rolls"

	def roll(self):
		self.value = (self.value + 1) % 100
		self.rolls += 1
		return self.value + 1

def play_game(players, dice):
	while True:
		for idx, player in enumerate(players):
			player.take_turn(dice)

			if player.score >= 1000:
				loser = players[(idx+1)%2]
				return loser.score * dice.rolls

def part_one():
	position = get_data("input.txt")

	players = [Player(0, position[0]-1), Player(1, position[1]-1)]
	dice = DeterministicDice()

	game_score = play_game(players, dice)
	print(game_score)
	
SCORE_LIMIT = 21
@dataclass(frozen=True, eq=True)
class State:
	# (p1_pos, p1_score, p2_pos, p2_score)
	players: Tuple[int]
	permutations: int = field(hash=False)

	def new_players(self, steps, player_idx):
		players = list(self.players)
		# Update position
		players[2*player_idx] = (players[2*player_idx] + steps) % 10
		# Update score
		players[2*player_idx+1] += players[2*player_idx]+1

		return tuple(players)

	def isWon(self):
		return any([score >= SCORE_LIMIT for score in self.players[1::2]])

STEP_PERMUTATIONS = Counter([sum(perm) for perm in set(permutations((1,1,1,2,2,2,3,3,3), 3))])
def get_next_states(state, player_idx):
	next_states = list()
	for steps, permutations in STEP_PERMUTATIONS.items():
		new_players = state.new_players(steps, player_idx)
		new_state = State(new_players, state.permutations*permutations)
		next_states.append(new_state)

	return next_states

def all_next_states(states, player_idx):
	next_states = list()
	for state in states:
		next_states += get_next_states(state, player_idx)

	return next_states

def remove_wins_and_duplicates(states, player_wins, player_idx):
	# Get unique states
	unique_states = dict()
	for state in states:
		# Skip if state is won
		if state.isWon():
			player_wins[player_idx] += state.permutations
			continue

		# Otherwise merge equal (same player positions and scores) states
		if hash(state) in unique_states:
			existing_state = unique_states[hash(state)]
			state = State(state.players, state.permutations+existing_state.permutations)

		unique_states[hash(state)] = state

	return unique_states.values(), player_wins

def part_two():
	position = get_data("input.txt")
	players = (position[0]-1, 0, position[1]-1, 0)
	states = [State(players, 1)]

	print(states)

	player_wins = [0, 0]
	player_idx = 0
	while states:
		next_states = all_next_states(states, player_idx)
		states, player_wins = remove_wins_and_duplicates(next_states, player_wins, player_idx)
		print(len(states))

		player_idx = (player_idx + 1) % 2

	print(max(player_wins))


if __name__ == '__main__':
	# part_one()
	part_two()