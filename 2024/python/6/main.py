from itertools import cycle
from multiprocessing import Pool


def get_data(path: str) -> list[str]:
    with open(path) as file:
        data = file.read().split("\n")

    return data


def parse(rows: list[str]) -> tuple[list[list[bool]], tuple[int]]:
    block_map = list()

    for y, row in enumerate(rows):
        block_row = list()
        for x, char in enumerate(row):
            if char == "^":
                start_coord = (x, y)

            if char == "#":
                block_row.append(True)
            else:
                block_row.append(False)

        block_map.append(block_row)

    return block_map, start_coord


def is_inside(block_map: list[list[bool]], coord: tuple[int]) -> bool:
    if any(dim < 0 for dim in coord):
        return False

    return coord[0] < len(block_map[0]) and coord[1] < len(block_map)


def is_blocked(block_map: list[list[bool]], coord: tuple[int]) -> bool:
    if not is_inside(block_map, coord):
        return False

    return block_map[coord[1]][coord[0]]


def add(first: tuple[int], second: tuple[int]) -> tuple[int]:
    return tuple(a + b for a, b in zip(first, second))


def get_visited_coords(
    block_map: list[list[bool]], coord: tuple[int]
) -> set[tuple[int]]:
    directions = cycle([(0, -1), (1, 0), (0, 1), (-1, 0)])
    direction = next(directions)
    visited_coords = {coord}
    while is_inside(block_map, coord):
        new_coord = add(coord, direction)

        if is_blocked(block_map, new_coord):
            direction = next(directions)

        else:
            coord = new_coord

            if is_inside(block_map, coord):
                visited_coords.add(coord)

    return visited_coords


def part_one():
    rows = get_data("6/input.txt")
    block_map, coord = parse(rows)
    visited_coords = get_visited_coords(block_map, coord)
    print(len(visited_coords) - 1)


def add_obstruction(
    blocked_map: list[list[bool]], coord: tuple[int]
) -> list[list[bool]]:
    map_copy = [[val for val in row] for row in blocked_map]
    map_copy[coord[1]][coord[0]] = True
    return map_copy


def infinite_loop_checker(start_coord: tuple[int]):
    def has_infinite_loop(block_map: list[list[bool]]) -> bool:
        coord = start_coord
        directions = cycle([(0, -1), (1, 0), (0, 1), (-1, 0)])
        direction = next(directions)
        visited_states = {(coord, direction)}

        while is_inside(block_map, coord):
            new_coord = add(coord, direction)

            if (new_coord, direction) in visited_states:
                return True

            if is_blocked(block_map, new_coord):
                direction = next(directions)

            else:
                coord = new_coord

                if is_inside(block_map, coord):
                    visited_states.add((coord, direction))

        return False

    return has_infinite_loop


def part_two():
    rows = get_data("6/input.txt")
    block_map, coord = parse(rows)
    visited_coords = get_visited_coords(block_map, coord)

    new_block_maps = [add_obstruction(block_map, coord) for coord in visited_coords]
    loop_checker = infinite_loop_checker(coord)

    with Pool as pool:
        has_loop = pool.map(loop_checker, new_block_maps)

    num_infinite_loops = len(loop for loop in has_loop if loop)
    # infinite_loop_maps = filter(loop_checker, new_block_maps)
    print(len(list(num_infinite_loops)))


if __name__ == "__main__":
    # part_one()
    part_two()
