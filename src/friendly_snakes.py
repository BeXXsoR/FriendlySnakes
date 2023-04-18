"""A multiplayer cooperative snake game"""

# ----- Imports --------
import utils
import sys
import itertools
import json
import pygame

pygame.init()

# ----- Constants ------
GREEN = (0, 153, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
PINK = (255, 51, 255)
CYAN = (51, 255, 255)
ORANGE = (255, 128, 0)
GREY = (192, 192, 192)
BG_COLOR = WHITE
ORIENT_UP = (-1, 0)
ORIENT_DOWN = (1, 0)
ORIENT_LEFT = (0, -1)
ORIENT_RIGHT = (0, 1)
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
FILENAME_LEVEL_INFO = "../res/levels.json"
FILENAME_SNAKE_PARTS = {GREEN: ["../res/snake_head_green.png", "../res/snake_body_straight_green.png", "../res/snake_body_corner_green.png"]}
FILENAME_ITEMS = {utils.Objects.APPLE: "../res/apple.png", utils.Objects.MELON: "../res/melon.png",
				  utils.Objects.COFFEE: "../res/coffee.png", utils.Objects.TEA: "../res/tea.png", utils.Objects.BEER: "../res/beer.png"}
GROWING_SIZES = {utils.Objects.APPLE: 1, utils.Objects.MELON: 3}
SPEEDING_FACTORS = {utils.Objects.COFFEE: 2, utils.Objects.TEA: 0.5}
UPDATE_SNAKES = [pygame.event.custom_type() for _ in range(4)]


# ----- Classes --------
class Communicator:
	"""Class for interacting between different parts of the game, e.g. start menu and game engine"""
	def __init__(self):
		player_names = ["Player1", "Player2", "Player3", "Player4"]
		player_colors = [GREEN, BLUE, CYAN, PINK]
		player_controls = [
			{pygame.K_UP: ORIENT_UP, pygame.K_LEFT: ORIENT_LEFT, pygame.K_DOWN: ORIENT_DOWN, pygame.K_RIGHT: ORIENT_RIGHT},
			{pygame.K_w: ORIENT_UP, pygame.K_a: ORIENT_LEFT, pygame.K_s: ORIENT_DOWN, pygame.K_d: ORIENT_RIGHT},
			{pygame.K_KP8: ORIENT_UP, pygame.K_KP4: ORIENT_LEFT, pygame.K_KP5: ORIENT_DOWN, pygame.K_KP6: ORIENT_RIGHT},
			{pygame.K_i: ORIENT_UP, pygame.K_j: ORIENT_LEFT, pygame.K_k: ORIENT_DOWN, pygame.K_l: ORIENT_RIGHT}]
		self.start_menu = None
		self.levels = []
		self.read_level_infos()
		# self.game = Game(player_names, player_colors, player_controls, self.levels[1])
		self.game = Game(player_names[:1], player_colors[:1], player_controls[:1], self.levels[0])

	def read_level_infos(self) -> None:
		"""Reads the level infos from the json file"""
		with (open(FILENAME_LEVEL_INFO)) as file_level_info:
			level_infos = json.load(file_level_info)
		for level_info in level_infos:
			self.levels.append(Level(level_info))

	def start_game(self):
		self.game.game_loop()


class Game:
	"""The main game class"""
	def __init__(self, player_names: [str], player_colors: [(int, int, int)], player_controls: [{}], level):
		self.clock = pygame.time.Clock()
		self.level = level
		self.snakes = [Snake(name, idx, color, controls) for idx, (name, color, controls) in enumerate(zip(player_names, player_colors, player_controls))]
		self.init_snake_pos()
		self.graphics = Graphics(self.level.num_rows, self.level.num_cols)
		# crashes is a list of tuples of positions. For each crash that occurred, it holds the coordinates of the
		# two squares between which the crash happened
		self.crashes = []
		self.upd_snake_events = [pygame.event.Event(event_id, {"snake_idx": idx}) for idx, event_id in enumerate(UPDATE_SNAKES[:len(self.snakes)])]

	def init_snake_pos(self) -> None:
		"""Initialize the positions of the snakes"""
		for snake, pos in zip(self.snakes, self.level.start_pos):
			snake.pos = pos

	def game_loop(self) -> None:
		"""Main game loop"""
		self.graphics.update_display(self.level, self.snakes, self.crashes)
		is_running = True
		# Initialize snake timer
		for snake in self.snakes:
			pygame.time.set_timer(self.upd_snake_events[snake.idx], int(1000 / snake.speed))
		# start game loop
		self.graphics.update_display(self.level, self.snakes, self.crashes)
		while is_running:
			snakes_to_update = []
			for event in pygame.event.get():
				if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
					# Quit
					is_running = False
				elif event.type == pygame.KEYDOWN:
					# Update orientation of snake
					for snake in self.snakes:
						snake.update_orientation(event.key)
				elif event.type in UPDATE_SNAKES:
					# Update position of snake
					# print(event)
					snakes_to_update.append(self.snakes[event.snake_idx])
			# Update display
			# time_passed += self.clock.tick()
			# snakes_to_update = self.get_snakes_to_update(time_passed)
			if snakes_to_update:
				self.update_snakes(snakes_to_update)
				self.graphics.update_display(self.level, self.snakes, self.crashes)
				for snake in snakes_to_update:
					pygame.time.set_timer(self.upd_snake_events[snake.idx], int(1000 / snake.speed))
			self.clock.tick(FPS)
			# pygame.time.delay(int(1.000 / max([snake.speed for snake in self.snakes])))

	# def update_snake_wo_considering_other_snakes(self, snake):
	# 	new_square = utils.add_tuples([snake.head, snake.orientation])
	# 	obj_at_new_pos = self.level.map[new_square[0]][new_square[1]]
	# 	match obj_at_new_pos:
	# 		case utils.Objects.WALL:
	# 			self.crashes.append((snake.head, new_square))
	# 		case eatable if eatable in utils.Eatable:
	# 			snake.grow(EATABLE_GROWS[eatable])
	# 			self.level.map[new_square[0]][new_square[1]] = utils.Objects.NONE
	# 		case _:
	# 			pass
	# 	if snake.is_growing > 0:
	# 		return [new_square] + snake.pos
	# 	else:
	# 		return [new_square] + snake.pos[:-1]

	def update_snakes(self, snakes_to_upd: []) -> None:
		"""Update the position of the snakes"""
		new_posis = []
		remaining_posis = [snake.pos for snake in self.snakes if snake not in snakes_to_upd]
		# update snake positions locally and check for collisions with obstacles
		for snake in snakes_to_upd:
			new_square = utils.add_tuples([snake.head, snake.orientation])
			obj_at_new_pos = self.level.map[new_square[0]][new_square[1]]
			match obj_at_new_pos:
				case utils.Objects.WALL:
					self.crashes.append((snake.head, new_square))
				case item if item in utils.Speeding:
					snake.adjust_speed(SPEEDING_FACTORS[item])
					self.level.map[new_square[0]][new_square[1]] = utils.Objects.NONE
				case item if item in utils.Growing:
					snake.grow(GROWING_SIZES[item])
					self.level.map[new_square[0]][new_square[1]] = utils.Objects.NONE
				case utils.Objects.BEER:
					snake.transpose_controls()
					self.level.map[new_square[0]][new_square[1]] = utils.Objects.NONE
				case _:
					pass
			new_posis.append([new_square] + (snake.pos if snake.is_growing > 0 else snake.pos[:-1]))
			# if snake.is_growing > 0:
			# 	new_posis.append([new_square] + snake.pos)
			# else:
			# 	new_posis.append([new_square] + snake.pos[:-1])
		# Check for crashes with same snake
		self.crashes.extend([(new_pos[1], new_pos[0]) for new_pos in new_posis if new_pos[0] in new_pos[1:]])
		# Check for crashes with other snakes
		self.crashes.extend([(new_pos[1], new_pos[0]) for new_pos, other_pos in itertools.product(new_posis, new_posis + remaining_posis) if new_pos != other_pos and new_pos[0] in other_pos])
		# self.crashes.extend([(new_pos[1], new_pos[0]) for new_pos, other_pos in itertools.product(new_posis, remaining_posis) if new_pos[0] in other_pos])
		# Update real snake positions if no crash happened
		if not self.crashes:
			for snake, new_pos in zip(snakes_to_upd, new_posis):
				snake.pos = new_pos


class Level:
	"""The class for the levels"""
	def __init__(self, level_info: {}):
		self.name = None
		self.map = []
		self.start_pos = []
		self.items = []
		self.trg_score = None
		self.profiles = []
		for k, v in level_info.items():
			if k == "map":
				self.map = utils.strings_to_objects(v)
				self.start_pos = self.get_start_pos(v)
			else:
				setattr(self, k, v)
		self.num_cols = len(self.map)
		self.num_rows = len(self.map[0])

	def get_start_pos(self, map_str: [str]):
		start_pos = []
		sep = ','
		for row, line in enumerate(map_str):
			for col, value in enumerate(line.split(sep)):
				if len(value) == 3 and value[0] == 's':
					player_idx = int(value[1]) - 1
					body_idx = int(value[2]) - 1
					while len(start_pos) <= player_idx:
						start_pos.append([])
					while len(start_pos[player_idx]) <= body_idx:
						start_pos[player_idx].append(tuple())
					start_pos[player_idx][body_idx] = (row, col)
		return start_pos


class Snake:
	"""The class for the players/ snakes"""

	def __init__(self, name: str, idx: int, color: (int, int, int), controls: {}):
		self.name = name
		self.idx = idx
		self.color = color
		# controls is a dict for the inputs that control the snake. Keys are the keyboard keys as pygame constants,
		# values are the orientations (as (int, int) tuples)
		self.controls = controls
		self._pos = None
		self.head = None
		self.tail = None
		self.orientation = None
		self.speed = 4
		self.is_growing = 0
		self.is_drunk = False

	@property
	def pos(self) -> [(int, int)]:
		return self._pos

	@pos.setter
	def pos(self, new_pos):
		"""Update head, tail and orientation together with pos"""
		self._pos = new_pos
		self.head = new_pos[0]
		self.tail = new_pos[-1]
		self.orientation = utils.subtract_tuples(self.head, self.pos[1])
		self.is_growing = max(self.is_growing - 1, 0)

	def update_orientation(self, key) -> None:
		"""Update the orientation based on the pressed key"""
		cur_orient = utils.subtract_tuples(self.head, self._pos[1])
		if key in self.controls and utils.add_tuples([self.controls[key], cur_orient]) != (0, 0):
			self.orientation = self.controls[key]

	def grow(self, size: int):
		"""Let the snake grow by the given size"""
		self.is_growing += size

	def adjust_speed(self, factor: float):
		"""Adjust the speed of the snake by multiplying it with the given factor"""
		self.speed = max(MIN_SNAKE_SPEED, min(int(factor * self.speed), MAX_SNAKE_SPEED))

	def transpose_controls(self) -> None:
		"""Transpose the controls for up<->down and left<->right"""
		if not self.is_drunk:
			tp = {ORIENT_UP: ORIENT_DOWN, ORIENT_LEFT: ORIENT_RIGHT, ORIENT_DOWN: ORIENT_UP, ORIENT_RIGHT: ORIENT_LEFT}
			self.controls = {k: tp[v] for k, v in self.controls.items()}
			self.is_drunk = True


class Graphics:
	"""The class for displaying all graphics on the screen"""
	def __init__(self, num_rows: int, num_cols: int):
		self.main_surface = pygame.display.set_mode((0, 0))
		self.square_size = int(min(self.main_surface.get_width() * MAP_TO_SCREEN_RATIO / num_cols, self.main_surface.get_height() * MAP_TO_SCREEN_RATIO / num_rows))
		start_pos = utils.subtract_tuples(self.main_surface.get_rect().center,
										  (self.square_size * num_cols / 2.0, self.square_size * num_rows / 2.0))
		self.square_posis = [[(start_pos[0] + j * self.square_size, start_pos[1] + i * self.square_size) for j in range(num_cols)] for i in range(num_rows)]
		# Prepare images
		self.items_orig = {obj: pygame.image.load(filename).convert_alpha() for obj, filename in FILENAME_ITEMS.items()}
		self.items = {obj: pygame.transform.scale(img_orig, (self.square_size, self.square_size))
					  for obj, img_orig in self.items_orig.items()}
		self.snake_parts_orig = {k: [pygame.image.load(filename).convert_alpha() for filename in v] for k, v in FILENAME_SNAKE_PARTS.items()}
		self.snake_parts = {k: [pygame.transform.scale(img_orig, (self.square_size, self.square_size)) for img_orig in v] for k, v in self.snake_parts_orig.items()}

	def update_display(self, level: Level, snakes: [Snake], crashes: [((int, int), (int, int))]) -> None:
		"""Draw everything onto the screen"""
		self.main_surface.fill(BG_COLOR)
		# Draw level
		wall_color = GREY
		for row, obj_row in enumerate(level.map):
			for col, obj in enumerate(obj_row):
				screen_pos = self.grid_to_screen_pos((row, col))
				if obj == utils.Objects.WALL:
					pygame.draw.rect(self.main_surface, wall_color, pygame.rect.Rect(screen_pos, (self.square_size, self.square_size)))
				elif obj != utils.Objects.NONE:
					self.main_surface.blit(self.items[obj], screen_pos)
		# Draw snakes
		for snake in snakes:
			for idx, pos in enumerate(snake.pos):
				screen_pos = self.grid_to_screen_pos(pos)
				if idx == 0 and snake.color in self.snake_parts:
					# snake head
					self.main_surface.blit(pygame.transform.rotate(self.snake_parts[snake.color][utils.SnakeParts.HEAD.value], ROTATIONS_STRAIGHT[snake.orientation]), screen_pos)
				elif idx != len(snake.pos) - 1 and snake.color in self.snake_parts:
					# snake body
					orientation_front = utils.subtract_tuples_int(snake.pos[idx - 1], pos)
					orientation_back = utils.subtract_tuples_int(pos, snake.pos[idx + 1])
					# snake_part_idx = utils.SnakeParts.BODY_STRAIGHT.value if orientation_front == orientation_back else utils.SnakeParts.BODY_CORNER.value
					# rotation = ROTATIONS_STRAIGHT[orientation_front] if orientation_front == orientation_back else \
					# ROTATIONS_CORNER[(orientation_front, orientation_back)]
					if orientation_front == orientation_back:
						snake_part_idx = utils.SnakeParts.BODY_STRAIGHT.value if orientation_front == orientation_back else utils.SnakeParts.BODY_CORNER.value
						rotation = ROTATIONS_STRAIGHT[orientation_front] if orientation_front == orientation_back else ROTATIONS_CORNER[(orientation_front, orientation_back)]
					else:
						snake_part_idx = utils.SnakeParts.BODY_CORNER.value
						rotation = ROTATIONS_CORNER[(orientation_front, orientation_back)]
					self.main_surface.blit(pygame.transform.rotate(self.snake_parts[snake.color][snake_part_idx], rotation), screen_pos)
				else:
					pygame.draw.rect(self.main_surface, snake.color, pygame.rect.Rect(screen_pos, (self.square_size, self.square_size)))
		# Draw crashes
		radius1 = self.square_size / 2.0 * 0.7
		radius2 = self.square_size / 2.0 * 0.8
		crashes_centers = tuple([utils.multiply_tuple(utils.add_tuples([self.grid_to_screen_pos(crash[0]), self.grid_to_screen_pos(crash[1]), (self.square_size, self.square_size)]), 0.5) for crash in crashes])
		for center in crashes_centers:
			pygame.draw.circle(self.main_surface, ORANGE, center, radius2)
			pygame.draw.circle(self.main_surface, RED, center, radius1)
		pygame.display.update()

	def grid_to_screen_pos(self, grid_pos: (int, int)) -> (int, int):
		"""Translates coordinates in the grid to the screen position of the topleft corner of the corresponding rect"""
		return self.square_posis[grid_pos[0]][grid_pos[1]]


# ----- Main script ----
if __name__ == "__main__":
	comm = Communicator()
	sys.exit(comm.start_game())
