import copy
import math
import matplotlib.pyplot as plt
import numpy as np
import re
import scipy.signal as sig

def get_data(path):
	with open(path) as file:
		data = [piece.split("\n") for piece in file.read().split("\n\n")]

	return data

"""
Part 1
"""
class JigsawPiece:

	def __init__(self, *args):
		if len(args) == 1 and isinstance(args[0], list):
			entry = args[0]
			id_ = int(re.findall(r"[0-9]+", entry[0])[0])
			dots = JigsawPiece.string_to_matrix(entry[1:]) 

		elif len(args) == 2:
			id_ = args[0]
			dots = args[1]

		self.id = id_
		self.dots = dots
		self.set_edges()

	def __str__(self):
		string = "Tile: %d\n" % self.id
		for row in self.dots:
			string += "%s\n" % row

		return string

	def set_edges(self):
		top = self.dots[0]
		right = np.array([row[-1] for row in self.dots])
		bottom = self.dots[-1]
		left = np.array([row[0] for row in self.dots])

		self.edges = {"T": top, "R": right, "B": bottom, "L": left}
		

	@staticmethod
	def string_to_matrix(string):
		width = len(string[0])
		height = len(string)

		matrix = np.zeros((height, width), dtype=bool)
		for i, row in enumerate(string):
			for j, char in enumerate(row):
				matrix[i, j] = 1 if char == "#" else 0

		return matrix

def arrange_remaining_pieces(arranged_pieces, unarranged_pieces):
	pass

def has_matching_edge(id_, edge, pieces):
	for compare_piece in pieces:
		if id_ == compare_piece.id:
			continue
				
		for compare_edge_key in compare_piece.edges:
			compare_edge = compare_piece.edges[compare_edge_key]
			compare_edge_reverse = compare_edge[::-1]

			if (edge == compare_edge).all():
				return True

			elif (edge == compare_edge_reverse).all():
				return True

	return False

def part_one():
	data = get_data("input.txt")
	
	# Parse all pieces
	pieces = list()
	for entry in data:
		piece = JigsawPiece(entry)
		pieces.append(piece)

	# Find corner pieces
	corner_pieces = list()
	for piece in pieces:

		num_matching_edges = 0
		for edge_key in piece.edges:
			if has_matching_edge(piece.id, piece.edges[edge_key], pieces):
				num_matching_edges += 1

		if num_matching_edges == 2:
			print("Piece #%d is a corner piece" % piece.id)
			corner_pieces.append(piece)

	piece_id_product = np.prod([float(piece.id) for piece in corner_pieces])
	print("Piece ID product is: %d" % piece_id_product)
	
"""
Part 2
"""
class Jigsaw:

	def __init__(self, num_pieces_per_edge, pixels_per_pieces):
		
		self.pieces = [[None for _ in range(num_pieces_per_edge)] for _ in range(num_pieces_per_edge)]
		self.used_ids = list()
		
		self.num_rows = num_pieces_per_edge
		self.num_cols = num_pieces_per_edge

		self.piece_dim = pixels_per_pieces
		self.num_pieces_per_edge = num_pieces_per_edge
		matrix_dim = self.num_pieces_per_edge * self.piece_dim
		self.matrix = np.zeros((matrix_dim, matrix_dim))

	def __str__(self):
		string = ""
		for row in self.pieces:
			for piece in row:
				if piece is None:
					string += "None "

				else:
					string += "%d " % piece.id

			string += "\n"

		return string

	def to_image(self):
		piece_dim = self.piece_dim - 2
		matrix_dim = self.num_pieces_per_edge * piece_dim
		matrix = np.zeros((matrix_dim, matrix_dim))

		for row in range(self.num_pieces_per_edge):
			for col in range(self.num_pieces_per_edge):

				startX = col * piece_dim
				endX = startX + piece_dim
				startY = row * piece_dim
				endY =  startY + piece_dim
				matrix[startY:endY, startX:endX] = self.pieces[row][col].dots[1:-1, 1:-1]

		return matrix


	def add_piece(self, piece, coords):
		
		(row, col) = coords
		self.pieces[row][col] = piece
		self.used_ids.append(piece.id)

		startX = col * self.piece_dim
		endX = startX + self.piece_dim
		startY = row * self.piece_dim
		endY =  startY + self.piece_dim
		self.matrix[startY:endY, startX:endX] = piece.dots

	def get_last_piece_coords(self):
		coords = None

		for row in range(self.num_rows):
			for col in range(self.num_cols):
				if self.pieces[row][col] is None:
					return coords, (row, col)

				coords = (row, col)

		return coords, coords


def complete_jigsaw(jigsaw, pieces):
	""" Recursive function used to complete jigsaw

	If multiple matches are found for a single spot, all of them are tried. Returns
	None if no matches are found before the jigsaw is complete 
	"""
	# Get ind for next piece
	(row, col), new_coords = jigsaw.get_last_piece_coords()

	# Same or new row for next piece?
	if col < jigsaw.num_cols - 1:
		matches = find_match(jigsaw, (row, col), pieces, "R")

	else:
		matches = find_match(jigsaw, (row, 0), pieces, "B")

	# Break recursion if not matches are found before reaching the end
	if not matches:
		if row == jigsaw.num_rows - 1 and col == jigsaw.num_cols - 1:
			return jigsaw

		else:
			print("No matches found!")
			return None

	# Continue with one (or more) matches
	copy_needed = len(matches) > 1
	for new_piece in matches:
		if copy_needed:
			new_jigsaw = copy.deepcopy(jigsaw)

		else:
			new_jigsaw = jigsaw

		# Rotate and flip (transform) piece if needed and add to jigsaw
		new_jigsaw.add_piece(new_piece, new_coords)
		jigsaw = complete_jigsaw(new_jigsaw, pieces)
		if jigsaw is not None:
			return jigsaw

def find_match(jigsaw, coords, pieces, direction):
	(row, col) = coords
	edge = jigsaw.pieces[row][col].edges[direction]

	matches = list()
	for candidate_piece in pieces:
		if candidate_piece.id in jigsaw.used_ids:
			continue

		for candidate_direction, candidate_edge in candidate_piece.edges.items():
			if (edge == candidate_edge).all():
				transform = get_transform(direction, candidate_direction)
				new_piece = transform_piece(candidate_piece, transform)
				matches.append(new_piece)

			elif (edge == candidate_edge[::-1]).all():
				transform = get_transform(direction, candidate_direction, reversed_=True)
				new_piece = transform_piece(candidate_piece, transform)
				matches.append(new_piece)

	return matches

def get_corner_rotations(matching_edges):
	"""
	
	Get number of CW 90 deg rotations to get matching edges of
	top-left corner piece to face "inwards" (i.e. left and bottom)
	"""
	if "T" in matching_edges:
		if "R" in matching_edges:
			return 1

		elif "L" in matching_edges:
			return 2

	elif "B" in matching_edges:
		if "R" in matching_edges:
			return 0

		elif "L" in matching_edges:
			return 3

def get_transform(edge_direction, new_edge_direction, reversed_=False):
	# Number of CW 90 deg turns needed
	ROTATIONS = {"T": 3, "R": 2, "B": 1, "L": 0} 
	
	if edge_direction == "R":
		rotations = ROTATIONS[new_edge_direction]
		flip = reversed_ != (new_edge_direction in ["R", "T"]) 
		flip = 0 if flip else None

	elif edge_direction == "B":
		rotations = (ROTATIONS[new_edge_direction] + 1) % 4
		flip = reversed_ != (new_edge_direction in ["B", "L"])
		flip = 1 if flip else None  

	return (rotations, flip)

def transform_piece(piece, transform):
	
	id_ = piece.id
	dots = piece.dots

	(rotations, flip) = transform
	dots = np.rot90(dots, k=-rotations)	# Rotate CW == -rotations
	if flip is not None:
		dots = np.flip(dots, axis=flip)

	new_piece = JigsawPiece(id_, dots)
	return new_piece

def find_sea_monster_orientation(sea_monster_image, sea_monster_pattern):

	match_max = np.sum(sea_monster_pattern)

	for flip in range(2):
		if flip == 1:
			sea_monster_image = np.flip(sea_monster_image, axis=0)
		
		for rotate in range(4):
			match = sig.correlate2d(sea_monster_image, sea_monster_pattern, mode="same")

			if match.max() == match_max:
				return sea_monster_image, match

			sea_monster_image = np.rot90(sea_monster_image, k=1)

def create_sea_monster_overlay(sea_monster_pattern, dim, index):
	overlay = np.zeros(dim)

	for i in range(len(index[0])):
		startX = index[1][i] - 9
		endX = startX + 20
		startY = index[0][i] - 1
		endY = startY + 3
		overlay[startY:endY, startX:endX] += sea_monster_pattern

	return overlay

def part_two():
	data = get_data("input.txt")
	
	# Parse all pieces
	pieces = list()
	for entry in data:
		piece = JigsawPiece(entry)
		pieces.append(piece)

	# Create jigsaw
	num_pieces = len(pieces)
	num_pieces_per_edge = int(math.sqrt(num_pieces))
	pixels_per_pieces = pieces[0].dots.shape[0]
	jigsaw = Jigsaw(num_pieces_per_edge, pixels_per_pieces)
	
	# Find corner piece to start with
	for piece in pieces:

		matching_edges = []
		for direction, edge in piece.edges.items():
			if has_matching_edge(piece.id, edge, pieces):
				matching_edges.append(direction)

		if len(matching_edges) == 2:
			corner_piece = piece
			break

	# Flip and/or rotate corner piece if needed
	rotations = get_corner_rotations(matching_edges)
	corner_piece = transform_piece(corner_piece, (rotations, None))
	jigsaw.add_piece(corner_piece, (0, 0))

	# Complete jigsaw
	completed_jigsaw = complete_jigsaw(jigsaw, pieces)

	# Find sea monsters
	sea_monster_pattern = JigsawPiece.string_to_matrix(open("seaMonster.txt").read().split("\n"))
	sea_monster_image = completed_jigsaw.to_image()
	
	sea_monster_image, match = find_sea_monster_orientation(sea_monster_image, sea_monster_pattern)
	index = np.where(match == np.sum(sea_monster_pattern))
	sea_monster_overlay = create_sea_monster_overlay(sea_monster_pattern, sea_monster_image.shape, index)
	sea_roughness = np.count_nonzero((sea_monster_image + sea_monster_overlay) == 1)

	print(index)
	print(sea_roughness)

	plt.subplot(221)
	plt.imshow(sea_monster_pattern)
	plt.subplot(222)
	plt.imshow(sea_monster_overlay)
	plt.subplot(223)
	plt.imshow(sea_monster_image)
	plt.subplot(224)
	plt.imshow(sea_monster_image + sea_monster_overlay)

	plt.show()

"""
Main
"""
if __name__ == '__main__':
	#part_one()
	part_two()