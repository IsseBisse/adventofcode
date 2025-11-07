def get_data(path: str) -> list[str]:
    with open(path) as file:
        data = file.read().split("\n")

    return data


DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def get_adjacent(position: tuple[int], trail_map: list[int]) -> list[tuple[int]]:
    candidates = [(position[0] + x, position[1] + y) for x, y in DIRECTIONS]
    adjacent = [
        cand
        for cand in candidates
        if (
            cand[0] >= 0
            and cand[1] >= 0
            and cand[0] < len(trail_map[0])
            and cand[1] < len(trail_map[1])
        )
    ]
    return adjacent


def get_reachable_peaks(
    position: tuple[int], trail_map: list[list[int]]
) -> set[tuple[int]]:
    x, y = position
    height = trail_map[y][x]
    if height == 9:
        return {position}

    peaks = set()
    for adj_x, adj_y in get_adjacent(position, trail_map):
        if trail_map[adj_y][adj_x] == height + 1:
            peaks = peaks.union(get_reachable_peaks((adj_x, adj_y), trail_map))

    return peaks


def part_one():
    rows = get_data("10/input.txt")
    trail_map = [[int(char) for char in row] for row in rows]

    starting_positions = list()
    for y, row in enumerate(trail_map):
        for x, height in enumerate(row):
            if height == 0:
                starting_positions.append((x, y))

    num_reachable_peaks = [
        len(get_reachable_peaks(position, trail_map)) for position in starting_positions
    ]
    print(sum(num_reachable_peaks))


def get_available_paths(
    position: tuple[int], trail_map: list[list[int]], path: list[tuple[int]] | None
) -> list[list[tuple[int]]]:
    if path is None:
        path = list()

    # Copy
    new_path = [prev_position for prev_position in path]
    new_path.append(position)

    x, y = position
    height = trail_map[y][x]
    if height == 9:
        return [new_path]

    paths = list()
    for adj_x, adj_y in get_adjacent(position, trail_map):
        if trail_map[adj_y][adj_x] == height + 1:
            paths += get_available_paths((adj_x, adj_y), trail_map, new_path)

    return paths


def part_two():
    rows = get_data("10/input.txt")
    trail_map = [[int(char) if char != "." else -1 for char in row] for row in rows]

    starting_positions = list()
    for y, row in enumerate(trail_map):
        for x, height in enumerate(row):
            if height == 0:
                starting_positions.append((x, y))

    num_available_paths = [
        len(get_available_paths(position, trail_map, None))
        for position in starting_positions
    ]
    print(sum(num_available_paths))


if __name__ == "__main__":
    part_one()
    part_two()
