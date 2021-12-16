def num_fish(days):
    with open("input.txt") as f:
        all_fish = list(map(int, f.read().split(",")))

    for d in range(days):
        print(f"Day {d}")
        for i in range(len(all_fish)):
            if all_fish[i] == 0:
                all_fish.append(8)
                all_fish[i] = 6
            else:
                all_fish[i] -= 1
    
    print(f"Fish Count: {len(all_fish)}")

if __name__ == "__main__":
    num_fish(80)