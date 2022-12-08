from collections import defaultdict as dd
from typing import DefaultDict, Tuple

FILE_NAME = 'input8.in'

trees = dd(int)
max_row = 0
max_column = 0

with open(FILE_NAME, 'r') as file:
    row, column = 0, 0
    for line in file:
        value = line.strip()
        for charo in value:
            trees[(row, column)] = int(charo)
            column += 1
        row += 1
        max_column = column-1
        column = 0
    max_row = row - 1


def look_up(trees: DefaultDict[Tuple[int, int], int], x: int, y: int) -> list:
    return [trees[(i, y)] >= trees[(x, y)] for i in range(x-1, -1, -1)]


def look_down(trees: DefaultDict[Tuple[int, int], int], x: int, y: int) -> list:
    return [trees[(i, y)] >= trees[(x, y)] for i in range(x+1, max_row+1)]


def look_left(trees: DefaultDict[Tuple[int, int], int], x: int, y: int) -> list:
    return [trees[(x, i)] >= trees[(x, y)] for i in range(y-1, -1, -1)]


def look_right(trees: DefaultDict[Tuple[int, int], int], x: int, y: int) -> list:
    return [trees[(x, i)] >= trees[(x, y)] for i in range(y+1, max_column+1)]


def up_visible(trees: DefaultDict[Tuple[int, int], int], x: int, y: int) -> bool:
    return not any(look_up(trees, x, y))


def down_visible(trees: DefaultDict[Tuple[int, int], int], x: int, y: int) -> bool:
    return not any(look_down(trees, x, y))


def left_visible(trees: DefaultDict[Tuple[int, int], int], x: int, y: int) -> bool:
    return not any(look_left(trees, x, y))


def right_visible(trees: DefaultDict[Tuple[int, int], int], x: int, y: int) -> bool:
    return not any(look_right(trees, x, y))


def left_score(trees: DefaultDict[Tuple[int, int], int], x: int, y: int) -> int:
    return len(get_visibility(look_left(trees, x, y)))


def down_score(trees: DefaultDict[Tuple[int, int], int], x: int, y: int) -> int:
    return len(get_visibility(look_down(trees, x, y)))


def right_score(trees: DefaultDict[Tuple[int, int], int], x: int, y: int) -> int:
    return len(get_visibility(look_right(trees, x, y)))


def up_score(trees: DefaultDict[Tuple[int, int], int], x: int, y: int) -> int:
    return len(get_visibility(look_up(trees, x, y)))


def get_visibility(visibility: list) -> list:
    try:
        max_index = visibility.index(True)
    except ValueError:
        return visibility
    return visibility[:max_index+1] if max_index != len(visibility) else visibility[:max_index]


def is_visible(trees: DefaultDict[Tuple[int, int], int], x: int, y: int) -> bool:
    return up_visible(trees, x, y) or down_visible(trees, x, y) or left_visible(trees, x, y) or right_visible(trees, x, y)


def get_tree_score(trees: DefaultDict[Tuple[int, int], int], x: int, y: int) -> int:
    return up_score(trees, x, y) * down_score(trees, x, y) * left_score(trees, x, y) * right_score(trees, x, y)


visible = 0
score = 0

for key in trees.keys():
    x, y = key
    visible += is_visible(trees, x, y)
    score = max(score, get_tree_score(trees, x, y))


print(visible)  #part1
print(score)   #part2