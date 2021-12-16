with open("input.txt") as f:
    data = f.read().split("\n")

counts = [0] * len(data[0])

for line in data:
    for i, bit in enumerate(line):
        if bit == "1":
            counts[i] += 1
        else:
            counts[i] -= 1

gamma_bits = [n > 0 for n in counts]
epsilon_bits = [n < 0 for n in counts]

def make_int(bit_list) -> int:
    n = 0
    for i, bit in enumerate(bit_list):
        n += bit << (len(bit_list) - i - 1)
    
    return n

gamma = make_int(gamma_bits)
epsilon = make_int(epsilon_bits)

print("Gamma:", gamma)
print("Epsilon:", epsilon)
print("Power Consumption:", gamma * epsilon)