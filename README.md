# Memory-Game

This project contains a memory game where you have to find all the matching pairs in a set of cards. Scores are saved and recorded to a 'Scores.txt' file at the end of a game.

## Game Instructions

Each round in the game, you have options to:
- Input coordinates of a card to flip
- Enter 'reveal' which shows all cards for a short duration but adds a penalty

## Score Calculation

Scores are calculated based on the following equation:
- `final_score = base_score - reveal_penalty - attempt_penalty`

Where:
- `base_score = unique_cards * 100`
- `reveal_penalty = reveals_used * 50`
- `attempt_penalty = max(0, (attempts - unique_cards) * 10)`

## Running the Game
You need to make sure you have python installed on your machine.
This game will frequently clear the console, so permission to clear may be required if using non-native terminal.

To run the code for the memory game:
1. Clone a local copy of the project from [Memory-Game](https://github.com/YakMan101/Memory-Game.git) or download the zip file.
2. Open the terminal and `cd` into the directory containing `Memory-Game.py`.
3. Run `Memory-Game.py` using:
   ```bash
   python3 Memory-Game.py
4. Follow the prompts given in the terminal.

Enjoy the game and try to get the highest score!