maximum = {"red": 12, "green": 13, "blue": 14}

def load():
    with open("input.txt") as f:
        lines = f.read().splitlines()
    
    data = []

    for line in lines:
        id_part, sections = line.split(": ")
        id = int(id_part.split(" ")[-1])
        line_data = []
        
        for section in sections.split("; "):
            counts = {}
            for part in section.split(", "):
                count, colour = part.split(" ")
                counts[colour] = int(count)
            line_data.append(counts)
        
        data.append((id, line_data))
    
    return data


def main():
    games = load()
    total = 0
    ptotal = 0
    for id, game in games:
        valid = True
        mins = {}
        for reveal in game:
            for colour, count in reveal.items():
                if count > maximum.get(colour, 0):
                    valid = False
                if colour not in mins or count > mins[colour]:
                    mins[colour] = count
        
        t = 1
        for count in mins.values():
            t *= count
        
        ptotal += t

        if valid:
            total += id
        
    
    print(f"Part 1: {total}")
    print(f"Part 2: {ptotal}")


main()