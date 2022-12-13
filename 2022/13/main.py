from typing import *
import json
from enum import IntEnum
from dataclasses import dataclass

Packet = Union[int, List['Packet']]

class Order(IntEnum):
    INCORRECT = 0
    CORRECT = 1
    UNKNOWN = 2

with open("input.txt") as f:
    pairs = f.read().split("\n\n")
    pairs: List[Tuple[Packet, Packet]] = [tuple(map(json.loads, pair.split("\n"))) for pair in pairs]


def compare(left: Packet, right: Packet) -> Order:
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return Order.CORRECT
        elif left == right:
            return Order.UNKNOWN
        
        return Order.INCORRECT
    
    elif isinstance(left, list) and isinstance(right, list):
        for i in range(max(len(left), len(right))):
            if i >= len(left):
                return Order.CORRECT
            elif i >= len(right):
                return Order.INCORRECT
            l = left[i]
            r = right[i]
            result = compare(l, r)
            if result != Order.UNKNOWN:
                return result
        
        return Order.UNKNOWN
    
    elif isinstance(left, int):
        return compare([left], right)
    
    elif isinstance(right, int):
        return compare(left, [right])


index_sum = 0

for i, pair in enumerate(pairs):
    left, right = pair
    result = compare(left, right)
    if result == Order.CORRECT:
        index_sum += i + 1

print("Part 1:", index_sum)

# bubble sort to fix the order of the packets?

@dataclass
class PacketContainer:
    packet: Packet
    divider: bool

    def __lt__(self, other: 'PacketContainer'):
        return compare(self.packet, other.packet) == Order.CORRECT

packets = [PacketContainer([[2]], True), PacketContainer([[6]], True)] # divider packets

for pair in pairs:
    packets.append(PacketContainer(pair[0], False))
    packets.append(PacketContainer(pair[1], False))

key = 1
for i, p in enumerate(sorted(packets)):
    if p.divider:
        key *= i + 1

print("Part 2:", key)
