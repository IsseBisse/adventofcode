from itertools import permutations


def get_data(path: str) -> list[str]:
    with open(path) as file:
        data = file.read().split("\n")

    return data


def sub(first: tuple[int], second: tuple[int]) -> tuple[int]:
    return tuple(f - s for f, s in zip(first, second))


def add(first: tuple[int], second: tuple[int]) -> tuple[int]:
    return tuple(f + s for f, s in zip(first, second))


def is_inside(node: tuple[int], dim: tuple[int]) -> bool:
    if any(val < 0 for val in node):
        return False

    if any(node_val >= dim_val for node_val, dim_val in zip(node, dim)):
        return False

    return True


def calculate_antinodes(nodes: set[tuple[int]], dim: tuple[int]) -> None:
    node_permutations = permutations(nodes, 2)

    antinodes = set()
    for first, second in node_permutations:
        diff = sub(second, first)

        new_node = add(second, diff)
        if is_inside(new_node, dim):
            antinodes.add(new_node)

        new_node = sub(first, diff)
        if is_inside(new_node, dim):
            antinodes.add(new_node)

    return antinodes


def parse(rows: list[str]) -> dict[str, list[tuple[int]]]:
    antennas = dict()

    for y, row in enumerate(rows):
        for x, char in enumerate(row):
            if char == ".":
                continue

            if char in antennas:
                antennas[char].add((x, y))

            else:
                antennas[char] = {(x, y)}

    return antennas


def part_one():
    rows = get_data("8/input.txt")

    dim = (len(rows[0]), len(rows))
    nodes = parse(rows)
    antinodes = {name: calculate_antinodes(node, dim) for name, node in nodes.items()}

    all_antinodes = set.union(*antinodes.values())
    print(len(all_antinodes))


def calculate_repeating_antinodes(nodes: set[tuple[int]], dim: tuple[int]) -> None:
    node_permutations = permutations(nodes, 2)

    antinodes = set()
    for first, second in node_permutations:
        diff = sub(second, first)

        new_node = add(second, diff)
        while is_inside(new_node, dim):
            antinodes.add(new_node)
            new_node = add(new_node, diff)

        new_node = sub(first, diff)
        while is_inside(new_node, dim):
            antinodes.add(new_node)
            new_node = sub(new_node, diff)

    return antinodes


def pretty_print(rows: list[str], all_antinodes: set[tuple[int]]):
    for y, row in enumerate(rows):
        for x, char in enumerate(row):
            if char != ".":
                print(char, end="")

            elif (x, y) in all_antinodes:
                print("X", end="")

            else:
                print(".", end="")

        print("")


def part_two():
    rows = get_data("8/input.txt")

    dim = (len(rows[0]), len(rows))
    nodes = parse(rows)
    antinodes = {
        name: calculate_repeating_antinodes(node, dim) for name, node in nodes.items()
    }

    all_antinodes = set.union(*antinodes.values()).union(*nodes.values())
    pretty_print(rows, all_antinodes)
    print(len(all_antinodes))


if __name__ == "__main__":
    part_one()
    part_two()
