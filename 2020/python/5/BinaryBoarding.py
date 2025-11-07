SMALL_INPUT = ["FBFBBFFRLR",
	"BFFFBBFRRR",
	"FFFBBBFRRR",
	"BBFFBBFRLL"]

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	return data

def part_one():
	#data = SMALL_INPUT
	data = get_data("input.txt")

	seat_data = list()
	for entry in data:
		row_string = entry[0:7]
		col_string = entry[7:]

		row_bin = "".join(["1" if char=="B" else "0" for char in row_string])
		col_bin = "".join(["1" if char=="R" else "0" for char in col_string])		

		row = int(row_bin, 2)
		col = int(col_bin, 2)
		seat_id = int(row_bin + col_bin, 2)

		seat_data.append((row, col, seat_id))

	seat_ids = [entry[2] for entry in seat_data]
	return max(seat_ids)


def part_two():
	data = get_data("input.txt")

	seat_data = list()
	for entry in data:
		row_string = entry[0:7]
		col_string = entry[7:]

		row_bin = "".join(["1" if char=="B" else "0" for char in row_string])
		col_bin = "".join(["1" if char=="R" else "0" for char in col_string])		

		row = int(row_bin, 2)
		col = int(col_bin, 2)
		seat_id = int(row_bin + col_bin, 2)

		seat_data.append((row, col, seat_id))

	seat_ids = [entry[2] for entry in seat_data]

	for i in range(max(seat_ids)):
		if i not in seat_ids:
			print(i)

if __name__ == '__main__':
	#part_one()
	part_two()