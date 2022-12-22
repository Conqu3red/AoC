from typing import *
from dataclasses import dataclass
from enum import Enum
import math

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

def create_net(board: List[List[CellState]]):
    total_area = sum(sum(cell != CellState.INVALID for cell in row) for row in board)
    face_edge = int(math.sqrt(total_area // 6))

    faces: Set[Tuple[int, int]] = set()

    # scan for faces and add
    for y in range(1, len(board), face_edge):
        for x in range(1, len(board[y]), face_edge):
            if board[y][x] != CellState.INVALID:
                faces.add(((x - 1) // face_edge, (y - 1) // face_edge))
    
    return faces, face_edge


class Vec3(NamedTuple):
    x: int
    y: int
    z: int

    def __add__(self, other: 'Vec3'):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other: 'Vec3'):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)


def rotate_90(direction: int, point: Vec3, axis: int):
    if axis == 0:
        return Vec3(point.x,             point.z * direction,  -point.y * direction)
    elif axis == 1:
        return Vec3(point.z * direction, point.y,              -point.x * direction)
    elif axis == 2:
        return Vec3(point.y * direction, -point.x * direction, point.z)


@dataclass
class CubeFace:
    net_x: int
    net_y: int

    points: List[Vec3]
    inward_normal: Vec3

def rotate_all(rotation_origin: Vec3, prev: Tuple[int, int], location: Tuple[int, int], cube_faces: Dict[Tuple[int, int], CubeFace], direction: int, axis: int):
    face = cube_faces[location]
    print(f"Rotate face @ net:{face.net_x},{face.net_y} {direction} axis {axis}", end="")

    face.points = [
        rotate_90(direction, point - rotation_origin, axis) + rotation_origin for point in face.points
    ]

    face.inward_normal = rotate_90(direction, face.inward_normal, axis)
    print(f"  Inward normal {face.inward_normal}")

    x, y = location
    for dx, dy in DIRECTIONS:
        nx, ny = x + dx, y + dy
        if (nx, ny) in cube_faces and (nx, ny) != prev:
            rotate_all(rotation_origin, location, (nx, ny), cube_faces, direction, axis)




def fold_cube(net: Set[Tuple[int, int]]):
    cube_faces = {
        (x, y): CubeFace(
            x, y, [
                Vec3(x, y, 0),
                Vec3(x + 1, y, 0),
                Vec3(x + 1, y + 1, 0),
                Vec3(x, y + 1, 0),
            ],
            Vec3(0, 0, 1) # facing +z
        ) for x, y in net
    }

    visited: Set[Tuple[int, int]] = set()
    to_visit: List[Tuple[int, int]] = []
    first = net.pop()
    net.add(first)
    to_visit.append(first)

    while to_visit:
        x, y = to_visit.pop()
        visited.add((x, y))
        face = cube_faces[(x, y)]

        for direction in range(4):
            dx, dy = DIRECTIONS[direction]
            nx, ny = x + dx, y + dy
            if (nx, ny) in cube_faces and (nx, ny) not in visited:
                connected_face = cube_faces[(nx, ny)]
                # apply a rotation to all of the faces connected to this one
                # NOTE: the rotation direction must be relative to the face it is connected to!
                shared_points: List[Vec3] = []
                for p in connected_face.points:
                    if p in face.points:
                        shared_points.append(p)
                
                rotation_axis = shared_points[1] - shared_points[0]
                print(f"Exploring face ({x} {y}) -> ({nx} {ny})")
                print(f"  shared points {shared_points} rot axis {rotation_axis}")
                
                base_point = shared_points[0]
                index = connected_face.points.index(base_point)
                other_point = connected_face.points[(index + 1) % 4]
                if other_point in shared_points:
                    other_point = connected_face.points[(index - 1) % 4]
                
                connected_normal = base_point - other_point
                # we are trying to rotate the connected_normal to be equal to face.inwards_normal
                print("  target normal", face.inward_normal)
                rot_direction = 1 if 1 in rotation_axis else -1
                rot_axis = rotation_axis.index(rot_direction)
                if rotate_90(rot_direction, connected_normal, rot_axis) != face.inward_normal:
                    rot_direction = -rot_direction

                # apply rotation to all faces
                rotate_all(base_point, (x, y), (nx, ny), cube_faces, rot_direction, rot_axis)
                
                to_visit.append((nx, ny))
                
    for face in cube_faces.values():
        print(f"F {face.inward_normal}")
        
    return cube_faces


# write an algorithm to fold cubes from a flat net
# for ever face we find, fold all neighbouring faces up towards it
# do it to each face in isolation from the 2d net
# merge all of these bits together?

def opposite_edge(cube: Dict[Tuple[int, int], CubeFace], cube_size: int, board: List[List[CellState]], x: int, y: int, direction: int):
    net_x = x // cube_size
    net_y = y // cube_size
    current_face = cube[(net_x, net_y)]
    print(f"Direction {direction} coords {x % cube_size, y % cube_size} net {net_x, net_y}")
    # d = direction
    # cur = current face
    # other = face that shares edge
    # d cur     other   cur    other
    # 0 right | left  = 1, 2 | 3, 0
    # 1 down  | up    = 2, 3 | 0, 1
    # 2 left  | right = 3, 0 | 1, 2
    # 3 up    | down  = 0, 1 | 2, 3
    #                  +1 +2  -1 +0   
    point1 = current_face.points[(direction + 1) % 4]
    point2 = current_face.points[(direction + 2) % 4]

    # find the other face which shares these points
    for face in cube.values():
        if face.net_x == net_x and face.net_y == net_y:
            continue

        p1_index = None
        p2_index = None
        for i, point in enumerate(face.points):
            if point == point1:
                p1_index = i
            if point == point2:
                p2_index = i
        
        if p1_index is None or p2_index is None:
            continue
        
        print("match", face)
        break
    
    # face is now the face that shares the same edge
    print(f"Shared edge, {point1, point2} {face.points[p1_index], face.points[p2_index]} {(direction + 1) % 4, (direction + 2) % 4} {p1_index, p2_index}")


    print(x, y)#amount_along_edge
    new_edge = (p1_index, p2_index)
    new_x = 0
    new_y = 0
    # edges:
    # 0--1
    # |  |
    # 3--2
    
    # d = direction
    # cur = current face
    # other = face that shares edge
    # numbers show index of points that are matching
    # d cur     other   cur    other
    # 0 right | left  = 1, 2 | 0, 3
    # 1 down  | up    = 2, 3 | 1, 0
    # 2 left  | right = 3, 0 | 2, 1
    # 3 up    | down  = 0, 1 | 3, 2
    #                  +1 +2  +0 -1

    lx, ly = (x + DIRECTIONS[direction][0]) % cube_size, (y + DIRECTIONS[direction][1]) % cube_size
    print("L", lx, ly)

    offsetted = [None, None, None, None]
    offsetted[direction % 4] = p1_index
    offsetted[(direction - 1) % 4] = p2_index
    print(offsetted)
    new_direction = direction
    while offsetted.index(p1_index) != p1_index and offsetted.index(p2_index) != p2_index:
        offsetted = [offsetted[-1]] + offsetted[:-1]
        print("rotate!")
        lx -= (cube_size - 1) / 2
        ly -= (cube_size - 1) / 2
        ly = -ly
        lx, ly = ly, -lx
        ly = -ly
        lx += (cube_size - 1) / 2
        ly += (cube_size - 1) / 2
        lx = int(lx)
        ly = int(ly)

        new_direction = (new_direction + 1) % 4

    #print("L coords", lx, ly)

    

    print("new local coords", lx, ly, "direction", new_direction)
    print(f"Direction {new_direction} coords {lx, ly} net {face.net_x, face.net_y}")
    print()
    return (face.net_x * cube_size + lx, face.net_y * cube_size + ly), new_direction

    # need to return new coordinates and direction

def print_map(board: List[List[CellState]], x: int, y: int, direction: int):
    for cy, row in enumerate(board):
        for cx, cell in enumerate(row):
            if cx == x and cy == y:
                print(">V<^"[direction], end="")
            elif cell == CellState.WALL:
                print("#", end="")
            elif cell == CellState.TILE:
                print(".", end="")
            else:
                print(" ", end="")
        print()



def traverse_path(cube, cube_size, board: List[List[CellState]], path: List[Union[str, int]]):
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
            print(f"!Forward {entry} direction {direction}")
            for _ in range(entry):
                direction_vector = DIRECTIONS[direction]
                new_y = y + direction_vector[1]
                new_x = x + direction_vector[0]
                new_direction = direction

                if 0 > new_y or new_y >= len(board) or 0 > new_x or new_x >= len(board[new_y]) or board[new_y][new_x] == CellState.INVALID:
                    #print("EDGE")
                    #print_map(board, x, y, direction)
                    #input()
                    (new_x, new_y), new_direction = opposite_edge(cube, cube_size, board, x, y, direction)
                    #print("EDGE RESOLVE")
                    #print_map(board, new_x, new_y, new_direction)
                    #input()
                    #print("-- EDGE --")

                
                cell = board[new_y][new_x]
                if cell == CellState.WALL:
                    break

                direction = new_direction
                
                x = new_x
                y = new_y
            
    column = x + 1
    row = y + 1
    print(f"Row: {row}, Column: {column}, direction: {direction}")
    return 1000 * row + 4 * column + direction



board, path = load()

net, face_edge = create_net(board)
cube = fold_cube(net)
print("\n\n")

print(traverse_path(cube, face_edge, board, path))