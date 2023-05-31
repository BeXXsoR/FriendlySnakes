"""Module for the ingame menu class in the friendly snakes package"""

# ----- Imports --------
from menus import *
import pygame
import pygame_menu

# ----- Constants --------
MENU_FRAME_START = (945, 367)
MENU_FRAME_SIZE = (670, 705)

# ----- Classes --------
class IngameMainMenu(MainMenu):
	"""Class for the in-game menu"""

	def __init__(self, main_surface: pygame.Surface):
		"""Initialize the in-game menu"""
		super().__init__(main_surface)
		usable_rect = pygame.rect.Rect(utils.mult_tuple_to_int(MENU_FRAME_START, self.scaling_factor), utils.mult_tuple_to_int(MENU_FRAME_SIZE, self.scaling_factor))


