from typing import *
from collections import Counter

def load_data() -> Tuple[str, Dict[str, str]]:
    with open("input.txt") as f:
        lines = f.read().split("\n")

    start_polymer = lines[0]
    patterns = {}
    for line in lines[2:]:
        k, v = line.split(" -> ")
        patterns[k] = v
    
    return start_polymer, patterns


def step_polymer(polymer: str, patterns: Dict[str, str]) -> str:
    new_polymer = ""
    for i in range(len(polymer) - 1):
        cur_pair = polymer[i: i + 2]
        new_polymer += cur_pair[0] + patterns.get(cur_pair, "")
    
    new_polymer += polymer[-1]
    
    return new_polymer

def get_polymer_diff(polymer, patterns, num_steps):
    for i in range(num_steps):
        polymer = step_polymer(polymer, patterns)
    
    c = Counter(polymer)
    val = max(c.values()) - min(c.values())
    return val

def main():
    polymer, patterns = load_data()
    print(f"Part 1: {get_polymer_diff(polymer, patterns, 10)}")

if __name__ == "__main__":
    main()