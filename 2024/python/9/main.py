from dataclasses import dataclass


def get_data(path: str) -> str:
    with open(path) as file:
        data = file.read()

    return data


def parse(data: str) -> list[int | None]:
    file_system = list()
    is_file = True
    file_id = 0

    for char in data:
        if is_file:
            append_num = file_id
            file_id += 1

        else:
            append_num = None

        is_file = not is_file

        for _ in range(int(char)):
            file_system.append(append_num)

    return file_system


def pack(file_system: list[int | None]) -> list[int]:
    next_empty = 0
    current = len(file_system) - 1

    while next_empty < current:
        while file_system[next_empty] is not None:
            next_empty += 1

        while file_system[current] is None:
            current -= 1

        file_system[next_empty] = file_system[current]
        file_system[current] = None

    return [num for num in file_system if num is not None]


def checksum(file_system: list[int]) -> int:
    return sum(idx * val for idx, val in enumerate(file_system))


def part_one():
    data = get_data("9/smallInput.txt")
    file_system = parse(data)
    packed_file_system = pack(file_system)
    print(packed_file_system)
    # print(checksum(packed_file_system))


@dataclass
class Block:
    id: int
    size: int


def parse_two(data: str) -> list[Block]:
    file_system = list()
    file_id = 0
    is_file = True

    for char in data:
        if is_file:
            file_system.append(Block(file_id, int(char)))
            file_id += 1

        else:
            file_system.append(Block(None, int(char)))

        is_file = not is_file

    return file_system


def find_next_empty(file_system: list[Block], size: int, stop_idx: int) -> int | None:
    for idx, block in enumerate(file_system[:stop_idx]):
        if block.id is None and block.size >= size:
            return idx, block.size

    return None, None


def to_string(file_system: list[Block]) -> str:
    string = ""
    for block in file_system:
        char = "." if block.id is None else str(block.id)
        string += "".join(char for _ in range(block.size))

    return string


def pack_two(file_system: list[Block]):
    idx = len(file_system) - 1
    while idx >= 0:
        block = file_system[idx]
        if block.id is None:
            idx -= 1
            continue

        swap_idx, swap_size = find_next_empty(file_system, block.size, idx)
        if swap_idx is None:
            idx -= 1
            continue

        file_system[swap_idx] = block
        file_system[idx] = Block(None, block.size)
        if swap_size > block.size:
            file_system.insert(swap_idx + 1, Block(None, swap_size - block.size))
            idx += 1

        idx -= 1

    return file_system


def checksum_two(file_system: list[Block]) -> int:
    checksum = 0
    block_position = 0
    for block in file_system:
        for _ in range(block.size):
            value = block.id if block.id is not None else 0
            checksum += block_position * value
            block_position += 1

    return checksum


def part_two():
    data = get_data("9/input.txt")
    file_system = parse_two(data)
    packed_file_system = pack_two(file_system)
    print(checksum_two(packed_file_system))


if __name__ == "__main__":
    # part_one()
    part_two()
