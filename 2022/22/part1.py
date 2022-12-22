from typing import *
from dataclasses import dataclass
from enum import Enum

class CellState(Enum):
    INVALID = "x"
    TILE = "."
    WALL = "#"

def load():
    with open("input.txt") as f:
        data = f.read()

    board: List[List[CellState]] = []

    lines, path = data.split("\n\n")
    
    for line in lines.split("\n"):
        board.append([])
        for char in line:
            if char == ".":
                board[-1].append(CellState.TILE)
            elif char == "#":
                board[-1].append(CellState.WALL)
            else:
                board[-1].append(CellState.INVALID)
    
    split_path = []
    path_buf = ""
    for char in path:
        if char == "L" or char == "R":
            if path_buf:
                split_path.append(int(path_buf))
                path_buf = ""
            
            split_path.append(char)
        else:
            path_buf += char
    
    if path_buf:
        split_path.append(int(path_buf))
    
    return board, split_path

# right, down, left, up
DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

def opposite_edge(board: List[List[CellState]], x: int, y: int, direction: Tuple[int, int]):
    while True:
        new_y = y + direction[1]
        new_x = x + direction[0]

        if 0 > new_y or new_y >= len(board) or 0 > new_x or new_x >= len(board[new_y]) or board[new_y][new_x] == CellState.INVALID:
            break

        x = new_x
        y = new_y

    return x, y


def traverse_path(board: List[List[CellState]], path: List[Union[str, int]]):
    direction = 0
    y = 0
    for i, cell in enumerate(board[0]):
        if cell == CellState.TILE:
            x = i
            break
    
    for entry in path:
        if isinstance(entry, str):
            # direction change
            if entry == "L":
                direction = (direction - 1) % len(DIRECTIONS)
            elif entry == "R":
                direction = (direction + 1) % len(DIRECTIONS)
        
        else:
            # step forward
            direction_vector = DIRECTIONS[direction]
            for _ in range(entry):
                new_y = y + direction_vector[1]
                new_x = x + direction_vector[0]

                if 0 > new_y or new_y >= len(board) or 0 > new_x or new_x >= len(board[new_y]) or board[new_y][new_x] == CellState.INVALID:
                    new_x, new_y = opposite_edge(board, x, y, (-direction_vector[0], -direction_vector[1]))
                
                cell = board[new_y][new_x]
                if cell == CellState.WALL:
                    break
                
                x = new_x
                y = new_y
            
    column = x + 1
    row = y + 1
    print(f"Row: {row}, Column: {column}, direction: {direction}")
    return 1000 * row + 4 * column + direction



board, path = load()

print(traverse_path(board, path))