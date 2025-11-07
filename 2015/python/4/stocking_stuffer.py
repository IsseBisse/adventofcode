import hashlib

def part_one():
	data = "bgvyzdsv"

	five_zeros = False
	suffix = 1
	while not five_zeros:
		input_string = "%s%s" % (data, suffix)
		result = hashlib.md5(input_string.encode("utf-8")).hexdigest()

		five_zeros = result[0:5] == "00000"
		suffix += 1

	print(suffix-1)
	print(result)
	
def part_two():
	data = "bgvyzdsv"

	five_zeros = False
	suffix = 1
	while not five_zeros:
		input_string = "%s%s" % (data, suffix)
		result = hashlib.md5(input_string.encode("utf-8")).hexdigest()

		five_zeros = result[0:6] == "000000"
		suffix += 1

	print(suffix-1)
	print(result)

if __name__ == '__main__':
	#part_one()
	part_two()