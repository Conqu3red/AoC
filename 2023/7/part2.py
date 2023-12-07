def get_counts(hand: str):
    cards = "J23456789TQKA"
    values = [cards.index(card) for card in hand]
    counts = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    
    return values, counts


def joker_hand_sort_key(hand: str):
    values, counts = get_counts(hand)
    j = counts.pop(0, 0)
    repeats = list(counts.values())
    repeats.sort(reverse=True)
    if not repeats:
        repeats.append(0)
    
    if repeats[0] + j == 5:
        hand_type = 6
    elif repeats[0] + j == 4:
        hand_type = 5
    elif repeats[0] + repeats[1] + j == 5:
        hand_type = 4
    elif repeats[0] + j >= 3:
        hand_type = 3
    elif repeats[0] + repeats[1] + j >= 4:
        hand_type = 2
    elif repeats[0] + j >= 2:
        hand_type = 1
    else:
        hand_type = 0

    return (hand_type, *values)


def main():
    with open("input.txt") as f:
        lines = f.read().splitlines()
    
    hands = [line.split() for line in lines]
    p2 = 0

    sorted_hands = sorted(hands, key=lambda h: joker_hand_sort_key(h[0]))
    for rank, (hand, winnings) in enumerate(sorted_hands, start=1):
        #print(rank, hand, winnings)
        p2 += rank * int(winnings)
    
    print(f"Part 2: {p2}")


main()