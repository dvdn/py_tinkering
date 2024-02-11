# py_labyrinth_online

Labyrinth minimalist game written in Python (for learning purpose).
 You play from your Terminal and you can play online with your friends.
 Several maps available. You can also create your own maps.

It's an evolution of [py_labyrinth](https://github.com/dvdn/py_tinkering/tree/main/py_labyrinth)

## Rules of the game

Find your way around a map to exit ('U' sign)
- to move : direction (n, s, e or o) + steps number
- spells on doors or walls : 'm' to wall up, 'p' to pierce + direction (n, s, e or o)

## Standalone version
One player local game

    python3 run.py
    
## Multiplayer version

Launch server, wait some players and choose map to play

    python3 serveur.py
    
As a player, from a terminal
    
    python3 client.py
    
Game is finished when a player reach the exit ('U' sign).

You can also type 'exit'.

Note : 9 players maximum allowed by game session.

## Tests

To launch tests

    python3 -m unittest discover -s test 
    
