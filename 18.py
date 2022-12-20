from typing import List, Set, Tuple

FILE_NAME = 'input18.in'

DUMMY_MAX = 99999
cubes_coords = set()
mino_x, maxo_x = DUMMY_MAX, 0
mino_y, maxo_y = DUMMY_MAX, 0
mino_z, maxo_z = DUMMY_MAX, 0


def get_neighs(cube: Tuple[int, int, int]) -> List[Tuple[int, ...]]:
    neighs = []
    for change in [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]:
        neighs.append(tuple(sum(val) for val in zip(cube, change)))
    return neighs


def is_exterior(cube: Tuple[int, ...], exteriers: Set[Tuple[int, int, int]]) -> Tuple[bool,
                                                                                      Set[Tuple[int, int, int]]]:
    visited = {cube}
    queue = [cube]

    while queue:
        x, y, z = queue.pop(0)
        if (x, y, z) in exteriers:
            return True, exteriers | (visited - cubes_coords)
        if not mino_x <= x <= maxo_x or not mino_y <= y <= maxo_y or not mino_z <= z <= maxo_z:
            return True, exteriers | (visited - cubes_coords)
        for neigh in get_neighs((x, y, z)):
            if neigh not in visited and neigh not in cubes_coords:
                visited.add(neigh)
                queue.append(neigh)

    return False, exteriers


with open(FILE_NAME, 'r') as file:
    for line in file:
        x, y, z = list(map(int, line.strip().split(',')))
        mino_x, maxo_x = min(mino_x, x), max(maxo_x, x)
        mino_y, maxo_y = min(mino_y, y), max(maxo_y, y)
        mino_z, maxo_z = min(mino_z, z), max(maxo_z, z)
        cubes_coords.add((x, y, z))

surface = 0

for coords in cubes_coords:
    for neigh in get_neighs(coords):
        if neigh not in cubes_coords:
            surface += 1

print(surface)

exteriers = set()
bsurface = 0

for coords in cubes_coords:
    for neigh in get_neighs(coords):
        if neigh not in cubes_coords:
            res, exteriers = is_exterior(neigh, exteriers)
            bsurface += res

print(bsurface)
