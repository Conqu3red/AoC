from typing import *
from dataclasses import dataclass

def apply_op(old: int, op: Tuple[str, str, str]) -> int:
    op1 = int(op[0]) if op[0] != "old" else old
    op2 = int(op[2]) if op[2] != "old" else old
    if op[1] == "+":
        return op1 + op2
    
    if op[1] == "*":
        return op1 * op2
    
    print(f"Unknown op {op}")

@dataclass
class Monkey:
    operation: Tuple[str, str, str]
    test: int
    branch_true: int
    branch_false: int
    items: List[int]
    n_inspected: int

with open("input.txt") as f:
    monkey_data = f.read().split("\n\n")

monkeys: Dict[int, Monkey] = {}

for data in monkey_data:
    lines = data.split("\n")
    monkey_id = int(lines[0].split(" ")[1][:-1])
    items = list(map(int, lines[1].split(": ")[1].split(", ")))
    op1, operator, op2 = lines[2].split("= ")[1].split(" ")
    test = int(lines[3].split(" ")[-1])
    branch_true = int(lines[4].split(" ")[-1])
    branch_false = int(lines[5].split(" ")[-1])

    monkeys[monkey_id] = Monkey((op1, operator, op2), test, branch_true, branch_false, items, 0)


for turns in range(20):
    for m in monkeys.values():
        for item in m.items:
            m.n_inspected += 1
            new = apply_op(item, m.operation) // 3
            if new % m.test == 0:
                monkeys[m.branch_true].items.append(new)
            else:
                monkeys[m.branch_false].items.append(new)
        
        m.items = []



monkey_business = sorted([m.n_inspected for m in monkeys.values()])[-2:]
print(f"Monkey business: {monkey_business[0] * monkey_business[1]}")