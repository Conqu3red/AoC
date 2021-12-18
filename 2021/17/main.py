from typing import *
import math

def load_data():
    with open("input.txt") as f:
        l = f.read().replace("target area: ", "")
    
    pairs = l.split(", ")
    xs = pairs[0][2:].split("..")
    ys = pairs[1][2:].split("..")
    
    x1 = int(xs[0])
    x2 = int(xs[1])
    y1 = int(ys[0])
    y2 = int(ys[1])

    return (x1, x2, y1, y2)

def simulate(tx1, tx2, ty1, ty2, vx: int, vy: int) -> bool:
    x = 0
    y = 0
    while True:
        x += vx
        y += vy

        if vx > 0:
            vx -= 1
        elif vx < 0:
            vx += 1
        vy -= 1

        if (tx1 <= x <= tx2) and (ty1 <= y <= ty2):
            return True
        
        if y < ty1 and vy < 0: # below, down
            return False
        
        if not (tx1 <= x <= tx2) and vx == 0:
            return False

def get_vx_value(dist: int):
    """
                  n = x * (x + 1) / 2
                  n = .5 * (x^2 + x)
                 2n = x^2 + x
                 2n = (x + 0.5)^2 - 0.5^2
          2n - 0.25 = (x + 0.5)^2
    sqrt(2n - 0.25) = x + 0.5
    sqrt(2n - 0.25) - 0.5 = x
    """
    return math.sqrt(2 * dist + 0.25) - 0.5

def main():
    target = load_data()
    max_vy = -1 - target[2]
    peak_y = max_vy * (max_vy + 1) // 2
    print(f"Part 1: {peak_y}")

    c = 0

    checking_area = list(target)
    if abs(checking_area[0]) < abs(checking_area[1]):
        checking_area[0] = get_vx_value(min(abs(target[0]), abs(target[1])))
    else:
        checking_area[1] = get_vx_value(min(abs(target[0]), abs(target[1])))
    
    if abs(checking_area[2]) < abs(checking_area[3]):
        checking_area[2] = 0
    else:
        checking_area[3] = 0

    for vy in range(checking_area[2], max_vy + 1):
        for vx in range(checking_area[0], checking_area[1] + 1):
            c += simulate(*target, vx, vy)
    
    print(f"Part 2: {c}")

if __name__ == "__main__":
    main()
