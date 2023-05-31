"""A module for global constants used across the friendly snakes package"""

import utils

# ----- Constants ------
# region Constants
GREEN = (0, 153, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
PINK = (255, 51, 255)
CYAN = (51, 255, 255)
ORANGE = (255, 128, 0)
GREY = (192, 192, 192)
BLACK = (0, 0, 0)
BG_COLOR = WHITE
ORIENT_UP = (-1, 0)
ORIENT_DOWN = (1, 0)
ORIENT_LEFT = (0, -1)
ORIENT_RIGHT = (0, 1)
NO_ORIENTATION = (0, 0)
ROTATIONS_STRAIGHT = {ORIENT_RIGHT: 0, ORIENT_UP: 90, ORIENT_LEFT: 180, ORIENT_DOWN: 270}
ROTATIONS_CORNER = {(ORIENT_DOWN, ORIENT_LEFT): 90, (ORIENT_LEFT, ORIENT_DOWN): 270,
					(ORIENT_DOWN, ORIENT_RIGHT): 0, (ORIENT_RIGHT, ORIENT_DOWN): 180,
					(ORIENT_UP, ORIENT_LEFT): 180, (ORIENT_LEFT, ORIENT_UP): 0,
					(ORIENT_UP, ORIENT_RIGHT): 270, (ORIENT_RIGHT, ORIENT_UP): 90}
MIN_SNAKE_SIZE = 4
MIN_SNAKE_SPEED = 1
MAX_SNAKE_SPEED = 1000
FPS = 60
MAP_TO_SCREEN_RATIO = 0.9
DROP_ITEM_SPEED = 5
BOMB_CNTDWN = 9
EXPLOSION_CNTDWN = 2
DRUNK_DURATION = 10
PIQUANCY_GROWING_DURATION = 3
SPIT_FIRE_DURATION = 2
SPIT_FIRE_RANGE = 2
FILENAME_SNAKE_PARTS = {GREEN: ["../res/snake_head_green.png", "../res/snake_body_straight_green.png", "../res/snake_body_corner_green.png", "../res/snake_tail_green.png"],
						BLUE: ["../res/snake_head_blue.png", "../res/snake_body_straight_blue.png", "../res/snake_body_corner_blue.png", "../res/snake_tail_blue.png"],
						CYAN: ["../res/snake_head_cyan.png", "../res/snake_body_straight_cyan.png", "../res/snake_body_corner_cyan.png", "../res/snake_tail_cyan.png"],
						PINK: ["../res/snake_head_pink.png", "../res/snake_body_straight_pink.png", "../res/snake_body_corner_pink.png", "../res/snake_tail_pink.png"]}
FILENAME_ITEMS = {utils.Objects.APPLE: "../res/apple.png", utils.Objects.MELON: "../res/melon.png",
				  utils.Objects.COFFEE: "../res/coffee.png", utils.Objects.TEA: "../res/tea.png", utils.Objects.BEER: "../res/beer.png",
				  utils.Objects.CHILI: "../res/chili.png"}
FILENAME_FIRE_SPIT = "../res/fire_spit.png"
FILENAME_BOMB = "../res/bomb.gif"
FILENAME_EXPLOSION = "../res/explosion.gif"
FILENAME_DRUNK = "../res/drunk.gif"
FILENAME_PIQU_RISING = "../res/piquancy_rising.gif"
FILENAME_SPEEDO = "../res/speedo.png"
FILENAMES_BG = {utils.Backgrounds.DESERT: "../res/bg_desert.png"}
FILENAME_TITLE_THEME = "../res/title_theme.ogg"
GROWING_SIZES = {utils.Objects.APPLE: 1, utils.Objects.MELON: 3}
SPEEDING_FACTORS = {utils.Objects.COFFEE: 2, utils.Objects.TEA: 0.5}
REOCC_DUR = 250
REOCC_PER_SEC = int(1000 / REOCC_DUR)
SNAKE_NAME_FONT_SIZE = 40
SNAKE_INFO_FONT_SIZE = 40
BG_ITEMS = [("Desert", 0)]
MUSIC_TRACK_ITEMS = [("Bells Song", 0)]
# endregion