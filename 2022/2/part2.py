# 0 = Rock, 1 = Paper, 2 = Scissors
ROCK = 0
PAPER = 1
SCISSORS = 2

left_idx = "ABC"
right_idx = "XYZ"

# what to pick when up against <key> to L, D, W
lookup = {
    ROCK: (SCISSORS, ROCK, PAPER),
    PAPER: (ROCK, PAPER, SCISSORS),
    SCISSORS: (PAPER, SCISSORS, ROCK),
}

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
        
        choice = lookup[left][right]
        total += choice + 1 + points(left, choice)


    
print("Total Score:", total)