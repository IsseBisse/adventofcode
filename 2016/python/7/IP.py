'''
Input
'''
def parseInput(filename):
	f = open(filename, "r")
	data = f.read()

	data = data.split()

	return data

'''
Part One
'''
def splitString(string):
	normals = list()
	hypernets = list()

	# Find first normal sequence
	parts = string.split("[")
	normals.append(parts[0])

	for part in parts[1:]:
		sub_parts = part.split("]")
		normals.append(sub_parts[1])
		hypernets.append(sub_parts[0])

	return normals, hypernets

def containsPair(string):
	for i in range(len(string)-3):
		start = string[i:i+2]
		end = string[i+2:i+4]

		if start == end[::-1] and not (start[0] == start[1]):
			return True

	return False

def partOne():
	data = parseInput("input.txt")
	
	num_support_tls = 0
	for line in data:
		normals, hypernets = splitString(line)

		support_tls = False
		for normal in normals:
			support_tls = support_tls or containsPair(normal)

		for hypernet in hypernets:
			support_tls = support_tls and not containsPair(hypernet)

		if support_tls:
			num_support_tls += 1

	print("%d IPs support TLS" % num_support_tls)

'''
Part Two
'''
def findABAs(string):
	aba = list()

	for i in range(len(string)-2):
		if string[i] == string[i+2]:
			aba.append(string[i:i+3])

	return aba

def convertABAtoBAB(aba):
	return aba[1] + aba[0] + aba[1]

def containsBABs(babs, string):

	print(string)
	for i in range(len(string)-2):
		substring = string[i:i+3]
		print(substring)

		if substring in babs:
			return True

	return False

def partTwo():
	data = parseInput("testInput2.txt")
	
	num_support_ssl = 0
	for line in data:
		supernets, hypernets = splitString(line)
		print(line)

		# Find all ABAs
		abas = list()
		for supernet in supernets:
			abas += findABAs(supernet)

		# Convert to BABs
		babs = list()
		for aba in abas:
			babs.append(convertABAtoBAB(aba))

		# Look for BABs in hypernets
		for hypernet in hypernets:
			if containsBABs(babs, hypernet):
				num_support_ssl += 1

				#print(line)
				#print(abas)
				#print(babs)
				#print("SSL confirmed!")
				#print()
				break

	print("%d IPs support SSL" % num_support_ssl)


		#for hypernet in hypernets:
			#found_

'''
Main
'''
if __name__ == '__main__':
	partTwo()