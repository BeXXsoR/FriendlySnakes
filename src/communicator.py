"""Module for the communicator class in the friendly snakes package"""

# ----- Imports --------
import utils
import json
from start_menu import StartMenu
from game import Game
from level import Level
from graphics import Graphics
from constants import GREEN, BLUE, CYAN, PINK, ORIENT_UP, ORIENT_DOWN, ORIENT_LEFT, ORIENT_RIGHT, REOCC_DUR, FPS
import pygame

pygame.init()

# ----- Constants ------
FILENAME_LEVEL_INFO = "../res/levels.json"
FILENAME_ITEM_SOUNDS = {utils.Objects.APPLE: "../res/eat.ogg", utils.Objects.MELON: "../res/eat.ogg", utils.Objects.CHILI: "../res/eat.ogg",
						utils.Objects.COFFEE: "../res/slurp.ogg", utils.Objects.TEA: "../res/slurp.ogg", utils.Objects.BEER: "../res/burp.ogg"}
FILENAME_CRASH_SOUND = "../res/crash.ogg"
UPDATE_SNAKES = [pygame.event.custom_type() for _ in range(4)]
REOCC_TIMER = pygame.event.custom_type()


# ----- Classes --------
class Communicator:
	"""Class for interacting between different parts of the game, e.g. start menu and game engine"""
	def __init__(self):
		snake_names = ["Kokosnuss", "Tiger", "Muh", "Mausi"]
		snake_colors = [GREEN, BLUE, CYAN, PINK]
		snake_controls = [
			{pygame.K_UP: ORIENT_UP, pygame.K_LEFT: ORIENT_LEFT, pygame.K_DOWN: ORIENT_DOWN, pygame.K_RIGHT: ORIENT_RIGHT},
			{pygame.K_w: ORIENT_UP, pygame.K_a: ORIENT_LEFT, pygame.K_s: ORIENT_DOWN, pygame.K_d: ORIENT_RIGHT},
			{pygame.K_KP8: ORIENT_UP, pygame.K_KP4: ORIENT_LEFT, pygame.K_KP5: ORIENT_DOWN, pygame.K_KP6: ORIENT_RIGHT},
			{pygame.K_i: ORIENT_UP, pygame.K_j: ORIENT_LEFT, pygame.K_k: ORIENT_DOWN, pygame.K_l: ORIENT_RIGHT}]
		self.snake_controls_all = []
		for controls in snake_controls:
			self.snake_controls_all.extend(controls.keys())
		self.main_surface = pygame.display.set_mode((0, 0))
		self.levels = []
		self.read_level_infos()
		# pygame.mixer_music.load(FILENAME_TITLE_THEME)
		# pygame.mixer_music.play(fade_ms=2000)
		self.start_menu = None
		self.init_start_menu()
		self.level = self.levels[0]
		# self.game = Game(snake_names, snake_colors, snake_controls, self.level, self.main_surface)
		self.game = Game(snake_names[:1], snake_colors[:1], snake_controls[:1], self.level, self.main_surface)
		# self.game = Game(snake_names[:2], snake_colors[:2], snake_controls[:2], self.level, self.main_surface)
		self.graphics = Graphics(self.main_surface, self.level.num_rows, self.level.num_cols)
		self.upd_snake_events = [pygame.event.Event(event_id, {"snake_idx": idx}) for idx, event_id in enumerate(UPDATE_SNAKES[:len(self.game.snakes)])]
		self.reocc_event = pygame.event.Event(REOCC_TIMER, {"duration": REOCC_DUR})
		self.item_sounds = {k: pygame.mixer.Sound(v) for k, v in FILENAME_ITEM_SOUNDS.items()}
		self.crash_sound = pygame.mixer.Sound(FILENAME_CRASH_SOUND)
		self.clock = pygame.time.Clock()

	def read_level_infos(self) -> None:
		"""Reads the level infos from the json file"""
		with (open(FILENAME_LEVEL_INFO)) as file_level_info:
			level_infos = json.load(file_level_info)
		for level_info in level_infos:
			self.levels.append(Level(level_info))

	def init_start_menu(self):
		self.start_menu = StartMenu(self.main_surface)
		# Wait for user pressing key
		key_pressed = False
		while not key_pressed:
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					key_pressed = True
		self.start_menu.slide_menu_in()

	def handle_start_menu(self) -> bool:
		"""Handle the start menu. Returns True if the user starts a new game or False if they want to exit"""
		return self.start_menu.menu_loop()

	def start_game(self):
		# self.game.show_map()
		self.game_loop()

	def game_loop(self) -> None:
		"""Main game loop"""
		# Initialize timer
		for snake in self.game.snakes:
			pygame.time.set_timer(self.upd_snake_events[snake.idx], int(1000 / snake.speed))
		pygame.time.set_timer(self.reocc_event, REOCC_DUR)
		self.graphics.update_display(*self.game.get_infos_for_updating_display())
		# start game loop
		is_running = True
		crashed = False
		while is_running:
			snake_ids_to_update = []
			for event in pygame.event.get():
				if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
					# Quit
					is_running = False
				elif event.type == pygame.KEYDOWN and event.key in self.snake_controls_all and not crashed:
					# Update orientation of snake
					self.game.update_snake_orientation(event.key)
				elif event.type == pygame.KEYDOWN and not crashed:
					# Handle other pressed keys
					pass
				elif event.type in UPDATE_SNAKES and not crashed:
					# Update position of snake (only add to list here, real updating is done later)
					snake_ids_to_update.append(event.snake_idx)
				elif event.type == REOCC_TIMER and not crashed:
					# update all counting elements
					self.game.update_counting()
				# Update position of snakes
				if snake_ids_to_update:
					items = self.game.update_snakes(snake_ids_to_update)
					self.play_sounds(items)
					for _id in snake_ids_to_update:
						pygame.time.set_timer(self.upd_snake_events[_id], int(1000 / self.game.snakes[_id].speed))
				if self.game.crashes and not crashed:
					self.crash_sound.play()
					crashed = True
				# Update display
				self.graphics.update_display(*self.game.get_infos_for_updating_display())
				self.clock.tick(FPS)

	def play_sounds(self, items: [utils.Objects]) -> None:
		"""Play the sounds for the given items"""
		for item in items:
			if item in self.item_sounds:
				self.item_sounds[item].play()
