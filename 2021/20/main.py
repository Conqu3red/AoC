from typing import *

def load_data() -> Tuple[str, List[List[bool]]]:
    with open("input.txt") as f:
        lookup, input_data = f.read().split("\n\n")
    
    lines = input_data.split("\n")
    input_formatted = [[c == "#" for c in line] for line in lines]

    return [c == "#" for c in lookup], input_formatted

def enhance(lookup: List[bool], image: List[List[bool]], background_state=False):
    # expand image by 2 in every direction
    
    width = len(image[0])
    for _ in range(2):
        image.insert(0, [background_state for _ in range(width)])
        image.append([background_state for _ in range(width)])
    
    for line in image:
        line.insert(0, background_state)
        line.insert(0, background_state)
        line.append(background_state)
        line.append(background_state)
    
    new_image = [[background_state for _ in range(len(row))] for row in image]

    # apply "enhancement"

    for y, row in enumerate(image):
        for x, value in enumerate(row):
            num = 0
            i = 8
            for ly in range(y - 1, y + 2):
                for lx in range(x - 1, x + 2):
                    if 0 <= ly < len(image) and 0 <= lx < len(row):
                        num += image[ly][lx] << i
                    else:
                        num += background_state << i
                    i -= 1
            
            new_image[y][x] = lookup[num]
    

    # return new background state
    bnum = 0
    for i in range(9):
        bnum += background_state << i
    background_state = lookup[bnum]
    
    return background_state, new_image

def print_image(image: List[List[bool]]):
    for line in image:
        for value in line:
            print("#" if value else ".", end="")
        print()

def main():
    lookup, image = load_data()
    

    background = False
    for i in range(50):
        background, image = enhance(lookup, image, background)

        if i == 2: # part 1
            lit_up = sum(row.count(True) for row in image)
            print(f"Part 1: {lit_up}")
    
    lit_up = sum(row.count(True) for row in image)
    print(f"Part 2: {lit_up}")

    
   

if __name__ == "__main__":
    main()