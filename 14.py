from utils import *

example = False

FILE_NAME = 'input14.in' if not example else 'example.in'

row, column = 0, 0
max_row, max_column = 0, 0
res = 0
maxo_x = 0

mapo = dd(str)

for i in range(300):
    for j in range(1000):
        mapo[(i, j)] = '.'

with open(FILE_NAME, 'r') as file:
    for line in file:
        last_value = None
        value = line.strip().split(" -> ")
        for val in value:
            y, x = val.split(",")
            x, y = int(x), int(y)
            maxo_x = max(x, maxo_x)
            if last_value is None:
                last_value = (x, y)
            else:
                lx, ly = last_value
                if x == lx:
                    mino, maxo = min(y, ly), max(y, ly)
                    for i in range(mino, maxo+1):
                        mapo[(x, i)] = "#"
                else:
                    mino, maxo = min(x, lx), max(x, lx)
                    for i in range(mino, maxo+1):
                        mapo[(i, y)] = "#"
                last_value = (x, y)
        last_value = None

for j in range(1000):
    mapo[(maxo_x+2, j)] = '#'

simulate = True
start = (0, 500)
sands = 0

while simulate:
    sands += 1
    cx, cy = start
    moving = True
    first = True
    while moving:
        #if cx >= maxo_x:#first part
        if (cx, cy) == start and not first:
            simulate = False
            break
        first = False
        nexto = mapo[(cx+1, cy)]
        if nexto == '.':
            cx += 1
            continue
        nexto = mapo[(cx + 1, cy - 1)]
        if nexto == '.':
            cx += 1
            cy -= 1
            continue
        nexto = mapo[(cx + 1, cy + 1)]
        if nexto == '.':
            cx += 1
            cy += 1
            continue
        else:
            moving = False
            if (cx, cy) == start:
                simulate = False
                break
            mapo[(cx, cy)] = 'o'

print(sands-1) #first part
print(sands)

