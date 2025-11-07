def has_double(number):
	
	number_string = str(number)

	ok = False
	for i, char in enumerate(number_string[:-1]):
		ok |= char == number_string[i+1]

	return ok

def never_lower(number):

	number_string = str(number)
	
	ok = True
	for i, char in enumerate(number_string[:-1]):
		ok &= char <= number_string[i+1]

	return ok

def part_one(low, high):

	valid_passwords = 0
	for candidate in range(low, high + 1):

		ok = never_lower(candidate)
		ok &= has_double(candidate)

		valid_passwords += ok

	print("%d valid passwords in range %d-%d" % (valid_passwords, low, high))

def has_lonely_double(number):

	number_string = str(number)
	
	matching = [number_string[0]]
	for i, char in enumerate(number_string[1:]):

		if char == number_string[i]:
			matching[-1] += char

		else:
			matching.append(char)

	return sum([len(x) == 2 for x in matching]) > 0

def part_two(low, high):
	valid_passwords = 0
	for candidate in range(low, high + 1):

		ok = never_lower(candidate)
		ok &= has_lonely_double(candidate)

		valid_passwords += ok

	print("%d valid passwords in range %d-%d" % (valid_passwords, low, high))

if __name__ == '__main__':
	low = 138307
	high = 654504

	#part_one(low, high)
	part_two(low, high)