from typing import *
from dataclasses import dataclass
import math
import re
import collections

LINE_EXPR = r"Blueprint \d+: Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian."

@dataclass
class Blueprint:
    robot_costs: Dict[str, Dict[str, int]]

class Count(NamedTuple):
    ore: int
    clay: int
    obsidian: int
    geode: int

@dataclass(unsafe_hash=True)
class State:
    robot_counts: Count
    resource_counts: Count

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

def can_make_robot(type: str, blueprint: Blueprint, resource_counts: Count):
    return (
        blueprint.robot_costs[type].get("ore", 0) <= resource_counts.ore
        and blueprint.robot_costs[type].get("clay", 0) <= resource_counts.clay
        and blueprint.robot_costs[type].get("obsidian", 0) <= resource_counts.obsidian
    )

def step_state(state: State) -> State:
    return State(state.robot_counts, Count(*(v + state.robot_counts[i] for i, v in enumerate(state.resource_counts))))


def time_to_make_robot(type: str, blueprint: Blueprint, state: State) -> int:
    time = 0
    # if material required
    if "ore" in blueprint.robot_costs[type]:
        # if has no robots, can't ever make this type
        if state.robot_counts.ore == 0:
            return -1
        
        required = blueprint.robot_costs[type]["ore"] - state.resource_counts.ore
        if required >= 0:
            time = max(time, math.ceil(required / state.robot_counts.ore))
    
    if "clay" in blueprint.robot_costs[type]:
        # if has no robots, can't ever make this type
        if state.robot_counts.clay == 0:
            return -1
        
        required = blueprint.robot_costs[type]["clay"] - state.resource_counts.clay
        if required >= 0:
            time = max(time, math.ceil(required / state.robot_counts.clay))
    
    if "obsidian" in blueprint.robot_costs[type]:
        # if has no robots, can't ever make this type
        if state.robot_counts.obsidian == 0:
            return -1
        
        required = blueprint.robot_costs[type]["obsidian"] - state.resource_counts.obsidian
        if required >= 0:
            time = max(time, math.ceil(required / state.robot_counts.obsidian))
    
    return time


# TODO: DFS is too inneficient, also construction may not be happening at quite the right time
def max_geodes(blueprint: Blueprint, state: State, time_left: int) -> int:
    best = 0
    #print(best, time_left, state.resource_counts, state.robot_counts)

    # check if robots can be made
    made_robots = False
    for i, type in enumerate(blueprint.robot_costs.keys()):
        time_to_make = time_to_make_robot(type, blueprint, state)
        if time_to_make == -1 or time_left - time_to_make <= 0:
            continue

        made_robots = True
        local = state
        # robot can be afforded, build it, step state, push
        for _ in range(time_to_make + 1):
            local = step_state(local)
        
        assert time_to_make_robot(type, blueprint, local) == 0
        
        new_resource_counts = Count(
            local.resource_counts.ore - blueprint.robot_costs[type].get("ore", 0),
            local.resource_counts.clay - blueprint.robot_costs[type].get("clay", 0),
            local.resource_counts.obsidian - blueprint.robot_costs[type].get("obsidian", 0),
            local.resource_counts.geode,
        )

        robot_counts = list(local.robot_counts)
        robot_counts[i] += 1
        #print(i, type, time_left - time_to_make - 1, Count(*robot_counts))

        s = (time_left - (time_to_make + 1), State(Count(*robot_counts), new_resource_counts))
        #if s not in visited:
        new = max_geodes_memo(blueprint, State(Count(*robot_counts), new_resource_counts), time_left - time_to_make - 1)
        if new > best:
            best = new

    # skip forward
    while time_left > 0:
        state = step_state(state)
        time_left -= 1
    
    if state.resource_counts.geode > best:
        best = state.resource_counts.geode
        #print(f"New best: {best}")
    #stack.appendleft((time_left, state))
    # TODO: add new states if geodes can be constructed using resources present in old state...
    
    return best


cache = {}
def max_geodes_memo(blueprint: Blueprint, state: State, time_left: int) -> int:
    key = (state, time_left)

    if key in cache:
        return cache[key]
    
    result = max_geodes(blueprint, state, time_left)
    cache[key] = result
    return result


blueprints = load()
print(
    max_geodes(
        blueprints[0],
        State(Count(1, 0, 0, 0), Count(0, 0, 0, 0)),
        24
    )
)