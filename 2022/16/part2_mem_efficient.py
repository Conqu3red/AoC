from typing import *
import re
from dataclasses import dataclass
import time
import functools
import collections

LINE_EXPR = r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? ((\w+(, )?)+)"

@dataclass
class Valve:
    name: str
    rate: int
    tunnels: List[str]

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
        valves[valve_lookup[k]] = Valve(k, rate, [valve_lookup[t] for t in tunnels])

    return valve_lookup, valves

def path_to(valves: Dict[int, Valve], start: int, dest: int):
    visited = set()
    queue = collections.deque([start, v] for v in valves[start].tunnels)
    while queue:
        path = queue.popleft()
        if path[-1] == dest:
            return len(path)
        for t in valves[path[-1]].tunnels:
            if t not in visited:
                visited.add(t)
                queue.append(path + [t])

def value_graph(valve_lookup: Dict[str, int], valves: Dict[int, Valve]) -> Dict[int, Dict[int, int]]:
    real_values = {k: v for k, v in valves.items() if v.rate > 0}
    adjacency = {}
    for v in {valve_lookup["AA"]: valves[valve_lookup["AA"]], **valves}:
        adjacency[v] = {}
        for v2 in real_values:
            if v != v2:
                adjacency[v][v2] = path_to(valves, v, v2)
    
    return adjacency

valve_lookup, valves = load()
adjacency = value_graph(valve_lookup, valves)

# maybe: always step the one that has higher time_left
def search(enabled: int, location: int, location2: int, time_left: int, time_left2: int) -> int:
    best = 0

    done = False

    if time_left > time_left2:
        for dest, cost in adjacency[location].items():
            if (dest & enabled) or time_left - cost < 0:
                continue

            valve = valves[dest]
            flow = valve.rate * (time_left - cost)
            
            result = search_memoize(enabled | dest, dest, location2, time_left - cost, time_left2)
            if flow + result > best:
                best = flow + result
            
            done = True
    
    if not done:
        for dest, cost in adjacency[location2].items():
            if (dest & enabled) or time_left2 - cost < 0:
                continue
        
            valve = valves[dest]
            flow = valve.rate * (time_left2 - cost)
            
            result = search_memoize(enabled | dest, location, dest, time_left, time_left2 - cost)
            if flow + result > best:
                best = flow + result
    
    return best


s_cache = {}
def search_memoize(enabled: int, location: int, location2: int, minute: int, minute2: int) -> int:
    key = (enabled, location, location2, minute, minute2)
    if key in s_cache:
        return s_cache[key]
    
    result = search(enabled, location, location2, minute, minute2)
    s_cache[key] = result

    return result


# DFS is way too inneficient
    
# maybe:
# traverse graph and construct the full acyclic graph with depth of 30?
# probably need to prune the graph a lot during creation (merge when possible)

s = time.time()
best = search(0, valve_lookup["AA"], valve_lookup["AA"], 26, 26)
e = time.time()
print("Part 2:", best)
print(f"Completed in {e - s:.2f}s")
