with open("input.txt") as f:
    data = f.read().split("\n")

def count_bit(numbers, i) -> int:
    c = 0
    for line in numbers:
        if line[i] == "1":
            c += 1
        else:
            c -= 1
    
    return c

def filter_through(data, most_common = True) -> int:
    numbers = set(data)
    for i in range(len(data[0])):
        count = count_bit(numbers, i)
        
        expected_bit = str(int(count >= 0 if most_common else count < 0))
    
        print(expected_bit, count, i, numbers)
        
        numbers = set(filter(lambda x: x[i] == expected_bit, numbers))
        
        if len(numbers) == 1:
            return int(numbers.pop(), base=2)

generator_level = filter_through(data, True)
scrubber = filter_through(data, False)

life_support = generator_level * scrubber

print("Generator:", generator_level)
print("Scrubber:", scrubber)
print("Life Support:", life_support)
