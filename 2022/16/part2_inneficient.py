from typing import *
import re
from dataclasses import dataclass
import time
import functools

LINE_EXPR = r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? ((\w+(, )?)+)"

@dataclass
class Valve:
    rate: int
    tunnels: List[int]

def load() -> Tuple[Dict[str, int], Dict[int, Valve]]:
    with open("input.txt") as f:
        lines = f.read().split("\n")
    
    temp_valves: Dict[str, Tuple[int, List[str]]] = {}

    for line in lines:
        label, flow_rate, tunnels = re.match(LINE_EXPR, line).groups()[:3]

        temp_valves[label] = (int(flow_rate), tunnels.split(", "))
    
    valve_lookup: Dict[str, int] = {}
    for i, k in enumerate(temp_valves.keys()):
        valve_lookup[k] = 1 << i + 1

    valves: Dict[int, Valve] = {}
    for k, (rate, tunnels) in temp_valves.items():
        valves[valve_lookup[k]] = Valve(rate, [valve_lookup[t] for t in tunnels])

    return valve_lookup, valves

valve_lookup, valves = load()

def search(enabled: int, locations: Tuple[int, int], turn: int, minute: int) -> int:
    turn = int(not turn)
    valve = valves[locations[turn]]

    if minute >= 26:
        #print(total_flow)
        return 0
    
    best = 0

    # branch: enable valve
    if valve.rate != 0 and (enabled & locations[turn]) == 0:
        enabled |= locations[turn]
        if turn == 1: minute += 1
        change = valve.rate * (26 - minute)
        flow = change

        result = search_memoize(enabled, locations, turn, minute)
        if flow + result > best:
            best = flow + result
        
        enabled ^= locations[turn]
        if turn == 1: minute -= 1
    
    # branch: traverse to locations
    for new_location in valve.tunnels:
        #if location in enabled:
        #    continue
        if turn == 1: minute += 1


        new = (new_location, locations[1]) if turn == 0 else (locations[0], new_location)

        result = search_memoize(enabled, new, turn, minute)
        if result > best:
            best = result
        
        if turn == 1: minute -= 1
    
    return best


s_cache = {}
def search_memoize(enabled: int, locations: Tuple[int, int], turn: int, minute: int) -> int:
    key = (enabled, locations, minute) # maybe turn?
    if key in s_cache:
        return s_cache[key]
    
    result = search(enabled, locations, turn, minute)
    if turn == 1: s_cache[key] = result

    return result


# DFS is way too inneficient
    
# maybe:
# traverse graph and construct the full acyclic graph with depth of 30?
# probably need to prune the graph a lot during creation (merge when possible)


s = time.time()
best = search_memoize(0, (valve_lookup["AA"], valve_lookup["AA"]), 0, 0)
e = time.time()
print("Part 1:", best)
print(f"Completed in {e - s:.2f}s")
print(len(s_cache))