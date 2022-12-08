from typing import *
from dataclasses import dataclass

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

def under_100000(folder: Folder) -> int:
    overall = 0
    t = total(folder)
    if t <= 100000:
        overall += t
    
    overall += sum(under_100000(f) for f in folder.folders)

    return overall

print(under_100000(stack[0]))