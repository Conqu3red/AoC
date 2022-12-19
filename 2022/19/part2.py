from typing import *
from dataclasses import dataclass
import math
import re
import collections
import time

LINE_EXPR = r"Blueprint \d+: Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian."

class Count(NamedTuple):
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0

@dataclass
class Blueprint:
    robot_costs: Dict[str, Count]

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
                "ore": Count(ore=int(m[0])),
                "clay": Count(ore=int(m[1])),
                "obsidian": Count(ore=int(m[2]), clay=int(m[3])),
                "geode": Count(ore=int(m[4]), obsidian=int(m[5]))
            }
        )
    
        blueprints.append(blueprint)
        

    return blueprints

def can_make_robot(type: str, blueprint: Blueprint, resource_counts: Count):
    return (
        blueprint.robot_costs[type].ore <= resource_counts.ore
        and blueprint.robot_costs[type].clay <= resource_counts.clay
        and blueprint.robot_costs[type].obsidian <= resource_counts.obsidian
    )

def step_state(state: State) -> State:
    return State(state.robot_counts, Count(*(v + state.robot_counts[i] for i, v in enumerate(state.resource_counts))))


def time_to_make_robot(type: str, blueprint: Blueprint, state: State) -> int:
    time = 0
    # if material required
    if blueprint.robot_costs[type].ore > 0:
        # if has no robots, can't ever make this type
        if state.robot_counts.ore == 0:
            return -1
        
        required = blueprint.robot_costs[type].ore - state.resource_counts.ore
        if required >= 0:
            time = max(time, math.ceil(required / state.robot_counts.ore))
    
    if blueprint.robot_costs[type].clay > 0:
        # if has no robots, can't ever make this type
        if state.robot_counts.clay == 0:
            return -1
        
        required = blueprint.robot_costs[type].clay - state.resource_counts.clay
        if required >= 0:
            time = max(time, math.ceil(required / state.robot_counts.clay))
    
    if blueprint.robot_costs[type].obsidian > 0:
        # if has no robots, can't ever make this type
        if state.robot_counts.obsidian == 0:
            return -1
        
        required = blueprint.robot_costs[type].obsidian - state.resource_counts.obsidian
        if required >= 0:
            time = max(time, math.ceil(required / state.robot_counts.obsidian))
    
    return time


# TODO: DFS is too inneficient, also construction may not be happening at quite the right time
def max_geodes(blueprint: Blueprint, t: int) -> int:

    visited: Set[State] = set() # FIXME: might need to store time as well
    stack: Deque[Tuple[int, State]] = collections.deque()

    stack.append((t, State(Count(1, 0, 0, 0), Count(0, 0, 0, 0)))) # start state

    best = 0

    max_required = Count(
        max(c.ore for c in blueprint.robot_costs.values()),
        max(c.clay for c in blueprint.robot_costs.values()),
        max(c.obsidian for c in blueprint.robot_costs.values()),
        math.inf
    )

    #print(state.robot_counts)
    while stack:
        time_left, state = stack.popleft() # pop?
        #print(best, time_left, state.resource_counts, state.robot_counts)

        # check if robots can be made
        made_robots = False
        for i, type in enumerate(blueprint.robot_costs.keys()):
            time_to_make = time_to_make_robot(type, blueprint, state)
            if time_to_make == -1 or time_left - time_to_make <= 0:
                continue
        
            if state.robot_counts[i] + 1 > max_required[i]:
                continue

            made_robots = True
            local = state
            """
            # robot can be afforded, build it, step state, push
            for _ in range(time_to_make + 1):
                local = step_state(local)
            
            assert time_to_make_robot(type, blueprint, local) == 0 """
            
            new_resource_counts = Count(
                local.resource_counts.ore + ((time_to_make + 1) * state.robot_counts.ore) - blueprint.robot_costs[type].ore,
                local.resource_counts.clay + ((time_to_make + 1) * state.robot_counts.clay) - blueprint.robot_costs[type].clay,
                local.resource_counts.obsidian + ((time_to_make + 1) * state.robot_counts.obsidian) - blueprint.robot_costs[type].obsidian,
                local.resource_counts.geode + ((time_to_make + 1) * state.robot_counts.geode),
            )

            robot_counts = list(local.robot_counts)
            robot_counts[i] += 1
            #print(i, type, time_left - time_to_make - 1, Count(*robot_counts))

            s = (time_left - (time_to_make + 1), State(Count(*robot_counts), new_resource_counts))
            if s[1] not in visited:
                #to_geode = time_to_make_robot("geode", blueprint, s[1])
                visited.add(s[1])
                #if s[1].robot_counts.geode > 1 or to_geode == -1 or time_left - time_to_make - 1 - to_geode > 0:
                stack.append(s)

        if len(stack) % 10_000 == 0:
            print(len(stack))


        # skip forward
        n_geodes = state.resource_counts.geode + time_left * state.robot_counts.geode
        """ while time_left > 0:
            state = step_state(state)
            time_left -= 1 """
        
        if n_geodes > best:
            best = n_geodes
            print(f"New best: {best}")
        #stack.appendleft((time_left, state))
        # TODO: add new states if geodes can be constructed using resources present in old state...
    
    return best


cache = {}
def max_geodes_memo(blueprint: Blueprint, state: State, time_left: int):
    key = (tuple(state.robot_counts.values()), tuple(state.resource_counts.values()), time_left)

    if key in cache:
        return cache[key]
    
    result = max_geodes(blueprint, state, time_left)
    cache[key] = result
    return result


blueprints = load()[:3]
total = 0

for i, blueprint in enumerate(blueprints):
    s = time.time()
    geodes = max_geodes(
        blueprint,
        32
    )
    e = time.time()

    robots_to_resources = {}

    print(f"Blueprint {i + 1} can produce {geodes} geodes. (Completed in {e - s:.2f}s)")
    total += (i + 1) * geodes

print("Part 1:", total)