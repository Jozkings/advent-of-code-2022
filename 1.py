FILE_NAME = 'input1.in'

VALUES_NUMBER = 1 #change to 3 for part 2

res = sum(sorted([sum([value for value in map(int, line.split("\n"))]) for line in open(FILE_NAME).read().split("\n\n")]
                 , reverse=True)[:VALUES_NUMBER])

print(res)

