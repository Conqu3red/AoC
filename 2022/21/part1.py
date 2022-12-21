from typing import *
from dataclasses import dataclass

@dataclass
class Calculation:
    left: str
    op: str
    right: str
    computed: Optional[int]


def load():
    with open("input.txt") as f:
        lines = f.read().split("\n")
    
    nodes: Dict[str, Calculation] = {}

    for line in lines:
        name, other = line.split(": ")
        parts = other.split(" ")
        if len(parts) == 1:
            nodes[name] = Calculation("", "", "", int(parts[0]))
        else:
            nodes[name] = Calculation(*parts, None)
        
    return nodes



def evaluate(nodes: Dict[str, Calculation], current: str):
    node = nodes[current]
    if node.computed is not None:
        return node.computed
    
    left = evaluate(nodes, node.left)
    right = evaluate(nodes, node.right)

    if node.op == "+": node.computed = left + right
    elif node.op == "-": node.computed = left - right
    elif node.op == "*": node.computed = left * right
    elif node.op == "/": node.computed = left // right

    return node.computed



nodes = load()
print("Part 1:", evaluate(nodes, "root"))
