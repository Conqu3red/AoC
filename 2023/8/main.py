import math

def load():
    with open("input.txt") as f:
        commands, lines = f.read().split("\n\n")
    
    graph = {}
    for line in lines.split("\n"):
        key, children = line.split("=")
        graph[key.strip()] = children.strip()[1:-1].split(", ")
    return commands, graph

def get_cycle(commands, graph, location, any_z: bool):
    steps = 0
    while not location.endswith("Z") if any_z else location != "ZZZ":
        command = commands[steps % len(commands)] == "R"
        location = graph[location][command]
        steps += 1
    return steps

def main():
    commands, graph = load()
    p1 = get_cycle(commands, graph, "AAA", any_z=False)
    p2 = math.lcm(*(get_cycle(commands, graph, loc, any_z=True) for loc in graph if loc.endswith("A")))
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")

main()