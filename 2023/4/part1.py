def main():
    with open("input.txt") as f:
        games = f.read().splitlines()

    total = 0

    for game in games:
        stuff = game.split(": ")[1]
        target, yours = stuff.split(" | ")
        matches = (set(target.split(" ")) & set(yours.split(" "))) - {""}
        if matches:
            score = 2 ** (len(matches) - 1)
            total += score
    
    print(f"Part 1: {total}")


main()