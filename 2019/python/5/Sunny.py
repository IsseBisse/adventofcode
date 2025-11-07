from Program import Program

def part_one_and_two():
	
	program = Program()
	program.load_code("input.txt")
	program.run()

if __name__ == '__main__':
	part_one_and_two()