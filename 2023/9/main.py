def process(seq: list[int]):
    seqs = [seq]
    while not all(n == 0 for n in seq):
        seq = [seq[i + 1] - seq[i] for i in range(len(seq) - 1)]
        seqs.append(seq)
    
    after = sum(seq[-1] for seq in seqs)
    before = sum((1 if i % 2 == 0 else -1) * seq[0] for i, seq in enumerate(seqs))
    return after, before

def main():
    with open("input.txt") as f:
        lines = f.read().splitlines()
    
    sequences = [[int(n) for n in line.split()] for line in lines]

    p1 = sum(process(seq)[0] for seq in sequences)
    p2 = sum(process(seq)[1] for seq in sequences)

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


main()