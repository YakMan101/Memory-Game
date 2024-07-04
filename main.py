import itertools
import os
import random
import time
from datetime import datetime


def ask_board_size():
    while True:
        size = input("Enter number of unique cards: ").strip()
        if size.isdigit():
            if size in ['0', '1']:
                print('Number must be greater than 1')
                continue
            return int(size)
        else:
            print("Error: invalid input, please try again.")


def get_rows_and_columns(size):
    root = int(size**0.5)
    return root if root**2 == size else root + 1


def generate_characters(size):
    characters = "ABCDEFGHIJKLMNOPQRSTUVWYZ123456789ΞΠΣΦΨΩξπςφψω"
    if size < len(characters):
        combinations = list(characters)
    else:
        combinations = [
            ''.join(pair) for pair in itertools.product(characters, repeat=2)
        ]

    selected_strings = random.sample(combinations, size)
    final_strings = selected_strings * 2
    random.shuffle(final_strings)
    return final_strings


def create_board(size):
    strings = generate_characters(size)
    global row_col
    row_col = get_rows_and_columns(size * 2)
    board = [
        strings[row_col * r:row_col * (r + 1)] for r in range(row_col - 1)
    ]

    if strings[row_col * (row_col - 1):]:
        board.append(strings[row_col * (row_col - 1):])
    else:
        row_col -= 1
    return board


def print_board():
    row_padding = (len(str(row_col)) - 1)
    card_padding = max(len(board[0][0]), len(str(row_col))) + 1

    header_row = ' ' * row_padding + '    ' + ''.join(
        [(str(x) + ' ' * (card_padding - len(str(x))))
         for x in range(len(board[0]))])
    underline = ' ' * row_padding + '  ' + '-' * (len(header_row) -
                                                  row_padding - 3)

    print(header_row)
    print(underline)

    for r in range(row_col):
        print(str(r) + ' ' * (row_padding - len(str(r)) + 1) + ' |', end=' ')
        for c in range(len(board[r])):
            card = board[r][c] if revealed[r][c] else 'X'
            print(card + ' ' * (card_padding - len(card)), end='')
        print()
    print()


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def ask_for_coordinates():
    while True:
        user_input = input(
            "Enter the coordinates (row column) or type 'reveal': ").strip(
        ).lower()

        if user_input == 'reveal':
            clear_console()
            reveal_all()
            return 'reveal', 'reveal'

        try:
            x, y = map(int, user_input.split())
            if revealed[x][y]:
                print('Card already revealed.')
            else:
                revealed[x][y] = True
                return x, y

        except (ValueError, IndexError):
            print('Invalid input. Please enter valid coordinates.')


def reveal_all():
    global revealed
    revealed_original = [row[:] for row in revealed]
    revealed = [[True] * len(board[r]) for r in range(row_col)]
    print_board()
    time.sleep(2)
    clear_console()
    revealed = revealed_original


def calculate_score(size, reveals_used, attempts):
    base_score = size * 100
    reveal_penalty = reveals_used * 50
    attempt_penalty = max(0, (attempts - size) * 10)
    final_score = base_score - reveal_penalty - attempt_penalty
    return final_score


def record_score(attempts, size, reveals_used, score):
    fname = 'Scores.txt'
    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    score = calculate_score(size, reveals_used, attempts)
    with open(fname, "a") as f:
        f.write(
            f'\nScore: {score} (unique cards:{size}, attempts: {attempts}, '
            f'reveals used: {reveals_used}) | {dt_string}')


def play_memory_game():
    global board, revealed

    size = ask_board_size()
    board = create_board(size)
    revealed = [[False] * len(board[r]) for r in range(row_col)]

    reveal = input('Reveal board? (yes/no): ').strip().lower()
    clear_console()

    reveals_used = 0
    if reveal in ['yes', 'y']:
        reveals_used += 1
        reveal_all()

    attempts = 0
    pairs_found = 0
    card_revealed = False

    while pairs_found < size:
        print_board()

        if not card_revealed:
            x1, y1 = ask_for_coordinates()
            if x1 == 'reveal':
                reveals_used += 1
                continue
            clear_console()
            print_board()

        card_revealed = False
        x2, y2 = ask_for_coordinates()
        if x2 == 'reveal':
            reveals_used += 1
            card_revealed = True
            continue
        clear_console()
        print_board()

        attempts += 1

        if board[x1][y1] == board[x2][y2]:
            revealed[x1][y1] = revealed[x2][y2] = True
            pairs_found += 1
            print("It's a match!")
            time.sleep(1)
            clear_console()
        else:
            revealed[x1][y1] = revealed[x2][y2] = False
            print("Not a match.")
            time.sleep(2)
            clear_console()

    print_board()
    score = calculate_score(size, reveals_used, attempts)
    print(f"Congratulations! You found all pairs in {attempts} attempts.")
    print(f'Reveals used: {reveals_used}')
    print(f'Total score: {score}')
    record_score(attempts, size, reveals_used, score)


if __name__ == "__main__":
    play_memory_game()
