
def hand_sort_key(hand: str):
    cards = "23456789TJQKA"
    values = [cards.index(card) for card in hand]
    counts = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    
    repeats = list(counts.values())
    if 5 in repeats:
        hand_type = 6
    elif 4 in repeats:
        hand_type = 5
    elif 3 in repeats and 2 in repeats:
        hand_type = 4
    elif 3 in repeats:
        hand_type = 3
    elif repeats.count(2) == 2:
        hand_type = 2
    elif repeats.count(2) == 1:
        hand_type = 1
    else:
        hand_type = 0
    
    return (hand_type, *values)


def main():
    with open("input.txt") as f:
        lines = f.read().splitlines()
    
    hands = [line.split() for line in lines]
    
    p1 = 0

    sorted_hands = sorted(hands, key=lambda h: hand_sort_key(h[0]))
    for rank, (hand, winnings) in enumerate(sorted_hands, start=1):
        print(rank, hand, winnings)
        p1 += rank * int(winnings)
    
    print(f"Part 1: {p1}")


main()