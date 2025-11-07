import ast
from dataclasses import dataclass

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	data = [ast.literal_eval(string) for string in data]

	return data

class SnailNumber:
	@staticmethod
	def __add_leaf(leaf_list):
		if isinstance(leaf_list, int):
			return leaf_list

		else:
			return SnailNumber(leaf_list)

	def __init__(self, number_list):
		self.left = self.__add_leaf(number_list[0])
		self.right = self.__add_leaf(number_list[1]) 

	def __str__(self):
		return f"[{str(self.left)}, {str(self.right)}]"



def part_one():
	data = get_data("smallInput.txt")

	snail_num = SnailNumber(data[1])
	print(snail_num)

def part_two():
	data = get_data("smallInput.txt")

if __name__ == '__main__':
	part_one()
	part_two()