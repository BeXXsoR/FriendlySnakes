"""A module for global constants used across the friendly snakes package"""

import utils
from enum import Enum


class WidgetState(Enum):
	NORMAL = 0
	PUSHED = 1
	HOVERED = 2


# ----- Constants ------

# --- Colors ---
GREEN = (0, 153, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
PINK = (255, 51, 255)
CYAN = (51, 255, 255)
ORANGE = (255, 128, 0)
BLACK = (0, 0, 0)
COLOR_WIDGET_NORMAL = (76, 123, 209)
COLOR_WIDGET_HOVERED = (111, 164, 255)
BG_COLOR = (167, 226, 247)

# --- Game parameters ---
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
# MIN_SNAKE_SIZE = 4
MIN_SNAKE_SPEED = 1
MAX_SNAKE_SPEED = 1000
FPS = 60
DROP_ITEM_RATE = 5
BOMB_CNTDWN = 9
EXPLOSION_CNTDWN = 2
DRUNK_DURATION = 10
PIQUANCY_GROWING_DURATION = 3
SPIT_FIRE_DURATION = 2
SPIT_FIRE_RANGE = 2
GROWING_SIZES = {utils.Objects.APPLE: 1, utils.Objects.MELON: 3}
SPEEDING_SUMMANDS = {utils.Objects.COFFEE: 3, utils.Objects.TEA: -3}
ITEM_SCORES = {utils.Objects.APPLE: 3, utils.Objects.MELON: 6, utils.Objects.COFFEE: 9, utils.Objects.TEA: 0, utils.Objects.BEER: 7, utils.Objects.CHILI: 5}
REOCC_DUR = 250
REOCC_PER_SEC = int(1000 / REOCC_DUR)

# --- Graphics In-Game ---
FILENAME_SNAKE_PARTS = {GREEN: ["../res/snake_head_green.png", "../res/snake_body_straight_green.png", "../res/snake_body_corner_green.png", "../res/snake_tail_green.png"],
						BLUE: ["../res/snake_head_blue.png", "../res/snake_body_straight_blue.png", "../res/snake_body_corner_blue.png", "../res/snake_tail_blue.png"],
						CYAN: ["../res/snake_head_cyan.png", "../res/snake_body_straight_cyan.png", "../res/snake_body_corner_cyan.png", "../res/snake_tail_cyan.png"],
						PINK: ["../res/snake_head_pink.png", "../res/snake_body_straight_pink.png", "../res/snake_body_corner_pink.png", "../res/snake_tail_pink.png"]}
FILENAME_ITEMS = {utils.Objects.APPLE: "../res/apple.png", utils.Objects.MELON: "../res/melon.png",
				  utils.Objects.COFFEE: "../res/coffee.png", utils.Objects.TEA: "../res/tea.png", utils.Objects.BEER: "../res/beer.png",
				  utils.Objects.CHILI: "../res/chili.png"}
FILENAME_WALL = "../res/wall.png"
FILENAME_FIRE_SPIT = "../res/fire_spit.png"
FILENAME_BOMB = "../res/bomb.gif"
FILENAME_EXPLOSION = "../res/explosion.gif"
FILENAME_DRUNK = "../res/drunk.gif"
FILENAME_PIQU_RISING = "../res/piquancy_rising.gif"
FILENAME_SPEEDO = "../res/speedo.png"
FILENAMES_GAME_BGS_WITH_SCORE_COLORS = {"Desert": ("../res/bg_desert.png", BG_COLOR), "Forest": ("../res/forest.png", BG_COLOR), "Underwater": ("../res/underwater.jpg", BLUE),
										"Space": ("../res/space.png", BG_COLOR), "Sky": ("../res/sunny.png", BLUE), "Night": ("../res/full_moon.png", BG_COLOR)}
FILENAME_LEVEL_INFO = "../res/levels.json"

# --- Graphics Menu ---
FILENAME_START_BG = "../res/menu_bg.png"
FILENAME_PAUSE_MENU_BG = "../res/menu_bg.png"
FILENAMES_SNAKE_COLORS = {GREEN: "../res/menu_snake_green.png", BLUE: "../res/menu_snake_blue.png", CYAN: "../res/menu_snake_cyan.png", PINK: "../res/menu_snake_pink.png"}
FILENAME_LVL_PREV = "../res/level_prev_{}.png"
FILENAME_CONTROLS_BG = "../res/menu_controls_bg.png"
FILENAME_MENU_FRAME = "../res/menu_frame.png"
FILENAMES_BUTTON = {WidgetState.NORMAL: "../res/menu_button_normal.png", WidgetState.PUSHED: "../res/menu_button_pushed.png", WidgetState.HOVERED: "../res/menu_button_hovered.png"}
COLOR_WIDGETS = {WidgetState.NORMAL: COLOR_WIDGET_NORMAL, WidgetState.HOVERED: COLOR_WIDGET_HOVERED}

# --- Music & Sounds ---
FILENAMES_MUSIC_TRACKS = {"Bells Song": "../res/bells_song.ogg", "Happy Arcade": "../res/happy.mp3", "CC Soundtrack 4": "../res/cc_soundtrack4.mp3",
						  "Her Violet Eyes": "../res/HerVioletEyes.mp3", "Around The World": "../res/Aroundtheworld.mp3"}
FILENAMES_ITEM_SOUNDS = {utils.Objects.APPLE: "../res/eat.ogg", utils.Objects.MELON: "../res/eat.ogg", utils.Objects.CHILI: "../res/eat.ogg",
						 utils.Objects.COFFEE: "../res/slurp.ogg", utils.Objects.TEA: "../res/slurp.ogg", utils.Objects.BEER: "../res/burp.ogg",
						 utils.Objects.BOMB: "../res/bomb.ogg", utils.Objects.EXPLOSION: "../res/explosion.ogg", utils.Objects.FIRE_SPIT: "../res/fire_spit.ogg"}
FILENAME_CRASH_SOUND = "../res/crash.ogg"

# --- Fonts & Texts ---
FONT_COURIER_NEW = "Courier New"
FONT_SNAKE_CHAN = "../res/SnakeChan-MMoJ.ttf"
TEXTS_BUTTON_START_MENU = {utils.Language.GERMAN: ["Neues Spiel", "Highscore", "Steuerung", "Optionen", "Verlassen"],
						   utils.Language.ENGLISH: ["New game", "Highscore", "Controls", "Options", "Exit"]}
TEXTS_BUTTON_PAUSE_MENU = {utils.Language.GERMAN: ["Fortsetzen", "Highscore", "Steuerung", "Optionen", "Zurück zum Hauptmenü"],
						   utils.Language.ENGLISH: ["Resume", "Highscore", "Controls", "Options", "Back to main menu"]}
TEXTS_BUTTON_GAME_OVER_MENU = {utils.Language.GERMAN: ["Erneut spielen", "Highscore", "Steuerung", "Optionen", "Zurück zum Hauptmenü"],
							   utils.Language.ENGLISH: ["Play again", "Highscore", "Controls", "Options", "Back to main menu"]}

# --- Display parameters (benchmark screen: 2560x1440)---
BENCHMARK_HEIGHT = 1440
SNAKE_NAME_FONT_SIZE = 40
SNAKE_INFO_FONT_SIZE = 40
SCORE_FONT_SIZE = 40
MAP_TO_SCREEN_RATIO = 0.9
MENU_TOPLEFT = (0, 300)
MENU_SIZE = (670, 705)
BUTTON_AREA_START = (36, 267)
BUTTON_AREA_SIZE = (520, 370)
BUTTON_HEIGHT = 50
OPTIONS_TOP_MARGIN = 13
BUTTON_FONT_SIZE = 25
CONTROLS_FONT_SIZE = 35
SEL_OPTION_FONT_SIZE = 25
LEVEL_PREV_IMG_SIZE = (115, 115)
SNAKE_COLOR_IMG_SIZE = (120, 120)
CONTROL_BG_IMG_SIZE = (200, 200)
CONTROL_LBL_TO_BG_RATIO = 156 / 442
MAX_LEN_FOR_TEAM_NAME = 20
MAX_WIDTH_FOR_TEXT_INPUT = 20
