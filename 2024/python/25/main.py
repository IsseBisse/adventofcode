def parse(block: str) -> tuple[tuple[int], bool]:
    rows = block.split("\n")
    is_lock = all(char == "#" for char in rows[0])

    heights = list()
    for idx in range(5):
        heights.append(len([1 for row in rows if row[idx] == "#"])-1)

    return heights, is_lock


def get_data(path):
    with open(path) as file:
        blocks = file.read().split("\n\n")

    locks = list()
    keys = list()
    for block in blocks:
        heights, is_lock = parse(block)

        if is_lock:
            locks.append(heights)

        else:
            keys.append(heights)

    return locks, keys


def overlap(lock: list[int], key: list[int]) -> bool:
    return any((l_col + k_col) > 6 for l_col, k_col in zip(lock, key))


def part_one():
    locks, keys = get_data("25/input.txt")
    
    non_overlap = 0
    for lock in locks:
        for key in keys:
            if not overlap(lock, key):
                non_overlap += 1

    print(non_overlap)


def part_two():
    _ = get_data("25/smallInput.txt")


if __name__ == "__main__":
    part_one()
    part_two()
