"""Module for the level class in the friendly snakes package"""
import copy

# ----- Imports --------
import utils
import pygame
from constants import DROP_ITEM_RATE

pygame.init()

# ----- Constants ------


# ----- Classes --------
class Level:
	"""The class for the levels"""

	def __init__(self, level_info: {}):
		self.name = ""
		self.id = None
		self.orig_map = []
		self.map = []
		self.start_pos = []
		self.item_rates = {}
		self.drop_rate = DROP_ITEM_RATE
		self.goal = utils.Goals.NONE
		self.target = None
		self.bg = None
		self.highscore = []
		# Read infos from level_info dict
		for k, v in level_info.items():
			if k == "map":
				self.orig_map = utils.strings_to_objects(v)
				self.map = copy.deepcopy(self.orig_map)
				self.start_pos = self.get_start_pos(v, ",")
			elif k == "bg":
				self.bg = utils.Backgrounds[v]
			elif k == "goal":
				self.goal = utils.Goals[v]
			elif hasattr(self, k):
				setattr(self, k, v)
		self.num_cols = len(self.map)
		self.num_rows = len(self.map[0])
		# Init item list according to their rates
		self.items = []
		for k, v in self.item_rates.items():
			self.items.extend([utils.string_to_object(k)] * v)

	def get_start_pos(self, map_str: [str], sep: str) -> [[(int, int)]]:
		"""
		Determine the start position of the snakes in the given map.

		:param map_str: The map as a list of strings (each string represents one line of the map)
		:param sep: The separator character in the strings
		:return: A list with length equal to the number of snakes in the level (usually four), with each element containing a list of tuples denoting the start positions of the respective snake
		"""
		start_pos = []
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

	def reset(self):
		"""Reset all variables to their start state."""
		self.map = copy.deepcopy(self.orig_map)
