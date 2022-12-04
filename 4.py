FILE_NAME = 'input4.in'

res1 = 0
res2 = 0

with open(FILE_NAME, 'r') as file:
    for line in file:
        pairs = list(map(lambda val: val.split('-'), line.strip().split(",")))
        first = {i for i in range(int(pairs[0][0]), int(pairs[0][1])+1)}
        second = {i for i in range(int(pairs[1][0]), int(pairs[1][1])+1)}
        res1 += len(set(first) & set(second)) in (len(first), len(second))
        res2 += len(set(first) & set(second)) > 0

print(res1, res2)

