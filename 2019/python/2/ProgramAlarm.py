import copy

def parse_input(path):

	f = open(path, "r")

	data = [int(x) for x in  f.read().split(",")]

	return data

def add(code, pos):
	term_1_pos = code[pos + 1]
	term_2_pos = code[pos + 2]
	res_pos = code[pos + 3]

	code[res_pos] = code[term_1_pos] + code[term_2_pos]

def mult(code, pos):
	term_1_pos = code[pos + 1]
	term_2_pos = code[pos + 2]
	res_pos = code[pos + 3]

	code[res_pos] = code[term_1_pos] * code[term_2_pos]

def run(code):
	pos = 0
	while True:
		command = code[pos]

		if command == 1:
			add(code, pos)

		elif command == 2:
			mult(code, pos)

		elif command == 99:
			break

		else:
			print("ERROR! Incorrect op-code: %d!" % command)
			break

		pos += 4

	return code[0]

def part_one():
	#data = [1,9,10,3,2,3,11,0,99,30,40,50]
	code = parse_input("input.txt")
	
	code[1] = 12
	code[2] = 2

	print("Value at 0 is %d" % run(code))

def initialize_memory(code, noun, verb):

	ret = copy.deepcopy(code)

	ret[1] = noun
	ret[2] = verb

	return ret

def part_two():
	starting_code = parse_input("input.txt")
	desired_answer = 19690720

	try:
		for noun in range(100):
			for verb in range(100):
				code = initialize_memory(starting_code, noun, verb)

				answer = run(code)

				if answer == desired_answer:
					raise Exception
	
	except Exception as e:
		print("Correct parameters was noun: %d and verb: %d. Answer is %d" % (noun, verb, 100*noun + verb))

if __name__ == '__main__':
	part_two()