from collections import defaultdict as dd
from typing import DefaultDict, Tuple


FILE_NAME = 'input15.in'
FY = 2000000
MAX_COORDS = 4000000
sensors = dd(tuple)


def manhattan(fx: int, fy: int, sx: int, sy: int) -> int:
    return abs(fx - sx) + abs(fy - sy)


def part1(sensors: DefaultDict[Tuple[int, int], Tuple[int, int]]) -> int:
    taken = set()
    for sensor, beacon in sensors.items():
        sx, sy = sensor
        bx, by = beacon
        max_diff = manhattan(sx, sy, bx, by) - abs(sy - FY)
        taken |= set(range(sx - max_diff, sx + max_diff + 1))
    taken -= set([y for x, y in sensors.values() if y == FY])
    return len(taken)


def part2(sensors: DefaultDict[Tuple[int, int], Tuple[int, int]]) -> int: #takes a long time (approx. 10 mins)
    taken = set()
    for sensor, beacon in sensors.items():
        sx, sy = sensor
        bx, by = beacon
        max_diff = manhattan(sx, sy, bx, by) + 1
        for value in range(sx - max_diff, sx + max_diff + 1):
            if 0 <= value <= MAX_COORDS:
                y = sy + (max_diff - abs(sx - value))
                if 0 <= y <= MAX_COORDS:
                    taken.add((value, y))
                y = sy - (max_diff - abs(sx - value))
                if 0 <= y <= MAX_COORDS:
                    taken.add((value, y))
    for cx, cy in taken:
        possible = True
        for sensor, beam in sensors.items():
            sx, sy = sensor
            bx, by = beam
            if manhattan(sx, sy, bx, by) >= manhattan(sx, sy, cx, cy):
                possible = False
                break
        if possible:
            return cx * MAX_COORDS + cy


with open(FILE_NAME, 'r') as file:
    for line in file:
        value = line.strip()
        val = value.split(":")
        indeces = []
        for index, value in enumerate(val):
            data = value.split(", ")
            findex, sindex = data[0].index("="), data[1].index("=")
            cx, cy = int(data[0][findex+1:]), int(data[1][sindex+1:])
            if indeces:
                sensors[(indeces[0], indeces[1])] = (cx, cy)
            else:
                indeces = [cx, cy]


print(part1(sensors))
print(part2(sensors))



