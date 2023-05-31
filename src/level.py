"""Module for the level class in the friendly snakes package"""

# ----- Imports --------
import utils
import pygame

pygame.init()

# ----- Constants ------


# ----- Classes --------
class Level:
	"""The class for the levels"""

	def __init__(self, level_info: {}):
		self.name = None
		self.map = []
		self.start_pos = []
		self.item_rates = {}
		self.trg_score = None
		self.profiles = {}
		for k, v in level_info.items():
			if k == "map":
				self.map = utils.strings_to_objects(v)
				self.start_pos = self.get_start_pos(v, ",")
			else:
				setattr(self, k, v)
		self.num_cols = len(self.map)
		self.num_rows = len(self.map[0])
		# init item list according to their rates
		self.items = []
		for k, v in self.item_rates.items():
			self.items.extend([utils.string_to_object(k)] * v)

	def get_start_pos(self, map_str: [str], sep: str) -> [[(int, int)]]:
		"""
		Determine the start position of the snakes in the given map.

		:param map_str: The map as a list of strings (each string represents one line of the map)
		:param sep: The separator character in the strings
		:return: A list with length equal to the number of snakes in the level (usually four), with each element
		containing a list of tuples denoting the start positions of the respective snake
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