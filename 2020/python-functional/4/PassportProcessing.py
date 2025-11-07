import re

from functools import reduce

CONVERTERS = {"byr": int,
	"iyr": int,
	"eyr": int,
	"pid": int,
	"cid": int
	}

def parse_field(field_string):
	key = re.findall(r"[a-z]{3}:", field_string)[0][:-1]
	value = re.findall(r":.+", field_string)[0][1:]

	return {key: value}

def parse_lines(lines):
	lines = lines.replace("\n", " ")
	fields = lines.split(" ")

	parsed_fields = map(parse_field, fields)
	data = reduce(lambda x, y: {**x, **y}, parsed_fields)

	return data

def get_data(path):
	with open(path) as file:
		raw_data = file.read().split("\n\n")

	data = map(parse_lines, raw_data)

	return tuple(data)

def simple_check(passport_data):
	REQUIRED_FIELDS = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}

	required_fields_present = set(passport_data.keys()).intersection(REQUIRED_FIELDS)
	return len(required_fields_present) == len(REQUIRED_FIELDS)

def part_one():
	data = get_data("input.txt")
	correct_passports = map(simple_check, data)
	print(sum(correct_passports))

def check_year(value, min_limit, max_limit):
	matches = re.findall(r"^[0-9]{4}$", value)
	return len(matches) > 0 and min_limit <= int(matches[0]) <= max_limit

def check_height(value):
	matches = re.findall(r"([0-9]+)[in|cm]", value)
	if not matches:
		return False

	num_value = int(matches[0])
	if "in" in value:
		return 59 <= num_value <= 76
	else:
		return 150 <= num_value <= 193

def check_hair(value):
	return re.search(r"^#[a-f0-9]{6}$", value) is not None

def check_eyes(value):
	allowed_eyes = {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}
	return value in allowed_eyes
		
def check_pid(value):
	return re.search(r"^[0-9]{9}$", value) is not None

def advanced_check(passport_data):
	if not simple_check(passport_data):
		return False

	# Check years 
	year_data = ((passport_data["byr"], 1920, 2002),
		(passport_data["iyr"], 2010, 2020),
		(passport_data["eyr"], 2020, 2030))

	return check_year(passport_data["byr"], 1920, 2002) and \
		check_year(passport_data["iyr"], 2010, 2020) and \
		check_year(passport_data["eyr"], 2020, 2030) and \
		check_height(passport_data["hgt"]) and \
		check_hair(passport_data["hcl"]) and \
		check_eyes(passport_data["ecl"]) and \
		check_pid(passport_data["pid"])

def part_two():
	data = get_data("input.txt")
	correct_passports = map(advanced_check, data)
	print(sum(correct_passports))

if __name__ == '__main__':
	part_one()
	part_two()