from __future__ import annotations
from typing import List
from collections import defaultdict as dd


class Node:
    def __init__(self, parent: Node, value: str) -> None:
        self.parent = parent
        self.value = value
        self.files = dd(int)  #name, size
        self.children = []

    def add_child(self, node: Node) -> None:
        self.children.append(node)

    def files_size(self) -> int:
        return sum(self.files.values())

    def get_unique_name(self) -> str:
        parent_names = []
        node = self
        while node.parent is not None:
            parent_names.append(node.parent.value)
            node = node.parent
        return ''.join(parent_names[::-1]) + self.value

    def get_root(self) -> Node:
        return self.get_all_parents()[-1]

    def get_all_parents(self) -> List[Node]:
        node = self
        parents = []
        while node.parent is not None:
            parents.append(node.parent)
            node = node.parent
        return parents


FILE_NAME = 'input7.in'
ROOT = "/"
node = None
SIZE_THRESHOLD = 100000
SPACE = 70000000
UNUSED_SPACE = 30000000

with open(FILE_NAME, 'r') as file:
    for line in file:
        value = line.strip().split(" ")
        if value[0] == '$':
            if value[1] == "cd":
                where = value[2]
                if where == ROOT:
                    node = Node(None, ROOT)
                elif where == "..":
                    node = node.parent
                else:
                    child = Node(node, where)
                    node.add_child(child)
                    node = child
        else:
            pos_size, name = value
            if pos_size != "dir":
                node.files[name] += int(pos_size)

node = node.get_root()
queue = [(node, node.files_size())]
res = dd(int)

while queue:
    current_node, size = queue.pop(0)
    parents = current_node.get_all_parents()
    for parent in parents:
        res[parent.get_unique_name()] += size
    res[current_node.get_unique_name()] = size
    for child in current_node.children:
        queue.append((child, child.files_size()))


print(sum(value for value in res.values() if value <= SIZE_THRESHOLD))    #part1
print(min(value for value in res.values() if SPACE - res[node.get_unique_name()] + value >= UNUSED_SPACE))   #part2



