from collections import defaultdict
from heapq import heappush, heappop
from tqdm import tqdm


def get_data(path: str, num_bytes) -> set[tuple[int]]:
    with open(path) as file:
        data = file.read().split("\n")

    is_blocked = {tuple(int(num) for num in row.split(",")) for row in data[:num_bytes]}

    return is_blocked


def manhattan(end: tuple[int]):
    def manhattan_to(start: tuple[int]):
        return sum(abs(first - second) for first, second in zip(start, end))

    return manhattan_to


def neighbor_getter(is_blocked: set[tuple[int]]):
    def is_valid_coord(coord: tuple):
        return all(0 <= axis <= GRID_SIZE for axis in coord) and coord not in is_blocked

    def get_neighbors(current: tuple[int]) -> list[tuple[int]]:
        x, y = current
        neighbors = [(x + offset, y) for offset in [-1, 1]] + [
            (x, y + offset) for offset in [-1, 1]
        ]
        return list(filter(is_valid_coord, neighbors))

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
    h = manhattan(end)
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
        if current == end:
            return path_rec(came_from, current)

        for neighbor in get_neighbors(current):
            tentative_g_score = g_score[current] + 1

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + h(neighbor)

                if (f_score[neighbor], neighbor) not in open_set:
                    heappush(open_set, (f_score[neighbor], neighbor))


GRID_SIZE = 70


def part_one():
    is_blocked = get_data("18/input.txt", 1024)
    shortest_path = dijkstra(is_blocked, (0, 0), (GRID_SIZE, GRID_SIZE))
    print(len(shortest_path) - 1)


def get_data_two(path: str) -> set[tuple[int]]:
    with open(path) as file:
        data = file.read().split("\n")

    data = [tuple(int(num) for num in row.split(",")) for row in data]

    return data


def part_two():
    shortest_path = None
    path = "18/input.txt"

    corrupted_bytes = get_data_two(path)
    is_blocked = set()

    for byte in tqdm(corrupted_bytes):
        is_blocked.add(byte)
        if shortest_path is not None and byte not in shortest_path:
            continue

        shortest_path = dijkstra(is_blocked, (0, 0), (GRID_SIZE, GRID_SIZE))

        if shortest_path is None:
            break

    print(byte)


if __name__ == "__main__":
    # part_one()
    part_two()
