

with open("input.txt") as f:
    data = f.read()

    for i in range(4, len(data)):
        if len(set(data[i-4:i])) == 4:
            print(i)
            break