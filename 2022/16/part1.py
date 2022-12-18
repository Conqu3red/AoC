from typing import *
import re
from dataclasses import dataclass
import time
import functools

LINE_EXPR = r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? ((\w+(, )?)+)"

@dataclass
class Valve:
    rate: int
    tunnels: List[str]

def load():
    with open("input.txt") as f:
        lines = f.read().split("\n")
    
    valves: Dict[str, Valve] = {}

    for line in lines:
        label, flow_rate, tunnels = re.match(LINE_EXPR, line).groups()[:3]

        valves[label] = Valve(int(flow_rate), tunnels.split(", "))

    return valves

valves = load()

def search(enabled: Set[str], location: str, minute: int) -> int:
    valve = valves[location]

    if minute >= 30:
        #print(total_flow)
        return 0
    
    best = 0

    # branch: enable valve
    if valve.rate != 0 and location not in enabled:
        enabled.add(location)
        minute += 1
        change = valve.rate * (30 - minute)
        flow = change

        result = search_memoize(enabled, location, minute)
        if flow + result > best:
            best = flow + result
        
        enabled.remove(location)
        minute -= 1
    
    # branch: traverse to locations
    for new_location in valve.tunnels:
        #if location in enabled:
        #    continue
        minute += 1

        result = search_memoize(enabled, new_location, minute)
        if result > best:
            best = result
        
        minute -= 1
    
    return best


s_cache = {}
def search_memoize(enabled: Set[str], location: str, minute: int) -> int:
    key = (tuple(enabled), location, minute)
    if key in s_cache:
        return s_cache[key]
    
    result = search(enabled, location, minute)
    s_cache[key] = result

    return result


# DFS is way too inneficient
    
# maybe:
# traverse graph and construct the full acyclic graph with depth of 30?
# probably need to prune the graph a lot during creation (merge when possible)



valves = load()
s = time.time()
best = search(set(), "AA", 0)
e = time.time()
print("Part 1:", best)
print(f"Completed in {e - s:.2f}s")
