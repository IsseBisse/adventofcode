from collections import defaultdict
from dataclasses import dataclass, field
from typing import TypeVar

import numpy as np
from scipy.signal import convolve2d


def get_data(path):
    with open(path) as file:
        data = file.read().split("\n")

    return data


Node = TypeVar("Node")


@dataclass
class Node:
    plant: str
    coord: tuple[int]
    adjacent: list[Node | None] = field(default_factory=list)

    def __str__(self):
        return f"{self.plant} {self.coord}"


def get_adjacent_coords(coord: tuple[int]):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    return [tuple(c + d for c, d in zip(coord, direction)) for direction in directions]


@dataclass
class Region:
    nodes: list[Node]
    area: int = field(init=False)
    perimeter: int = field(init=False)

    def __post_init__(self):
        self.area = len(self.nodes)
        self.perimeter = sum(
            len([adj for adj in node.adjacent if adj is None]) for node in self.nodes
        )

    def __str__(self):
        return str([str(node) for node in self.nodes])

    def get_cost(self):
        return self.area * self.perimeter


def get_regions(nodes: defaultdict[tuple[int], Node], dim: tuple[int]) -> list[Region]:
    unvisited_coords = {(x, y) for x in range(dim[0]) for y in range(dim[1])}

    regions = list()
    while len(unvisited_coords) > 0:
        start_coord = unvisited_coords.pop()
        region_coords = {start_coord}
        unvisited_region_coords = set(
            node.coord for node in nodes[start_coord].adjacent if node is not None
        )

        while len(unvisited_region_coords) > 0:
            region_coord = unvisited_region_coords.pop()
            region_coords.add(region_coord)
            unvisited_coords.remove(region_coord)

            new_unvisited_region_coords = set(
                node.coord for node in nodes[region_coord].adjacent if node is not None
            )
            new_unvisited_region_coords = new_unvisited_region_coords.intersection(
                unvisited_coords
            )
            unvisited_region_coords = unvisited_region_coords.union(
                new_unvisited_region_coords
            )

        regions.append(Region([nodes[coord] for coord in region_coords]))

    return regions


def part_one():
    rows = get_data("12/input.txt")

    nodes = defaultdict(lambda: None)
    dim = (len(rows[0]), len(rows))
    for y, row in enumerate(rows):
        for x, char in enumerate(row):
            nodes[(x, y)] = Node(char, (x, y))

    for coord in list(nodes):
        adjacent_nodes = [nodes[adj_coord] for adj_coord in get_adjacent_coords(coord)]
        nodes[coord].adjacent = [
            node if (node is None or node.plant == nodes[coord].plant) else None
            for node in adjacent_nodes
        ]

    regions = get_regions(nodes, dim)

    print(sum(region.get_cost() for region in regions))


corners = [
    np.array(((-1, 1), (1, 1))),
    np.array(((1, -1), (1, 1))),
    np.array(((1, 1), (-1, 1))),
    np.array(((1, 1), (1, -1))),
    np.array(((1, -1), (-1, 0))),
    np.array(((-1, 1), (0, -1))),
    np.array(((-1, 0), (1, -1))),
    np.array(((0, -1), (-1, 1))),
    # np.array(((0, 1), (1, 0))),
    # np.array(((1, 0), (0, 1))),
]


def count_corners(region: np.array) -> int:
    corner_count = 0
    for corner_kernel in corners:
        # print(corner_kernel)
        corner_map = convolve2d(region, corner_kernel / np.sum(corner_kernel == 1))
        # print(corner_map)
        corner_count += np.sum(corner_map == 1)

    return corner_count


def to_array(region: Region, dim: tuple[int]):
    # Add padding
    array = np.zeros((dim[0] + 2, dim[1] + 2))

    for node in region.nodes:
        x, y = node.coord
        # To make it print the right way
        array[y + 1, x + 1] = 1

    return array


def part_two():
    rows = get_data("12/input.txt")

    nodes = defaultdict(lambda: None)
    dim = (len(rows[0]), len(rows))
    for y, row in enumerate(rows):
        for x, char in enumerate(row):
            nodes[(x, y)] = Node(char, (x, y))

    for coord in list(nodes):
        adjacent_nodes = [nodes[adj_coord] for adj_coord in get_adjacent_coords(coord)]
        nodes[coord].adjacent = [
            node if (node is None or node.plant == nodes[coord].plant) else None
            for node in adjacent_nodes
        ]

    regions = get_regions(nodes, dim)

    total_discount_cost = 0
    for region in regions:
        array = to_array(region, dim)
        num_corners = count_corners(array)
        discount_cost = region.area * num_corners
        total_discount_cost += discount_cost

    print(total_discount_cost)


if __name__ == "__main__":
    # part_one()
    part_two()
