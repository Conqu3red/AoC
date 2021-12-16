"""

  0:      1:      2:      3:      4:
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

  5:      6:      7:      8:      9:
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg
"""

segments_values = [
    set("abcefg"),
    set("cf"),
    set("acdeg"),
    set("acdfg"),
    set("bcdf"),
    set("abdfg"),
    set("abdefg"),
    set("acf"),
    set("abcdefg"),
    set("abcdfg"),
]

def create_output_map(inputs):
    """
    a: one with length 3 - one with length 2
    b: 6 occurences
    c: 8 occurrences
    d: one with length 4 - b - c - f
    e: 4 occurrences
    f: 9 occurrences
    g: last character left
    """
    all_chars = [i for input in inputs for i in input]
    chars_left = set("abcdefg")
    encoded_to_segment = {}

    a = (set(next(filter(lambda x: len(x) == 3, inputs))) - set(next(filter(lambda x: len(x) == 2, inputs)))).pop()
    chars_left.remove(a)
    encoded_to_segment[a] = "a"
    
    for char in "abcdefg":
        count = all_chars.count(char)
        if count == 4: encoded_to_segment[char] = "e"
        elif count == 6: encoded_to_segment[char] = "b"
        elif count == 8 and char != a: encoded_to_segment[char] = "c"
        elif count == 9: encoded_to_segment[char] = "f"
        else:
            continue
        
        chars_left.remove(char)
    
    encoded_to_segment_reversed = {v: k for k, v in encoded_to_segment.items()}
    
    
    d = (set(next(filter(lambda x: len(x) == 4, inputs))) - {encoded_to_segment_reversed["b"], encoded_to_segment_reversed["c"], encoded_to_segment_reversed["f"]}).pop()
    chars_left.remove(d)
    encoded_to_segment[d] = "d"

    encoded_to_segment[chars_left.pop()] = "g"
    return encoded_to_segment

    
def get_number(digit, pattern_digit_map):
    return segments_values.index(set(pattern_digit_map[d] for d in digit))


def main():
    with open("input.txt") as f:
        data = [line.split(" | ") for line in f.read().split("\n")]
    
    total = 0
    for patterns, output in data:
        patterns = patterns.split(" ")
        output = output.split(" ")
        pattern_digit_map = create_output_map(patterns)

        num = 0
        for i, digit in enumerate(output):
            num += get_number(digit, pattern_digit_map) * 10 ** (len(output) - i - 1)
        
        print(f"Num: {num}")
        
        total += num
        
    
    
    print(f"Total: {total}")


if __name__ == "__main__":
    main()