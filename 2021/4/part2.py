from part1 import *

def main():
    numbers_todo, boards = get_data()
    marked_numbers = []

    last_score = 0

    for n in numbers_todo:
        marked_numbers.append(n)
        boards_left = []
        for board in boards:
            if board_complete(board, marked_numbers):
                print(board)
                last_score = board_score(board, marked_numbers)
            else:
                boards_left.append(board)
        
        boards = boards_left

    print("Score:", last_score)

if __name__ == "__main__":
    main()