from collections import defaultdict
from tqdm import tqdm


def get_data(path: str):
    with open(path) as file:
        data = file.read().split("\n")

    dim = (len(data[0]), len(data))
    is_blocked = set()
    for y, row in enumerate(data):
        for x, char in enumerate(row):
            if char == "#":
                is_blocked.add((x, y))

            elif char == "S":
                start = (x, y)

            elif char == "E":
                end = (x, y)

    return start, end, is_blocked, dim


def add(first, second):
    return tuple(f + s for f, s in zip(first, second))


def is_inside(coord, dim):
    return all(0 <= axis < axis_max for axis, axis_max in zip(coord, dim))


def get_adjacent(coord, dim, is_blocked=None):
    DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))
    candidates = [add(coord, direction) for direction in DIRECTIONS]
    inside_candidates = [coord for coord in candidates if is_inside(coord, dim)]

    if is_blocked is not None:
        non_blocked_candidates = [
            coord for coord in inside_candidates if coord not in is_blocked
        ]
        return non_blocked_candidates

    return inside_candidates


def get_unblocked_path(start, end, dim, is_blocked):
    prev = end
    current = start
    cost = 0

    path = {current: cost}
    while current != end:
        candidates = [
            cand for cand in get_adjacent(current, dim, is_blocked) if cand != prev
        ]
        prev = current
        current = candidates[0]

        cost += 1
        path[current] = cost

    return path


def get_cheat_paths(path, dim):
    cheats = defaultdict(lambda: 0)

    for coord, cost in path.items():
        candidates = set(
            [(1, cand) for cand in get_adjacent(coord, dim)]
            + [
                (2, candcand)
                for cand in get_adjacent(coord, dim)
                for candcand in get_adjacent(cand, dim)
            ]
        )

        for extra_cost, cand in candidates:
            if cand in path and cost + extra_cost < path[cand]:
                diff = path[cand] - (cost + extra_cost)
                cheats[diff] += 1

    return cheats


def part_one():
    start, end, is_blocked, dim = get_data("20/input.txt")
    path = get_unblocked_path(start, end, dim, is_blocked)
    cheats = get_cheat_paths(path, dim)

    limit = 100
    num_great_cheats = sum(
        amount for time_saved, amount in cheats.items() if time_saved >= limit
    )

    print(num_great_cheats)


def get_candidates(coord, dim):
    candidates = list()
    c_x, c_y = coord

    for x in range(-21, 21):
        for y in range(-21, 21):
            new_x = c_x + x
            new_y = c_y + y
            if new_x < 0 or new_x >= dim[0] or new_y < 0 or new_y >= dim[1]:
                continue

            cost = abs(x) + abs(y)
            if cost > 20:
                continue

            candidates.append(((c_x + x, c_y + y), cost))

    return candidates


def get_cheat_paths_two(path, dim):
    cheats = defaultdict(lambda: 0)

    for coord, cost in tqdm(path.items()):
        for cand, extra_cost in get_candidates(coord, dim):
            if cand in path and cost + extra_cost < path[cand]:
                diff = path[cand] - (cost + extra_cost)
                cheats[diff] += 1

    return cheats


def part_two():
    start, end, is_blocked, dim = get_data("20/input.txt")
    path = get_unblocked_path(start, end, dim, is_blocked)
    cheats = get_cheat_paths_two(path, dim)

    limit = 100
    num_great_cheats = sum(
        amount for time_saved, amount in cheats.items() if time_saved >= limit
    )

    print(num_great_cheats)


if __name__ == "__main__":
    # part_one()
    part_two()
