from itertools import groupby

def convert_dig(dig_group):
	return f"{len(dig_group)}{dig_group[0]}"

def elf_encoding(number):
	digit_groups = [list(group) for _, group in groupby(str(number))]

	new_digits = list()
	for group in digit_groups:
		new_digits.append(convert_dig(group))

	new_number = int("".join(new_digits))

	return new_number

def part_one():
	test_numbers = [1, 11, 21, 1211, 111221]

	for number in test_numbers:
		new_number = elf_encoding(number)
		print(number, new_number)

	number = 1113222113
	for lap in range(40):
		number = elf_encoding(number)

	print(len(str(number)))

def lookandsay(number):
	return ''.join( str(len(list(g))) + k
		        for k,g in groupby(number) )

def part_two():
	number = "1113222113"
	for lap in range(50):
		number = lookandsay(number)

	print(len(str(number)))

if __name__ == '__main__':
	#part_one()
	part_two()