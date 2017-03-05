# Chess Python 3 Client

This is the root of you AI. Stay out of the `joueur/` folder, it does most of the heavy lifting to play on our game servers. Your AI, and the game objects it manipulates are all in `games/chess/`, with your very own AI living in `games/chess/ai.py` for you to make smarter.

## How to Run

To run from a linux prompt, use 'testRun <game\_name>', where <game\_name> is a name of a game for another client to connect to to allow the two clients to play together.
To use a different starting board given a URL encoded FEN string, use 'testRun <game\_name> --gameSettings fen=<fen\_string>'