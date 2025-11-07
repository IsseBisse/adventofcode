from dataclasses import dataclass
import itertools
import numpy as np
import re
from typing import Tuple

def process_row(row):
    on = row[:2] == "on"

    coords = [int(coord) for coord in re.findall(r"[\-0-9]+", row)]
    coords = [(coords[2*idx], coords[2*idx+1]) for idx in range(3)]
    return on, coords

def get_data(path):
    with open(path) as file:
        data = file.read().split("\n")

    parsed_data = map(process_row, data)

    return list(parsed_data)

@dataclass
class LightCube:
    cube: np.ndarray = np.zeros((101, 101, 101), dtype=bool)
    dim: Tuple[int] = (-50, 50)

    def execute_step(self, step):
        turn_on, coords = step
        value = 1 if turn_on else 0

        cube_coords = list()
        for coord in coords:
            if coord[1] < self.dim[0] or coord[0] > self.dim[1]:
                # Change completely outside cube range
                return
            squeezed_coord = (max(self.dim[0], coord[0]), min(self.dim[1], coord[1]))
            offset_coord = tuple([coord+50 for coord in squeezed_coord])
            cube_coords.append(offset_coord)

        x, y, z = cube_coords
        self.cube[x[0]:x[1]+1, y[0]:y[1]+1, z[0]:z[1]+1] = value

    def count(self):
        return np.sum(self.cube)

def reboot(cube, steps):
    for step in steps:
        cube.execute_step(step)

def part_one():
    reboot_steps = get_data("input.txt")
    cube = LightCube()

    reboot(cube, reboot_steps)
    print(cube.count())


class Rect:
    def size(self):
        return (self.x2-self.x1)*(self.y2-self.y1)

    def to_voxels(self):
        voxels = list()
        for x in range(self.x1, self.x2):
            for y in range(self.y1, self.y2):
                voxels.append((x, y))

        return voxels

    def intersection(self, other):
        a, b = self, other
        x1 = max(min(a.x1, a.x2), min(b.x1, b.x2))
        y1 = max(min(a.y1, a.y2), min(b.y1, b.y2))
        x2 = min(max(a.x1, a.x2), max(b.x1, b.x2))
        y2 = min(max(a.y1, a.y2), max(b.y1, b.y2))
        if x1<x2 and y1<y2:
            return type(self)(x1, y1, x2, y2)
    __and__ = intersection

    def difference(self, other):
        inter = self&other
        if not inter:
            yield self
            return
        xs = {self.x1, self.x2}
        ys = {self.y1, self.y2}
        if self.x1<other.x1<self.x2: xs.add(other.x1)
        if self.x1<other.x2<self.x2: xs.add(other.x2)
        if self.y1<other.y1<self.y2: ys.add(other.y1)
        if self.y1<other.y2<self.y2: ys.add(other.y2)
        for (x1, x2), (y1, y2) in itertools.product(
            pairwise(sorted(xs)), pairwise(sorted(ys))
        ):
            rect = type(self)(x1, y1, x2, y2)
            if rect!=inter:
                yield rect
    __sub__ = difference

    def __init__(self, x1, y1, x2, y2):
        if x1>x2 or y1>y2:
            raise ValueError("Coordinates are invalid")
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

    def __iter__(self):
        yield self.x1
        yield self.y1
        yield self.x2
        yield self.y2

    def __eq__(self, other):
        return isinstance(other, Rect) and tuple(self)==tuple(other)
    def __ne__(self, other):
        return not (self==other)

    def __repr__(self):
        return type(self).__name__+repr(tuple(self))


class Cube:
    def size(self):
        return (self.x2-self.x1)*(self.y2-self.y1)*(self.z2-self.z1)

    def to_voxels(self):
        voxels = list()
        for x in range(self.x1, self.x2):
            for y in range(self.y1, self.y2):
                for z in range(self.z1, self.z2):
                    voxels.append((x, y, z))

        return voxels

    def intersection(self, other):
        a, b = self, other
        x1 = max(min(a.x1, a.x2), min(b.x1, b.x2))
        y1 = max(min(a.y1, a.y2), min(b.y1, b.y2))
        z1 = max(min(a.z1, a.z2), min(b.z1, b.z2))
        x2 = min(max(a.x1, a.x2), max(b.x1, b.x2))
        y2 = min(max(a.y1, a.y2), max(b.y1, b.y2))
        z2 = min(max(a.z1, a.z2), max(b.z1, b.z2))
        if x1<x2 and y1<y2 and z1<z2:
            return type(self)(x1, y1, z1, x2, y2, z2)
    __and__ = intersection

    def difference(self, other):
        inter = self&other
        if not inter:
            yield self
            return
        xs = {self.x1, self.x2}
        ys = {self.y1, self.y2}
        zs = {self.z1, self.z2}
        if self.x1<other.x1<self.x2: xs.add(other.x1)
        if self.x1<other.x2<self.x2: xs.add(other.x2)
        if self.y1<other.y1<self.y2: ys.add(other.y1)
        if self.y1<other.y2<self.y2: ys.add(other.y2)
        if self.z1<other.z1<self.z2: zs.add(other.z1)
        if self.z1<other.z2<self.z2: zs.add(other.z2)
        for (x1, x2), (y1, y2), (z1, z2) in itertools.product(
            pairwise(sorted(xs)), pairwise(sorted(ys)), pairwise(sorted(zs))
        ):
            rect = type(self)(x1, y1, z1, x2, y2, z2)
            if rect!=inter:
                yield rect
    __sub__ = difference

    def __init__(self, x1, y1, z1, x2, y2, z2):
        if x1>x2 or y1>y2 or z1>z2:
            raise ValueError("Coordinates are invalid")
        self.x1, self.y1, self.z1, self.x2, self.y2, self.z2 = x1, y1, z1, x2, y2, z2

    def __iter__(self):
        yield self.x1
        yield self.y1
        yield self.z1
        yield self.x2
        yield self.y2
        yield self.z2

    def __eq__(self, other):
        return isinstance(other, Cube) and tuple(self)==tuple(other)
    def __ne__(self, other):
        return not (self==other)

    def __repr__(self):
        return type(self).__name__+repr(tuple(self))


def pairwise(iterable):
    # https://docs.python.org/dev/library/itertools.html#recipes
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)

def one_step(prev_cubes, step):
    is_on, coords = step
    args = [item[0] for item in coords] + [item[1]+1 for item in coords]
    cube = Cube(*args)
    
    cubes = list()
    if is_on:
        cubes.append(cube)

    for prev_cube in prev_cubes:
        if prev_cube&cube is not None:
            prev_cube_parts = prev_cube-cube
            cubes += prev_cube_parts

        else:
            cubes.append(prev_cube)

    return cubes

def part_two():
    steps = get_data("input.txt")
    # print(steps)

    cubes = list()
    for idx, step in enumerate(steps):
        cubes = one_step(cubes, step)
        # if idx == 2:
        #     break

    # print(cubes)
    print(sum([c.size() for c in cubes]))

    # total_size = 0
    # prev_voxels = Cube(10, 10, 10, 12, 12, 12).to_voxels()
    # voxels = list()
    # for cube in cubes:
    #     voxels += cube.to_voxels()
    #     total_size += cube.size()
    #     print(cube, cube.size())

    # diff_voxels = set(voxels).difference(set(prev_voxels))
    # diff_voxels = sorted(list(diff_voxels))
    # print(len(voxels))
    # print(len(prev_voxels))
    # print(len(diff_voxels))

    # for vox in diff_voxels:
    #     print(vox)
    # print(total_size)

def get_cube():   
    phi = np.arange(1,10,2)*np.pi/4
    Phi, Theta = np.meshgrid(phi, phi) 

    x = np.cos(Phi)*np.sin(Theta)
    y = np.sin(Phi)*np.sin(Theta)
    z = np.cos(Theta)/np.sqrt(2)
    return x,y,z

if __name__ == '__main__':
    # part_one()
    part_two()

    # a = Cube(10, 10, 10, 13, 13, 13)
    # b = Cube(11, 11, 11, 14, 14, 14)
    # cubes = [b] + list(a-b)
    # # cubes = [a]

    # # print(a.x2, a.x1)

    # # print(a.size(), b.size())
    # # print((a&b).size())
    # # print(cubes)
    # # for cube in cubes:
    # #     print(cube, cube.size())

    # import numpy as np
    # import matplotlib.pyplot as plt
    # from mpl_toolkits.mplot3d import Axes3D

    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # L = 1

    # for cube in cubes:
    #     x,y,z = get_cube()
        
    #     # print(cube)
    #     # Change the centroid of the cube from zero to values in data frame
    #     x = x*(cube.x2 - cube.x1) + (cube.x2 + cube.x1)/2
    #     y = y*(cube.y2 - cube.y1) + (cube.y2 + cube.y1)/2
    #     z = z*(cube.z2 - cube.z1) + (cube.z2 + cube.z1)/2
    #     ax.plot_surface(x, y, z, alpha=0.5)
    #     ax.set_zlabel("z")

    # plt.xlabel("x")
    # plt.ylabel("y")
    # plt.show()



