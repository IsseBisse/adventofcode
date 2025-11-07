class Recipes:

	def __init__(self, input):
		self.history = input

		self.first_elf = 0
		self.second_elf = 1

	def __str__(self):
		string = ""

		for i, item in enumerate(self.history):
			if i == self.first_elf:
				item_string = "(%d)" % item
			elif i == self.second_elf:
				item_string = "[%d]" % item
			else:
				item_string = "%d" % item

			string += item_string + " "

		return string

	def __len__(self):
		return len(self.history)

	def moveForward(self):
		first_elf_steps = self.history[self.first_elf] + 1
		second_elf_steps = self.history[self.second_elf] + 1

		self.first_elf = (self.first_elf + first_elf_steps) % len(self.history)
		self.second_elf = (self.second_elf + second_elf_steps) % len(self.history)

	def createNewRecipe(self):
		# Add new score(s)
		new_score = self.history[self.first_elf] + self.history[self.second_elf]
		new_digits = [int(d) for d in str(new_score)]

		for digit in new_digits:
			self.history.append(digit)

		# Move elves
		self.moveForward()

	def getScore(self, index, length):
		score_list = self.history[index:index+length]

		score_string = ""
		for score in score_list:
			score_string += "%d" % score

		return score_string