# 0 = Rock, 1 = Paper, 2 = Scissors
ROCK = 0
PAPER = 1
SCISSORS = 2

left_idx = "ABC"
right_idx = "XYZ"

def points(left: int, right: int):
    if left == right:
        return 3
    if (left == ROCK and right == PAPER) or (left == PAPER and right == SCISSORS) or (left == SCISSORS and right == ROCK):
        return 6
    
    return 0

total = 0

with open("input.txt") as f:
    lines = f.read().split("\n")
    for line in lines:
        left, right = line.split(" ")
        left = left_idx.index(left)
        right = right_idx.index(right)
        total += right + 1 + points(left, right)



print("Total Score:", total)