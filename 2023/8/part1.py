def load():
    with open("input.txt") as f:
        commands, lines = f.read().split("\n\n")
    
    graph = {}
    for line in lines.split("\n"):
        print(line)
        key, children = line.split("=")
        graph[key.strip()] = children.strip()[1:-1].split(", ")
    
    return commands, graph

def main():
    commands, graph = load()
    steps = 0
    location = "AAA"
    while location != "ZZZ":
        command = 0 if commands[steps % len(commands)] == "L" else 1
        location = graph[location][command]
        steps += 1
    
    print(f"Part 1: {steps}")


main()