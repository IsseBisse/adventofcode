def get_data(path):
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


def get_shortest_paths(keypad):
    paths = dict()

    for start_coord, start in keypad.items():
        paths_from_start = dict()

        for end_coord, end in keypad.items():
            x_diff, y_diff = tuple(b - a for a, b in zip(start_coord, end_coord))

            path = ""
            y_char = "^" if y_diff < 0 else "v"
            if x_diff < 0:
                # Move up/down first
                path += y_char * abs(y_diff)
                path += "<" * abs(x_diff)

            else:
                # Move right/left first
                path += ">" * abs(x_diff)
                path += y_char * abs(y_diff)

            paths_from_start[end] = path

        paths[start] = paths_from_start

    return paths


def get_code_path(code, paths, initial="A"):
    path = ""
    prev = initial
    for char in code:
        path += paths[prev][char]
        path += "A"

        prev = char

    return path


def get_all_code_paths(code, paths):
    code_paths = [get_code_path(code, paths[0])]
    for _ in range(2):
        code_paths.append(get_code_path(code_paths[-1], paths[1]))

    return code_paths


# def invert_code(code, path_map):
#     parts = code.split("A")[:-1]
#     invert_path_map = {start: {path: end for end, path in start_map.items()} for start, start_map in path_map.items()}

#     prev = "A"
#     inverted_code = ""
#     for part in parts:
#         current = invert_path_map[prev][part]
#         inverted_code += current
#         prev = current

#     return inverted_code


def complexity(code, path):
    return int(code[:-1]) * len(path)


def part_one():
    codes = get_data("21/smallInput.txt")
    paths = [get_shortest_paths(keypad) for keypad in KEYPADS]
    code_paths = [get_all_code_paths(code, paths) for code in codes]
    complexities = [complexity(code, path[2]) for code, path in zip(codes, code_paths)]

    # invert_code(code_paths[0][0], paths[0])

    # third_part = "v<<A>>^AvA^Av<A<AA>>^AAvA^<A>AAvA^Av<A>^AA<A>Av<<A>A>^AAAvA^<A>A"
    # second_part = invert_code(third_part, paths[1])
    # first_part = invert_code(second_part, paths[1])
    # code = invert_code(first_part, paths[0])

    print(sum(complexities))


def part_two():
    _ = get_data("21/smallInput.txt")


if __name__ == "__main__":
    part_one()
    part_two()
