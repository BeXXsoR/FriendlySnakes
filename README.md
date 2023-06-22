# Friendly Snakes
Friendly Snakes is a multiplayer cooperative variant of the classic snake game. Up to four players each control their own snake, eating (and drinking) items that change the snakes size, speed, controls, avoiding fire, bombs and explosions, surviving as long as possible while getting larger and larger. But the larger the snakes, the less room there is to maneuver, and suddenly your snake might be trapped without an escape route. Work together and let the snakes shine!

## Installation
The repository already contains a ready-to-use executable file for win64. Just download the zip file (i.e. click the green *Code*-button in the top right, then choose *Download ZIP*), unpack it, navigate to the *build_win64* directory and open *friendly_snakes.exe*.
If you have a GitHub account, you can of course just clone the repo as well instead of downloading the zip.

## Start Menu
In the menu you find the following options:
- New Game: Select level and number of players and start a new game
- Highscore: View highscores
- Controls: Change the snakes colors and controls
- Options: Change the music track and volume, the sound volume and the in-game background
- Exit: Exit the game

## How To Play
The game itself is mostly self-explanatory. Just try it out and see what happens :).

If you still like to know some infos beforehand, read ahead:
The game is played on one device. Each player controls their snake with four keyboard keys. The default keys and colors are shown below. To customize them, choose "Controls" in the start menu.

|Action|Player 1|Player 2|Player 3|Player 4|
|:-----|:------:|:------:|:------:|:------:|
|Move snake up|Up arrow|W|KP8|I|
|Move snake down|Down arrow|S|KP5|K|
|Move snake left|Left arrow|A|KP4|J|
|Move snake right|Right arrow|D|KP6|L|
|Pause the game|ESC|ESC|ESC|ESC|

|Player|Default color|
|:-----|:------:|
|Player 1|Green|
|Player 2|Blue|
|Player 3|Cyan|
|Player 4|Pink|

Each snake moves with a certain speed that can be affected by items like coffee or tea. The faster a snake moves, the harder it is to control (obviously). When a snake hits a wall, another snake or itself, or when it gets burned by fire or explosions, the game is over.
There are two types of levels: Highscore and Survive. In Highscore levels, the goal is to reach as many points as possible, while in Survive levels you want to survive as long as possible without crashing. You can see the type of a level in the top right of the game screen.

### Items
Here is an overview about the various items in the game:
- **Apple**: Grow the snake by 1
- **Watermelon**: Grow the snake by 3
- **Coffee**: Increase the snakes speed by 3
- **Tea**: Decrease the snakes speed speed by 3
- **Beer**: Reverse the snakes controls for ten seconds (i.e. switch up<->down and left<->right)
- **Chili**: Uh-Oh. The snake can't handle so much spice. For three seconds, the snakes mouth will get hotter and hotter. After that, the snake will spit fire for two seconds. If it burns another snake or itself, the game is over.
- **Bomb**: Get the hell outta here! The bomb explodes after nine seconds, burning everything in a 3x3 square around it. If a snake is in that square or enters it while the explosion is still firing, the game is over.
  - Bombs can be pushed! If a snake hits a bomb before it explodes, it moves in the respective direction as long as it hits an undestroyable object (like a wall) or a snake. Items in a bombs way will be erased. But be aware that the snakes are only strong enough to push a single bomb. If you try to push two bombs that are one behind the other, or if you try to push a bomb when there's a wall behind it, you crash!

## Prerequesites (for using the python code)
The python code uses the following packages:
- Pygame v2.4.0
- Pygame Menu v4.4.3
- Pillow v9.5.0
- cx-Freeze v6.14.7

## Troubleshooting
In case of problems contact me on Discord (BeXXsor).

## Credits
- Game design and implementation: **Thomas Schneider**
- Further credits: see *Credits.md*
