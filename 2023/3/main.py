
def main():
    with open("input.txt")as f:
        lines = f.read().splitlines()

    total = 0

    ratios = {}
    
    for y, line in enumerate(lines):
        num = ""
        for x, char in enumerate(line + "."):
            if char.isdigit():
                num += char
            elif num:
                valid = False              
                for cy in range(y-1, y+2):
                    for cx in range(x - len(num) - 1, x + 1):
                        if 0 <= cy < len(lines) and 0 <= cx < len(lines[cy]) and not lines[cy][cx].isdigit() and lines[cy][cx] != ".":
                            valid = True
                            if lines[cy][cx] == "*":
                                adj, ratio = ratios.get((cy, cx), (0, 1))
                                ratios[cy, cx] = adj + 1, ratio * int(num)
                
                if valid:
                    total += int(num)
                num = ""

    ratio_sum = sum(ratio for adj, ratio in ratios.values() if adj == 2)        
            
    print(f"Part 1: {total}")
    print(f"Part 2: {ratio_sum}")


main()