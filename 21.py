from collections import defaultdict as dd
from copy import deepcopy
from typing import DefaultDict, Union


FILE_NAME = 'input21.in'

FINAL = "root"
ME = "humn"

monkeys = dd(list)


def is_monkey_done(value: Union[int, list, None]) -> bool:
    return type(value) != list


def get_basic_result(f: int, operator: chr, s: int) -> int:
    match operator:
        case "+":
            return f + s
        case "-":
            return f - s
        case "/":
            return f // s
        case "*":
            return f * s
    raise Exception("Operator not found " + operator)


def get_complex_result(f: int, operator: chr, s: int, reverse: bool = True) -> int:
    f, s = int(f), int(s)
    match operator:
        case "+":
            return f - s
        case "-":
            return f + s if not reverse else -f + s
        case "*":
            return f // s
        case "/":
            return f * s if not reverse else s // f
    raise Exception("Operator not found " + operator)


def part1(monkeys: DefaultDict[str, Union[str, list, int]]) -> int:
    def get_value(current_monkey: str) -> int:
        if is_monkey_done(monkeys[current_monkey]):
            return monkeys[current_monkey]

        first, operator, second = monkeys[current_monkey]
        first_res = get_value(first)
        second_res = get_value(second)

        return get_basic_result(first_res, operator, second_res)

    return get_value(FINAL)


def part2(monkeys: DefaultDict[str, Union[str, list, int]]) -> int:
    monkeys[ME] = None
    monkeys[FINAL][1] = "-"

    def get_value(current_monkey: str, expected: Union[int, None] = None) -> int:
        if is_monkey_done(monkeys[current_monkey]):
            if monkeys[current_monkey] is None:
                return expected
            return monkeys[current_monkey]

        first, operator, second = monkeys[current_monkey]
        first_res = get_value(first)
        second_res = get_value(second)

        if expected is None:
            return get_basic_result(first_res, operator, second_res) if first_res and second_res else None
        if first_res is None:
            return get_value(first, get_complex_result(expected, operator, second_res, reverse=False))
        return get_value(second, get_complex_result(expected, operator, first_res, reverse=True))

    return get_value(FINAL, expected=0)


with open(FILE_NAME, 'r') as file:
    for line in file:
        value = line.strip().split(": ")
        val = value[1].split(" ")
        if len(val) == 1:
            val = int(val[0])
        monkeys[value[0]] = val

print(part1(deepcopy(monkeys)))
print(part2(deepcopy(monkeys)))
