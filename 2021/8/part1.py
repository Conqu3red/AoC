def main():
    with open("input.txt") as f:
        data = [line.split(" | ")[1].split(" ") for line in f.read().split("\n")]
        data = [l for line in data for l in line]
    
    lengths = {2, 3, 4, 7}
    new = [l for l in data if len(l) in lengths]
    print(f"Count: {len(new)}")


if __name__ == "__main__":
    main()