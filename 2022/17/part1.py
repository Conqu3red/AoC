from typing import *
import math

def load():
    with open("input.txt") as f:
        data = f.read()
    
    directions = [-1, 1]
    return [directions["<>".index(c)] for c in data]

def parse_rock(rock: str) -> Set[Tuple[int, int]]:
    points = set()
    rows = rock.split("\n")
    for y, row in enumerate(rows):
        for x, char in enumerate(row):
            if char == "#":
                points.add((x, len(rows) - y - 1))
    
    return points

string_rocks = [
    "####",

    ".#.\n"
    "###\n"
    ".#.",

    "..#\n"
    "..#\n"
    "###",

    "#\n"
    "#\n"
    "#\n"
    "#",

    "##\n"
    "##"
]

rocks = [parse_rock(rock) for rock in string_rocks]

def max_y(points: Set[Tuple[int, int]]):
    max_y = -math.inf
    for point in points:
        if point[1] > max_y:
            max_y = point[1]

    return max_y

def add_rock(field: Set[Tuple[int, int]], wind: List[int], rock: Set[Tuple[int, int]], turn: int, wind_index: int):
    max_rock_y = max_y(rock)
    max_field_y = max_y(field)

    rock_state = {(x + 2, max_field_y + 4 + y) for x, y in rock}


    
    while True:
        turn += 1
        if turn % 2 == 0:
            # move down
            new_rock = {(x, y - 1) for x, y in rock_state}
            intersect = field & new_rock
            if intersect:
                break
            
            rock_state = new_rock
        else:
            # gas push
            velocity = wind[wind_index % len(wind)]
            wind_index += 1

            new_rock = {(x + velocity, y) for x, y in rock_state}
            min_x = min(x for x, _ in new_rock)
            max_x = max(x for x, _ in new_rock)
            intersect = field & new_rock
            if intersect or min_x <= -1 or max_x >= 7:
                continue
            
            rock_state = new_rock
    
    # freeze rock in
    field |= rock_state

    return turn, wind_index


    
def main():
    wind = load()

    # add floor
    field = {(x, -1) for x in range(-1, 9)}
    turn = 0
    wind_index = 0
    for i in range(2022):
        rock = rocks[i % len(rocks)]
        
        turn, wind_index = add_rock(field, wind, rock, turn, wind_index)
    
    print("Part 1:", max_y(field) + 1)


if __name__ == "__main__":
    main()
        