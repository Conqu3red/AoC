import math

def main():
    with open("input.txt") as f:
        data = [int(l) for l in f.read().split(",")]
    
    best_fuel = math.inf
    for i in range(min(data), max(data) + 1):
        fuel_used = sum(abs(i - c) for c in data)
        if fuel_used < best_fuel:
            best_fuel = fuel_used

    print(best_fuel)

if __name__ == "__main__":
    main()