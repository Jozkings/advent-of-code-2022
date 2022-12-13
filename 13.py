from functools import cmp_to_key
from typing import Union, List

FILE_NAME = 'input13.in'


def compare_list(left: Union[int, List[Union[int, list]]], right: Union[int, List]) -> int:
    if type(left) == int:
        if type(right) == int:
            return compare_int(left, right)
        left = [left]
    if type(right) == int:
        right = [right]

    mino = min(len(left), len(right))
    for i in range(mino):
        res = compare_list(left[i], right[i])
        if res != 0:
            return res
    return compare_int(len(left), len(right))


def compare_int(left: int, right: int) -> int:
    return 1 if left > right else 0 if left == right else -1


first_divider, second_divider = [[2]], [[6]]
all_packets = [first_divider, second_divider]
order_sum = 0

with open(FILE_NAME, 'r') as file:
    packets = []
    index = 1
    for line in file:
        if line != '\n':
            evaled_line = eval(line)
            all_packets.append(evaled_line)
            packets.append(evaled_line)
            if len(packets) == 2:
                if compare_list(packets[0], packets[1]) == -1:
                    order_sum += index
                index += 1
                packets = []

print(order_sum)  #part1
all_packets = sorted(all_packets, key=cmp_to_key(compare_list))
print((all_packets.index(first_divider)+1) * (all_packets.index(second_divider)+1))  #part2
