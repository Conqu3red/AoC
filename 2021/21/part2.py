from typing import *
import random

def wrap_num(n: int, bound: int) -> int:
    return ((n - 1) % bound) + 1


class Dice:
    UPPER_BOUND = 100
    def __init__(self) -> None:
        self.nrolls = 0
    
    def roll(self) -> int:
        r = (self.nrolls % 100) + 1
        self.nrolls += 1
        
        return random.randint(1, 3)


def load_data():
    with open("input.txt") as f:
        data = f.read().split("\n")
    s1 = int(data[0].split(": ")[1])
    s2 = int(data[1].split(": ")[1])

    return s1, s2


def change_weights():
    weights = {}
    for d1 in range(1, 4):
        for d2 in range(1, 4):
            for d3 in range(1, 4):
                weights[d1 + d2 + d3] = weights.get(d1 + d2 + d3, 0) + 1
    
    return weights

class GameDetail(NamedTuple):
    s1: int
    p1: int
    s2: int
    p2: int

def move1(is_s1: bool, weights: Dict[GameDetail, int]) -> Dict[GameDetail, int]:
    new = {}
    base = change_weights()
    for g, count in weights.items():
        if max(g.s1, g.s2) < 21:
            for c, ncount in base.items(): # TODO: make this work for every permutation
                # push new totals for s1 and s2 could change to:
                if is_s1:
                    np = wrap_num(g.p1 + c, 10)
                    new_k = GameDetail(g.s1 + np, np, g.s2, g.p2)
                else:
                    np = wrap_num(g.p2 + c, 10)
                    new_k = GameDetail(g.s1, g.p1, g.s2 + np, np)
                
                new[new_k] = new.get(new_k, 0) + count * ncount
                # how does the tree actually branch??
        else:
            new[g] = new.get(g, 0) + count
    
    return new


def apply_turn(weights: Dict[GameDetail, int]) -> Dict[GameDetail, int]:
    new = move1(True, weights)
    new = move1(False, new)
    return new


def play(s1: int, s2: int) -> Dict[GameDetail, int]:
    w = {GameDetail(0, s1, 0, s2): 1}
    while True:
        w = apply_turn(w)
        c = False
        for g in w.keys():
            if max(g.s1, g.s2) < 21:
                c = True
                break
        if not c:
            break
    
    return w

def main():
    s1, s2 = load_data()
    games = play(s1, s2)
    
    w1_wins = 0
    for game, amount in games.items():
        if game.s1 >= 21:
            w1_wins += amount

    w2_wins = 0
    for game, amount in games.items():
        if game.s2 >= 21:
            w2_wins += amount
    
    print(f"Part 2: {max(w1_wins, w2_wins)}")


if __name__ == "__main__":
    main()