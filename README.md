# tricks
Part1: Run the class Tricks.py and the game will start by asking you about your name then it will start the game.
no libraries needed to run the game.

Tricks.py will call Player.py class which will call player_jack.py, player_diamonds.py, player_king.py, player_tricks.py, player_queens.py depending on the subgame played. 

The result of each subgame will be recorded in a named: players (name of the game).txt   

Part2: The agent can be trained using these five classes: jack_training.py, diamonds_training.py, king_training.py, tricks_training.py, queens_training.py which are supposed to call the classes trained_player_jack, trained_player_diamonds, trained_player_king, trained_player_tricks and trained_player_queens.



Due to failure in designing the reward function the code that construct the game tree and evaluate the tricks was commented.



part3: few minor corrections that was discussed with Dr. Sandy Gould and Dr. Peter Hancox were made to make sure the code runs smoothly. 

1: line 44 in tricks.py was changed from: (line = name + ': 0P(0), 1M(0), 2T(0), 3O(0), dr:0') to be (line = name + ': 0P(0), 1M(0), 2T(0), 3O(0), dr:0 \n')

2: line 52 in player_jack.py was changed from: ('worst bad', 'worst bad high ',) to be ('worst bad', 'worst bad high',)

3: trained_player_diamonds was accidentally deleted and replaced with trained_player_queens, so I copied the correct code which can be found in the GitHub under branch diamonds_training and paste it in the right place.

4: tricks_training was calling trick_player when it was supposed to call the class trained_player_tricks, so it was corrected.

5: The class Player.py uses the .txt files that store the learned Q table, so I changed the name of the files, so it can be overwritten when the training classes are called.

