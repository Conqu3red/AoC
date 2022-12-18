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

def search(enabled: Set[str], location: str, time_left: int) -> int:
    best = 0

    for dest, cost in adjacency[location].items():
        if dest in enabled or time_left < cost:
            continue

        valve = valves[dest]
        change = valve.rate * (time_left - cost)
        flow = change

        result = search_memoize(enabled | {dest}, dest, time_left - cost)
        if flow + result > best:
            best = flow + result
    
    return best


s_cache = {}
def search_memoize(enabled: Set[str], location: str, time_left: int) -> int:
    key = (tuple(enabled), location, time_left)
    if key in s_cache:
        return s_cache[key]
    
    result = search(enabled, location, time_left)
    s_cache[key] = result

    return result


s = time.time()
best = search(set(), "AA", 30)
e = time.time()
print("Part 1:", best)
print(f"Completed in {e - s:.2f}s")
