FILE_NAME = 'input10.in'

x = 1
START = 20
REPEAT = 40
xses = []


def print_res(res: str) -> None:
    for i in range(6):
        for j in range(REPEAT):
            print(res[((i * REPEAT) + j)], end="")
        print("")


with open(FILE_NAME, 'r') as file:
    for line in file:
        value = line.strip().split(" ")
        if value[0] == "addx":
            xses += [x, x]
            x += int(value[1])
        else:
            xses.append(x)

strength = 0
res = ""

for x, pos in enumerate(xses):
    if x == START-1 or (x - START + 1) % REPEAT == 0:
        strength += pos * (x+1)
    if (x % REPEAT) in (pos-1, pos, pos+1):
        res += "#"
    else:
        res += "."

print(strength)  #part1
print_res(res)   #part2
