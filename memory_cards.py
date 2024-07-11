"""
This script is used to run the memory card game
"""

import itertools
import os
import random
import time
from datetime import datetime


def ask_for_number_of_cards() -> int:
    """
    Ask user for number of unique cards they wish to play with
    """
    while True:
        size = input("Enter number of unique cards: ").strip()
        if size.isdigit():
            if size in ['0', '1']:
                print('Number must be greater than 1')
                continue
            return int(size)
        else:
            print("Error: invalid input, please try again.")


def get_number_of_rows(size) -> int:
    """
    Returns number of rows and columns to be used
    to create the board
    """
    root = int(size**0.5)
    return root if root**2 == size else root + 1


def generate_characters(size) -> list[str]:
    """
    Generates all the cards on the board
    """
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789ΞΠΣΦΨΩξπςφψω"
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


def create_board(size) -> list[list[str]]:
    """
    Generates the nested (can also be staggered) 
    list (the board) that contains all the card info.
    """
    strings = generate_characters(size)
    global no_rows
    no_rows = get_number_of_rows(size * 2)
    board = [
        strings[no_rows * r:no_rows * (r + 1)] for r in range(no_rows - 1)
    ]

    if strings[no_rows * (no_rows - 1):]:
        board.append(strings[no_rows * (no_rows - 1):])
    else:
        no_rows -= 1
    return board


def print_board():
    """
    Prints the current state of the board as it exists now
    """
    row_padding = (len(str(no_rows)) - 1)
    card_padding = max(len(board[0][0]), len(str(no_rows))) + 1

    header_row = ' ' * row_padding + '    '
    for x in range(len(board[0])):
        header_row += str(x) + ' ' * (card_padding - len(str(x)))

    underline = ' ' * row_padding + '  '
    underline += '-' * (len(header_row) - row_padding - 3)

    print(header_row)
    print(underline)

    for r in range(no_rows):
        print(str(r) + ' ' * (row_padding - len(str(r)) + 1) + ' |', end=' ')
        for c in range(len(board[r])):
            card = board[r][c] if revealed[r][c] else '?'
            print(card + ' ' * (card_padding - len(card)), end='')
        print()
    print()


def clear_console():
    """
    Clears all content in the terminal
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def ask_for_coordinates() -> tuple:
    """
    Asks the user for coordinates of cards
    to reveal and wether they want to reveal 
    all of the board
    """
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
    """
    Reveals the contents of the entire board
    """
    global revealed
    revealed_original = [row[:] for row in revealed]
    revealed = [[True] * len(board[r]) for r in range(no_rows)]
    print_board()
    time.sleep(2)
    clear_console()
    revealed = revealed_original


def calculate_score(size: int, reveals_used: int, attempts: int) -> int:
    """
    Calculates the score of the user based on
    attempts made, number of unique cards and reveals used. 
    """
    base_score = size * 100
    reveal_penalty = reveals_used * 50
    attempt_penalty = max(0, (attempts - size) * 10)
    final_score = base_score - reveal_penalty - attempt_penalty
    return final_score


def load_scores(filename: str) -> dict:
    """
    Reads in all of the existing scores from
    file if it exists
    """
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            lines = [x.strip().split(')')[1].split('|')
                     for x in f.readlines() if x.strip()]
            scores = []
            for line in lines:
                score_info = line[0].strip().split(',')
                score_dict = {
                    'score': int(score_info[0].split(':')[1].strip()),
                    'unique_cards': int(score_info[1].split(':')[1].strip()),
                    'attempts': int(score_info[2].split(':')[1].strip()),
                    'reveals_used': int(score_info[3].split(':')[1].strip()),
                    'timestamp': line[1].strip()
                }
                scores.append(score_dict)
            return scores
    return []


def save_scores(filename: str, scores: dict):
    """
    re-writes any existing scores and score of the user
    in descending order of scores
    """
    with open(filename, 'w') as f:
        for i, score in enumerate(scores):
            f.write(f'({i+1}) Score: {score["score"]}, unique cards: {score["unique_cards"]}, '
                    f'attempts: {score["attempts"]}, reveals used: {score["reveals_used"]} | {score["timestamp"]}\n')


def record_score(attempts: int, size: int, reveals_used: int, score: int):
    """
    Performs the reading and writing of all scores
    obtained in the game
    """
    filename = 'scores.txt'
    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    score_entry = {
        'score': score,
        'unique_cards': size,
        'attempts': attempts,
        'reveals_used': reveals_used,
        'timestamp': dt_string
    }

    scores = load_scores(filename)
    scores.append(score_entry)
    scores = sorted(scores, key=lambda x: x['score'], reverse=True)
    save_scores(filename, scores)


def ask_for_initial_board_reveal() -> bool:
    """
    Asks user if they want to reveal the board
    before making any attempts
    """
    while True:
        user_input = input(
            'Reveal board? (yes/no), this will add a penalty: ').strip().lower()
        clear_console()

        if user_input in ['yes', 'y']:
            return True

        if user_input in ['no', 'n']:
            return False

        print("Invalid input, please try again... ")


def play_memory_game():
    """
    Performs the main game play loop of the memory card game
    """
    global board, revealed

    no_unique_cards = ask_for_number_of_cards()
    board = create_board(no_unique_cards)
    revealed = [[False] * len(board[r]) for r in range(no_rows)]

    reveal = input('Reveal board? (yes/no): ').strip().lower()
    clear_console()

    reveals_used = 0
    if ask_for_initial_board_reveal():
        reveals_used += 1
        reveal_all()

    attempts = 0
    pairs_found = 0
    card_revealed = False

    while pairs_found < no_unique_cards:
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
    score = calculate_score(no_unique_cards, reveals_used, attempts)
    print(f"Congratulations! You found all pairs in {attempts} attempts.")
    print(f'Reveals used: {reveals_used}')
    print(f'Total score: {score}')
    record_score(attempts, no_unique_cards, reveals_used, score)


if __name__ == "__main__":
    play_memory_game()
