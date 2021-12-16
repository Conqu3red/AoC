from typing import *
from dataclasses import dataclass
from copy import deepcopy

@dataclass
class Polymer:
    letter_counts: Dict[str, int]
    pairs: Dict[Tuple[str, str], int]

def load_data() -> Tuple[Polymer, Dict[Tuple[str, str], str]]:
    with open("input.txt") as f:
        lines = f.read().split("\n")

    start_polymer = lines[0]

    counts = {}
    pairs = {}
    for i in range(len(start_polymer) - 1):
        a, b = start_polymer[i], start_polymer[i + 1]
        pairs[a, b] = pairs.get((a, b), 0) + 1
        counts[a] = counts.get(a, 0) + 1
    
    counts[start_polymer[-1]] = counts.get(start_polymer[-1], 0) + 1

    patterns = {}
    for line in lines[2:]:
        k, v = line.split(" -> ")
        patterns[k[0], k[1]] = v
    
    return Polymer(counts, pairs), patterns


def step_polymer(polymer: Polymer, patterns: Dict[Tuple[str, str], str]) -> str:
    new_polymer = Polymer(letter_counts=deepcopy(polymer.letter_counts), pairs={})
    
    for cur_pair, quantity in polymer.pairs.items():
        replacement = patterns.get(cur_pair)
        if replacement is not None:
            new_polymer.letter_counts[replacement] = new_polymer.letter_counts.get(replacement, 0) + quantity
            
            new_polymer.pairs[cur_pair[0], replacement] = new_polymer.pairs.get((cur_pair[0], replacement), 0) + quantity
            new_polymer.pairs[replacement, cur_pair[1]] = new_polymer.pairs.get((replacement, cur_pair[1]), 0) + quantity
        
        else:
            new_polymer.pairs[cur_pair] = new_polymer.pairs.get(cur_pair, 0) + quantity
    
    return new_polymer

def get_polymer_diff(polymer: Polymer, patterns, num_steps):
    for i in range(num_steps):
       polymer = step_polymer(polymer, patterns)
    
    val = max(polymer.letter_counts.values()) - min(polymer.letter_counts.values())
    return val

def main():
    polymer, patterns = load_data()
    print(f"Part 1: {get_polymer_diff(polymer, patterns, 10)}")
    print(f"Part 2: {get_polymer_diff(polymer, patterns, 40)}")

if __name__ == "__main__":
    main()