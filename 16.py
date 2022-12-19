from collections import defaultdict as dd
from typing import DefaultDict, List, Tuple


FILENAME = "input16.in"
DUMMY_MAX = 99999999
valves = dd(tuple)  #name : (rate, neighbours)
OPEN_VALVE_TIME = 1
 

def floyd_warshall(valves: DefaultDict[str, Tuple[str, ...]]) -> DefaultDict[str, DefaultDict[str, int]]:
    distances = dd(lambda: dd(lambda: DUMMY_MAX))
 
    for name, valve in valves.items():
        for neigh in valve[1]:
            distances[name][neigh] = 1
 
    for k in valves:
        for i in valves:
            for j in valves:
                distances[i][j] = min(distances[i][j], distances[i][k] + distances[k][j])
 
    return distances
 
 
def generate_paths(pos: str, path: List[str], time: int) -> List[List[str]]:
    res = []
    for name, specs in valves.items():
        if specs[0] > 0 and name not in path and distances[pos][name] <= time:
            new_time = time - distances[pos][name] - OPEN_VALVE_TIME
            res += generate_paths(name, path + [name], new_time)
    res.append(path[:])
    return res


def get_path_score(current: str, open_order: List[str], time: int) -> int:
    res = 0
    for valve in open_order:
        time -= distances[current][valve] + OPEN_VALVE_TIME
        res += valves[valve][0] * time
        current = valve
    return res


def is_intersecting(first: List[str], second: List[str]) -> bool:
    return any([f in second for f in first])


def part1() -> int:
    res = 0
    for way in generate_paths("AA", [], 30):
        res = max(res, get_path_score("AA", way, 30))
    return res


def part2() -> int:
    paths = generate_paths("AA", [], 26)
    res = 0
    scores = [get_path_score("AA", path, 26) for path in paths]
    paths_n_scores = zip(paths, scores)
    paths_n_scores = sorted(paths_n_scores, key=lambda data: data[1], reverse=True)

    for i, (fp, fs) in enumerate(paths_n_scores):
        if fs + paths_n_scores[i+1][1] < res:
            break
        for j, (tp, ts) in enumerate(paths_n_scores):
            if fs + ts > res and i < j and not is_intersecting(fp, tp):
                res = fs + ts

    return res


with open(FILENAME, "r") as file:
    for line in file:
        value = line.strip()
        val = value.split("=")
        until = val[1].index(";")
        rate = int(val[1][:until])
        name = val[0].split(" ")[1]
        next_info = val[1].split(", ")
        nexts = []
        for index, nexto in enumerate(next_info):
            if index == 0:
                split_point = nexto.index("valve") + 5
                if "valves" in nexto:
                    split_point += 1
                nexts.append(nexto[split_point+1:])
            else:
                nexts.append(nexto)
        valve = (rate, nexts)
        valves[name] = valve


distances = floyd_warshall(valves)
print(part1())
print(part2())
