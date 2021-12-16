from typing import *
from dataclasses import dataclass

hex_lookup = {
    "0": [0, 0, 0, 0],
    "1": [0, 0, 0, 1],
    "2": [0, 0, 1, 0],
    "3": [0, 0, 1, 1],
    "4": [0, 1, 0, 0],
    "5": [0, 1, 0, 1],
    "6": [0, 1, 1, 0],
    "7": [0, 1, 1, 1],
    "8": [1, 0, 0, 0],
    "9": [1, 0, 0, 1],
    "A": [1, 0, 1, 0],
    "B": [1, 0, 1, 1],
    "C": [1, 1, 0, 0],
    "D": [1, 1, 0, 1],
    "E": [1, 1, 1, 0],
    "F": [1, 1, 1, 1],
}

def hex_str_to_bit_list(hex_str: str) -> List[bool]:
    l = []
    for char in hex_str:
        l += hex_lookup[char]
    
    return l

def bit_list_to_int(bits: List[bool]) -> int:
    # assumes big endian
    r = 0
    for i, bit in enumerate(reversed(bits)):
        r += bit << i
    
    return r

def load_data():
    with open("input.txt") as f:
        data = f.read()
    
    return data

@dataclass
class Packet:
    version: int
    id: int

    def evaluate(self) -> int:
        pass

@dataclass
class Literal(Packet):
    bits: List[bool]
    
    def evaluate(self) -> int:
        return bit_list_to_int(self.bits)

@dataclass
class Operator(Packet):
    sub_packets: List[Packet]

    def evaluate(self) -> int:
        if self.id == 0:
            return sum(p.evaluate() for p in self.sub_packets)
        if self.id == 1:
            v = 1
            for p in self.sub_packets:
                v *= p.evaluate()
            return v
        if self.id == 2:
            return min(p.evaluate() for p in self.sub_packets)
        if self.id == 3:
            return max(p.evaluate() for p in self.sub_packets)
        if self.id == 5:
            return int(self.sub_packets[0].evaluate() > self.sub_packets[1].evaluate())
        if self.id == 6:
            return int(self.sub_packets[0].evaluate() < self.sub_packets[1].evaluate())
        if self.id == 7:
            return int(self.sub_packets[0].evaluate() == self.sub_packets[1].evaluate())
        else:
            print(f"Invalid id {self.id}")


class PacketParser:
    def __init__(self, bits: List[bool]) -> None:
        self.bits = bits
        self.pos = 0

        self.v_total = 0
    
    def read(self, n: int) -> List[bool]:
        b = self.bits[self.pos : self.pos + n]
        self.pos += n
        return b
    
    def read_int(self, n: int) -> int:
        return bit_list_to_int(self.read(n))

    def get_packet(self) -> Packet:
        version = self.read_int(3)
        self.v_total += version
        id = self.read_int(3)

        if id == 4:
            return self.get_literal(version, id)
        else:
            return self.get_operator(version, id)
    
    def get_literal(self, version: int, id: int) -> Literal:
        bits = []
        is_end = False
        while not is_end:
            is_end = not self.read(1)[0]

            bits += self.read(4)
        
        return Literal(version, id, bits)
    
    def get_operator(self, version: int, id: int) -> Operator:
        lt_id = self.read(1)[0]
        sub_packets = []
        if lt_id == 0:
            length = self.read_int(15)
            start = self.pos
            while self.pos - start < length:
                sub_packets.append(self.get_packet())
        else:
            num_packets = self.read_int(11)
            for i in range(num_packets):
                sub_packets.append(self.get_packet())
        
        return Operator(version, id, sub_packets)


def main():
    bits = hex_str_to_bit_list(load_data())
    p = PacketParser(bits)
    packet = p.get_packet()

    print(f"Part 1: {p.v_total}")
    print(f"Part 2: {packet.evaluate()}")

if __name__ == "__main__":
    main()