FILE_NAME = 'input6.in'

part1 = True   #set to false for part 2
unique_count = 4 if part1 else 14

inputo = open(FILE_NAME).read()
DUMMY_CONSTANT = len(inputo)+1

print(min(([i+unique_count if len(set(inputo[i:i+unique_count])) == unique_count else DUMMY_CONSTANT for i in range(len(inputo)-unique_count)])))
