from collections import defaultdict as dd
import re
from typing import Callable, DefaultDict, List, Tuple

FILE_NAME = 'input22.in'
DUMMY_INSTRUCTION = 'X'
mapo = dd(str)
ins_start = False
first = True


def wrap(mapo: DefaultDict[Tuple[int, int], chr], x: int, y: int, facing: int) -> Tuple[int, int, int]:
    dx, dy = FACINGS_CHANGE[facing]
    cx, cy = x, y
    while (cx, cy) in mapo and mapo[(cx, cy)] != ' ':
        nx, ny = cx, cy
        cx -= dx
        cy -= dy
    return nx, ny, facing


def wrap_cube(mapo: DefaultDict[Tuple[int, int], chr], x: int, y: int, facing: int) -> Tuple[int, int, int]:
    if facing == 0:  # hard coded, hard determined ))
        if 0 <= x <= 49:
            return 149 - x, y - 50, 2
        if 50 <= x <= 99:
            return y - 50, x + 50, 3
        if 100 <= x <= 149:
            return 149 - x, y + 50, 2
        return y + 100, x - 100, 3

    if facing == 1:
        if 0 <= y <= 49:
            return 199 - x, y + 100, 1
        if 50 <= y <= 99:
            return y + 100, x - 100, 2
        return y - 50, x + 50, 2

    if facing == 2:
        if 0 <= x <= 49:
            return 149 - x, y - 50, 0
        if 50 <= x <= 99:
            return y + 50, x - 50, 1
        if 100 <= x <= 149:
            return 149 - x, y + 50, 0
        return y, x - 100, 1

    if facing == 3:
        if 0 <= y <= 49:
            return y + 50, x - 50, 0
        if 50 <= y <= 99:
            return y + 100, x, 0
        return 199 - x, y - 100, 3


def move(x: int, y: int, facing: int, mapo: DefaultDict[Tuple[int, int], chr], much: int, where: chr,
         is_cube: bool = False, wrap_function: Callable = wrap) -> Tuple[int, int, int]:
    if where != DUMMY_INSTRUCTION:
        facing = facing + 1 if where == "R" else facing - 1
        facing %= 4
    dx, dy = FACINGS_CHANGE[facing]
    for _ in range(much):
        nx, ny = x + dx, y + dy
        if (nx, ny) not in mapo or mapo[(nx, ny)] == ' ':
            nx, ny, nfacing = wrap_function(mapo, x, y, facing)
            if is_cube:
                if mapo[(nx, ny)] == "#":
                    break
                facing = nfacing
                dx, dy = FACINGS_CHANGE[facing]
        if mapo[(nx, ny)] == "#":
            break
        x, y = nx, ny

    return x, y, facing


def solve(mapo: DefaultDict[Tuple[int, int], chr], facing: int, instructions: List[str], first_part: bool = True):
    wrap_function = wrap if first_part else wrap_cube
    x, y = START
    for i in range(0, len(instructions), 2):
        much = int(instructions[i + 1])
        where = instructions[i]
        x, y, facing = move(x, y, facing, mapo, much, where, not first_part, wrap_function)
    return ((x + 1) * 1000) + ((y + 1) * 4) + facing


with open(FILE_NAME, 'r') as file:
    row, column = 0, 0
    for line in file:
        if not line.strip():
            ins_start = True
        elif ins_start:
            instructions = line
            break
        else:
            for charo in line.rstrip():
                mapo[(row, column)] = charo
                if first and charo == ".":
                    START = (row, column)
                    first = False
                column += 1
        column = 0
        row += 1

splitted_instructions = [DUMMY_INSTRUCTION] + re.split('(\d+)', instructions)[1:-1]
facing = 0
FACINGS_CHANGE = {0: (0, 1), 1: (1, 0), 2: (0, -1), 3: (-1, 0)}

print(solve(mapo, facing, splitted_instructions))
print(solve(mapo, facing, splitted_instructions, first_part=False))
