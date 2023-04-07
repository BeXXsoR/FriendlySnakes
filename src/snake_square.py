"""A multiplayer cooperative snake game"""

# ----- Imports --------
import utils
import sys
import itertools
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
FPS = 30
MAP_TO_SCREEN_RATIO = 0.9
BASE_MAP = [
	"w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w",
	"w, , , , , , , , , , , , , , , , , , , , , , , ,w",
	"w, , , , , , , , , , , , , , , , , , , , , , , ,w",
	"w, , , , , , , , , , , , , , , , , , , , , , , ,w",
	"w, , , , , , , , , ,t1,b1,b1,h1, , , , , , , , , , ,w",
	"w, , , , , , , , , , , , , , , , , , , , , , , ,w",
	"w, , , , , , , , , , , , , , , , , , , , , , , ,w",
	"w, , , , , , , , , , , , , , , , , , , , , , , ,w",
	"w, , , , , , , , , , , , , , , , , , , , , , , ,w",
	"w, , , , , , , , , , , , , , , , , , , , , , , ,w",
	"w, , , ,h3, , , , , , , , , , , , , , , ,t4, , , ,w",
	"w, , , ,b3, , , , , , , , , , , , , , , ,b4, , , ,w",
	"w, , , ,b3, , , , , , , , , , , , , , , ,b4, , , ,w",
	"w, , , ,t3, , , , , , , , , , , , , , , ,h4, , , ,w",
	"w, , , , , , , , , , , , , , , , , , , , , , , ,w",
	"w, , , , , , , , , , , , , , , , , , , , , , , ,w",
	"w, , , , , , , , , , , , , , , , , , , , , , , ,w",
	"w, , , , , , , , , , , , , , , , , , , , , , , ,w",
	"w, , , , , , , , , , , , , , , , , , , , , , , ,w",
	"w, , , , , , , , , , , , , , , , , , , , , , , ,w",
	"w, , , , , , , , , ,h2,b2,b2,t2, , , , , , , , , , ,w",
	"w, , , , , , , , , , , , , , , , , , , , , , , ,w",
	"w, , , , , , , , , , , , , , , , , , , , , , , ,w",
	"w, , , , , , , , , , , , , , , , , , , , , , , ,w",
	"w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w"]


# ----- Classes --------
class Game:
	"""The main game class"""

	def __init__(self, player_names: [str], player_colors: [(int, int, int)]):
		self.clock = pygame.time.Clock()
		self.level = Level()
		self.snakes = [Snake(name, color) for name, color in zip(player_names, player_colors)]
		self.init_snake_pos()
		self.graphics = Graphics(self.level.num_rows, self.level.num_cols)
		# crashes is a list of tuples of positions. For each crash that occurred, it holds the coordinates of the
		# two squares between which the crash happened
		self.crashes = []

	def init_snake_pos(self) -> None:
		"""Initialize the positions of the snakes"""
		poss = [[(5, 14), (5, 13), (5, 12), (5, 11)],
				[(21, 11), (21, 12), (21, 13), (21, 14)],
				[(11, 5), (12, 5), (13, 5), (14, 5)],
				[(11, 21), (12, 21), (13, 21), (14, 21)]]
		for snake, pos in zip(self.snakes, poss):
			snake.pos = pos

	def game_loop(self) -> None:
		is_running = True
		while is_running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
					# Quit
					is_running = False
			self.update_snakes()
			self.clock.tick(FPS)
			self.graphics.update_display(self.level, self.snakes, self.crashes)
			pygame.time.delay(250)

	def update_snakes(self) -> None:
		"""Update the position of the snakes"""
		new_posis = []
		# update snake positions locally and check for crashes with obstacles
		for snake in self.snakes:
			new_square = utils.add_tuples([snake.head, snake.orientation])
			new_posis.append([new_square] + snake.pos[:-1])
			match self.level.map[new_square[0]][new_square[1]]:
				case utils.Objects.WALL:
					self.crashes.append((snake.head, new_square))
				case _:
					pass
		# Check for crashes between snakes
		self.crashes.extend([(new_pos[1], new_pos[0]) for new_pos, other_pos in itertools.product(new_posis, new_posis) if new_pos != other_pos and new_pos[0] in other_pos])
		# Update real snake positions if no crash happened
		if not self.crashes:
			for snake, new_pos in zip(self.snakes, new_posis):
				snake.pos = new_pos


class Level:
	"""The class for the levels"""

	def __init__(self):
		self.map = utils.strings_to_objects(BASE_MAP)
		self.num_cols = len(self.map)
		self.num_rows = len(self.map[0])


class Snake:
	"""The class for the players/ snakes"""

	def __init__(self, name, color):
		self.name = name
		self.color = color
		self._pos = None
		self.head = None
		self.tail = None
		self.orientation = None

	@property
	def pos(self) -> [(int, int)]:
		return self._pos

	@pos.setter
	def pos(self, new_pos):
		"""Update head, tail and orientation together with pos"""
		self._pos = new_pos
		self.head = new_pos[0]
		self.tail = new_pos[-1]
		# Update orientation (0=up, 1=left, 2=down, 3=right)
		self.orientation = utils.subtract_tuples(self.head, self.pos[1])


class Graphics:
	"""The class for displaying all graphics on the screen"""
	def __init__(self, num_rows, num_cols):
		self.main_surface = pygame.display.set_mode((0, 0))
		self.square_size = int(min(self.main_surface.get_width() * MAP_TO_SCREEN_RATIO / num_cols, self.main_surface.get_height() * MAP_TO_SCREEN_RATIO / num_rows))
		start_pos = utils.subtract_tuples(self.main_surface.get_rect().center,
										  (self.square_size * num_cols / 2.0, self.square_size * num_rows / 2.0))
		self.square_posis = [[(start_pos[0] + j * self.square_size, start_pos[1] + i * self.square_size) for j in range(num_cols)] for i in range(num_rows)]

	def update_display(self, level: Level, snakes: [Snake], crashes: [((int, int), (int, int))]) -> None:
		"""Draw everything onto the screen"""
		self.main_surface.fill(BG_COLOR)
		# Draw level
		wall_color = GREY
		for obj_row, square_pos_row in zip(level.map, self.square_posis):
			for obj, square_pos in zip(obj_row, square_pos_row):
				match obj:
					case utils.Objects.WALL:
						pygame.draw.rect(self.main_surface, wall_color, pygame.rect.Rect(square_pos, (self.square_size, self.square_size)))
						# self.main_surface.fill(wall_color, pygame.rect.Rect(square_pos, (self.square_size, self.square_size)))
		# Draw snakes
		for snake in snakes:
			for pos in snake.pos:
				pygame.draw.rect(self.main_surface, snake.color, pygame.rect.Rect(self.square_posis[pos[0]][pos[1]], (self.square_size, self.square_size)))
				# self.main_surface.fill(snake.color, pygame.rect.Rect(self.square_posis[pos[0]][pos[1]], (self.square_size, self.square_size)))
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
	game = Game(["Player1", "Player2", "Player3", "Player4"], [GREEN, BLUE, CYAN, PINK])
	game.game_loop()
	sys.exit()
