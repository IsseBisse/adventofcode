import Operations as op
import re

def parseTestList(filename):
	f = open(filename, "r")
	test_list = list()

	ind = 0
	test = dict()
	for line in f:
		if ind == 0:
			test["in"] = [int(s) for s in re.findall("(\d+)", line)]
		elif ind == 1:
			
			test["opcode"] = [int(s) for s in re.findall("(\d+)", line)]
		elif ind == 2:
			
			test["out"] = [int(s) for s in re.findall("(\d+)", line)]
		elif ind == 3:
			test_list.append(test)
			test = dict()
		
		ind = (ind + 1) % 4

	return test_list

def parseProgramSequence(filename):
	f = open(filename, "r")
	program_sequence = list()

	for line in f:
		program_sequence.append([int(s) for s in re.findall("(\d+)", line)])

	return program_sequence


'''
Part 1
'''
def partOne(test_list):
	matching_more_than_three = 0

	for item in test_list:
		input_register = item["in"]
		output_register = item["out"]
		opcode = item["opcode"]

		results = op.testAllFunctions(input_register, output_register, opcode)
		if len(results) >= 3:
			matching_more_than_three += 1

	print("Number of samples matching three or more opcodes: %d" % matching_more_than_three)

'''
Part 2
'''
def functionAND(possible_matches, current_matches):
	for match in possible_matches:
		if match not in current_matches:
			possible_matches.remove(match)

	return possible_matches

def removeDuplicates(possible_matches, taken_functions):
	for match in possible_matches:
		if match in taken_functions:
			possible_matches.remove(match)

	return possible_matches


def partTwo(test_list, program_sequence):
	# List all alternatives
	possible_matches = list()
	for i in range(16):
		possible_matches.append(list())
		for func in op.functions:
			possible_matches[i].append(func.__name__)

	# Loop through list and remove impossible options
	for item in test_list:
		input_register = item["in"]
		output_register = item["out"]
		opcode = item["opcode"]

		results = op.testAllFunctions(input_register, output_register, opcode)
		print("Opcode %d: " % opcode[0], end="")
		print(results)

		possible_matches[opcode[0]] = functionAND(possible_matches[opcode[0]], results)

	for i, match in enumerate(possible_matches):
		print("Opcode %d: " % i, end="")
		print(match)
	print("")

	# Loop through matches and find final setup
	taken_functions = list()
	while len(taken_functions) < 16:
		taken_functions = list()
		for match in possible_matches:
			if len(match) == 1:
				taken_functions.append(match[0])

		for i, match in enumerate(possible_matches):
			if len(match) > 1:
				possible_matches[i] = removeDuplicates(match, taken_functions)

		for i, match in enumerate(possible_matches):
			print("Opcode %d: " % i, end="")
			print(match)
		print("")

	register = [0] * 4
	for row in program_sequence:
		opcode = possible_matches[row[0]][0]
		A = row[1]
		B = row[2]
		C = row[3]

		register = getattr(op, opcode)(register, A, B, C)

	print("The value in register 0 is: %d" % register[0])

	
'''
Main
'''
if __name__ == '__main__':
	test_list = parseTestList("input.txt")
	program_sequence = parseProgramSequence("input2.txt")
	
	#partOne(test_list)
	partTwo(test_list, program_sequence)