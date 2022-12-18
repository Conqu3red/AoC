from typing import *
import math
from dataclasses import dataclass

def load():
    with open("input.txt") as f:
        data = f.read()
    
    directions = [-1, 1]
    return [directions["<>".index(c)] for c in data]

def parse_rock(rock: str) -> List[Tuple[int, int]]:
    lows_and_highs = []
    rows = rock.split("\n")
    for x in range(len(rows[0])):
        low_y = math.inf
        high_y = -math.inf
        for y in range(len(rows)):
            char = rows[y][x]
            if char == "#":
                true_y = len(rows) - y - 1
                if true_y < low_y:
                    low_y = true_y
                if true_y > high_y:
                    high_y = true_y
        
        lows_and_highs.append((low_y, high_y))
    
    return lows_and_highs

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

@dataclass
class Col:
    top_value: int

@dataclass
class Field:
    cols: List[Col]

# BUG: this doesn't account for weird gaps possibly?

def add_rock(field: Field, wind: List[int], rock: List[Tuple[int, int]], turn: int, wind_index: int):
    max_field_y = max(col.top_value for col in field.cols)

    rock_x = 2
    rock_y = max_field_y + 4
    
    while True:
        turn += 1
        if turn % 2 == 0:
            # move down
            rock_y -= 1
            intersect = False

            for x, y_range in enumerate(rock):
                field_y = field.cols[x + rock_x].top_value
                if rock_y + y_range[0] <= field_y:
                    intersect = True
                    break

            if intersect:
                rock_y += 1
                break
            
        else:
            # gas push
            velocity = wind[wind_index % len(wind)]
            wind_index += 1

            rock_x += velocity
            intersect = False
            for x, y_range in enumerate(rock):
                field_y = field.cols[x + rock_x].top_value
                if y_range[0] <= field_y:
                    intersect = True
                    break
            
            if intersect or rock_x <= -1 or rock_x + len(rock) - 1 >= 7:
                rock_x -= velocity
                continue
            
    
    print(rock_x, rock_y)
    # freeze rock in
    #field |= rock_state
    for x, y_range in enumerate(rock):
        field.cols[x + rock_x].top_value = max(field.cols[x + rock_x].top_value, rock_y + y_range[1])

    return turn, wind_index


    
def main():
    wind = load()

    # add floor
    field = Field([Col(-1) for _ in range(8)])#{(x, -1) for x in range(-1, 9)}
    turn = 0
    wind_index = 0
    for i in range(2022):
        if i % 1_000_000 == 0:
            print(f"{100 * i / 1_000_000_000_000:.6f}%")
        rock = rocks[i % len(rocks)]
        
        turn, wind_index = add_rock(field, wind, rock, turn, wind_index)
    
    print("Part 1:", max(col.top_value for col in field.cols) + 1)


if __name__ == "__main__":
    main()
        