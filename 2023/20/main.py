from collections import deque
import math

def load():
    with open("input.txt") as f:
        lines = f.read().splitlines()
    
    states = {}
    transitions = {}
    for line in lines:
        start, nexts = line.split(" -> ")
        if start[0] == "%":
            states[start[1:]] = ["%", False]
        elif start[0] == "&":
            states[start[1:]] = ["&", {}]
        else:
            states[start] = [None, False]
    
    for line in lines:
        start, nexts = line.split(" -> ")
        if start[0] == "%":
            start = start[1:]
        elif start[0] == "&":
            start = start[1:]
        
        transitions[start] = []
        for p in nexts.split(", "):
            if p not in states:
                states[p] = [None, False]
            if states[p][0] == "&":
                states[p][1][start] = False
            transitions[start].append(p) 
    
    return states, transitions

def push_button(states, transitions, counts, check_low=None):
    queue = deque()
    counts[0] += 1
    queue.append(("button", "broadcaster", False))

    found = False
    
    while queue:
        prev, target, state = queue.popleft()
        if check_low and prev == check_low and state == False:
            found = True

        output = None
        if states[target][0] == "%": # flip-flop
            if not state:
                states[target][1] = not states[target][1]
                output = states[target][1]
        elif states[target][0] == "&":
            states[target][1][prev] = state
            output = not all(states[target][1].values())
        else:
            states[target][1] = state
            output = state
        
        if output is not None and target in transitions:
            for dest in transitions[target]:
                counts[output] += 1
                queue.append((target, dest, output))
    
    return found

def accessible(start, transitions):
    visited = set()
    queue = [start]
    while queue:
        loc = queue.pop()
        if loc in visited:
            continue
        visited.add(loc)
        if loc in transitions:
            for l in transitions[loc]:
                queue.append(l)
    
    return visited


def part2():
    states, transitions = load()
    end_collector = next(t for t, vs in transitions.items() if "rx" in vs)
    inversors = {t for t, vs in transitions.items() if end_collector in vs}
    starts = transitions["broadcaster"]

    nums = []
    
    for st in starts:
        states, transitions = load()
        access = accessible(st, transitions)
        transitions = {k: v for k, v in transitions.items() if k in access}
        transitions["broadcaster"] = [st]
        conjunction  = next(s for s in access - inversors - {end_collector} if states[s][0] == "&")

        s = 0
        found = False
        while not found:
            found = push_button(states, transitions, [0, 0], check_low=conjunction)
            s += 1
        
        nums.append(s)
    
    return math.lcm(*nums)
            
        
            

def main():
    states, transitions = load()
    print(states)
    print(transitions)

    counts = [0, 0]
    for i in range(1000):
        push_button(states, transitions, counts)
    p1 = counts[0] * counts[1]
    print(f"Part 1: {p1}")
    
    p2 = part2()
    print(f"Part 2: {p2}")

main()