import re

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	return data[:-1]

FORBIDDEN = ["ab", "cd", "pq", "xy"]

def is_string_ok(string):
	# Check for >3 vowels
	vowels = re.findall(r"[aeiou]", string)
	vowels_ok = len(vowels) > 2

	# Check for double letters
	doubles = re.findall(r"(.)\1+", string)
	doubles_ok = len(doubles) > 0

	# Check for forbidden sub strings 
	forbidden_ok = True
	for forb in FORBIDDEN:
		if forb in string:
			forbidden_ok = False

	return vowels_ok and doubles_ok and forbidden_ok


def part_one():
	data = get_data("input.txt")
	#data = ["ugknbfddgicrmopn", "jchzalrnumimnmhp", "haegwjzuvuyypxyu", "dvszwmarrgswjxmb"]

	nice_strings = 0
	for string in data:
		nice_strings += 1 if is_string_ok(string) else 0
	
	print("Number of nice strings: %d" % nice_strings)

def new_is_string_ok(string):
	# Check twice pair
	twice = re.findall(r"(..).*\1", string)
	twice_ok = len(twice) > 0

	# Check separated repeat
	repeat = re.findall(r"(.).\1", string)
	repeat_ok = len(repeat) > 0

	return twice_ok and repeat_ok

def part_two():
	data = get_data("input.txt")
	#data = ["qjhvhtzxzqqjkmpb", "aaxxyxx", "uurcxstgmygtbstg", "ieodomkazucvgmuy", "aaa"]

	nice_strings = 0
	for string in data:
		nice_strings += 1 if new_is_string_ok(string) else 0
	
	print("Number of nice strings: %d" % nice_strings)

if __name__ == '__main__':
	#part_one()
	part_two()