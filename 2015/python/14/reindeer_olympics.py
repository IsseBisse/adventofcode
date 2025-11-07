import re

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n")

	return data

def parse_data(data):
	reindeers = list()
	for line in data:
		reindeer = line.split(" ")[0]
		speed, active_time, rest_time = [int(num_string) for num_string in re.findall(r"[0-9]+", line)]

		reindeers.append({"name": reindeer, 
			"speed": speed, 
			"active_time": active_time, 
			"rest_time": rest_time, 
			"cycle_time": active_time + rest_time})

	return reindeers

def run_race(reindeers, num_seconds):
	for reindeer in reindeers:
		num_finished_cycles = num_seconds // reindeer["cycle_time"]
		remaining_seconds = num_seconds % reindeer["cycle_time"]

		position = 0
		position += num_finished_cycles * reindeer["active_time"] * reindeer["speed"]
		position += min(remaining_seconds, reindeer["active_time"]) * reindeer["speed"]

		reindeer["position"] = position

def part_one():
	data = get_data("input.txt")
	reindeers = parse_data(data)

	run_race(reindeers, 2503)	

	reindeers.sort(key=lambda x:x["position"])
	print(reindeers[-1])
	
def run_points_race(reindeers, num_seconds):
	for reindeer in reindeers:
		reindeer["position"] = 0
		reindeer["points"] = 0

	for current_second in range(num_seconds):
		for reindeer in reindeers:
			reindeer["position"] += reindeer["speed"] if (current_second % reindeer["cycle_time"]) < reindeer["active_time"] else 0

		max_position = max([reindeer["position"] for reindeer in reindeers])
		for reindeer in reindeers:
			if reindeer["position"] == max_position:
				reindeer["points"] += 1


def part_two():
	data = get_data("input.txt")
	reindeers = parse_data(data)

	run_points_race(reindeers, 2503)

	reindeers.sort(key=lambda x:x["points"])
	for reindeer in reindeers:
		print(f"{reindeer['name']}: {reindeer['points']}")


if __name__ == '__main__':
	# part_one()
	part_two()