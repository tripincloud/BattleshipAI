# BattleshipAI
The objective of this project is to study the game of naval battle from a probabilistic point of view. It will first study the combinatorics of the game,then
provide game modeling to optimize a player's chances of winning, and finally to study a more realistic variant of the game.
The game of naval battle is played on a grid of 10 squares by 10 squares. The opponent places on this grid a certain number of ships which are characterized by their
length :
- an aircraft carrier (5 cells) ;
- a cruiser (4 cells);
- a destroyer (3 cells);
- a submarine (3 cells);
- a torpedo boat (2 cells).
The game has the right to place them vertically or horizontally. The positioning of the boats remains secret. The player's objective is to sink all the opponent's boats by
a minimum number of shots. At each turn of the game, he chooses a square where he shoots: if there is no boat on the square, the answer is empty; if the square is occupied by a cell of a boat, the answer is hit; if all the cells of a boat have been hit, then the answer is cast and the corresponding boxes are revealed. When all
boats have been sunk, the game stops and the player's score is the number of moves that were played. The lower the score, the better the player performs.
Note : The player in this game is the AI.
