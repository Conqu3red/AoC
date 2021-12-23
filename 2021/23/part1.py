from typing import *
from copy import deepcopy
import math

costs = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000
}

index_lookup = {"A": 2, "B": 4, "C": 6, "D": 8}

def load_data():
    # can maybe be expressed as a list of lists? idk
    with open("input.txt") as f:
        lines = f.read().split("\n")
    amphipods = [
        lines[2][3:-3].split("#"),
        lines[3][3:-1].split("#")
    ]
    return amphipods

def is_sorted(grid: List[List[Optional[str]]]):
    return (
        grid[2][1:] == ["A", "A"]
        and grid[4][1:] == ["B", "B"]
        and grid[6][1:] == ["C", "C"]
        and grid[8][1:] == ["D", "D"]
    )

def is_path_clear(x1: int, y1: int, x2: int, y2: int, grid: List[List[Optional[str]]]):

    def line_clear(_x1: int, _y1: int, _x2: int, _y2: int, grid: List[List[Optional[str]]]):
        #print(f"Line {x1} {y1} {x2} {y2}")
        if _y1 == 0 and _y2 == 0:
            for x in range(min(_x1, _x2), max(_x1, _x2) + 1):
                if x != x1:
                    if grid[x][0] is not None:
                        return False
            return True
        
        if _x1 == _x2:
            for y in range(min(_y1, _y2), max(_y1, _y2) + 1):
                if y != y1:
                    if grid[_x1][y] is not None:
                        return False
            return True

        return False

    # up line 1?
    # across line
    # down line?
    return (
        line_clear(x1, y1, x1, 0, grid)
        and line_clear(x1, 0, x2, 0, grid)
        and line_clear(x2, y2, x2, 0, grid)
    )
    


def accessible_locations(x: int, y: int, grid: List[List[Optional[str]]]):
    v = grid[x][y]
    
    if v is None:
        return
    # cell
    nx = index_lookup[v]
    if index_lookup[v] == x and ((y == 1 and grid[x][2] == v) or y == 2):
        return

    # cell
    column = grid[nx]
    ny = 1
    #print(nx, column)
    if column[ny] is None:

        if column[2] is None:
            ny = 2
        
        if ((ny == 1 and column[2] == v) or ny == 2) and is_path_clear(x, y, nx, ny, grid):
            yield nx, ny
            return
    
    if y != 0: # corridor can't move to corridor:
        
        if index_lookup[v] == x: # already in correct place
            if y == 2: return
            if y == 1 and grid[x][2] == v: return

        for nx, column in enumerate(grid):
            t = column[0]
            if t is None and nx != x:
                if nx not in (2, 4, 6, 8):
                    if is_path_clear(x, y, nx, 0, grid):
                        yield nx, 0

def move_cost(x1: int, y1: int, x2: int, y2: int, piece: str):
    # TODO: FIX THIS?
    # does it count correctly??
    return (abs(x2 - x1) + y1 + y2) * costs[piece]

class Grid(NamedTuple):
    g: List[List[Optional[str]]]

    def __hash__(self) -> int:
        return hash(tuple(tuple(v for v in g) for g in self.g))

def print_grid(g: List[List[Optional[str]]]):
    for y in range(0, 3):
        for x in range(0, 11):
            if y < len(g[x]):
                print("." if g[x][y] is None else g[x][y], end="")
            else:
                print(" ", end="")
        print()


class RecursiveGame:
    least_cost = math.inf
    ncalls = 0

    memory: Dict[Grid, int] = {}
    
    @staticmethod
    def try_sort(_grid: Grid, cost: int = 0):
        if _grid in RecursiveGame.memory and cost >= RecursiveGame.memory[_grid]:
            return
        RecursiveGame.memory[_grid] = cost
        
        grid = _grid.g
        RecursiveGame.ncalls += 1
        if cost >= RecursiveGame.least_cost: # no point
            return
        
        if is_sorted(grid):
            if cost < RecursiveGame.least_cost:
                print(cost)
                #for g in history + [grid]:
                #    print_grid(g)
                #    print()
                #print("####################")
                RecursiveGame.least_cost = cost
                return
        
        # I think some cases are not being simulated correctly

        for x, column in enumerate(grid):
            for y, t in enumerate(column):
                if t is not None:
                    for new_x, new_y in accessible_locations(x, y, grid):
                        new_grid = deepcopy(grid)
                        new_grid[x][y] = None
                        new_grid[new_x][new_y] = t
                        #print_grid(new_grid)
                        RecursiveGame.try_sort(Grid(new_grid), cost + move_cost(x, y, new_x, new_y, t))


def get_shortest_sort_route(amphipods: List[List[str]]):
    grid: List[List[Optional[str]]] = [[None] for _ in range(11)]
    grid[2] += [amphipods[0][0], amphipods[1][0]]
    grid[4] += [amphipods[0][1], amphipods[1][1]]
    grid[6] += [amphipods[0][2], amphipods[1][2]]
    grid[8] += [amphipods[0][3], amphipods[1][3]]

    RecursiveGame.try_sort(Grid(grid), cost=0) # sorting seems to be taking way too many steps, some possibilities missed?
    print(f"Part 1: {RecursiveGame.least_cost}")

    # solve this recursively??
    # Constraints:
    #   won't stop directly above room
    #   never move from hallway to room unless its their dest + has no other types in
    #   stays in its place in hallway until can move to room

def main():
    amphipods = load_data()
    get_shortest_sort_route(amphipods)

if __name__ == "__main__":
    main()