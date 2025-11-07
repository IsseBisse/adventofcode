import re


def get_data(path):
	with open(path) as file:
		rules, messages = file.read().split("\n\n")

	rules = [tuple(row.split(": ")) for row in rules.split("\n")]
	rules = [(int(idx), rule.replace("\n", "")) for idx, rule in rules]
	messages = messages.split("\n")

	return rules, messages


class Rule:
	def __init__(self, idx):
		self.idx = idx
		self.sequences = "Object not initialized yet!"
		self.print_during_match = False

	def __str__(self):
		string = f"{self.idx}: "
		if isinstance(self.sequences, str):
			string += self.sequences

		else:
			sequence_strings = [" ".join(str(group.idx) for group in sequence) for sequence in self.sequences]
			string += " | ".join(sequence_strings)

		return string

	def initialize(self, sequences):
		self.sequences = sequences

	def is_match(self, string):
		if self.print_during_match:
			print(self, string)

		if string == "":
			# This means "main" string is too short
			return False, ""

		if isinstance(self.sequences, str):
			return string[0] == self.sequences, string[1:]

		for sequence in self.sequences:
			string_rem = string
			for rule in sequence:
				match, string_rem = rule.is_match(string_rem)

				if not match:
					break

			if match:
				return match, string_rem

		return match, string_rem


def parse_rules(rule_strings):
	rules = dict()
	for idx, rule_string in rule_strings:
		rule = Rule(idx)

		if "a" in rule_string or "b" in rule_string:
			rule.initialize(rule_string.replace("\"", ""))

		rules[idx] = rule

	for idx, rule_string in rule_strings:
		if "a" in rule_string or "b" in rule_string:
			# Already initialized, move along
			continue

		rule = rules[idx]
		sequence_strings = rule_string.split(" | ")
		sequences = [[rules[int(idx)] for idx in string.split(" ")] for string in sequence_strings]
		rule.initialize(sequences)

	return rules


def part_one():
	rule_strings, messages = get_data("input.txt")
	rules = parse_rules(rule_strings)

	def matching_function(string):
		match, string_rem = rules[0].is_match(string)
		match = match if string_rem == "" else False
		return match

	matches = list(filter(matching_function, messages))
	print(len(matches))


def part_two():
	rule_strings, messages = get_data("manualLooping_mediumInput.txt")
	rules = parse_rules(rule_strings)

	def matching_function(string):
		match, string_rem = rules[0].is_match(string)
		match = match if string_rem == "" else False
		return match

	expected_matches = {"bbabbbbaabaabba",
						"babbbbaabbbbbabbbbbbaabaaabaaa",
						"aaabbbbbbaaaabaababaabababbabaaabbababababaaa",
						"bbbbbbbaaaabbbbaaabbabaaa",
						"bbbababbbbaaaaaaaabbababaaababaabab",
						"ababaaaaaabaaab",
						"ababaaaaabbbaba",
						"baabbaaaabbaaaababbaababb",
						"abbbbabbbbaaaababbbbbbaaaababb",
						"aaaaabbaabaaaaababaa",
						"aaaabbaabbaaaaaaabbbabbbaaabbaabaaa",
						"aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba"}

	matches = set(filter(matching_function, messages))
	print(matches)
	print(len(matches))

	# [print(rule) for _, rule in sorted(rules.items(), key=lambda item: item[0])]
	# for rule in rules.values():
	# 	rule.print_during_match = True
	#
	# incorrect = list(expected_matches.difference(matches))
	# print(incorrect)
	# matching_function(incorrect[0])


if __name__ == '__main__':
	# part_one()
	part_two()

	def string_rep(string, times):
		return " ".join([string] * times)
	print(" | ".join([f"{string_rep('42', idx)} {string_rep('31', idx)}" for idx in range(1, 30)]))
	print(" | ".join([f"{string_rep('42', idx)}" for idx in range(1, 30)]))