PUBLIC_KEYS = [14788856,
	19316454]
# PUBLIC_KEYS = [5764801,
# 	17807724]

PUBLIC_SUBJECT_NUMBER = 7
NUMERATOR = 20201227

def transform(value, subject_number):
	value *= subject_number
	value = value % NUMERATOR
	return value

def part_one():
	# Find num_loops
	num_loops = [0, 0]
	for user in range(2):
		value = 1

		while value != PUBLIC_KEYS[user]:
			value = transform(value, PUBLIC_SUBJECT_NUMBER)

			num_loops[user] += 1
	
	print(num_loops)

	# Get encryption key
	encryption_keys = [None, None]
	for user in range(2):

		value = 1
		print("Start: %d. Num loops: %d" % (value, num_loops[1-user]))
		for loop in range(num_loops[1-user]):
			value = transform(value, PUBLIC_KEYS[user])

		encryption_keys[user] = value

	print(encryption_keys)

def part_two():
	pass

if __name__ == '__main__':
	part_one()