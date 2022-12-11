from typing import *
from dataclasses import dataclass
import time

def apply_op(old: Dict[int, int], op: Tuple[str, str, str]) -> int:
    new = {}
    for modulo, v in old.items():
        if op[1] == "+":
            new[modulo] = v + int(op[2])
        elif op[1] == "*":
            if op[2] == "old":
                new[modulo] = v * v
            else:
                new[modulo] = v * int(op[2])
    
    return {k: v % k for k, v in new.items()}

@dataclass
class Monkey:
    operation: Tuple[str, str, str]
    test: int
    branch_true: int
    branch_false: int
    start_items: List[int]
    items: List[Dict[int, int]]
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

    monkeys[monkey_id] = Monkey((op1, operator, op2), test, branch_true, branch_false, items, [], 0)

for m in monkeys.values():
    for item in m.start_items:
        m.items.append({})
        for m2 in monkeys.values():
            m.items[-1][m2.test] = item

s = time.time()
for round in range(10_000):
    for m in monkeys.values():
        for item in m.items:
            m.n_inspected += 1
            new = apply_op(item, m.operation)
            if new[m.test] == 0:
                monkeys[m.branch_true].items.append(new)
            else:
                monkeys[m.branch_false].items.append(new)
        
        m.items = []

e = time.time()

for k, m in monkeys.items():
    print(k, m.n_inspected)


monkey_business = sorted([m.n_inspected for m in monkeys.values()])[-2:]
print(f"Monkey business: {monkey_business[0] * monkey_business[1]}")
print(f"Done in {e - s:.1f}s")