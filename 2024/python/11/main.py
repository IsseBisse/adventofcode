from collections import Counter, defaultdict


def get_data(path: str) -> list[str]:
    with open(path) as file:
        data = file.read().split("\n")

    return data


def split(num: int) -> list[int]:
    string = str(num)
    half_idx = len(string) // 2
    return [int(string[:half_idx]), int(string[half_idx:])]


def process(stone: int) -> list[int]:
    if stone == 0:
        return [1]

    elif len(str(stone)) % 2 == 0:
        return split(stone)

    else:
        return [stone * 2024]


def part_one():
    data = get_data("11/input.txt")
    stones = [int(num) for num in data[0].split(" ")]

    num_laps = 25
    for _ in range(num_laps):
        stones = [new_stone for stone in stones for new_stone in process(stone)]

    print(len(stones))


def part_two():
    data = get_data("11/input.txt")
    stones = [int(num) for num in data[0].split(" ")]
    stones = Counter(stones)

    num_laps = 75
    # Wow this is UGLY!
    for _ in range(num_laps):
        new_stones = defaultdict(lambda: 0)

        for key, count in stones.items():
            new_keys = process(key)

            for new_key in new_keys:
                new_stones[new_key] += count

        stones = new_stones

    print(sum(stones.values()))


if __name__ == "__main__":
    part_one()
    part_two()
