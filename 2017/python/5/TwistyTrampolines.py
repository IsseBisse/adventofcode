def readInput(filename):
	f = open(filename, "r")

	data = list()
	for line in f:
		row = line.split("\n")[0]
		row = int(row)

		data.append(row)

	return data

'''
Part one
'''	
def partOne():
	data = readInput("input.txt")
	#data = [0, 3, 0, 1, -3]

	index = 0
	start_index = 0
	end_index = len(data) - 1

	steps = 0
	while (index >= start_index) & (index <= end_index):
		#print(index)
		new_index = data[index]
		if data[index] >= 3:
			data[index] -= 1
		else:
			data[index] += 1
		index += new_index
		steps += 1

	print("Steps required: %d" % steps)

'''
Part two
'''
def partTwo():
	data = readInput("input.txt")


if __name__ == '__main__':
	partOne()