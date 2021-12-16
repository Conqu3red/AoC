with open("input.txt") as f:
    numbers = [int(line) for line in f.read().split("\n")]

def count_increases(numbers):
    increases = 0

    for i in range(1, len(numbers)):
        if numbers[i] > numbers[i - 1]:
            increases += 1

    return increases

# calculate sums
sums = []
for i in range(0, len(numbers)):
    sums.append(sum(numbers[i : i + 3]))

print("Increases:", count_increases(sums))