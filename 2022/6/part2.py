

with open("input.txt") as f:
    data = f.read()

    for i in range(14, len(data)):
        if len(set(data[i-14:i])) == 14:
            print(i)
            break