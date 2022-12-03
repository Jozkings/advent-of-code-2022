FILE_NAME = 'input3.in'

res1 = 0
res2 = 0


def get_lower_value(charo: chr) -> int:
    return ord(charo) - 96


def get_higher_value(charo: chr) -> int:
    return ord(charo) - 38


with open(FILE_NAME, 'r') as file:
    group_share = set()
    group_index = 0
    for line in file:
        rucksack = line.strip()
        length = len(rucksack) // 2
        first, second = set(rucksack[:length]), set(rucksack[length:])
        bcommon = (first & second).pop()
        res1 += get_lower_value(bcommon) if bcommon.islower() else get_higher_value(bcommon)
        if group_index == 0:
            group_share = set(rucksack)
        elif group_index < 2:
            group_share &= set(rucksack)
        else:
            group_share &= set(rucksack)
            common = group_share.pop()
            res2 += get_lower_value(common) if common.islower() else get_higher_value(common)
            group_share = set()
            group_index = -1
        group_index += 1

print(res1, res2)


