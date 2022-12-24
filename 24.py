from collections import defaultdict as dd
from heapq import heappop, heappush
from typing import DefaultDict, List, Set, Tuple


FILE_NAME = 'input24.in'


min_row, max_row = 0, 0
min_column, max_column = 0, 0
mapo = dd(str)
blizzards = dd(list)
dirs = {'>': (0, 1), '<': (0, -1), 'v': (1, 0), '^': (-1, 0)}
blizzard_signs = ['<', '>', 'v', '^']
START = (0, 1)
DUMMY_MIN = 9999999


def print_mapo(mapo: DefaultDict[Tuple[int, int], chr]) -> None:  # for debugging purposes
    for i in range(min_row, max_row+1):
        for j in range(min_column, max_column+1):
            if len(mapo[(i, j)]) > 1:
                print(f'{len(mapo[(i,j)])}', end="")
            else:
                print(mapo[(i, j)][0], end="")
        print()
    print()


def get_steps(position: Tuple[int, int]) -> List[Tuple[int, int]]:
    x, y = position
    return [(x, y), (x-1, y), (x+1, y), (x, y-1), (x, y+1)]


def get_manhattan(position: Tuple[int, int], end: Tuple[int, int]) -> int:
    x, y = position
    ex, ey = end
    return abs(x - ex) + abs(y - ey)


def is_legal(position: Tuple[int, int]) -> bool:
    if position == START or position == END:
        return True
    x, y = position
    return (0 < x < max_row) and (0 < y < max_column)


def simulate_one_blizzard(blizzards: DefaultDict[Tuple[int, int], List[chr]]) -> Tuple[DefaultDict[Tuple[int, int],
                          List[chr]], Set[Tuple[int, int]]]:
    nblizzards = simulate_blizzard(blizzards)
    all_blizzards_places = {key for key in nblizzards.keys()}

    return nblizzards,  all_blizzards_places


def simulate_blizzard(blizzards: DefaultDict[Tuple[int, int], List[chr]]) -> DefaultDict[Tuple[int, int], List[chr]]:
    new_blizzards = dd(list)
    for (x, y), directions in blizzards.items():
        for diro in directions:
            dx, dy = dirs[diro]
            nx, ny = x + dx, y + dy
            if not 0 < nx < max_row:
                nx = abs(nx - max_row + 1)
            if not 0 < ny < max_column:
                ny = abs(ny - max_column + 1)
            new_blizzards[(nx, ny)].append(diro)

    return new_blizzards


with open(FILE_NAME, 'r') as file:
    row, column = 0, 0
    for line in file:
        value = line.strip()
        for charo in value:
            mapo[(row, column)] = charo
            if charo in blizzard_signs:
                blizzards[(row, column)].append(charo)
            column += 1
        max_column = column - 1
        row += 1
        max_row = row - 1
        column = 0

END = (max_row, max_column-1)
initial_heuristic = get_manhattan(START, END)
current_blizzard, current_blizzard_places = blizzards, {key for key in blizzards.keys()}
all_blizzards_info = {0: (current_blizzard, current_blizzard_places)}
time = 0
repeat = 3  # 1 for part 1

for i in range(repeat):
    if i > 0:
        START, END = END, START
        time = min_time
    queue = [(initial_heuristic + time, START, time)]
    explored = set(queue[0])
    min_time = DUMMY_MIN
    while queue:
        heuristic, position, current_time = heappop(queue)

        if current_time + 1 not in all_blizzards_info:
            all_blizzards_info[current_time + 1] = simulate_one_blizzard(all_blizzards_info[current_time][0])

        for neigh in get_steps(position):
            if neigh == END:
                min_time = min(min_time, current_time + 1)
                continue

            if is_legal(neigh) and neigh not in all_blizzards_info[current_time + 1][1]:
                new_movement = (get_manhattan(neigh, END) + current_time + 1, neigh, current_time + 1)
                if new_movement not in explored:
                    if current_time + 1 < min_time:
                        heappush(queue, new_movement)
                        explored.add(new_movement)
    if i % 2 == 0:
        print(min_time)  # part1 + part2
