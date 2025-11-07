from itertools import permutations


def get_data(path: str) -> list[str]:
    with open(path) as file:
        data = file.read().split("\n")

    return data


KEYPADS = [
    {
        (0, 0): "7",
        (1, 0): "8",
        (2, 0): "9",
        (0, 1): "4",
        (1, 1): "5",
        (2, 1): "6",
        (0, 2): "1",
        (1, 2): "2",
        (2, 2): "3",
        (1, 3): "0",
        (2, 3): "A",
    },
    {
        (1, 0): "^",
        (2, 0): "A",
        (0, 1): "<",
        (1, 1): "v",
        (2, 1): ">",
    },
]

DIR_TO_COORD = {"^": (0, -1), "v": (0, 1), ">": (1, 0), "<": (-1, 0)}


def is_allowed(moves: tuple[str], start_coord: tuple[int], keypad: set[tuple[int]]):
    current = start_coord
    for move in moves:
        current = tuple(a + b for a, b in zip(current, DIR_TO_COORD[move]))

        if current not in keypad:
            return False

    return True


def get_moves(keypad):
    moves = dict()

    for start_coord, start in keypad.items():
        moves_from_start = dict()

        for end_coord, end in keypad.items():
            x_diff, y_diff = tuple(b - a for a, b in zip(start_coord, end_coord))

            y_char = "^" if y_diff < 0 else "v"
            x_char = "<" if x_diff < 0 else ">"
            steps = x_char * abs(x_diff) + y_char * abs(y_diff)

            possible_combinations = set(permutations(steps))
            allowed_combinations = [
                move
                for move in possible_combinations
                if is_allowed(move, start_coord, keypad)
            ]

            moves_from_start[end] = allowed_combinations

        moves[start] = moves_from_start

    return moves


def get_shortest_sequence(from_char, to_char, moves, level):
    if level == 1:
        possible_moves = moves[0]

    else:
        possible_moves = moves[1]

    if level == 3:
        return "".join(possible_moves[from_char][to_char][0]) + "A"

    combinations = possible_moves[from_char][to_char]
    shortest_sequence = None
    for c in combinations:
        comb_sequence = ""

        prev = "A"
        for char in c:
            sequence = get_shortest_sequence(prev, char, moves, level + 1)
            comb_sequence += sequence

        if shortest_sequence is None or len(comb_sequence) < len(shortest_sequence):
            shortest_sequence = comb_sequence

    return shortest_sequence + "A"


def get_sequences(code, moves):
    prev = "A"
    shortest_sequence = ""
    for char in code:
        sequence = get_shortest_sequence(prev, char, moves, 1)

        shortest_sequence += sequence
        prev = char

    return shortest_sequence


def complexity(code, path):
    return int(code[:-1]) * len(path)


def part_one():
    codes = get_data("21/smallInput.txt")
    all_moves = [get_moves(keypad) for keypad in KEYPADS]
    code_paths = [get_sequences(code, all_moves) for code in codes]
    complexities = [complexity(code, path) for code, path in zip(codes, code_paths)]

    print(sum(complexities))


def part_two():
    _ = get_data("21/smallInput.txt")


if __name__ == "__main__":
    part_one()
    part_two()
