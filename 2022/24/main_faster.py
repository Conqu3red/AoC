from typing import *
import time

def load():
    with open("input.txt") as f:
        data = f.read()
    
    
    direction_lookup = {
        "^": (0, -1),
        ">": (1, 0),
        "v": (0, 1),
        "<": (-1, 0)
    }

    walls: Set[Tuple[int, int]] = set()
    blizzards: Dict[Tuple[int, int], List[Tuple[int, int]]] = {}
    lines = data.split("\n")
    start_pos = (lines[0].index("."), 0)
    target_pos = (lines[-1].index("."), len(lines) - 1)
    
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char in "^>v<":
                blizzards[(x, y)] = [direction_lookup[char]]
            elif char == "#":
                walls.add((x, y))
    
    return walls, blizzards, start_pos, target_pos


def step_blizzards(walls: Set[Tuple[int, int]], start_blizzards: Dict[Tuple[int, int], List[Tuple[int, int]]]):
    new_blizzards: Dict[Tuple[int, int], List[Tuple[int, int]]] = {}

    for (x, y), directions in start_blizzards.items():
        for dx, dy in directions:
            nx = x + dx
            ny = y + dy
            
            if (nx, ny) in walls:
                # wrap around in a weird way
                nx -= dx
                ny -= dy
                while (nx, ny) not in walls:
                    nx -= dx
                    ny -= dy
                nx += dx
                ny += dy
            
            if nx < 0 or ny < 0:
                print("ERR", x, y, nx, ny)
            
            if (nx, ny) not in new_blizzards:
                new_blizzards[(nx, ny)] = []
            
            new_blizzards[(nx, ny)].append((dx, dy))
    
    return new_blizzards


def freeze_state(blizzards: Dict[Tuple[int, int], List[Tuple[int, int]]]) -> Set[Tuple[int, int]]:
    return {k for k in blizzards}


def generate_blizzard_states(walls: Set[Tuple[int, int]], start_blizzards: Dict[Tuple[int, int], List[Tuple[int, int]]]) -> List[Set[Tuple[int, int]]]:
    unique_frozen_states = [freeze_state(start_blizzards)]
    state = start_blizzards
    while True:
        #print("Step")
        state = step_blizzards(walls, state)
        frozen = freeze_state(state)
        if state == start_blizzards:
            break
        #print(state)
        unique_frozen_states.append(frozen)
    
    return unique_frozen_states

def render_board(walls: Set[Tuple[int, int]], blizzards: Set[Tuple[int, int]], pos: Tuple[int, int]):
    min_x = min(x for x, _ in walls)
    min_y = min(y for _, y in walls)
    max_x = max(x for x, _ in walls)
    max_y = max(y for _, y in walls)

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (x, y) in walls:
                print("#", end="")
            elif (x, y) in blizzards:
                print("%", end="")
            elif (x, y) == pos:
                print("E", end="")
            else:
                print(".", end="")
        print()


def fastest_route(walls: Set[Tuple[int, int]], blizzard_states: List[Set[Tuple[int, int]]], pos: Tuple[int, int], target: Tuple[int, int], start_time: int = 0):
    max_wall_y = max(y for _, y in walls)
    minute_locations: Set[Tuple[int, int]] = {pos}

    time = start_time

    while True:
        next_minute_locations: Set[Tuple[int, int]] = set()
        time += 1
        for x, y in minute_locations:
            #print(time, x, y)
            if (x, y) == target:
                #print("FOUND", time)
                return time - 1

            for (dx, dy) in ((0, -1), (1, 0), (-1, 0), (0, 0), (0, 1)):
                nx = x + dx
                ny = y + dy
                if ny < 0 or ny > max_wall_y or (nx, ny) in walls or (nx, ny) in (blizzard_states[time % len(blizzard_states)]):
                    continue
                
                next_minute_locations.add((nx, ny))

        minute_locations = next_minute_locations



walls, blizzards, start_pos, target_pos = load()
print(len(blizzards))
blizzard_states = generate_blizzard_states(walls, blizzards)
#print(blizzard_states)

#for b in blizzard_states:
#    render_board(walls, b, (1, 0))
#    print()

s = time.time()

there_time = fastest_route(walls, blizzard_states, start_pos, target_pos)
print("Part 1:", there_time)

back_to_start_time = fastest_route(walls, blizzard_states, target_pos, start_pos, start_time=there_time)
print("Time start-end-start:", back_to_start_time)
end_again_time = fastest_route(walls, blizzard_states, start_pos, target_pos, start_time=back_to_start_time)
print("Time start-end-start-end:", end_again_time)
print("Part 2:", end_again_time)

e = time.time()
print(f"Completed in {e - s:.2f}s")