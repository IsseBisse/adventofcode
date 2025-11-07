from collections import defaultdict
from heapq import heappush, heappop


def get_data(path):
    with open(path) as file:
        data = file.read().split("\n")

    is_blocked = set()
    for y, row in enumerate(data):
        for x, char in enumerate(row):
            if char == "#":
                is_blocked.add((x, y))

            elif char == "S":
                start = (x, y, 1)

            elif char == "E":
                end = (x, y)

    return is_blocked, start, end


def manhattan(end: tuple[int]):
    def manhattan_to(start: tuple[int]):
        return sum(abs(first - second) for first, second in zip(start, end))

    return manhattan_to


def neighbor_getter(is_blocked: set[tuple[int]]):
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    def add_direction(coord: tuple[int], dir_idx: int) -> tuple[int]:
        dir_x, dir_y = directions[dir_idx]
        x, y = coord
        return (x + dir_x, y + dir_y, dir_idx)

    def is_valid_coord(coord: tuple[int]):
        return coord not in is_blocked

    def get_neighbors(current: tuple[int]) -> list[tuple[int]]:
        *coord, dir_idx = current
        neighbors = [
            (1001, add_direction(coord, (dir_idx - 1) % 4)),
            (1, add_direction(coord, dir_idx)),
            (1001, add_direction(coord, (dir_idx + 1) % 4)),
        ]

        return list(filter(lambda item: is_valid_coord(item[1][:2]), neighbors))

    return get_neighbors


def path_reconstructor(start: tuple[int]):
    def reconstruct_path(
        came_from: dict[tuple[int], tuple[int]], current: tuple[int]
    ) -> list[tuple[int]]:
        path = [current]
        while current != start:
            current = came_from[current]
            path.append(current)

        path.reverse()
        return path

    return reconstruct_path


def dijkstra(
    is_blocked: set[tuple[int]], start: tuple[int], end: tuple[int]
) -> list[tuple[int]]:
    # h = manhattan(end)
    h = lambda end: 0
    path_rec = path_reconstructor(start)
    get_neighbors = neighbor_getter(is_blocked)

    g_score = defaultdict(lambda: int(1e9))
    g_score[start] = 0

    f_score = defaultdict(lambda: int(1e9))
    f_score[start] = h(start)

    open_set = [(f_score[start], start)]
    came_from = dict()

    while len(open_set) > 0:
        _, current = heappop(open_set)
        if current[:2] == end:
            return path_rec(came_from, current), g_score[current]

        for increased_cost, neighbor in get_neighbors(current):
            tentative_g_score = g_score[current] + increased_cost

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + h(neighbor)

                if (f_score[neighbor], neighbor) not in open_set:
                    heappush(open_set, (f_score[neighbor], neighbor))


def part_one():
    is_blocked, start, end = get_data("16/input.txt")
    _, cost = dijkstra(is_blocked, start, end)
    print(cost)


def part_two():
    is_blocked, start, end = get_data("16/smallInput.txt")
    shortest_path, _ = dijkstra(is_blocked, start, end)
    print(len(shortest_path))


if __name__ == "__main__":
    # part_one()
    part_two()
