from operator import add
from typing import List, Tuple

FILE_NAME = 'input8.in'

rope = [[0, 0] for _ in range(11)]   #0 -> head, 1 -> part1, 9 -> part2
dirs = {"R": [0, 1], "L": [0, -1], "U": [-1, 0], "D": [1, 0]}


def sign_value(value: int) -> int:
    return (value > 0) - (value < 0)


def get_diffs(head: List[int], tail: List[int]) -> Tuple[int, int]:
    hx, hy = head
    tx, ty = tail
    return hx - tx, hy - ty


with open('input9.in') as file:
    visited_one = {(0, 0)}
    visited_nine = {(0, 0)}
    for line in file:
        diro, numo = line.strip().split()
        numo = int(numo)
        for _ in range(numo):
            rope[0] = list(map(add, rope[0], dirs[diro]))
            for i in range(1, len(rope)):
                diff_x, diff_y = get_diffs(rope[i-1], rope[i])
                diffs = map(lambda x: sign_value(x), [diff_x, diff_y])
                if abs(diff_x) >= 2 or abs(diff_y) >= 2:
                    rope[i] = list(map(add, rope[i], diffs))
                if i == 1:
                    visited_one.add((rope[i][0], rope[i][1]))
                elif i == 9:
                    visited_nine.add((rope[i][0], rope[i][1]))


print(len(visited_one))
print(len(visited_nine))

                
            
         
        
