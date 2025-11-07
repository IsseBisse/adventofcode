'''
Input
'''
def parseInput(filename):
	f = open(filename, "r")
	data = f.read()

	data = data.split("\n")

	return data

'''
Part One
'''
def parseLine(line):
	parts = line.split("[")

	# Get checksum
	checksum = parts[1][:-1]
	
	# Get sector ID
	parts = parts[0].split("-")
	sector_id = int(parts[-1])

	# Get name
	name = ""
	for part in parts[:-1]:
		name += part + "-"
	name = name[:-1]

	return name, sector_id, checksum

def calculateChecksum(name):
	char_in_name = list(set(name))
	char_in_name.sort()
	char_occurance = [0] * len(char_in_name)

	for char in name:
		char_ind = char_in_name.index(char)
		char_occurance[char_ind] += 1

	max_ind = sorted(range(len(char_occurance)), key=lambda k: char_occurance[k], reverse=True)

	checksum = ""
	for ind in max_ind[0:5]:
		checksum += char_in_name[ind]
	
	return checksum
	
def partOne():
	data = parseInput("input.txt")

	sector_id_sum = 0
	for line in data:
		name, sector_id, claimed_checksum = parseLine(line)
		actual_checksum = calculateChecksum(name)

		if actual_checksum == claimed_checksum:
			sector_id_sum += sector_id

	print("Sum of all sector ID is: %d" % sector_id_sum)



'''
Part Two
'''
def partTwo():
	data = parseInput("input.txt")

	# Decryption parameters
	start = 97
	div = 26

	for line in data:
		name, sector_id, claimed_checksum = parseLine(line)

		dectrypted_name = ""
		for char in name:
			if char == "-":
				dectrypted_name += " "
			else:
				# Convert to number
				num = ord(char)

				# "Normalize" and shift
				num -= start
				num = (num + sector_id) % div
				num += start

				dectrypted_name += chr(num)

		if "north" in dectrypted_name:
			print("%s has sector ID: %d" % (dectrypted_name, sector_id))

	
'''
Main
'''
if __name__ == '__main__':
	#partOne()
	partTwo()