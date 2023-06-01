"""Module for the menu parent classes in the friendly snakes package"""

import utils
from constants import WHITE, FPS
import abc
from enum import Enum
import pygame
import pygame_menu

pygame.init()


class WidgetState(Enum):
	NORMAL = 0
	PUSHED = 1
	HOVERED = 2


class Language(Enum):
	GERMAN = 0
	ENGLISH = 1


# ----- Constants ------
FILENAMES_MUSIC_TRACKS = ["../res/title_theme.ogg"]
FILENAME_BG = "../res/menu_bg.png"
FILENAME_MENU_FRAME = "../res/menu_frame.png"
FILENAMES_BUTTON = {WidgetState.NORMAL: "../res/menu_button_normal.png", WidgetState.PUSHED: "../res/menu_button_pushed.png", WidgetState.HOVERED: "../res/menu_button_hovered.png"}
COLOR_WIDGETS = {WidgetState.NORMAL: (76, 123, 209), WidgetState.HOVERED: (111, 164, 255)}
BG_ITEMS = [("Desert", 0)]
MUSIC_TRACK_ITEMS = [("Bells Song", 0)]
# benchmark screen: 2560x1440
BENCHMARK_HEIGHT = 1440
BUTTON_HEIGHT = 50
BUTTON_FONT_SIZE = 25


# ----- Methods --------
def wdg_set_background(widget: pygame_menu.widgets.Widget, bg_color, trg_size: (int, int)) -> None:
	"""Set the background for the given widget to the given bg_color and inflate it to the given trg_size"""
	widget.set_background_color(bg_color)
	delta = utils.subtract_tuples_int(trg_size, widget.get_size())
	delta = (max(delta[0], 0), max(delta[1], 0))
	widget.set_background_color(bg_color, delta)


# ----- Classes --------
class BasicSprite(pygame.sprite.Sprite):
	"""Sprite subclass for static elements"""
	def __init__(self, image: pygame.Surface, rect: pygame.Rect):
		super().__init__()
		self.image = image
		self.rect = rect

	def update(self, rect=None, img=None) -> None:
		if rect:
			self.rect = rect
		if img:
			self.image = img


class BasicGroup(pygame.sprite.Group):
	"""Group for basic sprites"""
	def __init__(self, *sprites):
		super().__init__(*sprites)

	def collide_point(self, point: (int, int), surf: pygame.Surface = None) -> [BasicSprite]:
		offset = surf.get_abs_offset() if surf else (0, 0)
		adj_point = utils.subtract_tuples(point, offset)
		hit_sprites = []
		for sprite in self.sprites():
			if sprite.rect.collidepoint(adj_point):
				hit_sprites.append(sprite)
		return hit_sprites

	def collide_update_img(self, point: (int, int), img: pygame.Surface, surf: pygame.Surface = None) -> [BasicSprite]:
		"""Update the image of the sprites that collide with the given point"""
		offset = surf.get_abs_offset() if surf else (0, 0)
		adj_point = utils.subtract_tuples(point, offset)
		collided_sprites = []
		for sprite in self.sprites():
			if sprite.rect.collidepoint(adj_point):
				sprite.image = img
				collided_sprites.append(sprite)
		return collided_sprites


class Clickable(BasicSprite):
	"""Sprite subclass for the buttons in the start menu"""
	def __init__(self, image: pygame.Surface, rect: pygame.Rect, on_click_function):
		super().__init__(image, rect)
		self.on_click_function = on_click_function

	def on_click(self) -> None:
		self.on_click_function()


class ClickableGroup(BasicGroup):
	"""Sprites group for the buttons in the start menu"""
	def __init__(self, *sprites):
		super().__init__(*sprites)

	def collide_click(self, point: (int, int), surf: pygame.Surface = None) -> None:
		"""Call the on click method of the sprites that collide with the given point"""
		offset = surf.get_abs_offset() if surf else (0, 0)
		adj_point = utils.subtract_tuples(point, offset)
		for sprite in self.sprites():
			if sprite.rect.collidepoint(adj_point):
				try:
					sprite.on_click()
				except AttributeError:
					continue


class Menu(abc.ABC):
	"""Parent class for all menus in the game"""

	def __init__(self, parent_surface: pygame.Surface, menu_area_start: (int, int), menu_area_size: (int, int), buttons_area_start: (int, int), buttons_area_size: (int, int), button_texts: [str]):
		self.parent_surface = parent_surface
		self.scaling_factor = self.parent_surface.get_abs_parent().get_height() / BENCHMARK_HEIGHT
		# menu variables
		self.menu_rect = pygame.Rect(menu_area_start, menu_area_size)
		self.menu_surf = self.parent_surface.subsurface(self.menu_rect)
		self.menu_frame_img = pygame.transform.scale(pygame.image.load(FILENAME_MENU_FRAME).convert_alpha(), self.menu_rect.size)
		# self.set_menu_variables(*self.set_menu_area_start_and_size())
		# button variables
		self.button_font = pygame.font.SysFont("Snake Chan", int(BUTTON_FONT_SIZE * self.scaling_factor))
		self.buttons_area_start = buttons_area_start
		self.buttons_area_size = buttons_area_size
		self.buttons_area_rect = pygame.Rect(self.buttons_area_start, self.buttons_area_size)
		self.buttons_surf = self.menu_surf.subsurface(self.buttons_area_rect)
		self.button_size = (self.buttons_area_rect.w, BUTTON_HEIGHT * self.scaling_factor)
		self.button_texts = button_texts
		# self.set_button_variables(*self.get_button_area_start_and_size())
		self.clock = pygame.time.Clock()

	# @abc.abstractmethod
	# def set_menu_area_start_and_size(self) -> ((int, int), (int, int)):
	# 	"""
	# 	Return the menu area start position and size
	#
	# 	:return: Tuple containing [0] the menu area topleft position and [1] the menu area size
	# 	"""
	#
	# def set_menu_variables(self, menu_area_start: (int, int), menu_area_size: (int, int)):
	# 	# Menu area
	# 	self.menu_rect = pygame.Rect(utils.mult_tuple_to_int(menu_area_start, self.scaling_factor), utils.mult_tuple_to_int(menu_area_size, self.scaling_factor))
	# 	self.menu_surf = self.parent_surface.subsurface(self.menu_rect)
	# 	self.menu_frame_img = pygame.transform.scale(pygame.image.load(FILENAME_MENU_FRAME).convert_alpha(), self.menu_rect.size)
	#
	# @abc.abstractmethod
	# def get_button_area_start_and_size(self) -> ((int, int), (int, int)):
	# 	"""
	# 	Return the button area start position and size
	#
	# 	:return: Tuple containing [0] the button area topleft position and [1] the button area size
	# 	"""
	#
	# def set_button_variables(self, button_area_start: (int, int), button_area_size: (int, int)):
	# 	"""Set the class variables regarding the buttons"""
	# 	# Button area inside the menu area
	# 	self.buttons_area_start = button_area_start
	# 	self.buttons_area_size = button_area_size
	# 	self.buttons_area_rect = pygame.Rect(self.buttons_area_start, self.buttons_area_size)
	# 	self.buttons_surf = self.parent_surface.subsurface(self.buttons_area_rect)
	# 	self.button_size = self.set_button_size()
	#
	# def set_button_size(self) -> (int, int):
	# 	"""Return the size of a button"""
	# 	width = self.buttons_area_rect.w if self.buttons_area_rect else self.parent_surface.get_width()
	# 	return width, BUTTON_HEIGHT * self.scaling_factor

	@abc.abstractmethod
	def menu_loop(self) -> None:
		"""Main loop in the respective menu."""
		# """
		# Main loop in the respective menu.
		#
		# :return: True if play should start/ resume, False for exit
		# """
		# is_running = True
		# while is_running:
		# 	is_running = self.handle_events()


class MainMenu(Menu):
	"""Parent class for all main menus in the game, esp. the start and the in-game menu"""

	def __init__(self, main_surface: pygame.Surface, menu_area_start: (int, int), menu_area_size: (int, int), buttons_area_start: (int, int), buttons_area_size: (int, int), button_texts: [str]):
		"""Initialize the menu"""
		super().__init__(main_surface, menu_area_start, menu_area_size, buttons_area_start, buttons_area_size, button_texts)
		self.play_game = False
		self.exit = False
		self.lang = Language.ENGLISH
		# self.snake_names = ["Kokosnuss", "Tiger", "Muh", "Mausi"]
		# self.snake_colors = [GREEN, BLUE, CYAN, PINK]
		# self.snake_controls = [["↑", "←", "↓", "→"], ["W", "A", "S", "D"], ["8", "4", "5", "6"], ["I", "J", "K", "L"]]
		self.scaling_factor = main_surface.get_height() / BENCHMARK_HEIGHT
		# self.music_volume = 0.1
		# self.sound_volume = 1
		# self.cur_track_idx = 0
		# self.cur_bg_idx = 0
		# menu variables
		# self.menu_rect = None
		# self.menu_surf = None
		# self.menu_frame_img = None
		# self.set_menu_variables(*self.set_menu_area_start_and_size())
		# menu_area_start_wrt_benchmark, menu_area_size_wrt_benchmark = self.set_menu_area_and_size_wrt_benchmark()
		# button variables
		self.button_imgs_orig = {state: pygame.image.load(FILENAMES_BUTTON[state]).convert_alpha() for state in WidgetState}
		self.button_imgs = {state: pygame.transform.scale(img_orig, self.button_size) for state, img_orig in self.button_imgs_orig.items()}
		# self.button_base_imgs = {state: pygame_menu.BaseImage(image_path=FILENAMES_BUTTON[state], drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL) for state in WidgetState}
		# self.button_font = pygame.font.SysFont("Snake Chan", int(BUTTON_FONT_SIZE * self.scaling_factor))
		# self.buttons_area_start = None
		# self.buttons_area_size = None
		# self.buttons_area_rect = None
		# self.buttons_surf = None
		# self.set_button_variables(*self.set_button_area_and_size_wrt_benchmark())
		# button_area_start_wrt_benchmark, button_area_size_wrt_benchmark = self.set_button_area_and_size_wrt_benchmark()
		# self.button_texts = self.get_button_texts()
		self.button_texts_rend = [self.button_font.render(text, True, WHITE) for text in self.button_texts]
		num_buttons = len(self.button_texts)
		self.free_space = int((self.buttons_area_rect.h - num_buttons * self.button_size[1]) / (num_buttons - 1))
		self.button_rects = [pygame.Rect((0, i * (self.button_size[1] + self.free_space)), self.button_size) for i in range(num_buttons)]
		self.buttons: [Clickable] = []
		self.button_group = ClickableGroup()

	# @abc.abstractmethod
	# def get_button_area_start_and_size(self) -> ((int, int), (int, int)):
	# 	"""
	# 	Return the button area start position and size
	#
	# 	:return: Tuple containing [0] the button area topleft position and [1] the button area size
	# 	"""
	#
	# @abc.abstractmethod
	# def set_button_size(self) -> (int, int):
	# 	"""Return the size of a button"""
	#
	# @abc.abstractmethod
	# def get_button_texts(self) -> [str]:
	# 	"""Return the texts for the buttons"""

	# def set_button_variables(self, button_area_start: (int, int), button_area_size: (int, int)):
	# 	# Button area inside the menu area
	# 	self.buttons_area_start = utils.mult_tuple_to_int(button_area_start, self.scaling_factor)
	# 	self.buttons_area_size = utils.mult_tuple_to_int(button_area_size, self.scaling_factor)
	# 	self.buttons_area_rect = pygame.Rect(self.buttons_area_start, self.buttons_area_size)
	# 	self.buttons_surf = self.menu_surf.subsurface(self.buttons_area_rect)

	def menu_loop(self) -> bool:
		"""
		Handle the events in the menu.

		:return: True if play should start/ resume, False for exit
		"""
		pushed_button = None
		while not self.play_game and not self.exit:
			events = pygame.event.get()
			for event in events:
				if event.type == pygame.MOUSEMOTION and not pushed_button:
					# Check for hovering over buttons
					prev_pos = utils.subtract_tuples(event.pos, event.rel)
					self.button_group.collide_update_img(prev_pos, self.button_imgs[WidgetState.NORMAL], self.buttons_surf)
					self.button_group.collide_update_img(event.pos, self.button_imgs[WidgetState.HOVERED], self.buttons_surf)
				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					# Check for click on button
					buttons = self.button_group.collide_update_img(event.pos, self.button_imgs[WidgetState.PUSHED], self.buttons_surf)
					if buttons:
						pushed_button = buttons[0]
				if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
					# Execute on click function if cursor is on the pushed button
					buttons = self.button_group.collide_point(event.pos, self.buttons_surf)
					if buttons and buttons[0] == pushed_button:
						pushed_button.on_click()
					self.button_group.update(img=self.button_imgs[WidgetState.NORMAL])
					pushed_button = None
			self.update_display()
			self.clock.tick(FPS)
		return self.play_game

	@abc.abstractmethod
	def update_display(self) -> None:
		"""Display the current state on the screen"""


class Submenu(Menu):
	"""Parent class for the submenus"""

	def __init__(self, main_surface: pygame.Surface, buttons_area_topleft: (int, int), buttons_area_size: (int, int)):
		"""Initialize the submenu"""
		self.buttons_area_start = buttons_area_topleft
		self.buttons_area_size = buttons_area_size
		self.button_base_imgs: {WidgetState: pygame_menu.BaseImage} = None
		self.click_on_back = False
		super().__init__(main_surface)

	def get_button_area_start_and_size(self) -> ((int, int), (int, int)):
		"""
		Return the button area start position and size

		:return: Tuple containing [0] the button area topleft position and [1] the button area size
		"""
		return self.buttons_area_start, self.buttons_area_size

	@abc.abstractmethod
	def menu_loop(self) -> None:
		"""Main loop in the respective menu."""

	def mouse_over_widget(self, widget: pygame_menu.widgets.Widget, event: pygame.event.Event) -> None:
		"""
		Handle a mouseover on the given widget

		:param widget: The widget that the mouse hovered over
		:param event: The pygame event describing the mouse motion
		"""
		bg_color = self.button_base_imgs[WidgetState.HOVERED] if isinstance(widget, pygame_menu.widgets.Button) else COLOR_WIDGETS[WidgetState.HOVERED]
		wdg_set_background(widget, bg_color, self.button_size)
		widget.select(True, True)

	def mouse_leave_widget(self, widget: pygame_menu.widgets.Widget, event: pygame.event.Event) -> None:
		"""Handle a mouse leave on the given widget

		:param widget: The widget that the mouse left
		:param event: The pygame event describing the mouse motion
		"""
		bg_color = self.button_base_imgs[WidgetState.NORMAL] if isinstance(widget, pygame_menu.widgets.Button) else COLOR_WIDGETS[WidgetState.NORMAL]
		wdg_set_background(widget, bg_color, self.button_size)

	def click_on_back_button(self, *args, **kwargs) -> None:
		"""Leave the submenu. Standard callback method for the click on a back button in a submenu."""
		self.click_on_back = True
