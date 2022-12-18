from typing import *
import math
from dataclasses import dataclass

def load():
    with open("input.txt") as f:
        data = f.read()
    
    directions = [-1, 1]
    return [directions["<>".index(c)] for c in data]

def parse_rock(rock: str) -> List[List[bool]]:
    points = []
    rows = rock.split("\n")
    for row in reversed(rows):
        points.append([])
        for char in row:
            points[-1].append(char == "#")
    
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

@dataclass
class Field:
    rows: List[List[bool]] # cols[0] has y of floor_y + 1
    floor_y: int

# BUG: this doesn't account for weird gaps possibly?

class State(NamedTuple):
    rock_index: int
    wind_index: int
    board_state: Tuple[Tuple[bool, ...], ...]

class FieldState(NamedTuple):
    rock_count: int
    floor_y: int

def add_rock(field: Field, wind: List[int], rock_index: int, turn: int, wind_index: int):
    rock = rocks[rock_index % len(rocks)]
    max_field_y = -1
    for _y, row in enumerate(reversed(field.rows)):
        y = len(field.rows) - _y - 1
        if any(row):
            max_field_y = y
            break
    
    rock_x = 2
    rock_y = max_field_y + 4
    
    while True:
        turn += 1
        #print(rock_x, rock_y)
        if turn % 2 == 0:
            # move down
            rock_y -= 1
            intersect = False

            for local_y, row in enumerate(rock):
                for local_x, value in enumerate(row):
                    index_y = rock_y + local_y
                    if index_y >= len(field.rows):
                        break

                    if index_y <= -1:
                        intersect = True
                        break

                    index_x = rock_x + local_x
                    #print(index_x)
                    field_value = field.rows[index_y][index_x]
                    
                    if field_value and value:
                        intersect = True
                        break
                
                if intersect:
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
            for local_y, row in enumerate(rock):
                for local_x, value in enumerate(row):
                    index_y = rock_y + local_y
                    index_x = rock_x + local_x

                    if 0 > index_y or index_y >= len(field.rows):
                        break

                    if -1 >= index_x or index_x >= 7:
                        intersect = True
                        break
                    
                    field_value = field.rows[index_y][index_x]
                    
                    if field_value and value:
                        intersect = True
                        break
                
                if intersect:
                    break
            
            if intersect or rock_x < 0 or rock_x + len(rock[0]) - 1 >= 7: #or rock_x <= -1 or rock_x + len(rock) - 1 >= 7:
                rock_x -= velocity
                continue
            
    
    #print(rock_x, rock_y)
    # freeze rock in
    #field |= rock_state
    for local_y, row in enumerate(rock):
        index_y = rock_y + local_y
        for local_x, value in enumerate(row):
            index_x = rock_x + local_x

            while index_y >= len(field.rows):
                field.rows.append([False for _ in range(7)])
            
            
            field.rows[index_y][index_x] |= value
    
    #print(field)

    return turn, wind_index


def lowest_accessible(field: Field, index_x: int, index_y: int) -> int:
    lowest = index_y
    for y in range(index_y - 1, -1, -1):
        if field.rows[y][index_x]:
            lowest = min(lowest, y)
            
            if index_x > 0 and not field.rows[y + 1][index_x - 1]:
                # explore left
                lowest = min(lowest, lowest_accessible(field, index_x - 1, y))
            if index_x < 6 and not field.rows[y + 1][index_x + 1]:
                # explore right
                lowest = min(lowest, lowest_accessible(field, index_x + 1, y))
            
            break

    return lowest

def render_compressed(compressed: Tuple[Tuple[int, ...], ...]):
    for row in reversed(compressed):
        for entry in row:
            print("#" if entry else ".", end="")
        print()
    
def main():
    wind = load()

    tetris_lookup: Dict[State, FieldState] = {}
    # add floor
    field = Field([], floor_y=-1) # {(x, -1) for x in range(-1, 9)}
    turn = 0
    wind_index = 0
    rock_index = 0
    LIMIT = 1_000_000_000_000
    while rock_index < LIMIT:
        if rock_index % 10_000 == 0:
            print(f"{100 * rock_index / 1_000_000_000_000:.6f}%")
        
        turn, wind_index = add_rock(field, wind, rock_index, turn, wind_index)

        lowest = min(lowest_accessible(field, x, len(field.rows) - 1) for x in range(7))
        compressed = tuple(tuple(row) for row in field.rows[lowest:])


        # 1514285714288
        key = State(rock_index % len(rocks), wind_index % len(wind), compressed)
        field.floor_y += lowest
        field.rows = field.rows[lowest:]

        if key in tetris_lookup:
            #print("REPEAT", key)
            # skip as many as possile
            old_rock_index, old_floor_y = tetris_lookup[key]
            rocks_diff = rock_index - old_rock_index
            rocks_left = (LIMIT - rock_index)
            times_skipped = (rocks_left // rocks_diff)
            to_skip = rocks_diff * times_skipped

            if to_skip:
                print(f"REPEAT with {key.rock_index}, {key.wind_index}:")
                render_compressed(compressed)
                print("------------")
                print(f"Skip {to_skip} rocks, adding height of {times_skipped * (field.floor_y - old_floor_y)}")
                rock_index += times_skipped * rocks_diff
                field.floor_y += times_skipped * (field.floor_y - old_floor_y)

        else:
            tetris_lookup[key] = FieldState(rock_index, field.floor_y)


        
        rock_index += 1


    max_field_y = -1
    for _y, row in enumerate(reversed(field.rows)):
        y = len(field.rows) - _y - 1
        if any(row):
            max_field_y = y
            break
    
    print("Part 2:", field.floor_y + max_field_y + 2)


if __name__ == "__main__":
    main()
        