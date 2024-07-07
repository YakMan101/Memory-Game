# Memory-Game
This project contains a memory game where you have to find all the matching pairs in a set of cards.

Scores are saved and recorded to a 'Scores.txt' file at the end of a game.

Each round in the game, user has options to:
    
    - input coordinates of card to flip
    
    - or enter 'reveal' which shows all cards for a small duration but adds on a penalty

Scores are calculated based the equation:

    final_score = base_score - reveal_penalty - attempt_penalty,

where:

    base_score = number of unique cards*100

    reveal_penalty = number of reveals used * 50

    attempt_penalty = the larger of 0 and (attempts - size) * 10



To run the code for the memory game: 
1) Clone local copy of the project (https://github.com/YakMan101/Memory-Game.git) or download the zip
2) Open the terminal and 'cd' into the directory containing Memory-Game.py
3) run Memory-Game.py using: 'python3 Memory-Game.py'
4) Then simply follow the prompts given in the terminal