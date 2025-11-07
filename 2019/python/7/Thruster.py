from Program import Program
import itertools

def part_one():

	# Setup program
	program = Program()
	program.load_code("thrusterProgram.txt")

	# Try all phase setting permutations
	phase_configuration_permutations = itertools.permutations([0, 1, 2, 3, 4])
	
	max_output = 0
	for phase_configuration in phase_configuration_permutations:
		
		output = 0
		for phase in phase_configuration:	

			program.load_input([output, phase])
			program.reset()
			program.run()
			output = program.get_output()

		if output > max_output:
			max_output = output

	print("Highest signal to thrusters is: %d" % max_output)

def part_two():
	
	# Setup program
	program = list()
	for i in range(5):

		program.append(Program())
		program[i].load_code("thrusterProgram.txt")

	# Try all phase setting permutations
	phase_configuration_permutations = itertools.permutations([5, 6, 7, 8, 9])
	
	max_output = 0
	for phase_configuration in phase_configuration_permutations:

		# Start each program
		output = 0
		for i, phase in enumerate(phase_configuration):

			program[i].load_input([output, phase])
			program[i].run()
			output = program[i].get_output()

			#print("Output: %d from %d with phase %d" % (output, i, phase))

		# Run until done
		i = 0
		while not program[4].is_done():

			program[i].load_input([output])
			program[i].run()
			output = program[i].get_output()

			i = (i + 1) % 5

			#print([x.is_done() for x in program])
			#print("Output: %d from %d" % (output, i))

		if output > max_output:
			max_output = output

	print("Max output is: %d" % max_output)

if __name__ == '__main__':
	#part_one()
	part_two()