import re

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n\n")

	data_dicts = list()
	for entry in data:
		line = " ".join(entry.split("\n"))

		parts = line.split(" ")

		entry_dict = dict()
		for part in parts:
			key = part.split(":")[0]
			value = part.split(":")[1]

			entry_dict[key] = value

		data_dicts.append(entry_dict)

	return data_dicts

REQUIRED_FIELDS = ["byr",
	"iyr",
	"eyr",
	"hgt",
	"hcl",
	"ecl",
	"pid",
	"cid"]

def has_required_fields(entry):
	for field in REQUIRED_FIELDS[:-1]:
		if not field in entry.keys():
			return False

	return True


def part_one():
	data = get_data("input.txt")

	num_valid = 0
	for entry in data:
		if has_required_fields(entry):
			num_valid += 1

	print(num_valid)

VALIDS = {"byr": {"regex": [r"^[0-9]{4}$"], "limits": [(1920, 2002)]},
	"iyr": {"regex": [r"^[0-9]{4}$"], "limits": [(2010, 2020)]},
	"eyr": {"regex": [r"^[0-9]{4}$"], "limits": [(2020, 2030)]},
	"hgt": {"regex": [r"^[0-9]+cm", r"[0-9]+in"], "limits": [(150, 193), (59, 76)]},
	"hcl": {"regex": [r"^#[0-9a-f]{6}$"], "limits": None},
	"ecl": {"regex": None, "limits": ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]},
	"pid": {"regex": [r"^[0-9]{9}$"], "limits": None}}



def field_is_valid(key, value):
	if key not in VALIDS:
		return True

	regex = VALIDS[key]["regex"]
	limits = VALIDS[key]["limits"]

	if regex:
		matches = None
		i = 0
		while (not matches and i<len(regex)):
			matches = re.findall(regex[i], value)
			i += 1
		i -= 1

		if not matches:
			return False

		else:
			if limits:
				match_int = int(re.findall(r"[0-9]+", matches[0])[0])
				return match_int >= limits[i][0] and match_int <= limits[i][1] 

		return True

	else:
		return value in limits

def entry_is_valid(entry):

	if not has_required_fields(entry):
		return False

	for key in entry:
		if not field_is_valid(key, entry[key]):
			return False

	return True

def part_two():
	data = get_data("input.txt")

	num_valid = 0
	ok_entries = list()
	for entry in data:
		if entry_is_valid(entry):
			num_valid += 1
			ok_entries.append(entry)

	# for field in ["byr", "iyr", "eyr"]:
	# 	values = [entry[field] for entry in ok_entries]
	# 	print(values)
	# 	try:
	# 		print(min(values), max(values))
	
	# 	except Exception as e:
	# 		print("Min max not valid")

	# values = [entry["hgt"] for entry in ok_entries]
	# print(values)
	# cm_values = [int(val[:-2]) for val in values if "cm" in val]
	# in_values = [int(val[:-2]) for val in values if "in" in val]
	# print(cm_values)
	# print(in_values)
	# print(len(values), len(cm_values) + len(in_values))
	# print(min(cm_values), max(cm_values))
	# print(min(in_values), max(in_values))

	# values = [entry["hcl"] for entry in ok_entries]
	# print(values)
	# value_len = [len(val) for val in values]
	# print(min(value_len), max(value_len))
	# chars = set("".join(values))
	# print(chars)

	# values = [entry["ecl"] for entry in ok_entries]
	# print(set(values))

	# values = [entry["pid"] for entry in ok_entries]
	# print(values)
	# value_len = [len(val) for val in values]
	# print(min(value_len), max(value_len))

	# long_pid = [val for val in values if len(val) == 10]
	# print(long_pid)
	# matches = re.findall(VALIDS["pid"]["regex"], long_pid)
	# print(matches)

	print(num_valid)

if __name__ == '__main__':
	#part_one()
	part_two()