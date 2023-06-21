# Friendly Snakes
Friendly Snakes is a multiplayer cooperative variant of the classic snake game. Up to four players each control their own snake, eating (and drinking) items that change the snakes size, speed, controls, avoiding fire, bombs and explosions, surviving as long as possible while getting larger and larger. But the larger the snakes, the less room there is to maneuver, and suddenly your snake might be trapped without an escape route. Work together and let the snakes shine!

## Installation
A stand-alone installer can be found here: <Add GitHub repo for installer>
TODO: Add info about installer (different GitHub repo)

## How To Play
The game is played on one device. Each player controls their snake with four keyboard keys. The default keys are shown below. To customize the keys, choose "Controls" in the start menu.

|Action|Player 1|Player 2|Player 3|Player 4|
|:-----|:------:|:------:|:------:|:------:|
|Move snake up|Up arrow|W|KP8|I|
|Move snake down|Down arrow|S|KP5|K|
|Move snake left|Left arrow|A|KP4|J|
|Move snake right|Right arrow|D|KP6|L|

Each snake moves with a certain speed that can be affected by items like coffee or tea. The faster a snake moves, the harder it is to control (obviously). When a snake hits a wall, another snake or itself, or when it gets burned by fire or explosions, the game is over.

### Items
Here is an overview about the various items in the game:
- Apple: Grow the snake by 1
- Watermelon: Grow the snake by 3
- Coffee: Increase the snakes speed by 3
- Tea: Decrease the snakes speed speed by 3
- Beer: Reverse the snakes controls for ten seconds (i.e. switch up<->down and left<->right)
- Chili: Uh-Oh. The snake can't handle so much spice. For three seconds, the snakes mouth will get hotter and hotter. After that, the snake will spit fire for two seconds. If it burns another snake or itself, the game is over.
- Bomb: Get the hell outta here! The bomb explodes after nine seconds, burning everything in a 3x3 square around it. If a snake is in that square or enters it while the explosion is still firing, the game is over.
  - Bombs can be pushed! If a snake hits a bomb before it explodes, it moves in the respective direction as long as it hits an undestroyable object (like a wall) or a snake. Items in a bombs way will be erased. But be aware that the snakes are only strong enough to push a single bomb. If you try to push two bombs that are one behind the other, or if you try to push a bomb when there's a wall behind it, you crash!

## Prerequesites (for using the python code)
The python code uses the following packages:
- Pygame v2.4.0
- Pygame Menu v4.4.3
- Pillow v9.5.0
- cx-Freeze v6.14.7

## Troubleshooting
In case of problems contact me on Discord (BeXXsor) or GitHub.

## Credits
- Game design and implementation: **Thomas Schneider**
- All credits: see "Credits.md"
