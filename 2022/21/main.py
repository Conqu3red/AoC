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
        #if name == SEARCH_NODE:
        #    nodes[name] = Unit()
        if len(parts) == 1:
            nodes[name] = Calculation("", "", "", int(parts[0]))
        else:
            nodes[name] = Calculation(*parts, None)
        
    return nodes


def evaluate(nodes: Dict[str, Calculation], current: str, skip_node: Optional[str] = None) -> Optional[int]:
    if current == skip_node:
        return None
    
    node = nodes[current]
    if node.computed is not None:
        return node.computed
    
    left = evaluate(nodes, node.left, skip_node)
    right = evaluate(nodes, node.right, skip_node)

    if left is None or right is None:
        return None
    

    if node.op == "+": node.computed = left + right
    elif node.op == "-": node.computed = left - right
    elif node.op == "*": node.computed = left * right
    elif node.op == "/": node.computed = left // right
    
    return node.computed
    


def reverse_evaluate(nodes: Dict[str, Calculation], target: str, current: str, value: int):
    if current == target:
        return value
    
    node = nodes[current]
    if node.computed is not None:
        #print(node)
        return

    left = nodes[node.left].computed
    right = nodes[node.right].computed
    
    if left is None or node.left == target:
        # this way to humn
        # value = unkown <op> right
        if node.op == "+": value = value - right
        elif node.op == "-": value = value + right
        elif node.op == "*": value = value // right
        elif node.op == "/": value = value * right

        return reverse_evaluate(nodes, target, node.left, value)
    
    if right is None or node.right == target:
        # this way to humn
        # value = left <op> <unknown>
        if node.op == "+": value = value - left
        elif node.op == "-": value = left - value
        elif node.op == "*": value = value // left
        elif node.op == "/": value = left // value

        return reverse_evaluate(nodes, target, node.right, value)


SEARCH_NODE = "humn"

nodes = load()
print("Part 1:", evaluate(nodes, "root"))
nodes = load() # clean state
left = evaluate(nodes, nodes["root"].left, SEARCH_NODE)
right = evaluate(nodes, nodes["root"].right, SEARCH_NODE)
target_value = left if left is not None else right

result = reverse_evaluate(nodes, SEARCH_NODE, nodes["root"].left if left is None else nodes["root"].right, target_value)
print("Part 2:", result)