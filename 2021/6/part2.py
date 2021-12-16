def count(iterable):
    c = {}
    for v in iterable:
        c[v] = c.get(v, 0) + 1

    return c


def num_fish(days):
    with open("input.txt") as f:
        all_fish = {i: 0 for i in range(0, 9)}
        all_fish.update(count( map(int, f.read().split(",")) ))

    for d in range(days):
        next_step_fish = {i: 0 for i in range(0, 9)} # to avoid fish being processed twice in one step
        for i in all_fish:
            if i == 0:
                next_step_fish[8] += all_fish[i]
                next_step_fish[6] += all_fish[i] # reset fish that made new one
                next_step_fish[i] = 0
            else:
                next_step_fish[i - 1] += all_fish[i] # decrement
        
        all_fish = next_step_fish
    
    print(f"Fish Count: {sum(all_fish.values())}")

if __name__ == "__main__":
    num_fish(256)