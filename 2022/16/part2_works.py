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

def load():
    with open("input.txt") as f:
        lines = f.read().split("\n")
    
    valves: Dict[str, Valve] = {}

    for line in lines:
        label, flow_rate, tunnels = re.match(LINE_EXPR, line).groups()[:3]

        valves[label] = Valve(label, int(flow_rate), tunnels.split(", "))

    return valves

def path_to(valves: Dict[str, Valve], start: str, dest: str):
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

def value_graph(valves: Dict[str, Valve]) -> Dict[str, Dict[str, int]]:
    real_values = {k: v for k, v in valves.items() if v.rate > 0}
    adjacency = {}
    for v in {"AA": valves["AA"], **valves}:
        adjacency[v] = {}
        for v2 in real_values:
            if v != v2:
                adjacency[v][v2] = path_to(valves, v, v2)
    
    return adjacency

valves = load()
adjacency = value_graph(valves)


class Step(NamedTuple):
    name: str
    left: int

#@functools.lru_cache()
def get_paths(enabled: FrozenSet[str], location: str, time_left: int):
    paths: List[List[Step]] = []
    for dest, cost in adjacency[location].items():
        if time_left - cost < 0:
            continue
        
        new = get_paths(enabled | {dest}, dest, time_left - cost)
        for path in new:
            paths.append([Step(location, time_left)] + path)
    
    if time_left == 0:
        return [[Step(location, time_left)]]
    
    
    return paths
    

# maybe: always step the one that has higher time_left
def search(enabled: FrozenSet[str], location: str, location2: str, time_left: int, time_left2: int) -> int:
    best = 0

    done = False

    if time_left > time_left2:
        for dest, cost in adjacency[location].items():
            if dest in enabled or time_left - cost < 0:
                continue

            valve = valves[dest]
            flow = valve.rate * (time_left - cost)
            
            result = search_memoize(enabled | {dest}, dest, location2, time_left - cost, time_left2)
            if flow + result > best:
                best = flow + result
            
            done = True
    
    if not done:
        for dest, cost in adjacency[location2].items():
            if dest in enabled or time_left2 - cost < 0:
                continue

            valve = valves[dest]
            flow = valve.rate * (time_left2 - cost)
            
            result = search_memoize(enabled | {dest}, location, dest, time_left, time_left2 - cost)
            if flow + result > best:
                best = flow + result
    
    return best


s_cache = {}
def search_memoize(enabled: FrozenSet[str], location: str, location2: str, minute: int, minute2: int) -> int:
    key = (tuple(enabled), location, location2, minute, minute2)
    if key in s_cache:
        return s_cache[key]
    
    result = search(enabled, location, location2, minute, minute2)
    s_cache[key] = result

    return result


# DFS is way too inneficient
    
# maybe:
# traverse graph and construct the full acyclic graph with depth of 30?
# probably need to prune the graph a lot during creation (merge when possible)



valves = load()
s = time.time()
best = search(frozenset(), "AA", "AA", 26, 26)
e = time.time()
print("Part 2:", best)
print(f"Completed in {e - s:.2f}s")
