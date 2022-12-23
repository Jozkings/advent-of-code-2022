from collections import defaultdict as dd
from typing import DefaultDict, List, Tuple

FILE_NAME = 'input23.in'
DUMMY_MAX = 9999999
mapo = dd(chr)


def get_min_max(mapo: DefaultDict[Tuple[int, int], chr], elves_only: bool = False) -> Tuple[int, int, int, int]:
    min_row, max_row = DUMMY_MAX, 0
    min_column, max_column = DUMMY_MAX, 0
    for (x, y) in mapo:
        if elves_only:
            if mapo[key] == '#':
                min_row, max_row = min(x, min_row), max(x, max_row)
                min_column, max_column = min(y, min_column), max(y, max_column)
        else:
            min_row, max_row = min(x, min_row), max(x, max_row)
            min_column, max_column = min(y, min_column), max(y, max_column)
    return min_row, max_row, min_column, max_column


def print_mapo(mapo: DefaultDict[Tuple[int, int], chr]) -> None:  # for debugging purposes
    min_row, max_row, min_column, max_column = get_min_max(mapo)

    for i in range(min_row, max_row+1):
        for j in range(min_column, max_column+1):
            if (i, j) in mapo:
                print(mapo[(i, j)], end='')
            else:
                print('.', end='')
        print()
    print()


def get_neighs(x: int, y: int) -> List[Tuple[int, int]]:
    return [(x-1, y-1), (x-1, y), (x-1, y+1), (x, y-1), (x, y+1), (x+1, y-1), (x+1, y), (x+1, y+1)]


def check_up(x: int, y: int) -> List[Tuple[int, int]]:
    return [(x-1, y), (x-1, y+1), (x-1, y-1)]


def check_down(x: int, y: int) -> List[Tuple[int, int]]:
    return [(x+1, y), (x+1, y+1), (x+1, y-1)]


def check_left(x: int, y: int) -> List[Tuple[int, int]]:
    return [(x, y-1), (x-1, y-1), (x+1, y-1)]


def check_right(x: int, y: int) -> List[Tuple[int, int]]:
    return [(x, y+1), (x-1, y+1), (x+1, y+1)]


def elves_counts(mapo: DefaultDict[Tuple[int, int], chr], neighs: List[Tuple[int, int]]) -> int:
    return sum([1 if neigh in mapo and mapo[neigh] == '#' else 0 for neigh in neighs])


def get_open_count(mapo: DefaultDict[Tuple[int, int], chr]) -> int:
    min_row, max_row, min_column, max_column = get_min_max(mapo)
    rows = max_row - min_row + 1
    columns = max_column - min_column + 1
    return (rows * columns) - sum([1 if value == '#' else 0 for value in mapo.values()])


with open(FILE_NAME, 'r') as file:
    row, column = 0, 0
    for line in file:
        value = line.strip()
        for charo in value:
            mapo[(row, column)] = charo
            column += 1
        row += 1
        column = 0

checks = [check_up, check_down, check_left, check_right]
checks_changes = [(-1, 0), (1, 0), (0, -1), (0, 1)]
rounds = 0
res = 0


while True:
    rounds += 1
    proposes = dd(tuple)
    duplicates = set()
    for key, value in mapo.items():
        x, y = key
        if value == '#':
            if elves_counts(mapo, get_neighs(x, y)) == 0:
                continue
            for index, check in enumerate(checks):
                nx, ny = checks_changes[index]
                if elves_counts(mapo, check(x, y)) == 0:
                    proposed = (x+nx, y+ny)
                    if proposed in proposes.values():
                        duplicates.add(proposed)
                    else:
                        proposes[key] = proposed
                    break

    if len(proposes) == 0:
        break

    for key, value in proposes.items():
        if value not in duplicates:
            mapo[key] = '.'
            mapo[value] = '#'

    checks = checks[1:] + [checks[0]]
    checks_changes = checks_changes[1:] + [checks_changes[0]]

    if rounds == 10:
        res = get_open_count(mapo)
        print(res)  # part1


print(rounds)  # part2
