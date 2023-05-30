"""Classes for all the menus in the game"""

import utils
import abc
from enum import Enum
from constants import WHITE
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
FILENAME_BG = "../res/menu_bg.png"
FILENAMES_MUSIC_TRACKS = ["../res/title_theme.ogg"]
FILENAME_MENU_FRAME = "../res/menu_frame.png"
FILENAMES_BUTTON = {WidgetState.NORMAL: "../res/menu_button_normal.png", WidgetState.PUSHED: "../res/menu_button_pushed.png", WidgetState.HOVERED: "../res/menu_button_hovered.png"}
COLOR_WIDGETS = {WidgetState.NORMAL: (76, 123, 209), WidgetState.HOVERED: (111, 164, 255)}
BG_ITEMS = [("Desert", 0)]
MUSIC_TRACK_ITEMS = [("Bells Song", 0)]
# benchmark screen: 2560x1440
BENCHMARK_HEIGHT = 1440
BUTTON_HEIGHT = 50
BUTTON_FONT_SIZE = 25


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

	def collide_point(self, point: (int, int)) -> [BasicSprite]:
		hit_sprites = []
		for sprite in self.sprites():
			if sprite.rect.collidepoint(point):
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

	def collide_click(self, point: (int, int), surf: pygame.Surface=None) -> None:
		"""Call the on click method of the sprites that collide with the given point"""
		offset = surf.get_abs_offset() if surf else (0, 0)
		adj_point = utils.subtract_tuples(point, offset)
		for sprite in self.sprites():
			if sprite.rect.collidepoint(adj_point):
				try:
					sprite.on_click()
				except AttributeError:
					continue


def wdg_set_background(widget: pygame_menu.widgets.Widget, bg_color, trg_size: (int, int)) -> None:
	"""Set the background for the given widget to the given bg_color and inflate it to the given trg_size"""
	widget.set_background_color(bg_color)
	delta = utils.subtract_tuples_int(trg_size, widget.get_size())
	delta = (max(delta[0], 0), max(delta[1], 0))
	widget.set_background_color(bg_color, delta)


class Menu(abc.ABC):
	"""Parent class for all menus in the game, esp. the start and the in-game menu"""

	def __init__(self, main_surface: pygame.Surface):
		"""Initialize the menu"""
		self.main_surface = main_surface
		self.play_game = False
		self.exit = False
		self.lang = Language.ENGLISH
		self.button_texts = []
		# self.snake_names = ["Kokosnuss", "Tiger", "Muh", "Mausi"]
		# self.snake_colors = [GREEN, BLUE, CYAN, PINK]
		# self.snake_controls = [["↑", "←", "↓", "→"], ["W", "A", "S", "D"], ["8", "4", "5", "6"], ["I", "J", "K", "L"]]
		self.scaling_factor = main_surface.get_height() / BENCHMARK_HEIGHT
		self.music_volume = 0.1
		self.sound_volume = 1
		self.cur_track_idx = 0
		self.cur_bg_idx = 0
		# button variables
		self.button_size = self.set_button_size()
		self.button_imgs_orig = {state: pygame.image.load(FILENAMES_BUTTON[state]).convert_alpha() for state in WidgetState}
		self.button_imgs = {state: pygame.transform.scale(img_orig, self.button_size) for state, img_orig in self.button_imgs_orig.items()}
		self.button_base_imgs = {state: pygame_menu.BaseImage(image_path=FILENAMES_BUTTON[state], drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL) for state in WidgetState}
		self.button_font = pygame.font.SysFont("Snake Chan", int(BUTTON_FONT_SIZE * self.scaling_factor))
		self.button_texts_rend = [self.button_font.render(text, True, WHITE) for text in self.button_texts]

	@abc.abstractmethod
	def set_button_size(self) -> (int, int):
		"""Return the size of a button"""

	@abc.abstractmethod
	def handle_events(self) -> bool:
		"""
		Handle the events in the menu.

		:return: True if play should start/ resume, False for exit
		"""

	def change_music_volume(self, new_volume: float) -> None:
		"""
		Change the music volume.

		:param new_volume: New volume level. must be between 0.0 and 1.0.
		"""
		pygame.mixer_music.set_volume(new_volume)
		self.music_volume = new_volume

	def change_sound_volume(self, new_volume: float) -> None:
		"""
		Change the sound volume

		:param new_volume: New volume level. must be between 0.0 and 1.0.
		"""
		self.sound_volume = new_volume

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

	def change_music_track(self, sel_item_and_index, sel_value, **kwargs) -> None:
		"""Change the music track. Standard callback method for the respective selectors in a menu.

		:param sel_item_and_index: part of the standard callback interface, not used here
		:param sel_value: Index of the chosen track
		:param kwargs: Optional keyword arguments
		"""
		self.play_music_track(sel_value)
		self.cur_track_idx = sel_value

	def play_music_track(self, track_index: int) -> None:
		"""Change the music track and play it"""
		pygame.mixer_music.load(FILENAMES_MUSIC_TRACKS[track_index])
		pygame.mixer_music.set_volume(self.music_volume)
		pygame.mixer_music.play(loops=-1)

	@abc.abstractmethod
	def update_display(self) -> None:
		"""Display the current state on the screen"""
