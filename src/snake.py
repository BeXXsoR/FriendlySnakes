"""Module for the snake class in the friendly snakes package"""

# ----- Imports --------
import utils
from constants import *
import pygame

pygame.init()

# ----- Constants ------


# ----- Classes --------
class Snake:
	"""The class for the players/ snakes"""

	def __init__(self, name: str, idx: int, color: (int, int, int), controls: {}):
		self.name = name
		self.idx = idx
		self.color = color
		self.score = 0
		# controls is a dict for the inputs that control the snake. Keys are the keyboard keys as pygame constants,
		# values are the orientations (as (int, int) tuples)
		self.controls = controls
		self._pos = None
		self.head = None
		self.orientation = None
		self.speed = 4
		self.is_growing = 0
		self.is_drunk = 0
		self.piquancy_growing = 0
		self.spits_fire = 0
		self.spit_fire_posis = []

	@property
	def pos(self) -> [(int, int)]:
		return self._pos

	@pos.setter
	def pos(self, new_pos: [(int, int)]) -> None:
		"""Update head, tail and orientation together with pos"""
		self._pos = new_pos
		self.head = new_pos[0]
		self.orientation = utils.subtract_tuples(self.head, self.pos[1])
		self.is_growing = max(self.is_growing - 1, 0)

	def update_orientation(self, key) -> bool:
		"""Update the orientation based on the pressed key. Return True if the pressed key belonged to a snake"""
		if key in self.controls:
			cur_orient = utils.subtract_tuples(self.head, self._pos[1])
			if utils.add_tuples([self.controls[key], cur_orient]) != (0, 0):
				self.orientation = self.controls[key]
			return True
		return False

	def grow(self, size: int):
		"""Let the snake grow by the given size"""
		self.is_growing += size

	def adjust_speed(self, factor: float):
		"""Adjust the speed of the snake by multiplying it with the given factor"""
		self.speed = max(MIN_SNAKE_SPEED, min(int(factor * self.speed), MAX_SNAKE_SPEED))

	def update_counting(self) -> int:
		"""Handle reoccurring updates. Returns 1 if a fire spit started, 2 if it ended, and 0 otherwise"""
		update_spit_fire_posis = 0
		# Check drunk countdown
		if self.is_drunk > 1:
			self.is_drunk -= 1
		elif self.is_drunk == 1:
			self.get_sober()
		# Check piquancy and spit fire countdown
		if self.piquancy_growing > 1:
			self.piquancy_growing -= 1
		elif self.piquancy_growing == 1:
			self.spit_fire()
			update_spit_fire_posis = 1
		if self.spits_fire > 1:
			self.spits_fire -= 1
		elif self.spits_fire == 1:
			self.release_fire()
			update_spit_fire_posis = 2
		return update_spit_fire_posis

	def get_drunk(self) -> None:
		"""Handle the snake getting drunk"""
		if not self.is_drunk:
			self.transpose_controls()
		self.is_drunk = max(self.is_drunk, DRUNK_DURATION * REOCC_PER_SEC)

	def get_sober(self) -> None:
		"""Handle the snake getting sober"""
		if self.is_drunk:
			self.transpose_controls()
			self.is_drunk = 0

	def transpose_controls(self) -> None:
		"""Transpose the controls for up<->down and left<->right"""
		tp = {ORIENT_UP: ORIENT_DOWN, ORIENT_LEFT: ORIENT_RIGHT, ORIENT_DOWN: ORIENT_UP, ORIENT_RIGHT: ORIENT_LEFT}
		self.controls = {k: tp[v] for k, v in self.controls.items()}

	def get_piquant(self) -> None:
		"""Handle the snake eating a chili"""
		self.piquancy_growing = max(self.piquancy_growing, PIQUANCY_GROWING_DURATION * REOCC_PER_SEC)

	def spit_fire(self) -> None:
		"""Handle the piquancy countdown running out"""
		self.piquancy_growing = 0
		self.spits_fire = max(self.spits_fire, SPIT_FIRE_DURATION * REOCC_PER_SEC)

	def release_fire(self):
		"""Stop the snake spitting fire"""
		self.spits_fire = 0
		self.spit_fire_posis = []
