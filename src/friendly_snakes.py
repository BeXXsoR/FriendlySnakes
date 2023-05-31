"""A multiplayer cooperative snake game

import structure:

friendly_snakes
|-- communicator (incl. the main game loop)
|	|-- menu
|	|-- game
|	|	|-- graphics
|	|	|	|-- snake
|	|	|	|-- level
Additionally, the utils and constants class are widely used and imported in almost every module.
"""

#
# # ----- Imports --------
# import utils
import sys
from communicator import Communicator
# import itertools
# import random
# import json
# from dataclasses import dataclass
# import menu
# import animations
# import pygame
#
# pygame.init()
#
# # ----- Constants ------
# # region Constants
# GREEN = (0, 153, 0)
# RED = (255, 0, 0)
# YELLOW = (255, 255, 0)
# BLUE = (0, 0, 255)
# WHITE = (255, 255, 255)
# PINK = (255, 51, 255)
# CYAN = (51, 255, 255)
# ORANGE = (255, 128, 0)
# GREY = (192, 192, 192)
# BLACK = (0, 0, 0)
# BG_COLOR = WHITE
# ORIENT_UP = (-1, 0)
# ORIENT_DOWN = (1, 0)
# ORIENT_LEFT = (0, -1)
# ORIENT_RIGHT = (0, 1)
# NO_ORIENTATION = (0, 0)
# ROTATIONS_STRAIGHT = {ORIENT_RIGHT: 0, ORIENT_UP: 90, ORIENT_LEFT: 180, ORIENT_DOWN: 270}
# ROTATIONS_CORNER = {(ORIENT_DOWN, ORIENT_LEFT): 90, (ORIENT_LEFT, ORIENT_DOWN): 270,
# 					(ORIENT_DOWN, ORIENT_RIGHT): 0, (ORIENT_RIGHT, ORIENT_DOWN): 180,
# 					(ORIENT_UP, ORIENT_LEFT): 180, (ORIENT_LEFT, ORIENT_UP): 0,
# 					(ORIENT_UP, ORIENT_RIGHT): 270, (ORIENT_RIGHT, ORIENT_UP): 90}
# MIN_SNAKE_SIZE = 4
# MIN_SNAKE_SPEED = 1
# MAX_SNAKE_SPEED = 1000
# FPS = 60
# MAP_TO_SCREEN_RATIO = 0.9
# DROP_ITEM_SPEED = 5
# BOMB_CNTDWN = 9
# EXPLOSION_CNTDWN = 2
# DRUNK_DURATION = 10
# PIQUANCY_GROWING_DURATION = 3
# SPIT_FIRE_DURATION = 2
# SPIT_FIRE_RANGE = 2
# FILENAME_LEVEL_INFO = "../res/levels.json"
# FILENAME_SNAKE_PARTS = {GREEN: ["../res/snake_head_green.png", "../res/snake_body_straight_green.png", "../res/snake_body_corner_green.png", "../res/snake_tail_green.png"],
# 						BLUE: ["../res/snake_head_blue.png", "../res/snake_body_straight_blue.png", "../res/snake_body_corner_blue.png", "../res/snake_tail_blue.png"],
# 						CYAN: ["../res/snake_head_cyan.png", "../res/snake_body_straight_cyan.png", "../res/snake_body_corner_cyan.png", "../res/snake_tail_cyan.png"],
# 						PINK: ["../res/snake_head_pink.png", "../res/snake_body_straight_pink.png", "../res/snake_body_corner_pink.png", "../res/snake_tail_pink.png"]}
# FILENAME_ITEMS = {utils.Objects.APPLE: "../res/apple.png", utils.Objects.MELON: "../res/melon.png",
# 				  utils.Objects.COFFEE: "../res/coffee.png", utils.Objects.TEA: "../res/tea.png", utils.Objects.BEER: "../res/beer.png",
# 				  utils.Objects.CHILI: "../res/chili.png"}
# FILENAME_FIRE_SPIT = "../res/fire_spit.png"
# FILENAME_BOMB = "../res/bomb.gif"
# FILENAME_EXPLOSION = "../res/explosion.gif"
# FILENAME_DRUNK = "../res/drunk.gif"
# FILENAME_PIQU_RISING = "../res/piquancy_rising.gif"
# FILENAME_SPEEDO = "../res/speedo.png"
# FILENAMES_BG = {utils.Backgrounds.DESERT: "../res/bg_desert.png"}
# FILENAME_ITEM_SOUNDS = {utils.Objects.APPLE: "../res/eat.ogg", utils.Objects.MELON: "../res/eat.ogg", utils.Objects.CHILI: "../res/eat.ogg",
# 						utils.Objects.COFFEE: "../res/slurp.ogg", utils.Objects.TEA: "../res/slurp.ogg", utils.Objects.BEER: "../res/burp.ogg"}
# FILENAME_CRASH_SOUND = "../res/crash.ogg"
# FILENAME_TITLE_THEME = "../res/title_theme.ogg"
# GROWING_SIZES = {utils.Objects.APPLE: 1, utils.Objects.MELON: 3}
# SPEEDING_FACTORS = {utils.Objects.COFFEE: 2, utils.Objects.TEA: 0.5}
# UPDATE_SNAKES = [pygame.event.custom_type() for _ in range(4)]
# REOCC_TIMER = pygame.event.custom_type()
# REOCC_DUR = 250
# REOCC_PER_SEC = int(1000 / REOCC_DUR)
# SNAKE_NAME_FONT_SIZE = 40
# SNAKE_INFO_FONT_SIZE = 40
# # DROP_ITEM = pygame.event.custom_type()
# # endregion
#
#
# # ----- Classes --------
# class Communicator:
# 	"""Class for interacting between different parts of the game, e.g. start menu and game engine"""
# 	def __init__(self):
# 		player_names = ["Kokosnuss", "Tiger", "Muh", "Mausi"]
# 		player_colors = [GREEN, BLUE, CYAN, PINK]
# 		player_controls = [
# 			{pygame.K_UP: ORIENT_UP, pygame.K_LEFT: ORIENT_LEFT, pygame.K_DOWN: ORIENT_DOWN, pygame.K_RIGHT: ORIENT_RIGHT},
# 			{pygame.K_w: ORIENT_UP, pygame.K_a: ORIENT_LEFT, pygame.K_s: ORIENT_DOWN, pygame.K_d: ORIENT_RIGHT},
# 			{pygame.K_KP8: ORIENT_UP, pygame.K_KP4: ORIENT_LEFT, pygame.K_KP5: ORIENT_DOWN, pygame.K_KP6: ORIENT_RIGHT},
# 			{pygame.K_i: ORIENT_UP, pygame.K_j: ORIENT_LEFT, pygame.K_k: ORIENT_DOWN, pygame.K_l: ORIENT_RIGHT}]
# 		self.main_surface = pygame.display.set_mode((0, 0))
# 		self.levels = []
# 		self.read_level_infos()
# 		# pygame.mixer_music.load(FILENAME_TITLE_THEME)
# 		# pygame.mixer_music.play(fade_ms=2000)
# 		self.start_menu = None
# 		self.init_start_menu()
# 		# self.game = Game(player_names, player_colors, player_controls, self.levels[0], self.main_surface)
# 		self.game = Game(player_names[:1], player_colors[:1], player_controls[:1], self.levels[0], self.main_surface)
# 		# self.game = Game(player_names[:2], player_colors[:2], player_controls[:2], self.levels[0], self.main_surface)
#
# 	def read_level_infos(self) -> None:
# 		"""Reads the level infos from the json file"""
# 		with (open(FILENAME_LEVEL_INFO)) as file_level_info:
# 			level_infos = json.load(file_level_info)
# 		for level_info in level_infos:
# 			self.levels.append(Level(level_info))
#
# 	def init_start_menu(self):
# 		self.start_menu = menu.StartMenu(self.main_surface)
# 		# Wait for user pressing key
# 		key_pressed = False
# 		while not key_pressed:
# 			for event in pygame.event.get():
# 				if event.type == pygame.KEYDOWN:
# 					key_pressed = True
# 		self.start_menu.slide_menu_in()
#
# 	def handle_start_menu(self) -> bool:
# 		"""Handle the start menu. Returns True if the user starts a new game or False if they want to exit"""
# 		return self.start_menu.handle_events()
#
# 	def start_game(self):
# 		# self.game.show_map()
# 		self.game.game_loop()
#
#
# class Level:
# 	"""The class for the levels"""
# 	def __init__(self, level_info: {}):
# 		self.name = None
# 		self.map = []
# 		self.start_pos = []
# 		self.item_rates = {}
# 		self.trg_score = None
# 		self.profiles = {}
# 		for k, v in level_info.items():
# 			if k == "map":
# 				self.map = utils.strings_to_objects(v)
# 				self.start_pos = self.get_start_pos(v)
# 			else:
# 				setattr(self, k, v)
# 		self.num_cols = len(self.map)
# 		self.num_rows = len(self.map[0])
# 		# init item list according to their rates
# 		self.items = []
# 		for k, v in self.item_rates.items():
# 			self.items.extend([utils.string_to_object(k)] * v)
#
# 	def get_start_pos(self, map_str: [str]) -> [[(int, int)]]:
# 		start_pos = []
# 		sep = ','
# 		for row, line in enumerate(map_str):
# 			for col, value in enumerate(line.split(sep)):
# 				if len(value) == 3 and value[0] == 's':
# 					player_idx = int(value[1]) - 1
# 					body_idx = int(value[2]) - 1
# 					while len(start_pos) <= player_idx:
# 						start_pos.append([])
# 					while len(start_pos[player_idx]) <= body_idx:
# 						start_pos[player_idx].append(tuple())
# 					start_pos[player_idx][body_idx] = (row, col)
# 		return start_pos
#
#
# class Snake:
# 	"""The class for the players/ snakes"""
#
# 	def __init__(self, name: str, idx: int, color: (int, int, int), controls: {}):
# 		self.name = name
# 		self.idx = idx
# 		self.color = color
# 		# controls is a dict for the inputs that control the snake. Keys are the keyboard keys as pygame constants,
# 		# values are the orientations (as (int, int) tuples)
# 		self.controls = controls
# 		self._pos = None
# 		self.head = None
# 		self.tail = None
# 		self.orientation = None
# 		self.speed = 4
# 		self.is_growing = 0
# 		self.is_drunk = 0
# 		self.piquancy_growing = 0
# 		self.spits_fire = 0
# 		self.spit_fire_posis = []
#
# 	@property
# 	def pos(self) -> [(int, int)]:
# 		return self._pos
#
# 	@pos.setter
# 	def pos(self, new_pos: [(int, int)]) -> None:
# 		"""Update head, tail and orientation together with pos"""
# 		self._pos = new_pos
# 		self.head = new_pos[0]
# 		self.tail = new_pos[-1]
# 		self.orientation = utils.subtract_tuples(self.head, self.pos[1])
# 		self.is_growing = max(self.is_growing - 1, 0)
# 		# if self.spits_fire > 0:
# 		# 	self.spit_fire_posis = utils.get_spit_fire_squares(self.head, self.orientation, SPIT_FIRE_RANGE, _map)
#
# 	def update_orientation(self, key) -> bool:
# 		"""Update the orientation based on the pressed key. Return True if the pressed key belonged to a snake"""
# 		if key in self.controls:
# 			cur_orient = utils.subtract_tuples(self.head, self._pos[1])
# 			if utils.add_tuples([self.controls[key], cur_orient]) != (0, 0):
# 				self.orientation = self.controls[key]
# 			return True
# 		return False
#
# 	def grow(self, size: int):
# 		"""Let the snake grow by the given size"""
# 		self.is_growing += size
#
# 	def adjust_speed(self, factor: float):
# 		"""Adjust the speed of the snake by multiplying it with the given factor"""
# 		self.speed = max(MIN_SNAKE_SPEED, min(int(factor * self.speed), MAX_SNAKE_SPEED))
#
# 	def update_counting(self) -> bool:
# 		"""Handle reoccurring updates. Returns True if the spit fire posis need to be updated"""
# 		update_spit_fire_posis = False
# 		# Check drunk countdown
# 		if self.is_drunk > 1:
# 			self.is_drunk -= 1
# 		elif self.is_drunk == 1:
# 			self.get_sober()
# 		# Check piquancy and spit fire countdown
# 		if self.piquancy_growing > 1:
# 			self.piquancy_growing -= 1
# 		elif self.piquancy_growing == 1:
# 			self.spit_fire()
# 			update_spit_fire_posis = True
# 		if self.spits_fire > 1:
# 			self.spits_fire -= 1
# 		elif self.spits_fire == 1:
# 			self.release_fire()
# 			update_spit_fire_posis = True
# 		return update_spit_fire_posis
#
# 	def get_drunk(self) -> None:
# 		"""Handle the snake getting drunk"""
# 		if not self.is_drunk:
# 			self.transpose_controls()
# 		self.is_drunk = max(self.is_drunk, DRUNK_DURATION * REOCC_PER_SEC)
#
# 	def get_sober(self) -> None:
# 		"""Handle the snake getting sober"""
# 		if self.is_drunk:
# 			self.transpose_controls()
# 			self.is_drunk = 0
#
# 	def transpose_controls(self) -> None:
# 		"""Transpose the controls for up<->down and left<->right"""
# 		tp = {ORIENT_UP: ORIENT_DOWN, ORIENT_LEFT: ORIENT_RIGHT, ORIENT_DOWN: ORIENT_UP, ORIENT_RIGHT: ORIENT_LEFT}
# 		self.controls = {k: tp[v] for k, v in self.controls.items()}
#
# 	def get_piquant(self) -> None:
# 		"""Handle the snake eating a chili"""
# 		self.piquancy_growing = max(self.piquancy_growing, PIQUANCY_GROWING_DURATION * REOCC_PER_SEC)
#
# 	def spit_fire(self) -> None:
# 		"""Handle the piquancy countdown running out"""
# 		self.piquancy_growing = 0
# 		self.spits_fire = max(self.spits_fire, SPIT_FIRE_DURATION * REOCC_PER_SEC)
# 		# self.spit_fire_posis = utils.get_spit_fire_squares(self.head, self.orientation, SPIT_FIRE_RANGE)
# 		# return self.spit_fire_posis
#
# 	def release_fire(self):
# 		"""Stop the snake spitting fire"""
# 		self.spits_fire = 0
# 		self.spit_fire_posis = []
#
#
# class Game:
# 	"""The main game class"""
# 	def __init__(self, player_names: [str], player_colors: [(int, int, int)], player_controls: [{}], level, main_surface: pygame.Surface):
# 		self.clock = pygame.time.Clock()
# 		self.level = level
# 		self.snakes = [Snake(name, idx, color, controls) for idx, (name, color, controls) in enumerate(zip(player_names, player_colors, player_controls))]
# 		self.init_snake_pos()
# 		self.graphics = Graphics(main_surface, self.level.num_rows, self.level.num_cols)
# 		# crashes is a list of tuples of positions. For each crash that occurred, it holds the coordinates of the
# 		# two squares between which the crash happened
# 		self.crashes: [((int, int), (int, int))] = []
# 		self.free_squares = set([(i, j) for i, row in enumerate(level.map) for j, obj in enumerate(row) if obj == utils.Objects.NONE]) - set([pos for snake in self.snakes for pos in snake.pos])
# 		self.upd_snake_events = [pygame.event.Event(event_id, {"snake_idx": idx}) for idx, event_id in enumerate(UPDATE_SNAKES[:len(self.snakes)])]
# 		self.reocc_event = pygame.event.Event(REOCC_TIMER, {"duration": REOCC_DUR})
# 		self.passed_reoccs = 0
# 		self.item_sounds = {k: pygame.mixer.Sound(v) for k, v in FILENAME_ITEM_SOUNDS.items()}
# 		self.crash_sound = pygame.mixer.Sound(FILENAME_CRASH_SOUND)
# 		# counters is a dict tracking the game elements that needs to be updated every second. Its keys are tuples of
# 		# type (utils.Cntable, int), where the former shows the kind of element and the latter the additional index
# 		# corresponding to that kind of element (e.g. (utils.Cntable.BOMB, 0) would refer to bomb #0 in the bombs list.
# 		# If no additional index is needed, None is used for the latter.
# 		# The values of the dict are ints showing the countdown for the specific element w.r.t. to REOCC_DUR.
# 		self.counters = {(utils.Cntble.DROP_ITEM, None): DROP_ITEM_SPEED * REOCC_PER_SEC}
# 		# self.bombs is a dict of all bombs. Key is the location of the bomb, value is the cntdwn and the orientation of the bomb
# 		self.bombs: {(int, int): (int, (int, int))} = {}
# 		self.explosions: {(int, int): int} = {}
#
# 	def init_snake_pos(self) -> None:
# 		"""Initialize the positions of the snakes"""
# 		for snake, pos in zip(self.snakes, self.level.start_pos):
# 			snake.pos = pos
#
# 	def game_loop(self) -> None:
# 		"""Main game loop"""
# 		# Initialize timer
# 		for snake in self.snakes:
# 			pygame.time.set_timer(self.upd_snake_events[snake.idx], int(1000 / snake.speed))
# 		# pygame.time.set_timer(DROP_ITEM, DROP_ITEM_SPEED)
# 		pygame.time.set_timer(self.reocc_event, REOCC_DUR)
# 		self.graphics.update_display(self.level, self.snakes, self.crashes, self.create_bomb_dict(), self.explosions)
# 		# start game loop
# 		is_running = True
# 		crashed = False
# 		while is_running:
# 			snakes_to_update = []
# 			for event in pygame.event.get():
# 				if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
# 					# Quit
# 					is_running = False
# 				elif event.type == pygame.KEYDOWN and not crashed:
# 					# Try updating orientation of snake
# 					for snake in self.snakes:
# 						if snake.update_orientation(event.key):
# 							break
# 					else:
# 						# Check for other keys
# 						pass
# 				elif event.type in UPDATE_SNAKES and not crashed:
# 					# Update position of snake
# 					snakes_to_update.append(self.snakes[event.snake_idx])
# 				elif event.type == REOCC_TIMER and not crashed:
# 					# update all counting game elements
# 					self.update_counting()
# 					# threatened_squares = []
# 					for snake in self.snakes:
# 						if snake.update_counting():
# 							self.update_spit_fire_posis(snake)
# 					# crashed_squares = self.is_snake_on_squares(threatened_squares)
# 					# self.crashes.extend([(pos, pos) for pos in crashed_squares])
# 				# Update display
# 				if snakes_to_update:
# 					for item in self.update_snakes(snakes_to_update):
# 						# Play sounds
# 						if item in self.item_sounds:
# 							self.item_sounds[item].play()
# 					for snake in snakes_to_update:
# 						pygame.time.set_timer(self.upd_snake_events[snake.idx], int(1000 / snake.speed))
# 				self.graphics.update_display(self.level, self.snakes, self.crashes, self.create_bomb_dict(), self.explosions)
# 				if self.crashes and not crashed:
# 					self.crash_sound.play()
# 					crashed = True
# 				self.clock.tick(FPS)
#
# 	def update_snakes(self, snakes_to_upd: [Snake]) -> [utils.Objects]:
# 		"""Update the position of the snakes. Returns a list of objects that have been eaten"""
# 		new_posis = []
# 		remaining_posis = [snake.pos for snake in self.snakes if snake not in snakes_to_upd]
# 		new_spit_fire_posis = []
# 		rem_spit_fire_posis = [snake.spit_fire_posis for snake in self.snakes if snake not in snakes_to_upd]
# 		objects = []
# 		# update snake positions locally and check for collisions with obstacles
# 		for snake in snakes_to_upd:
# 			new_square = utils.add_tuples([snake.head, snake.orientation])
# 			obj_at_new_pos = self.level.map[new_square[0]][new_square[1]]
# 			match obj_at_new_pos:
# 				case obj if obj in utils.Hurting:
# 					self.crashes.append((snake.head, new_square))
# 				case item if item in utils.Speeding:
# 					snake.adjust_speed(SPEEDING_FACTORS[item])
# 					self.level.map[new_square[0]][new_square[1]] = utils.Objects.NONE
# 				case item if item in utils.Growing:
# 					snake.grow(GROWING_SIZES[item])
# 					self.level.map[new_square[0]][new_square[1]] = utils.Objects.NONE
# 				case utils.Objects.BOMB:
# 					self.bombs[new_square] = (self.bombs[new_square][0], snake.orientation)
# 					_, has_crashed = self.move_bomb(new_square)
# 					if has_crashed:
# 						self.crashes.append((snake.head, new_square))
# 				case utils.Objects.BEER:
# 					snake.get_drunk()
# 					self.level.map[new_square[0]][new_square[1]] = utils.Objects.NONE
# 				case utils.Objects.CHILI:
# 					snake.get_piquant()
# 					self.level.map[new_square[0]][new_square[1]] = utils.Objects.NONE
# 				case _:
# 					pass
# 			objects.append(obj_at_new_pos)
# 			new_snake_pos = [new_square] + (snake.pos if snake.is_growing > 0 else snake.pos[:-1])
# 			new_posis.append(new_snake_pos)
# 			if snake.spits_fire:
# 				new_spit_fire_posis.append(utils.get_spit_fire_squares(new_snake_pos[0], utils.subtract_tuples(new_snake_pos[0], new_snake_pos[1]), SPIT_FIRE_RANGE, self.level.map))
# 			else:
# 				new_spit_fire_posis.append([])
# 		# Check for crashes with same snake
# 		self.crashes.extend([(new_pos[1], new_pos[0]) for new_pos in new_posis if new_pos[0] in new_pos[1:]])
# 		# Check for crashes with other snakes
# 		self.crashes.extend([(new_pos[1], new_pos[0]) for new_pos, other_pos in itertools.product(new_posis, new_posis + remaining_posis) if new_pos != other_pos and new_pos[0] in other_pos])
# 		# Check for crashes by snakes running into explosions
# 		exploding_squares = [(row - 1 + i, col - 1 + j) for (row, col) in self.explosions for i in range(3) for j in range(3)]
# 		self.crashes.extend([(new_pos[1], new_pos[0]) for new_pos in new_posis if new_pos[0] in exploding_squares])
# 		# Update real snake positions if no crash happened
# 		if not self.crashes:
# 			for snake, new_pos, new_spit_fire_pos in zip(snakes_to_upd, new_posis, new_spit_fire_posis):
# 				self.free_squares |= {snake.pos[-1]} if snake.pos[-1] != new_pos[-1] else set()
# 				self.free_squares -= {new_pos[0]}
# 				snake.pos = new_pos
# 				snake.spit_fire_posis = new_spit_fire_pos
# 		# Check for crashes by snakes getting burned (only after the snake posis got updated, so that the new posis
# 		# incl. the new fire spit gets drawn on the screen)
# 		fire_posis = new_spit_fire_posis + rem_spit_fire_posis
# 		self.crashes.extend([(pos, pos) for snake_pos, fire_pos in itertools.product(new_posis + remaining_posis, fire_posis) for pos in snake_pos if pos in fire_pos])
# 		return objects
#
# 	def update_counting(self):
# 		""""Update all counting game elements"""
# 		# Update explosions
# 		for pos in list(self.explosions.keys()):
# 			self.explosions[pos] -= 1
# 			if self.explosions[pos] == 0:
# 				self.explosion_is_over(pos)
# 		# Update bombs
# 		for pos, (cntdwn, orientation) in list(self.bombs.items()):
# 			new_cntdwn = cntdwn - 1
# 			self.bombs[pos] = (new_cntdwn, orientation)
# 			if new_cntdwn == 0:
# 				self.handle_explosion(pos)
# 			elif orientation != NO_ORIENTATION:
# 				# Move the bomb one square
# 				self.move_bomb(pos)
# 		# Update Cntable
# 		for k, v in self.counters.items():
# 			elem, idx = k
# 			if v == 1:
# 				# Countdown reaches zero, handle it depending on the element.
# 				match elem:
# 					case utils.Cntble.DROP_ITEM:
# 						# drop a new item on the map
# 						i, j = random.choice(list(self.free_squares))
# 						new_object = random.choice(self.level.items)
# 						self.level.map[i][j] = new_object
# 						self.free_squares -= {(i, j)}
# 						self.counters[k] = DROP_ITEM_SPEED * REOCC_PER_SEC
# 						if new_object == utils.Objects.BOMB:
# 							self.bombs[(i, j)] = (BOMB_CNTDWN * REOCC_PER_SEC, NO_ORIENTATION)
# 					case _:
# 						pass
# 			else:
# 				self.counters[k] -= 1
#
# 	def handle_explosion(self, bomb_pos: (int, int)) -> None:
# 		"""Update the situation when a bomb explodes"""
# 		row, col = bomb_pos
# 		exploded_squares = [(row - 1 + i, col - 1 + j) for i in range(3) for j in range(3)]
# 		for i, j in exploded_squares:
# 			if self.level.map[i][j] not in utils.Undestroyable:
# 				self.level.map[i][j] = utils.Objects.EXPLOSION
# 		# Check for exploded snakes
# 		self.crashes.extend([(pos, pos) for snake in self.snakes for pos in snake.pos if pos in exploded_squares])
# 		# Update dicts
# 		self.explosions[bomb_pos] = EXPLOSION_CNTDWN * REOCC_PER_SEC
# 		del self.bombs[bomb_pos]
# 		return
#
# 	def explosion_is_over(self, pos: (int, int)) -> None:
# 		"""Update the situation when an explosion cools down"""
# 		row, col = pos
# 		rel_squares = [(row - 1 + i, col - 1 + j) for i in range(3) for j in range(3)]
# 		for i, j in rel_squares:
# 			if self.level.map[i][j] not in utils.Undestroyable:
# 				self.level.map[i][j] = utils.Objects.NONE
# 		del self.explosions[pos]
#
# 	def move_bomb(self, old_pos: (int, int)) -> ((int, int), bool):
# 		"""Move the bomb one square and return (a) it's new position (or the old one if the bomb isn't moving) and (b) a bool showing if the bomb hit a stopper like a wall, a snake part etc."""
# 		cntdwn, orientation = self.bombs[old_pos]
# 		new_pos = utils.add_two_tuples(old_pos, orientation)
# 		if orientation == NO_ORIENTATION:
# 			# Bomb isn't moving
# 			return old_pos, False
# 		snake_posis = [pos for snake in self.snakes for pos in snake.pos]
# 		if self.level.map[new_pos[0]][new_pos[1]] == utils.Objects.WALL or new_pos in snake_posis:
# 			# Bomb hit a stopper -> stop it's movement
# 			self.bombs[old_pos] = (cntdwn, NO_ORIENTATION)
# 			return old_pos, True
# 		self.level.map[new_pos[0]][new_pos[1]] = utils.Objects.BOMB
# 		self.level.map[old_pos[0]][old_pos[1]] = utils.Objects.NONE
# 		self.bombs[new_pos] = (cntdwn, orientation)
# 		del self.bombs[old_pos]
# 		return new_pos, False
#
# 	def is_snake_on_squares(self, squares: [(int, int)]) -> [(int, int)]:
# 		"""Returns all the squares of the given square list where a snake is on"""
# 		return [pos for pos in squares for snake in self.snakes if pos in snake.pos]
#
# 	def create_bomb_dict(self) -> {(int, int): int}:
# 		return {pos: cntdwn for pos, (cntdwn, orientation) in self.bombs.items()}
#
# 	def update_spit_fire_posis(self, snake: Snake):
# 		"""Updates the spit fire posis for the given snake"""
# 		if snake.spits_fire > 0:
# 			snake.spit_fire_posis = utils.get_spit_fire_squares(snake.pos[0], snake.orientation, SPIT_FIRE_RANGE, self.level.map)
# 		else:
# 			snake.spit_fire_posis = []
#
# 	def show_map(self):
# 		is_running = True
# 		while is_running:
# 			for event in pygame.event.get():
# 				if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
# 					is_running = False
# 			self.graphics.display_map(self.level)
#
#
# class Graphics:
# 	"""The class for displaying all graphics on the screen"""
# 	def __init__(self, main_surface: pygame.Surface, num_rows: int, num_cols: int):
# 		self.main_surface = main_surface
# 		self.bg = pygame.transform.scale(pygame.image.load(FILENAMES_BG[utils.Backgrounds.DESERT]).convert_alpha(), self.main_surface.get_size())
# 		self.edge_size = int(min(self.main_surface.get_width() * MAP_TO_SCREEN_RATIO / num_cols, self.main_surface.get_height() * MAP_TO_SCREEN_RATIO / num_rows))
# 		self.square_size = (self.edge_size, self.edge_size)
# 		map_size = (self.edge_size * num_cols, self.edge_size * num_rows)
# 		# Field surface
# 		self.map_rect = pygame.rect.Rect((0, 0), map_size)
# 		self.map_rect.center = self.main_surface.get_rect().center
# 		self.map_surface = self.main_surface.subsurface(self.map_rect)
# 		self.square_posis = [[(j * self.edge_size, i * self.edge_size) for j in range(num_cols)] for i in range(num_rows)]
# 		# snake status surfaces
# 		status_rect_size = (int((MAP_TO_SCREEN_RATIO * self.main_surface.get_width() - self.map_rect.width) / 2), int(self.map_rect.height / 4))
# 		status_rect = pygame.rect.Rect((0, 0), status_rect_size)
# 		self.snake_status_rects = []
# 		for i in range(4):
# 			cur_rect = status_rect.copy()
# 			cur_rect.top = self.snake_status_rects[-1].bottom if self.snake_status_rects else self.map_rect.top
# 			cur_rect.left = int((1 - MAP_TO_SCREEN_RATIO) / 2 * self.main_surface.get_width())
# 			# 	if i % 2 == 0 else self.map_rect.right
# 			self.snake_status_rects.append(cur_rect)
# 		self.status_surfaces = [self.main_surface.subsurface(rect) for rect in self.snake_status_rects]
# 		# Rects inside a snake status surface
# 		num_rows = 6
# 		num_cols = 6
# 		edge_size = int(min(status_rect.width / num_cols, status_rect.height / num_rows))
# 		rect_size = (edge_size, edge_size)
# 		self.snake_head_img_rect = pygame.rect.Rect((0, 0), rect_size)
# 		self.snake_name_rect = pygame.rect.Rect(self.snake_head_img_rect.topright, (3 * edge_size, edge_size))
# 		self.snake_body_img_rect = pygame.rect.Rect(self.snake_head_img_rect.bottomleft, rect_size)
# 		self.snake_size_rect = pygame.rect.Rect(self.snake_body_img_rect.topright, rect_size)
# 		self.snake_speed_img_rect = pygame.rect.Rect(self.snake_size_rect.topright, rect_size)
# 		self.snake_speed_rect = pygame.rect.Rect(self.snake_speed_img_rect.topright, rect_size)
# 		self.snake_drunk_rect = pygame.rect.Rect(self.snake_body_img_rect.bottomleft, rect_size)
# 		self.snake_chili_rect = pygame.rect.Rect(self.snake_speed_img_rect.bottomleft, rect_size)
# 		self.snake_burger_rects = [pygame.rect.Rect((i * edge_size, self.snake_drunk_rect.bottom), rect_size) for i in range(3)]
# 		# Prepare images
# 		self.items_orig = {obj: pygame.image.load(filename).convert_alpha() for obj, filename in FILENAME_ITEMS.items()}
# 		self.items = {obj: pygame.transform.scale(img_orig, self.square_size)
# 					  for obj, img_orig in self.items_orig.items()}
# 		self.fire = pygame.transform.scale(pygame.image.load(FILENAME_FIRE_SPIT).convert_alpha(), (SPIT_FIRE_RANGE * self.edge_size, self.edge_size))
# 		self.bomb_anim = animations.Animation(FILENAME_BOMB, self.square_size)
# 		self.explosion_anim = animations.Animation(FILENAME_EXPLOSION, (3 * self.edge_size, 3 * self.edge_size))
# 		self.drunk_anim = animations.Animation(FILENAME_DRUNK, self.square_size)
# 		self.piqu_rising_anim = animations.Animation(FILENAME_PIQU_RISING, self.square_size)
# 		# self.explosions = {}
# 		self.snake_parts_orig = {k: [pygame.image.load(filename).convert_alpha() for filename in v] for k, v in FILENAME_SNAKE_PARTS.items()}
# 		self.snake_parts = {k: [pygame.transform.scale(img_orig, self.square_size) for img_orig in v] for k, v in self.snake_parts_orig.items()}
# 		status_img_size = utils.mult_tuple_to_int(rect_size, 1)
# 		self.snake_status_imgs = {k: [pygame.transform.scale(img_orig, status_img_size) for img_orig in v] for k, v in self.snake_parts_orig.items() if k != utils.SnakeParts.TAIL}
# 		self.speedo_img = pygame.transform.scale(pygame.image.load(FILENAME_SPEEDO).convert_alpha(), utils.mult_tuple_to_int(rect_size, 0.8))
# 		self.drunk_img = pygame.transform.scale(self.items_orig[utils.Objects.BEER], utils.mult_tuple_to_int(rect_size, 0.8))
# 		# Prepare fonts
# 		self.snake_name_font = pygame.font.Font(None, SNAKE_NAME_FONT_SIZE)
# 		self.snake_info_font = pygame.font.Font(None, SNAKE_INFO_FONT_SIZE)
#
# 	def update_display(self, level: Level, snakes: [Snake], crashes: [((int, int), (int, int))], bombs: {(int, int): int}, explosions: {(int, int): int}) -> None:
# 		"""Draw everything onto the screen"""
# 		# Draw background
# 		# self.main_surface.fill(BG_COLOR)
# 		self.main_surface.blit(self.bg, (0, 0))
# 		# Draw level
# 		wall_color = GREY
# 		for row, obj_row in enumerate(level.map):
# 			for col, obj in enumerate(obj_row):
# 				grid_pos = (row, col)
# 				screen_pos = self.grid_to_screen_pos(grid_pos)
# 				if obj == utils.Objects.WALL:
# 					pygame.draw.rect(self.map_surface, wall_color, pygame.rect.Rect(screen_pos, self.square_size))
# 				elif obj == utils.Objects.BOMB:
# 					cur_frame_id = self.bomb_anim.num_frames - bombs[grid_pos]
# 					cur_frame = self.bomb_anim.pygame_frames[cur_frame_id]
# 					self.map_surface.blit(cur_frame, screen_pos)
# 				elif obj == utils.Objects.EXPLOSION:
# 					# Do nothing here, explosions are handled seperately later (so that for explosions at the edge,
# 					# the explosions are only drawn after the wall has been drawn)
# 					pass
# 				elif obj != utils.Objects.NONE:
# 					self.map_surface.blit(self.items[obj], screen_pos)
# 		# Draw explosions
# 		for grid_pos in explosions:
# 			screen_pos = self.grid_to_screen_pos(grid_pos)
# 			cur_frame_id = self.explosion_anim.num_frames - explosions[grid_pos]
# 			cur_frame = self.explosion_anim.pygame_frames[cur_frame_id]
# 			self.map_surface.blit(cur_frame, utils.subtract_tuples(screen_pos, self.square_size))
# 		# Draw snakes
# 		for snake in snakes:
# 			head_orientation = utils.subtract_tuples(snake.pos[0], snake.pos[1])
# 			for idx, pos in enumerate(snake.pos):
# 				screen_pos = self.grid_to_screen_pos(pos)
# 				if idx == 0 and snake.color in self.snake_parts:
# 					# snake head (incl. piquancy and drunk animation)
# 					self.map_surface.blit(pygame.transform.rotate(self.snake_parts[snake.color][utils.SnakeParts.HEAD.value], ROTATIONS_STRAIGHT[head_orientation]), screen_pos)
# 					if snake.piquancy_growing > 0:
# 						cur_frame_id = self.piqu_rising_anim.num_frames - snake.piquancy_growing
# 						cur_frame = self.piqu_rising_anim.pygame_frames[cur_frame_id]
# 						self.map_surface.blit(pygame.transform.rotate(cur_frame, ROTATIONS_STRAIGHT[head_orientation]), screen_pos)
# 					if snake.is_drunk > 0:
# 						cur_frame_id = self.drunk_anim.num_frames - snake.is_drunk
# 						cur_frame = self.drunk_anim.pygame_frames[cur_frame_id]
# 						self.map_surface.blit(pygame.transform.rotate(cur_frame, ROTATIONS_STRAIGHT[head_orientation] % 180), screen_pos)
# 				elif idx == len(snake.pos) - 1 and snake.color in self.snake_parts:
# 					# snake tail
# 					tail_orientation = utils.subtract_tuples_int(snake.pos[idx - 1], pos)
# 					self.map_surface.blit(pygame.transform.rotate(self.snake_parts[snake.color][utils.SnakeParts.TAIL.value], ROTATIONS_STRAIGHT[tail_orientation]), screen_pos)
# 				elif idx != len(snake.pos) - 1 and snake.color in self.snake_parts:
# 					# snake body
# 					orientation_front = utils.subtract_tuples_int(snake.pos[idx - 1], pos)
# 					orientation_back = utils.subtract_tuples_int(pos, snake.pos[idx + 1])
# 					if orientation_front == orientation_back:
# 						snake_part_idx = utils.SnakeParts.BODY_STRAIGHT.value if orientation_front == orientation_back else utils.SnakeParts.BODY_CORNER.value
# 						rotation = ROTATIONS_STRAIGHT[orientation_front] if orientation_front == orientation_back else ROTATIONS_CORNER[(orientation_front, orientation_back)]
# 					else:
# 						snake_part_idx = utils.SnakeParts.BODY_CORNER.value
# 						rotation = ROTATIONS_CORNER[(orientation_front, orientation_back)]
# 					self.map_surface.blit(pygame.transform.rotate(self.snake_parts[snake.color][snake_part_idx], rotation), screen_pos)
# 				else:
# 					pygame.draw.rect(self.map_surface, snake.color, pygame.rect.Rect(screen_pos, self.square_size))
# 			# Draw spit fire
# 			if snake.spit_fire_posis:
# 				screen_pos = self.grid_to_screen_pos(snake.spit_fire_posis[0 if head_orientation in [ORIENT_RIGHT, ORIENT_DOWN] else -1])
# 				# The spit fire range might be cut because of obstacles, so we have to check for that and only show
# 				# the image partially in that case
# 				factor = len(snake.spit_fire_posis) / SPIT_FIRE_RANGE
# 				trg_area = (0, 0, factor * self.fire.get_width(), self.fire.get_height())
# 				trg_image = self.fire.subsurface(trg_area)
# 				self.map_surface.blit(pygame.transform.rotate(trg_image, ROTATIONS_STRAIGHT[head_orientation]), screen_pos)
# 		# Draw crashes
# 		radius1 = self.edge_size / 2.0 * 0.7
# 		radius2 = self.edge_size / 2.0 * 0.8
# 		crashes_centers = tuple([utils.multiply_tuple(utils.add_tuples([self.grid_to_screen_pos(crash[0]), self.grid_to_screen_pos(crash[1]), self.square_size]), 0.5) for crash in crashes])
# 		for center in crashes_centers:
# 			pygame.draw.circle(self.map_surface, ORANGE, center, radius2)
# 			pygame.draw.circle(self.map_surface, RED, center, radius1)
# 		# Draw snake status
# 		for surf, snake in zip(self.status_surfaces, snakes):
# 			# surf.fill((random.randrange(255), random.randrange(255), random.randrange(255)))
# 			to_be_added_rects = [self.snake_chili_rect]
# 			to_be_added_rects.extend(self.snake_burger_rects)
# 			# Draw status images
# 			surf.blit(self.snake_status_imgs[snake.color][utils.SnakeParts.HEAD.value], self.snake_status_imgs[snake.color][utils.SnakeParts.HEAD.value].get_rect(center=self.snake_head_img_rect.center))
# 			surf.blit(self.snake_status_imgs[snake.color][utils.SnakeParts.BODY_STRAIGHT.value], self.snake_status_imgs[snake.color][utils.SnakeParts.HEAD.value].get_rect(center=self.snake_body_img_rect.center))
# 			surf.blit(self.speedo_img, self.speedo_img.get_rect(center=self.snake_speed_img_rect.center))
# 			# Display status texts
# 			name_font = self.snake_name_font.render(snake.name, True, snake.color)
# 			surf.blit(name_font, name_font.get_rect(center=self.snake_name_rect.center))
# 			len_font = self.snake_info_font.render(str(len(snake.pos)), True, BLACK)
# 			surf.blit(len_font, len_font.get_rect(center=self.snake_size_rect.center))
# 			speed_font = self.snake_info_font.render(str(snake.speed), True, BLACK)
# 			surf.blit(speed_font, speed_font.get_rect(center=self.snake_speed_rect.center))
# 			if snake.is_drunk:
# 				surf.blit(self.drunk_img, self.drunk_img.get_rect(center=self.snake_drunk_rect.center))
# 				drunk_font = self.snake_info_font.render(str(int(snake.is_drunk / REOCC_PER_SEC)), True, BLACK if snake.is_drunk > 3 else RED)
# 				surf.blit(drunk_font, drunk_font.get_rect(center=self.snake_drunk_rect.center))
# 			# for rect in to_be_added_rects:
# 				# pygame.draw.rect(surf, (random.randrange(255), random.randrange(255), random.randrange(255)), rect)
# 				# pygame.draw.rect(surf, GREY, rect)
# 		pygame.display.update()
#
# 	def grid_to_screen_pos(self, grid_pos: (int, int)) -> (int, int):
# 		"""Translates coordinates in the grid to the screen position of the topleft corner of the corresponding rect"""
# 		return self.square_posis[grid_pos[0]][grid_pos[1]]
#
# 	def display_map(self, level: Level):
# 		self.main_surface.fill(BG_COLOR)
# 		# Draw level
# 		wall_color = GREY
# 		for row, obj_row in enumerate(level.map):
# 			for col, obj in enumerate(obj_row):
# 				screen_pos = self.grid_to_screen_pos((row, col))
# 				if obj == utils.Objects.WALL:
# 					pygame.draw.rect(self.map_surface, wall_color,
# 									 pygame.rect.Rect(screen_pos, self.square_size))
# 		pygame.display.update()
#

# ----- Main script ----
if __name__ == "__main__":
	comm = Communicator()
	if comm.handle_start_menu():
		sys.exit(comm.start_game())
