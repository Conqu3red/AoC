total = 0

with open("input.txt") as f:
    lines = f.read().split("\n")
    for line in lines:
        left, right = line.split(",")
        l_low, l_high = left.split("-")
        r_low, r_high = right.split("-")
        l_low = int(l_low)
        l_high = int(l_high)
        r_low = int(r_low)
        r_high = int(r_high)

        if (r_low >= l_low and r_high <= l_high) or (l_low >= r_low and l_high <= r_high):
            total += 1

print("Total contained:", total)