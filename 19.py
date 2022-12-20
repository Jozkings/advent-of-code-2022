from collections import defaultdict as dd
from typing import Tuple, DefaultDict

FILE_NAME = 'input19.in'

blueprints = dd(lambda: dd(int))  # {blueprint_index:{element_name(subelement_name):cost_in_element}
# ore -> ore, clay -> ore, obsidian -> ore + clay, geode -> ore + obsidian


def elementwise_sum(first: Tuple[int, ...], second: Tuple[int, ...]) -> Tuple[int, ...]:
    return tuple(sum(val) for val in zip(first, second))


def quality_heuristic(state: Tuple[Tuple[int, ...], ...]) -> Tuple[Tuple[int, ...], ...]:  # heuristic, not foolproof
    robots, materials, mined, minutes = state
    return 2**10*mined[3] + 2**7*mined[2] + 2**4*mined[1] + mined[0]


def get_quality(data: DefaultDict[str, int], max_time: int, max_trim: int = 3000) -> int:
    minutes = 0
    queue = [((1, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), minutes)]  # robots, available, collected, minutes_left
    quality = 0
    level = 0
    while queue:
        robots, materials, mined, minutes = queue.pop(0)
        if minutes > level:
            queue = sorted(queue, key=quality_heuristic, reverse=True)[:max_trim]
            level = minutes
        if minutes == max_time:
            quality = max(quality, mined[3])
            continue

        old_materials = materials
        materials = elementwise_sum(materials, robots)
        mined = elementwise_sum(mined, robots)
        queue.append((robots, materials, mined, minutes+1))

        if old_materials[0] >= data["ore"]:  # ore robot
            queue.append((elementwise_sum(robots, (1,0,0,0)), elementwise_sum(materials, (-data["ore"],0,0,0)),
                          mined, minutes+1))
        if old_materials[0] >= data["clay"]:  # clay robot
            queue.append((elementwise_sum(robots, (0,1,0,0)), elementwise_sum(materials, (-data["clay"],0,0,0)),
                          mined, minutes+1))
        if old_materials[1] >= data["obsidian2-clay"] and old_materials[0] >= data["obsidian1-ore"]:  # obsidian robot
            queue.append((elementwise_sum(robots, (0,0,1,0)), elementwise_sum(materials,(-data["obsidian1-ore"],
                                                                                         -data["obsidian2-clay"],0,
                                                                                         0)), mined, minutes+1))
        if old_materials[2] >= data["geode2-obsidian"] and old_materials[0] >= data["geode1-ore"]:  # geode robot
            queue.append((elementwise_sum(robots, (0,0,0,1)), elementwise_sum(materials,(-data["geode1-ore"],0,
                                                                                         -data["geode2-obsidian"],
                                                                                         0)), mined, minutes+1))

    return quality


with open(FILE_NAME, 'r') as file:
    index = 1
    for line in file:
        value = line.strip().split(" ")
        was_obsidian = False
        was_ore = False
        for i, val in enumerate(value):
            if val == "ore." and not was_ore:
                blueprints[index]["ore"] = int(value[i-1])
                was_ore = True
            elif val == "ore." and was_ore:
                blueprints[index]["clay"] = int(value[i-1])
            elif val == "ore" and value[i+1] == "and" and not was_obsidian:
                blueprints[index]["obsidian1-ore"] = int(value[i-1])
                blueprints[index]["obsidian2-clay"] = int(value[i+2])
                was_obsidian = True
            elif val == "ore" and value[i+1] == "and" and was_obsidian:
                blueprints[index]["geode1-ore"] = int(value[i-1])
                blueprints[index]["geode2-obsidian"] = int(value[i+2])
        index += 1

res = 0
sres = 1

for blueprint, data in blueprints.items():
    quality = get_quality(data, max_time=24)
    res += (quality * blueprint)
    if blueprint < 4:
        squality = get_quality(data, max_time=32)
        sres *= squality

print(res)  # part1
print(sres)  # part2
