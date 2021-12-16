def get_data():
    with open("input.txt") as f:
        text = f.read()
        num_text, *boards_lines = text.split("\n")
        numbers_todo = [int(n) for n in num_text.split(",")]

    grid_size = 5
    boards = []

    for i in range(0, len(boards_lines), grid_size + 1):
        lines = boards_lines[i + 1 : i + grid_size + 1]
        boards.append([ [ int(line[i : i + 2]) for i in range(0, len(line), 3)] for line in lines])
    
    return numbers_todo, boards


def board_complete(board, numbers) -> bool:
    # check rows
    for row in board:
        if all(map(lambda x: x in numbers, row)):
            return True

    # check columns
    for i in range(len(board[0])):
        column = [row[i] for row in board]
        if all(map(lambda x: x in numbers, column)):
            return True

def board_score(board, numbers) -> int:
    s = sum([n if n not in numbers else 0 for row in board for n in row])
    return s * numbers[-1]

def main():
    numbers_todo, boards = get_data()
    marked_numbers = []

    for n in numbers_todo:
        marked_numbers.append(n)
        for board in boards:
            if board_complete(board, marked_numbers):
                print(board)
                # done! Compute score
                print("Score:", board_score(board, marked_numbers))
                return

if __name__ == "__main__":
    main()
