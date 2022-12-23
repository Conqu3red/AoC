from typing import *
from dataclasses import dataclass
import math


@dataclass
class ElfState:
    proposed_movement: Optional[Tuple[int, int]] = None


def load() -> Dict[Tuple[int, int], ElfState]:
    with open("input.txt") as f:
        data = f.read()

    elves: Dict[Tuple[int, int], ElfState] = {}

    for y, line in enumerate(data.split("\n")):
        for x, char in enumerate(line):
            if char == "#":
                elves[(x, y)] = ElfState()
    
    return elves


# N, S, W, E
DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]


def step_elves(elves: Dict[Tuple[int, int], ElfState], directions: List[Tuple[int, int]]):
    proposed_movements: Dict[Tuple[int, int], int] = {}
    new_elves: Dict[Tuple[int, int], ElfState] = {}

    # first half
    for elf in elves:
        neighbour_count = 0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx != 0 or dy != 0:
                    if (elf[0] + dx, elf[1] + dy) in elves:
                        neighbour_count += 1
        
        if neighbour_count == 0:
            continue
    
        # propose movement
        for direction in directions:
            dx, dy = direction
            valid = True
            if dx == 0:
                for dx in range(-1, 2):
                    if (elf[0] + dx, elf[1] + dy) in elves:
                        valid = False
            else:
                for dy in range(-1, 2):
                    if (elf[0] + dx, elf[1] + dy) in elves:
                        valid = False
            
            if not valid:
                continue

            proposed_movement = (elf[0] + direction[0], elf[1] + direction[1])
            #print("PROPOSE", direction)
            elves[elf].proposed_movement = proposed_movement
            proposed_movements[proposed_movement] = proposed_movements.get(proposed_movement, 0) + 1
            break
    
    # second half, try do all movements
    movement = False
    for position in elves:
        elf = elves[position]
        if elf.proposed_movement is not None and proposed_movements[elf.proposed_movement] == 1:
            new_elves[elf.proposed_movement] = ElfState()
            movement = True
        else:
            new_elves[position] = ElfState()

    # shift direction order
    directions = directions[1:] + [directions[0]]

    return new_elves, directions, movement


def render_board(elves: Dict[Tuple[int, int], ElfState]):
    min_x = math.inf
    max_x = -math.inf
    min_y = math.inf
    max_y = -math.inf

    for x, y in elves:
        min_x = min(x, min_x)
        max_x = max(x, max_x)
        min_y = min(y, min_y)
        max_y = max(y, max_y)
    
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (x, y) in elves:
                elf = elves[(x, y)]
                #if elf.proposed_movement is not None:
                print("#", end="")
            else:
                print(".", end="")
        print()
        

def area(elves: Dict[Tuple[int, int], ElfState]):
    min_x = math.inf
    max_x = -math.inf
    min_y = math.inf
    max_y = -math.inf

    for x, y in elves:
        min_x = min(x, min_x)
        max_x = max(x, max_x)
        min_y = min(y, min_y)
        max_y = max(y, max_y)
    
    #print(min_x, max_x, min_y, max_y)
    return ((max_x - min_x + 1) * (max_y - min_y + 1)) - len(elves)


elves = load()
#render_board(elves)
#print(elves)
directions = DIRECTIONS
i = 0
while True:
    i += 1
    #print(i)
    elves, directions, did_move = step_elves(elves, directions)

    if i == 10:
        print("Part 1:", area(elves))
    
    if not did_move:
        print("Part 2:", i)
        break
    #render_board(elves)
    #input()

#render_board(elves)

