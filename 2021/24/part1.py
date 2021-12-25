from typing import *
from dataclasses import dataclass
from copy import copy

@dataclass
class Instruction:
    name: str
    operands: List[Union[str, int]]

def load_data() -> List[Instruction]:
    instructions = []
    with open("input.txt") as f:
        lines = f.read().split("\n")
    
    for line in lines:
        name, *operands = line.split(" ")
        operands = [int(o) if o not in "wxyz" else o for o in operands]
        instructions.append(Instruction(name, operands))
    
    return instructions

def get_v(reg: Dict[str, str], operand: str) -> int:
    if operand in reg:
        return reg[operand]
    return int(operand)

#def get_reg(n: int):
#    return (n & (2 ** 32), (n >> 32) & (2 ** 32), (n >> 64) & (2 ** 32), (n >> 96) & (2 ** 32))
#
#def enc_reg(v: Tuple[int, int, int, int]):
#    return v[0] + (v[1] << 32) + (v[2] << 64) + (v[3] << 96)

class BruteForce:
    def __init__(self, instructions: List[Instruction]) -> None:
        self.instructions = instructions
        #self.visited_states: Set[Tuple[int, int, int, int, int]] = set()
        self.max_model_num = 0

        self.states: Dict[int, Tuple[int, int]] = {(0, 0, 0, 0): (0, 0)}
        self.new_states: Dict[int, Tuple[int, int]] = {}
    
    def run(self):
        for i in range(14):
            self.new_states = {}
            for r, s in self.states.items():
                self.get_all_states(r, s, i)
            
            print(f"Bit: {i + 1}, States: {len(self.new_states)}", )
            self.states = self.new_states
    
    def get_all_states(self, r: Tuple[int, int, int, int], state: Tuple[int, int], bits_done: int):
        reg = {"w": r[0], "x": r[1], "y": r[2], "z": r[3]}
        index, n = state
        
        for ind in range(index, len(self.instructions)):
            i = self.instructions[ind]

            if i.name == "inp":
                # branch for all bits
                for b in range(9, 0, -1):
                    reg[i.operands[0]] = b
                    _r = tuple(reg.values())
                    if _r in self.new_states and self.new_states[_r][1] > n + b * (10 ** (13 - bits_done)):
                        continue
                    
                    self.new_states[_r] = (ind + 1, n + b * (10 ** (13 - bits_done)))
                
                break
            
            elif i.name == "add":
                reg[i.operands[0]] += get_v(reg, i.operands[1])
            elif i.name == "mul":
                v = get_v(reg, i.operands[1])
                #if v == 0: break
                reg[i.operands[0]] *= v
            elif i.name == "div":
                reg[i.operands[0]] //= get_v(reg, i.operands[1])
            elif i.name == "mod":
                reg[i.operands[0]] %= get_v(reg, i.operands[1])
            elif i.name == "eql":
                reg[i.operands[0]] = (reg[i.operands[0]] == get_v(reg, i.operands[1])) + 0 # cast to int
        
        #if reg["z"] == 0 and n >= self.max_model_num:
        #    self.max_model_num = n
        #    #print(self.max_model_num)
        

def main():
    instructions = load_data()
    start_reg = {"w": 0, "x": 0, "y": 0, "z": 0}
    b = BruteForce(instructions)
    b.run()
    print(f"Part 1: {b.max_model_num}")

if __name__ == "__main__":
    main()