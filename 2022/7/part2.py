from typing import *
from dataclasses import dataclass
import math

@dataclass
class Folder:
    file_size: int
    folders: List['Folder']

with open("input.txt") as f:
    lines = f.read().split("\n")

stack = [Folder(0, [])]

for line in lines:
    if line.startswith("$"):
        line = line[2:]
        if line.startswith("cd"):
            folder = line.split(" ")[1]
            if folder == "/":
                del stack[1:]
            elif folder == "..":
                stack.pop()
            else:
                f = Folder(0, [])
                stack[-1].folders.append(f)
                stack.append(f)
    elif not line.startswith("dir"):
        size = int(line.split(" ")[0])
        stack[-1].file_size += size


def total(folder: Folder) -> int:
    return folder.file_size + sum(total(f) for f in folder.folders)

to_free = 30000000 - (70000000 - total(stack[0]))

def best_to_free(folder: Folder) -> int:
    best = math.inf
    t = total(folder)
    if t > to_free:
        best = t
    
    for f in folder.folders:
        best = min(best_to_free(f), best)

    return best


print(best_to_free(stack[0]))