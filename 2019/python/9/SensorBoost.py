from Program import Program 

def part_one():
	
	# Setup
	program = Program(1024*1024)
	program.load_code("testInput.txt")
	
	# Run
	#program.load_input([1])
	program.run()
	print(program.is_done())

	output = program.get_output()
	print(output)

def part_two():
	pass

if __name__ == '__main__':
	part_one()