import math

def combinations(t: int, d: int):
    # d < h * (t - h)
    # d < h*t - h^2
    # 0 < -h^2 + h*t - d
    a = -1
    b = t
    c = -d
    disc = b*b - 4*a*c
    if disc >= 0:
        h1 = (-b + math.sqrt(disc)) / (2 * a)
        h2 = (-b - math.sqrt(disc)) / (2 * a)
        h1 = math.floor(h1 + 1) # because it's > not >=
        h2 = math.ceil(h2 - 1) # because it's > not >=
        return h2 - h1 + 1
    return 0

def main():
    with open("input.txt") as f:
        times_data, distances_data = f.read().splitlines()
    
    times = [int(n) for n in times_data.split(":")[1].split()]
    distances = [int(n) for n in distances_data.split(":")[1].split()]

    p1 = 1

    for t, d in zip(times, distances):
        p1 *= combinations(t, d)

    p2 = combinations(
        t=int(times_data.split(":")[1].replace(" ", "")),
        d=int(distances_data.split(":")[1].replace(" ", ""))
    )
    

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


main()