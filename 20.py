from collections import deque
from typing import Deque, List, Tuple

FILE_NAME = 'input20.in'

values = []
DECRYPTION_KEY = 811589153


def mix(values: List[Tuple[int, int]], repeat: int = 1, dec_key: int = 0) -> Deque[Tuple[int, int]]:
    if dec_key:
        values = [(index, val * dec_key) for (index, val) in values]

    mixed = deque(values[:])

    for _ in range(repeat):
        for number in values:
            index = mixed.index(number)
            mixed.rotate(-index)
            mixed.popleft()
            mixed.rotate(-number[1])
            mixed.appendleft(number)

    return mixed


def get_result(values: Deque[Tuple[int, int]]) -> int:
    values_only = [val for _, val in values]
    zero_index = values_only.index(0)
    leno = len(values_only)

    first = values_only[(zero_index+1000) % leno]
    second = values_only[(zero_index+2000) % leno]
    third = values_only[(zero_index+3000) % leno]

    return first + second + third


with open(FILE_NAME, 'r') as file:
    for index, line in enumerate(file):
        value = int(line.strip())
        values.append((index, value))  # input contains duplicates!!!

print(get_result(mix(values)))  # part1
print(get_result(mix(values, repeat=10, dec_key=DECRYPTION_KEY)))  # part2
