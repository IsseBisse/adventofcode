def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	for i, entry in enumerate(data):
		data[i] = int(entry)

	return data

def combination_sums(numbers):

	sums = list()
	for i in numbers:
		for j in numbers:
			if not i == j:
				sums.append(i + j)

	return list(set(sums))

def part_one(path, preamble):
	data = get_data(path)
	
	for i in range(preamble, len(data)):
		if not data[i] in combination_sums(data[i-preamble:i]):
			break

	print("%d did not match!" % data[i])
	return data[i]



def part_two(path, mismatch):
	data = get_data(path)

	for i in range(len(data)):
		contiguous_sum = 0
		j = 0
		while contiguous_sum < mismatch:
			contiguous_sum += data[i+j]
			j += 1

		if contiguous_sum == mismatch:
			break

	contiguous_set = data[i:i+j]
	print("%d is the encryption weakness" % (min(contiguous_set) + max(contiguous_set)))

if __name__ == '__main__':
	mismatch = part_one("input.txt", 25)
	part_two("input.txt", mismatch)