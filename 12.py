from collections import defaultdict as dd
from typing import List, Tuple, DefaultDict, Set

FILE_NAME = 'input12.in'

mapo = dd(str)
starts = set()


def get_neighs(mapo: DefaultDict[Tuple[int, int], chr], x: int, y: int, max_row: int, max_column: int, visited: Set[
    Tuple[int, int]], part1: bool) -> List[Tuple[int, int]]:
    res = []
    for neigh in [(x+1, y), (x-1, y), (x, y-1), (x, y+1)]:
        nx, ny = neigh
        if nx < 0 or ny < 0 or nx > max_row or ny > max_column:
            continue
        if neigh in visited:
            continue
        diff = ord(mapo[neigh]) - ord(mapo[(x, y)])
        if (diff > 1 and part1) or (diff < -1 and not part1):
            continue
        res.append(neigh)
    return res


def solve(mapo: DefaultDict[Tuple[int, int], chr], start: Tuple[int, int], ends: Set[Tuple[int, int]], max_row: int,
          max_column: int, part1: bool) -> int:
    sx, sy = start
    queue = [(sx, sy, 0)]
    visited = {start}
    while queue:
        cx, cy, cost = queue.pop(0)
        if (cx, cy) in ends:
            return cost
        for neigh in get_neighs(mapo, cx, cy, max_row, max_column, visited, part1):
            nx, ny = neigh
            queue.append((nx, ny, cost + 1))
            visited.add(neigh)


with open(FILE_NAME, 'r') as file:
    row, column = 0, 0
    max_row, max_column = 0, 0
    for line in file:
        value = line.strip()
        for charo in value:
            if charo == "S":
                start = (row, column)
                mapo[(row, column)] = 'a'
            elif charo == "E":
                end = (row, column)
                mapo[(row, column)] = 'z'
            else:
                mapo[(row, column)] = charo
            if mapo[(row, column)] == 'a':
                starts.add((row, column))
            column += 1
        max_column = column-1
        max_row = row
        row += 1
        column = 0

print(solve(mapo, start, {end}, max_row, max_column, True)) #part1
print(solve(mapo, end, starts, max_row, max_column, False)) #part2

