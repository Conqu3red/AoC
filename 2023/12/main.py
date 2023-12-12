from functools import lru_cache


def arrangements(springs: str, groups: list[int]):
    @lru_cache
    def combinations(pos: int = 0, group_index: int = 0, damaged: int = 0):
        if pos == len(springs):
            return group_index == len(groups) or (group_index == len(groups) - 1 and damaged == groups[group_index])

        if springs[pos] == "#":
            if group_index < len(groups) and damaged < groups[group_index]:
                return combinations(pos + 1, group_index, damaged + 1)
            return 0
        elif springs[pos] == ".":
            if group_index == len(groups) or damaged == 0:
                return combinations(pos + 1, group_index, 0)
            elif damaged == groups[group_index]:
                return combinations(pos + 1, group_index + 1, 0)
            return 0
        
        c = 0
        if group_index < len(groups) and damaged < groups[group_index]:
            c += combinations(pos + 1, group_index, damaged + 1) # possible #
        if group_index == len(groups) or damaged == 0 or damaged == groups[group_index]:
            if group_index < len(groups) and damaged == groups[group_index]: # possible .
                group_index += 1
            c += combinations(pos + 1, group_index, 0)
        return c
    return combinations()


def main():
    with open("input.txt") as f:
        rows = [(line.split()[0], [int(n) for n in line.split()[1].split(",")]) for line in f.read().splitlines()]
    
    p1 = sum(arrangements(springs, groups) for springs, groups in rows)
    p2 = sum(arrangements("?".join([springs] * 5), groups * 5) for springs, groups in rows)
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")   


main()