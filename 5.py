from typing import Tuple, List
import copy

FILE_NAME = 'input5.in'

rows, columns = None, None
stacks = None


def create_empty_stacks(lines: List[str]) -> List[List[int]]:
    rows = len(lines)
    return [[None for _ in range(columns)] for _ in range(rows)]


def find_index(stacks: List[List[int]], index: int, numo: int) -> int:
    for i in range(len(stacks)):
        if stacks[i][index] is not None:
            return i


def find_second_index(stacks: List[List[int]], index: int, numo: int) -> int:
    count = 0
    for i in range(len(stacks)):
        if stacks[i][index] is not None:
            count += 1
        if count == numo:
            return i


def find_free_index(stacks: List[List[int]], index: int) -> int:
    for i in range(len(stacks)-1, -1, -1):
        if stacks[i][index] is None:
            return i


def get_bigger_stacks(stacks: List[List[int]]) -> List[List[int]]:
    current = len(stacks)
    new = [[None for _ in range(columns)] for _ in range(current+1)]
    for i in range(1, len(new)):
        new[i] = stacks[i-1]
    return new


def print_stacks(stacks: List[List[int]]) -> None:  #for debugging processes
    for i in range(len(stacks)):
        print(stacks[i], end="\n")


def get_results(stacks: List[List[int]]) -> str:
    used = [None for _ in range(columns)]
    for i in range(len(stacks)):
        for j in range(len(stacks[i])):
            if used[j] is None and stacks[i][j] is not None:
                used[j] = stacks[i][j][1:-1]
    return ''.join(used)


def get_command_values(command_line: str) -> Tuple[int, int, int]:
    first_index = command_line.index(" from")
    what = int(command_line[5:first_index])
    second_index = command_line.index(" to")
    fromo = int(command_line[first_index + 5:second_index])
    to = int(command_line[second_index + 3:])
    return what, fromo, to


def create_stacks(stacks: List[List[int]], lines: List[str]) -> List[List[int]]:
    command_index = 0
    for line in lines:
        row = [None for _ in range(columns)]
        current_box = ""
        blank_index = 0
        index = 0
        for charo in line:
            if charo == ' ':
                blank_index += 1
            elif charo not in (' ', '[', ']'):
                current_box += charo
            elif charo == ']':
                current_box += charo
                row[index] = current_box
                current_box = ""
                index += 1
            else:
                if blank_index > 5:
                    index += 2
                elif 2 <= blank_index <= 5:
                    index += 1
                blank_index = 0
                current_box += charo
        stacks[command_index] = row[:]
        command_index += 1
    return stacks


def get_from_box(stacks: List[List[int]], column: int, what: int, part1: bool) -> Tuple[int, int]:
    func = find_index if part1 else find_second_index
    index = func(stacks, column, what)
    value = stacks[index][column]
    return index, value


def get_to_box(stacks: List[List[int]], column: int) -> Tuple[list, int]:
    index = find_free_index(stacks, column)
    if index is None:
        stacks = get_bigger_stacks(stacks)
        index = find_free_index(stacks, column)
    return stacks, index


def solve(stacks: List[List[int]], commands: List[str], first_part: bool) -> str:
    for command in commands:
        what, fromo, to = get_command_values(command)
        for i in range(what):
            real_what = what if first_part else what - i
            from_index, value = get_from_box(stacks, fromo-1, real_what, first_part)
            stacks[from_index][fromo-1] = None

            stacks, to_index = get_to_box(stacks, to - 1)
            stacks[to_index][to - 1] = value
    return get_results(stacks)


with open(FILE_NAME, 'r') as file:
    stack_lines = []
    commands = []
    commands_start = False
    for line in file:
        value = line[:-1]
        if not value:
            continue
        if "[" not in value and not commands_start:
            columns = int(value.strip()[-1])
            stacks = create_empty_stacks(stack_lines)
            stacks = create_stacks(stacks, stack_lines)
            commands_start = True
        elif '[' in value:
            stack_lines.append(value)
        else:
            commands.append(line.strip())
    print(solve(copy.deepcopy(stacks), commands, True))
    print(solve(copy.deepcopy(stacks), commands, False))
