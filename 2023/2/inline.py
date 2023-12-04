maximum = {"red": 12, "green": 13, "blue": 14}

def main():
    with open("input.txt") as f:
        lines = f.read().splitlines()
    
    total = 0
    ptotal = 0
    
    for line in lines:
        valid = True
        mins = {}
        id_part, sections = line.split(": ")
        id = int(id_part.split(" ")[-1])
        
        for section in sections.split("; "):
            for part in section.split(", "):
                count, colour = part.split(" ")
                count = int(count)
                if count > maximum[colour]:
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