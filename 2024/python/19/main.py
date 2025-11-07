from tqdm import tqdm
from functools import lru_cache


def get_data(path: str) -> tuple[list[str], list[str]]:
    with open(path) as file:
        towels, designs = file.read().split("\n\n")

    towels = tuple(towel for towel in towels.split(", "))
    designs = list(design for design in designs.split("\n"))

    return towels, designs


@lru_cache
def is_possible(design: str, towels: tuple[str]) -> bool:
    if len(design) == 0:
        return True

    for num_chars in range(1, max(len(towel) for towel in towels) + 1):
        if num_chars > len(design):
            return False

        substr = design[:num_chars]
        if substr in towels:
            possible = is_possible(design[num_chars:], towels)

            if possible:
                return True

    return False


def part_one():
    towels, designs = get_data("19/input.txt")
    for design in tqdm(designs):
        is_possible(design, towels)


@lru_cache
def num_combinations(design: str, towels: tuple[str]) -> int:
    if len(design) == 0:
        return 1

    combinations = 0
    for num_chars in range(1, max(len(towel) for towel in towels) + 1):
        if num_chars > len(design):
            return combinations

        substr = design[:num_chars]
        if substr in towels:
            combinations += num_combinations(design[num_chars:], towels)

    return combinations


def part_two():
    towels, designs = get_data("19/input.txt")
    combinations = [num_combinations(design, towels) for design in tqdm(designs)]
    print(sum(combinations))


if __name__ == "__main__":
    # part_one()
    part_two()
