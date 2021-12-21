from typing import *

def wrap_num(n: int, bound: int) -> int:
    return ((n - 1) % bound) + 1


class Dice:
    UPPER_BOUND = 100
    def __init__(self) -> None:
        self.nrolls = 0
    
    def roll(self) -> int:
        r = (self.nrolls % 100) + 1
        self.nrolls += 1
        
        return r


def load_data():
    with open("input.txt") as f:
        data = f.read().split("\n")
    s1 = int(data[0].split(": ")[1])
    s2 = int(data[1].split(": ")[1])

    return s1, s2


def play_game(s1: int, s2: int, dice: Dice):
    scores = [0, 0]
    positions = [s1, s2]
    while True:
        for i in range(2):
            total = sum(dice.roll() for _ in range(3))
            positions[i] = wrap_num(positions[i] + total, 10)
            scores[i] += positions[i]

            if scores[i] >= 1000:
                return min(scores) * dice.nrolls

def main():
    s1, s2 = load_data()
    dice = Dice()
    r = play_game(s1, s2, dice)
    print(f"Part 1: {r}")

if __name__ == "__main__":
    main()