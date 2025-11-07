from collections import defaultdict
from itertools import permutations
from tqdm import tqdm


def get_data(path: str) -> list[str]:
    with open(path) as file:
        data = file.read().split("\n")

    return data


def find_interconnected(
    first: str, network: dict[str, list[str]]
) -> list[list[str]] | list:
    connected_computers = network[first]

    if len(connected_computers) < 2:
        return list()

    connected_groups = permutations(connected_computers, 2)

    interconnected = list()
    for second, third in connected_groups:
        if second in network[third] or third in network[second]:
            interconnected.append((first, second, third))

    return interconnected


def is_possible_historian_group(group: tuple[str]):
    return any(computer[0] == "t" for computer in group)


def get_network(connections: list[str]) -> defaultdict[str, list[str]]:
    network = defaultdict(lambda: list())

    for conn in connections:
        source, target = conn.split("-")
        network[source].append(target)
        network[target].append(source)

    return network


def part_one():
    connections = get_data("23/input.txt")
    network = get_network(connections)

    three_groups = list()
    for computer in network:
        three_groups += find_interconnected(computer, network)

    sorted_unique_groups = {tuple(sorted(group)) for group in three_groups}
    possible_historian_groups = [
        group for group in sorted_unique_groups if is_possible_historian_group(group)
    ]

    print(len(possible_historian_groups))


def find_group(
    computer: str, network: dict[str, list[str]], group_size: int
) -> tuple[str] | None:
    connected_computers = network[computer]

    if len(connected_computers) < group_size:
        return None

    possible_groups = permutations(connected_computers, group_size)

    for group in possible_groups:
        pairs = permutations(group, 2)
        if all(
            first in network[second] or second in network[first]
            for first, second in pairs
        ):
            return tuple([computer] + list(group))

    return None


def find_largest_group(
    computer: str, network: defaultdict[str, list[str]], largest_group_size: int
) -> tuple[str]:
    largest_interconnected = tuple()
    for group_size in range(largest_group_size, len(network[computer])):
        group = find_group(computer, network, group_size)

        if group is None:
            return largest_interconnected

        largest_interconnected = group

    return largest_interconnected


def part_two():
    connections = get_data("23/input.txt")
    network = get_network(connections)

    largest_group = ()
    for computer in tqdm(network):
        largest_current_group = find_largest_group(
            computer, network, max(2, len(largest_group))
        )

        if len(largest_current_group) > len(largest_group):
            largest_group = largest_current_group

    print(",".join(sorted(largest_group)))


if __name__ == "__main__":
    # part_one()
    part_two()
