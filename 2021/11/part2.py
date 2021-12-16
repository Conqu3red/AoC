from part1 import process_step, load_data, print_data

def main():
    data = load_data()

    full_num_flashes = len(data) * len(data[0])

    frame = 0
    while True:
        frame += 1    
        num_flashes = process_step(data)
        print_data(data)
        if num_flashes == full_num_flashes:
            break
    
    print(f"Frame: {frame}")
    print(f"Flashes: {num_flashes}")

if __name__ == "__main__":
    main()