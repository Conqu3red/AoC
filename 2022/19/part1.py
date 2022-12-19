from typing import *
from dataclasses import dataclass
import math
import re
import time

LINE_EXPR = r"Blueprint \d+: Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian."

class Cost(NamedTuple):
    ore: int
    clay: int
    obsidian: int

@dataclass
class Blueprint:
    robot_costs: Dict[str, Dict[str, int]]

@dataclass
class State:
    robot_counts: Dict[str, int]
    resource_counts: Dict[str, int]

def load():
    with open("input.txt") as f:
        lines = f.read().split("\n")

    blueprints = []

    for line in lines:
        m = re.match(LINE_EXPR, line).groups()

        blueprint = Blueprint(
            {
                "ore": {"ore": int(m[0])},
                "clay": {"ore": int(m[1])},
                "obsidian": {"ore": int(m[2]), "clay": int(m[3])},
                "geode": {"ore": int(m[4]), "obsidian": int(m[5])}
            }
        )
    
        blueprints.append(blueprint)
        

    return blueprints

def can_make_robot(type: str, blueprint: Blueprint, resource_counts: Dict[str, int]):
    for t, amount in resource_counts.items():
        if blueprint.robot_costs[type].get(t, 0) > amount:
            return False
    return True

# TODO: DFS is too inneficient, also construction may not be happening at quite the right time
def max_geodes(blueprint: Blueprint, state: State, time_left: int, can_create=True) -> int:
    #print(state.robot_counts)
    if time_left == 0:
        return state.resource_counts["geode"]
    
    # step all resource counts
    new_state = State(state.robot_counts, {k: v + state.robot_counts[k] for k, v in state.resource_counts.items()})

    # 1 minute to contruct a new robot
    best = 0
    for type in new_state.robot_counts.keys():
        if not can_create or not can_make_robot(type, blueprint, state.resource_counts):
            continue
        
        new_state.robot_counts[type] += 1
        for t, amount in blueprint.robot_costs[type].items():
            new_state.resource_counts[t] -= amount

        best = max(best, max_geodes_memo(blueprint, new_state, time_left - 1, can_create=False))

        for t, amount in blueprint.robot_costs[type].items():
            new_state.resource_counts[t] += amount
        new_state.robot_counts[type] -= 1
    
    best = max(best, max_geodes_memo(blueprint, new_state, time_left - 1, can_create=True))

    return best


cache = {}
def max_geodes_memo(blueprint: Blueprint, state: State, time_left: int, can_create=True):
    key = (tuple(state.robot_counts.values()), tuple(state.resource_counts.values()), time_left)

    if key in cache:
        return cache[key]
    
    result = max_geodes(blueprint, state, time_left, can_create)
    cache[key] = result
    return result

blueprints = load()
total = 0

for i, blueprint in enumerate(blueprints):
    s = time.time()
    geodes = max_geodes_memo(
        blueprint,
        State(
            {"ore": 1, "clay": 0, "obsidian": 0, "geode": 0},
            {"ore": 0, "clay": 0, "obsidian": 0, "geode": 0}
        ),
        24
    )
    e = time.time()

    cache = {}

    print(f"Blueprint {i + 1} can produce {geodes} geodes. (Completed in {e - s:.2f}s)")
    total += (i + 1) * geodes

print("Part 1:", total)