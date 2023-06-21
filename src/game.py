"""Module for the game class in the friendly snakes package"""

# ----- Imports --------
import copy
import itertools
import random
from snake import Snake
from level import Level
from constants import *
import pygame

pygame.init()

# ----- Constants ------


# ----- Classes --------
class Game:
	"""The main game class"""

	def __init__(self, player_names: [str], player_colors: [(int, int, int)], player_controls: [{}], level: Level):
		self.level = level
		self.snakes = [Snake(name, idx, color, controls) for idx, (name, color, controls) in enumerate(zip(player_names, player_colors, player_controls))]
		self.init_snake_pos()
		# crashes is a list of tuples of positions. For each crash that occurred, it holds the coordinates of the two squares between which the crash happened
		self.crashes: [((int, int), (int, int))] = []
		self.free_squares = set([(i, j) for i, row in enumerate(level.map) for j, obj in enumerate(row) if obj == utils.Objects.NONE]) - set([pos for snake in self.snakes for pos in snake.pos])
		self.passed_reoccs = 0
		# counters is a dict tracking the game elements that needs to be updated every second. Its keys are tuples of type (utils.Cntable, int), where the former shows the kind of element and the latter the additional index
		# corresponding to that kind of element (e.g. (utils.Cntable.BOMB, 0) would refer to bomb #0 in the bombs list. If no additional index is needed, None is used for the latter.
		# The values of the dict are ints showing the countdown for the specific element w.r.t. REOCC_DUR.
		self.counters = {(utils.Cntble.DROP_ITEM, None): self.level.drop_rate * REOCC_PER_SEC}
		# bombs is a dict of all bombs. Key is the location of the bomb, value is the countdown and the orientation of the bomb
		self.bombs: {(int, int): (int, (int, int))} = {}
		self.explosions: {(int, int): int} = {}

	def reset(self) -> None:
		"""Reset the game to its initial state"""
		names, colors, controls = [], [], []
		for snake in self.snakes:
			snake.reset()
			names.append(snake.name)
			colors.append(snake.color)
			controls.append(snake.controls)
		self.level.reset()
		self.__init__(names, colors, controls, self.level)

	def init_snake_pos(self) -> None:
		"""Initialize the positions of the snakes."""
		for snake, pos in zip(self.snakes, self.level.start_pos):
			snake.pos = pos

	def update_snake_orientation(self, key) -> bool:
		"""
		Update a snake's orientation.

		:param key: The key attribute of the KEYDOWN event that triggered the update
		:return: True if a snake was updated, False otherwise
		"""
		for snake in self.snakes:
			if snake.update_orientation(key):
				return True
		return False

	def update_snakes(self, snake_ids_to_upd: [int]) -> [utils.Objects]:
		"""
		Update the position of the snakes.

		:param snake_ids_to_upd: Indices of the snakes to update
		:return: List of objects that have been eaten
		"""
		snakes_to_upd = [self.snakes[idx] for idx in snake_ids_to_upd]
		new_posis = []
		remaining_posis = [snake.pos for snake in self.snakes if snake not in snakes_to_upd]
		new_spit_fire_posis = []
		rem_spit_fire_posis = [snake.spit_fire_posis for snake in self.snakes if snake not in snakes_to_upd]
		objects = []
		# Update snake positions locally and check for collisions with obstacles
		for snake in snakes_to_upd:
			new_square = utils.add_tuples([snake.head, snake.orientation])
			obj_at_new_pos = self.level.map[new_square[0]][new_square[1]]
			match obj_at_new_pos:
				case obj if obj in utils.Hurting:
					self.crashes.append((snake.head, new_square))
				case item if item in utils.Speeding:
					snake.adjust_speed(SPEEDING_SUMMANDS[item])
					self.level.map[new_square[0]][new_square[1]] = utils.Objects.NONE
				case item if item in utils.Growing:
					snake.grow(GROWING_SIZES[item])
					self.level.map[new_square[0]][new_square[1]] = utils.Objects.NONE
				case utils.Objects.BOMB:
					self.bombs[new_square] = (self.bombs[new_square][0], snake.orientation)
					hit_stopper = self.move_bomb(new_square)
					if hit_stopper:
						self.crashes.append((snake.head, new_square))
				case utils.Objects.BEER:
					snake.get_drunk()
					self.level.map[new_square[0]][new_square[1]] = utils.Objects.NONE
				case utils.Objects.CHILI:
					snake.get_piquant()
					self.level.map[new_square[0]][new_square[1]] = utils.Objects.NONE
				case _:
					pass
			objects.append(obj_at_new_pos)
			new_snake_pos = [new_square] + (snake.pos if snake.is_growing > 0 else snake.pos[:-1])
			new_posis.append(new_snake_pos)
			if snake.spits_fire:
				new_spit_fire_posis.append(utils.get_spit_fire_squares(new_snake_pos[0], utils.subtract_tuples(new_snake_pos[0], new_snake_pos[1]), SPIT_FIRE_RANGE, self.level.map))
			else:
				new_spit_fire_posis.append([])
		# Check for crashes with same snake
		self.crashes.extend([(new_pos[1], new_pos[0]) for new_pos in new_posis if new_pos[0] in new_pos[1:]])
		# Check for crashes with other snakes
		self.crashes.extend([(new_pos[1], new_pos[0]) for new_pos, other_pos in itertools.product(new_posis, new_posis + remaining_posis) if new_pos != other_pos and new_pos[0] in other_pos])
		# Check for crashes by snakes running into explosions
		exploding_squares = [(row - 1 + i, col - 1 + j) for (row, col) in self.explosions for i in range(3) for j in range(3)]
		self.crashes.extend([(new_pos[1], new_pos[0]) for new_pos in new_posis if new_pos[0] in exploding_squares])
		# Update real snake positions if no crash happened
		if not self.crashes:
			for snake, new_pos, new_spit_fire_pos, obj in zip(snakes_to_upd, new_posis, new_spit_fire_posis, objects):
				self.free_squares |= {snake.pos[-1]} if snake.pos[-1] != new_pos[-1] else set()
				self.free_squares -= {new_pos[0]}
				snake.pos = new_pos
				snake.spit_fire_posis = new_spit_fire_pos
				snake.score += ITEM_SCORES.get(obj, 0)
		# Check for crashes by snakes getting burned (only after the snake posis got updated, so that the new posis incl. the new fire spit gets drawn on the screen)
		fire_posis = new_spit_fire_posis + rem_spit_fire_posis
		self.crashes.extend([(pos, pos) for snake_pos, fire_pos in itertools.product(new_posis + remaining_posis, fire_posis) for pos in snake_pos if pos in fire_pos])
		return objects

	def update_counting(self) -> [utils.Objects]:
		"""Update all counting game elements and return a list of new objects (only bombs and explosions)."""
		new_obj = []
		# Update explosions
		explosions_copy = copy.deepcopy(self.explosions)
		for pos in explosions_copy.keys():
			self.explosions[pos] -= 1
			if self.explosions[pos] == 0:
				self.explosion_is_over(pos)
		# Update bombs
		bombs_copy = copy.deepcopy(self.bombs)
		for pos, (cntdwn, orientation) in bombs_copy.items():
			if pos not in self.bombs:
				# This only happens if the bomb in question was erased from self.bombs during the for-loop (e.g. by an explosion of a neighbor bomb). In that case we can ignore this bomb.
				continue
			new_cntdwn = cntdwn - 1
			self.bombs[pos] = (new_cntdwn, orientation)
			if new_cntdwn == 0:
				self.handle_explosion(pos)
				new_obj.append(utils.Objects.EXPLOSION)
			elif orientation != NO_ORIENTATION:
				# Move the bomb one square
				self.move_bomb(pos)
		# Update Cntable
		for k, v in self.counters.items():
			elem, idx = k
			if v == 1:
				# Countdown reaches zero, handle it depending on the element
				match elem:
					case utils.Cntble.DROP_ITEM:
						# Drop a new item on the map
						i, j = random.choice(list(self.free_squares))
						new_object = random.choice(self.level.items)
						self.level.map[i][j] = new_object
						self.free_squares -= {(i, j)}
						self.counters[k] = self.level.drop_rate * REOCC_PER_SEC
						if new_object == utils.Objects.BOMB:
							self.bombs[(i, j)] = (BOMB_CNTDWN * REOCC_PER_SEC, NO_ORIENTATION)
							new_obj.append(utils.Objects.BOMB)
					case _:
						pass
			else:
				self.counters[k] -= 1
		# Update each snake counting elements
		for snake in self.snakes:
			stat = snake.update_counting()
			if stat == 1:
				self.update_spit_fire_posis(snake)
				new_obj.append(utils.Objects.FIRE_SPIT)
			elif stat == 2:
				self.update_spit_fire_posis(snake)
		return new_obj

	def handle_explosion(self, bomb_pos: (int, int)) -> None:
		"""
		Update the situation when a bomb explodes, esp. the "self.bombs" and "self.explosions" dictionaries.

		:param bomb_pos: The position of the bomb.
		:return: A list of bombs that were on the exploding squares (incl the original one)
		"""
		row, col = bomb_pos
		exploded_squares = [(row - 1 + i, col - 1 + j) for i in range(3) for j in range(3)]
		for i, j in exploded_squares:
			if self.level.map[i][j] not in utils.Indestructible:
				self.level.map[i][j] = utils.Objects.EXPLOSION
			# If a bomb is hit, we additionally have to clear it from the bombs dictionary
			if (i, j) in self.bombs:
				del self.bombs[(i, j)]
		# Check for exploded snakes and update explosion dict
		self.crashes.extend([(pos, pos) for snake in self.snakes for pos in snake.pos if pos in exploded_squares])
		self.explosions[bomb_pos] = EXPLOSION_CNTDWN * REOCC_PER_SEC

	def explosion_is_over(self, pos: (int, int)) -> None:
		"""
		Update the situation when an explosion cools down, esp. the "self.expplosions" dictionary.

		:param pos: The position of the explosion.
		"""
		row, col = pos
		rel_squares = [(row - 1 + i, col - 1 + j) for i in range(3) for j in range(3)]
		for i, j in rel_squares:
			if self.level.map[i][j] not in utils.Indestructible:
				self.level.map[i][j] = utils.Objects.NONE
		del self.explosions[pos]

	def move_bomb(self, old_pos: (int, int)) -> bool:
		"""
		Move the bomb one square and update the self.bombs dictionary.

		:param old_pos: The (old) position of the bomb
		:return: A bool showing if the bomb hit a stopper like a wall, a snake part etc.
		"""
		cntdwn, orientation = self.bombs[old_pos]
		if orientation == NO_ORIENTATION:
			# Bomb isn't moving
			return False
		new_pos = utils.add_two_tuples(old_pos, orientation)
		snake_posis = [pos for snake in self.snakes for pos in snake.pos]
		if self.level.map[new_pos[0]][new_pos[1]] in utils.MoveStopper or new_pos in snake_posis:
			# Bomb hit a stopper -> stop it's movement
			self.bombs[old_pos] = (cntdwn, NO_ORIENTATION)
			return True
		elif self.level.map[new_pos[0]][new_pos[1]] == utils.Objects.EXPLOSION:
			# Bomb moves into an ongoing explosion
			self.level.map[old_pos[0]][old_pos[1]] = utils.Objects.NONE
			del self.bombs[old_pos]
			return False
		self.level.map[new_pos[0]][new_pos[1]] = utils.Objects.BOMB
		self.level.map[old_pos[0]][old_pos[1]] = utils.Objects.NONE
		self.bombs[new_pos] = (cntdwn, orientation)
		del self.bombs[old_pos]
		return False

	def is_snake_on_squares(self, squares: [(int, int)]) -> [(int, int)]:
		"""Returns all the squares of the given square list where a snake is on"""
		return [pos for pos in squares for snake in self.snakes if pos in snake.pos]

	def create_bomb_dict(self) -> {(int, int): int}:
		"""
		Return the bomb dictionary that is needed for updating the display.

		:return: A dict containing one item per bomb, with the bomb's position as key and its countdown as value
		"""
		return {pos: cntdwn for pos, (cntdwn, _) in self.bombs.items()}

	def update_spit_fire_posis(self, snake: Snake):
		"""Updates the spit fire posis for the given snake."""
		if snake.spits_fire > 0:
			snake.spit_fire_posis = utils.get_spit_fire_squares(snake.pos[0], snake.orientation, SPIT_FIRE_RANGE, self.level.map)
		else:
			snake.spit_fire_posis = []

	def get_infos_for_updating_display(self) -> (Level, [Snake], [((int, int), (int, int))], {(int, int): int}, {(int, int): int}):
		"""
		Return the infos that are needed to display the current state.

		:return: Tuple containing [0] the level, [1] the snakes, [2] the crashes, [3] the bombs and [4] the explosions
		"""
		return self.level, self.snakes, self.crashes, self.create_bomb_dict(), self.explosions
