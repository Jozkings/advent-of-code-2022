from collections import defaultdict as dd
from typing import DefaultDict, List, Tuple, Union

FILE_NAME = 'input17.in'

WIDE = 7
BLOCKS_FALLING = 10000  # enough for proper simulation
CUBES = 1000000000000
suter1 = "####"
suter2 = ".#.\n###\n.#."
suter3 = "..#\n..#\n###"  # mirrored
suter4 = "#\n#\n#\n#"
suter5 = "##\n##"
suters = [suter1, suter2, suter3, suter4, suter5]


def print_tetris(tetris: List[List[Tuple[int, int]]]) -> None:   # for debugging purposes
    maxo, mino = get_max_min(tetris)
    for i in range(maxo, mino-1, -1):
        for j in range(7):
            pos = any([(i, j) in val for val in tetris])
            if pos:
                print("#", end="")
            else:
                print(".", end="")
        print()


def save_tetris(tetris: List[List[Tuple[int, int]]]) -> DefaultDict[Tuple[int, int], chr]:
    mapo = dd(chr)
    maxo, mino = get_max_min(tetris)
    for x in range(mino, maxo + 1):
        for y in range(7):
            mapo[(x, y)] = '.'

    for block in tetris:
        for coord in block:
            mapo[coord] = "#"

    return mapo


def get_height(tetris: List[List[Tuple[int, int]]], heights: DefaultDict[int, int]) -> int:
    return heights[len(tetris)-1]


def get_max_min(tetris: List[List[Tuple[int, int]]]) -> Tuple[int, int]:
    maxo = max([x for block in tetris for x, _ in block])
    mino = min([x for block in tetris for x, _ in block])
    return maxo, mino


def get_starting_row(new: str, lasts: Union[None, List[List[Tuple[int, int]]]], suter_types: List[str]) -> int:
    if lasts is None:
        return 3
    maxo, _ = get_max_min(lasts)
    if new in (suter_types[1], suter_types[2]):
        return maxo + 6
    if new == suter_types[0]:
        return maxo + 4
    if new == suter_types[3]:
        return maxo + 7
    return maxo + 5


def get_starting_position(last_suters: Union[None, List[List[Tuple[int, int]]]], all_suter_types: List[str],
                          current_suter: int):
    coords = []
    block = all_suter_types[current_suter]
    row, column = get_starting_row(block, last_suters, all_suter_types), 2
    for charo in block:
        if charo == "#":
            coords.append((row, column))
            column += 1
        elif charo == '\n':
            row -= 1
            column = 2
        else:
            column += 1
    return coords


def is_intersecting(first: List[Tuple[int, int]], second: List[Tuple[int, int]]) -> bool:
    return any([coord in second for coord in first])


def check_intersection(tetris: List[List[Tuple[int, int]]], new_coords: List[Tuple[int, int]]) -> bool:
    return any([is_intersecting(block, new_coords) for block in tetris])


def move_suter_down(coords: List[Tuple[int, int]], tetris: List[List[Tuple[int, int]]]) -> Union[None, List[Tuple[
                    int, int]]]:
    new_coords = []
    for coord_x, coord_y in coords:
        newx = coord_x-1
        if newx == -1:
            return None
        new_coords.append((newx, coord_y))
    return None if check_intersection(tetris[-30:-1], new_coords) else new_coords


def move_suter_arrow(coords: List[Tuple[int, int]], tetris: List[List[Tuple[int, int]]], arrow: chr) -> List[Tuple[
                    int, int]]:
    new_coords = []
    for coord_x, coord_y in coords:
        newy = coord_y + 1 if arrow == '>' else coord_y - 1
        if newy < 0 or newy == WIDE:
            return coords
        new_coords.append((coord_x, newy))
    return coords if check_intersection(tetris[-30:-1], new_coords) else new_coords  # 30 last blocks is enough


def find_possible(start: int, length: int, heights_diff: List[int]) -> bool:  # heuristic for getting repeated pattern
    return heights_diff[start:start+length] == heights_diff[start+length:start+length + length]


def get_pattern_string(tetris: List[List[Tuple[int, int]]], tetris_map: DefaultDict[Tuple[int, int], chr]) -> str:
    res = ""
    maxo, mino = get_max_min(tetris)
    for i in range(mino, maxo + 1):
        for j in range(7):
            res += tetris_map[(i, j)]
    return res


def get_pattern(tetris: List[List[Tuple[int, int]]], block_length: int, tetris_map: DefaultDict[Tuple[int, int], chr],
                max_shift: int = 300) -> int:
    start_pattern = get_pattern_string(tetris[:block_length], tetris_map)
    max_shift = block_length + max_shift if max_shift is not None else len(tetris) - block_length
    for i in range(block_length, max_shift):
        current_pattern = get_pattern_string(tetris[i:i+block_length], tetris_map)
        if start_pattern == current_pattern:
            return i


def find_pattern(tetris: List[List[Tuple[int, int]]], tetris_map: DefaultDict[Tuple[int, int], chr],
                 heights_diff: List[int], min_start: int = 100, max_start: int = 1000, max_block_length: int = 2000,
                 min_block_length: int = 50) -> Tuple[int, int]:
    for start in range(min_start, max_start+1):     # arguments can be tuned
        for p in range(max_block_length, min_block_length, -1):
            if find_possible(start, p, heights_diff):
                index = get_pattern(tetris[start:], p, tetris_map)
                if index is not None:
                    return start, index


def calculate_height(start: int, cycle_length: int, heights: DefaultDict[int, int]) -> int:
    start_length = get_height(tetris[:start], heights)
    cycles_number = (CUBES - start) // cycle_length
    last = CUBES - (start + (cycles_number * cycle_length))
    last_length = get_height(tetris[:start+last], heights) - start_length
    all_cycles_length = (get_height(tetris[:start+cycle_length], heights) - start_length) * cycles_number

    return start_length + all_cycles_length + last_length


with open(FILE_NAME, 'r') as file:
    for line in file:
        arrows = line.strip()

done = 0
current_suter = 0
heights = dd(int)
heights_diff = [0]
position = get_starting_position(None, suters, current_suter)
tetris = [position]
last_max = -999

while done != BLOCKS_FALLING:
    for arrow in arrows:
        position = move_suter_arrow(position, tetris, arrow)
        tetris[done] = position
        position = move_suter_down(position, tetris)
        if position is None:
            current_height = max(last_max, max([x for x, _ in tetris[done]]) + 1)
            heights[done] = current_height
            heights_diff.append(heights[done-1] - current_height)
            last_max = heights[done]
            current_suter += 1
            current_suter %= 5
            done += 1
            if done == BLOCKS_FALLING:
                break
            position = get_starting_position(tetris[done-WIDE:], suters, current_suter)
            tetris.append(position)
        else:
            tetris[done] = position


print(get_height(tetris[:2022], heights))
tetris_map = save_tetris(tetris)
start, index = find_pattern(tetris, tetris_map, heights_diff)
print(calculate_height(start, index, heights))
