def process(seq: list[int]):
    seqs = [seq]
    while not all(n == 0 for n in seq):
        seq = [seq[i + 1] - seq[i] for i in range(len(seq) - 1)]
        seqs.append(seq)
    
    return sum(seq[-1] for seq in seqs)

def main():
    with open("input.txt") as f:
        lines = f.read().splitlines()
    
    sequences = [[int(n) for n in line.split()] for line in lines]

    p1 = sum(process(seq) for seq in sequences)
    p2 = sum(process([*reversed(seq)]) for seq in sequences)

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


main()