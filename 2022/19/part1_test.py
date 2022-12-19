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

# TODO: DFS is too inneficient, also construction may not be happening at quite the right time
def max_geodes(blueprint: Blueprint, time_left: int) -> int:
    states: Set[State] = set()
    states.add(State(Count(1, 0, 0, 0), Count(0, 0, 0, 0))) # start state

    #print(state.robot_counts)
    for m in range(time_left, -1, -1):
        new_states: Set[State] = set()
        # step each state
        for state in states:
            new_state = State(state.robot_counts, Count(*(v + state.robot_counts[i] for i, v in enumerate(state.resource_counts))))

            # TODO: add new states if geodes can be constructed using resources present in old state...

            for i, type in enumerate(blueprint.robot_costs.keys()):
                if not can_make_robot(type, blueprint, state.resource_counts):
                    continue
                
                new_resource_counts = Count(
                    new_state.resource_counts.ore - blueprint.robot_costs[type].get("ore", 0),
                    new_state.resource_counts.clay - blueprint.robot_costs[type].get("clay", 0),
                    new_state.resource_counts.obsidian - blueprint.robot_costs[type].get("obsidian", 0),
                    new_state.resource_counts.geode,
                )

                robot_counts = list(new_state.robot_counts)
                robot_counts[i] += 1

                new_states.add(State(new_resource_counts, Count(*robot_counts)))
            
            new_states.add(new_state)
        
        states = new_states
        print(f"Minute {m}, states: {len(states)}")


cache = {}
def max_geodes_memo(blueprint: Blueprint, state: State, time_left: int):
    key = (tuple(state.robot_counts.values()), tuple(state.resource_counts.values()), time_left)

    if key in cache:
        return cache[key]
    
    result = max_geodes(blueprint, state, time_left)
    cache[key] = result
    return result


blueprints = load()
print(
    max_geodes(
        blueprints[0],
        24
    )
)