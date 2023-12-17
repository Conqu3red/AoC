import math
import heapq
from typing import NamedTuple
from dataclasses import dataclass

class State(NamedTuple):
    x: int
    y: int
    dx: int
    dy: int
    steps: int

@dataclass
class Node:
    value: int
    tdist: int
    done: bool

def search(grid, ultra=False):
    grid = [[Node(val, math.inf, False) for val in row] for row in grid]
    unvisited: list[tuple[int, State]] = []
    visited = set()
    grid[0][0].tdist = 0
    heapq.heappush(unvisited, (0, State(0, 0, 0, 0, math.inf)))

    
    def neighbour_states(state: State):
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            if 0 <= state.x + dx < len(grid[0]) and 0 <= state.y + dy < len(grid) and not (-dx == state.dx and -dy == state.dy):
                new = State(state.x + dx, state.y + dy, dx, dy, (state.steps + 1) if dx == state.dx and dy == state.dy else 1)
                
                if ultra:
                    if not (dx == state.dx and dy == state.dy and state.steps >= 10) and ((dx == state.dx and dy == state.dy) or state.steps >= 4):
                        yield new
                else:
                    if not (dx == state.dx and dy == state.dy and state.steps >= 3):
                        yield new

    while unvisited:
        tdist, cur = heapq.heappop(unvisited)

        if cur in visited:
            continue

        for s in neighbour_states(cur):
            cell = grid[s.y][s.x]
            if not ultra or s.steps >= 4:
                cell.tdist = min(cell.tdist, tdist + cell.value)
            heapq.heappush(unvisited, (tdist + cell.value, s))

        visited.add(cur)

    return grid[-1][-1].tdist



def main():
    with open("input.txt") as f:
        grid = [[int(c) for c in line] for line in f.read().splitlines()]
    
    p1 = search(grid)
    print()
    p2 = search(grid, ultra=True)

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")

main()