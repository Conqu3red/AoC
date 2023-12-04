from dataclasses import dataclass

@dataclass
class Game:
    matches: int
    count: int = 1

def main():
    with open("input.txt") as f:
        lines = f.read().splitlines()

    total = 0
    games = {}

    for game in lines:
        identifier, stuff = game.split(": ")
        id = int(identifier.split(" ")[-1])
        target, yours = stuff.split(" | ")
        matches = set(target.split(" ")) & set(yours.split(" ")) - {""}
        games[id] = Game(len(matches))
        if matches:
            total += 2 ** (len(matches) - 1)
    
    for id, game in games.items():
        if game.count > 0:
            for i in range(id + 1, id + game.matches + 1):
                games[i].count += game.count
    
    p2 = sum(game.count for game in games.values())
    
    print(f"Part 1: {total}")
    print(f"Part 2: {p2}")


main()