# Friendly Snakes
Friendly Snakes is a multiplayer cooperative variant of the classic snake game. With up to four players, each controls their own snake, eating (and drinking) items that change the snakes size, speed, controls, avoiding fire, bombs and explosions, surviving as long as possible while getting larger and larger. But the larger the snakes, the less room there is to maneuver, and suddenly your snake might be trapped without an escape route. Work together and let the snakes shine!

## Installation
A stand-alone installer can be found here: <Add GitHub repo for installer>
TODO: Add info about installer (different GitHub repo)

## How To Play
The game is played on one device. Each player controls their snake with four keyboard keys. The default keys are shown below. To customize the keys, choose "Controls" in the start or in-game menu.

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
- Coffee: Double the snakes speed
- Tea: Halve the snakes speed
- Beer: Reverse the snakes controls for ten seconds (i.e. switch up<->down and left<->right)
- Chili: Uh-Oh. The snake can't handle so much spice. For three seconds, the snakes mouth will get hotter and hotter. After that, the snake will spit fire for two seconds. If it burns another snake or itself, the game is over.
- Bomb: Get the hell outta here! The bomb explodes after nine seconds, burning everything in a 3x3 square around it. If a snake is in that square or enters it while the explosion is still firing, the game is over.
  - Bombs can be pushed! If a snake hits a bomb before it explodes, it moves in the respective direction as long as it hits an undestroyable object (like a wall) or a snake. Items in a bombs way will be erased.

## Prerequesites
The python code uses the following packages:
- Pygame v2.4.0
- Pygame Menu v4.4.3
- Pillow v9.5.0
- cx-Freeze v6.14.7

## Troubleshooting
In case of problems contact me on Discord (BeXXsor) or GitHub.

## Credits
- Game design and implementation: **Thomas Schneider**
- Graphics:
  - Items: magdum, https://opengameart.org/content/32x32-food-set | thekingphoenix, https://opengameart.org/content/cc0-food-icons | Fleurman, https://opengameart.org/content/cc0-food-icons | GDJ, https://openclipart.org/detail/228333
  - Bomb & Explosion animation: Based on momopey, https://opengameart.org/content/pixel-art-bomb-animation, adjusted by me 
  - Menu Background: Design by me based on the following sources: https://www.pngwing.com/en/free-png-bcglq, https://www.pngwing.com/en/free-png-tszci, https://www.pngwing.com/en/free-png-bqtsy, https://www.pngwing.com/en/free-png-zrkot, https://www.pngwing.com/en/free-png-nepqc, https://www.pngwing.com/en/free-png-vwdzk, https://www.pngwing.com/en/free-png-bqiry, https://www.pngwing.com/en/free-png-ihwzr
  - Game Backgrounds: txturs, https://opengameart.org/content/2048-digitally-painted-tileable-desert-sand-texture
- Music:
  - 3xBlast, https://opengameart.org/content/happymelancholic-synth-bells-song-adaptive-layers-pack
- Sounds:
  - Pixabay, https://pixabay.com/sound-effects/ed-burp-and-pop-86789/ & https://pixabay.com/sound-effects/cartoon-slurp-37066/
  - rubberduck, https://opengameart.org/content/80-cc0-creature-sfx
  - soundslikewillem, https://freesound.org/people/soundslikewillem/sounds/184519/ (slightly adjusted by me, esp. volume and speed)
  - deleted_user_5405837, https://freesound.org/people/deleted_user_5405837/sounds/399303/ (slightly adjusted by me, esp. volume and speed)
- Fonts:
  - "Snake Chan" by Darrell Flood: https://www.fontspace.com/snake-chan-font-f29621
  - "Tehisa" by Sealoung: https://www.fontspace.com/tehisa-font-f45097
