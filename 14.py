from collections import defaultdict as dd

FILE_NAME = 'input14.in'
FREE = '.'
ROCK = '#'
SAND = 'o'
mapo = dd(lambda: FREE)
maxo_x = 0


with open(FILE_NAME, 'r') as file:
    for line in file:
        last_value = None
        value = line.strip().split(" -> ")
        for path in value:
            [y, x] = list(map(int, path.split(",")))
            maxo_x = max(x, maxo_x)
            if last_value is None:
                last_value = (x, y)
            else:
                lx, ly = last_value
                if x == lx:
                    mino, maxo = min(y, ly), max(y, ly)
                    for i in range(mino, maxo+1):
                        mapo[(x, i)] = ROCK
                else:
                    mino, maxo = min(x, lx), max(x, lx)
                    for i in range(mino, maxo+1):
                        mapo[(i, y)] = ROCK
                last_value = (x, y)

simulate = True
first_part = False
START = (0, 500)
sands = 0

while simulate:
    sands += 1
    cx, cy = START
    moving = True
    while moving:
        if cx >= maxo_x and not first_part:
            print(sands - 1)
            first_part = True
        if cx == maxo_x + 1:
            moving = False
            mapo[(cx, cy)] = SAND
        elif mapo[(cx+1, cy)] == FREE:
            cx += 1
        elif mapo[(cx + 1, cy - 1)] == FREE:
            cx += 1
            cy -= 1
        elif mapo[(cx + 1, cy + 1)] == FREE:
            cx += 1
            cy += 1
        else:
            moving = False
            mapo[(cx, cy)] = SAND
            if (cx, cy) == START:
                simulate = False

print(sands)

