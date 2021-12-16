from typing import *
from copy import copy, deepcopy
def load_data() -> Dict[str, List[str]]:
    with open("input.txt") as f:
        pairs = [pair.split("-") for pair in f.read().split("\n")]
    
    mapping = {k: [] for k, _ in pairs}
    mapping.update({v: [] for _, v in pairs})
    for k, v in pairs:
        mapping[k].append(v)
        mapping[v].append(k)
    
    return mapping

class PathVisitor:
    def __init__(self, mapping: Dict[str, List[str]]) -> None:
        self.paths = []
        self.mapping = mapping

    def find_path(self, path: List[str], visited: Set[str] = None):
        if visited is None:
            visited = set()
        to_visit = self.mapping.get(path[-1], [])
        for v in to_visit:
            if v == "end":
                path.append(v)
                self.paths.append(path)
            elif v.islower() and v in visited:
                pass
            else:
                new_visited = deepcopy(visited)
                new_visited.add(v)
                new_path = deepcopy(path)
                new_path.append(v)
                self.find_path(new_path, new_visited)

def main():
    mapping = load_data()
    p = PathVisitor(mapping)
    p.find_path(["start"], {"start"})

    print(f"Part 1: {len(p.paths)}")

if __name__ == "__main__":
    main()