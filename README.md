# AI-University
All the code written for the Knowledge Representation part of the Artificial Intelligence class in my 2nd year of University.

The most relevant files are:
* `problema_lacatului.py`, which is basically a backtracking problem in which a node state is represented by the configuration of a lock. The goal of the problem is to open the lock. This is implemented using the A* search.

* `tictactoe.py`, which implements a bot that plays Tic Tac Toe in the console with the user. The bot can be configured to use either min-max or alpha-beta as its decision making algorithm.

* `reversi.py`, which implements a bot that plays Reversi in the console with the user. The bot can use min-max or alpha-beta and it has several different levels of difficulty. Since this game is more complex than Tic Tac Toe, the heuristic choice comes more into play. I combined 3 concepts for the bot's heuristic: 
  *  the degree of mobility that each player has (i.e. the number of moves they can make)
  *  the number of corners occupied by each player, since they are the most valuable positions in this game.
  *  the sum of the static weights of each player (i.e. the sum of "values" of the positions occupied by each player). Each position on the grid has a static weight assigned that will contribute to the heuristic score of the player that occupies it.
