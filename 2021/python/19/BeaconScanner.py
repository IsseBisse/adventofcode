from dataclasses import dataclass
import numpy as np

def get_data(path):
	with open(path) as file:
		data = file.read().split("\n\n")

	data = [[np.array([int(item) for item in coord.split(",")]) for coord in row.split("\n")[1:]] for row in data]

	return data

def distance_sorted_magnitude(first, second):
	distance = np.abs(first - second)
	distance.sort()

	return tuple(distance)

# @dataclass
# class Beacon:
# 	absolute_index: int = -1
# 	absolute_position: np.ndarray

def get_inter_distances(absolute_beacon_positions):
	inter_beacon_distances = dict()
	for first_idx, first in enumerate(absolute_beacon_positions):
		for second_idx, second in enumerate(absolute_beacon_positions):
			if first_idx == second_idx:
				continue

			distance = distance_sorted_magnitude(first, second)

			if distance not in inter_beacon_distances:
				inter_beacon_distances[distance] = (first_idx, second_idx)

	return inter_beacon_distances

def find_absolute_index(first, scanner, inter_beacon_distances):
	candidate_idx = None

	for second in scanner:
		distance = distance_sorted_magnitude(first, second)

		if distance in inter_beacon_distances:
			if candidate_idx is None:
				candidate_idx = set(inter_beacon_distances[distance])
				# print(candidate_idx)

			else:
				candidate_idx = candidate_idx.intersection(set(inter_beacon_distances[distance]))
				# print(candidate_idx)

		if candidate_idx is not None and len(candidate_idx) == 1:
			(idx,) = candidate_idx	# Unpack set
			return idx


def relative_to_absolute(beacon, R, P_centroid, Q_centroid):
	absolute_beacon = np.matmul(np.linalg.inv(R), beacon - Q_centroid) + P_centroid
	absolute_beacon = np.round(absolute_beacon)
	return absolute_beacon

def get_kabsch_transform(P, Q):
	P_centroid = 1 / P.shape[0] * np.sum(P, axis=0)
	Q_centroid = 1 / Q.shape[0] * np.sum(Q, axis=0)

	H = np.matmul(np.transpose(P-P_centroid), Q-Q_centroid)
	U, S, Vt = np.linalg.svd(H)
	V = np.transpose(Vt)

	d = np.linalg.det(np.matmul(V, np.transpose(U)))

	R = np.matmul(np.matmul(V, np.array(((1, 0, 0), (0, 1, 0), (0, 0, d)))), np.transpose(U))
	R = np.round(R)

	return R, P_centroid, Q_centroid

def add_absolute_beacons(absolute_beacon_positions, inter_beacon_distances, scanner):
	index_pairs = list()
	new_indicies = list()
	for scanner_idx, beacon in enumerate(scanner):
		absolute_idx = find_absolute_index(beacon, scanner, inter_beacon_distances)
		if absolute_idx is not None:
			index_pairs.append((scanner_idx, absolute_idx))
		
		else:
			new_indicies.append(scanner_idx)

	# Not enough common points
	if len(index_pairs) < 12:
		return None

	# Get scanner orientation and add new points
	P = list()
	Q = list()
	for scanner_idx, absolute_idx in index_pairs:
		P.append(absolute_beacon_positions[absolute_idx])
		Q.append(scanner[scanner_idx])

	P = np.array(P)
	Q = np.array(Q)
	R, P_centroid, Q_centroid = get_kabsch_transform(P, Q)

	# for scanner_idx, absolute_idx in index_pairs:
	# 	print(relative_to_absolute(scanner[scanner_idx], R, P_centroid, Q_centroid))
	# 	print(absolute_beacon_positions[absolute_idx])
	
	for idx in new_indicies:
		beacon = scanner[idx] 

		absolute_beacon = relative_to_absolute(beacon, R, P_centroid, Q_centroid)
		absolute_beacon_positions.append(absolute_beacon)

	absolute_scanner = relative_to_absolute(np.array((0, 0, 0)), R, P_centroid, Q_centroid)

	# TODO: Re-calculate distances
	inter_beacon_distances = get_inter_distances(absolute_beacon_positions)

	return absolute_beacon_positions, inter_beacon_distances, absolute_scanner

def get_absolute_beacons_and_scanners(relative_beacons):
	scanners = [np.array((0, 0, 0))]
	absolute_beacon_positions = relative_beacons[0].copy()
	inter_beacon_distances = get_inter_distances(absolute_beacon_positions)
	relative_beacons.pop(0)
	idx = 0
	while True:
		scanner = relative_beacons[idx]
		res = add_absolute_beacons(absolute_beacon_positions, inter_beacon_distances, scanner)
		if res is not None:
			absolute_beacon_positions, inter_beacon_distances, absolute_scanner = res
			scanners.append(absolute_scanner)
			relative_beacons.pop(idx)
			
		if len(relative_beacons) == 0:
			break
		else:
			idx = (idx + 1) % len(relative_beacons)
		
	return absolute_beacon_positions, scanners

def part_one():
	relative_beacons = get_data("input.txt")
	absolute_beacons, _ = get_absolute_beacons_and_scanners(relative_beacons)
	
	print(len(absolute_beacons))

def part_two():
	relative_beacons = get_data("input.txt")
	absolute_beacons, scanners = get_absolute_beacons_and_scanners(relative_beacons)
	inter_scanner_distances = get_inter_distances(scanners)

	manhattan_distances = [sum(key) for key in inter_scanner_distances]
	print(max(manhattan_distances))

if __name__ == '__main__':
	# part_one()
	part_two()