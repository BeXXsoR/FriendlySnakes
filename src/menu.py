"""Classes for all the menus in the game"""

# ----- Imports ------
import itertools
from enum import Enum
from dataclasses import dataclass
from typing import Callable, Union
from constants import *
import pygame
import pygame_menu

pygame.init()


# ----- Constants ------
# region Constants
NUM_PLAYER_ITEMS = [("1", 1), ("2", 2), ("3", 3), ("4", 4)]
PLAYER_ITEMS = [("Player 1", 0), ("Player 2", 1), ("Player 3", 2), ("Player 4", 3)]
COLOR_ITEMS = [("Green", GREEN), ("Blue", BLUE), ("Cyan", CYAN), ("Pink", PINK)]
LEVEL_PREV_IMG_ID = "Level_Prev_Img"
CONTROLS_LABEL_IDS = ("Control_Up", "Control_Left", "Control_Down", "Control_Right")
CONTROLS_BG_IMG_ID = "Controls_Background"
HIGHSCORE_LBL_IDS = ("Highscore1", "Highscore2", "Highscore3")
PLAYER_SEL_ID = "Sel_Player"
SNAKE_COLOR_IMG_ID = "Snake_Color"
SNAKE_COLOR_SEL_ID = "Sel_Color"
# endregion


# ----- Methods ------
def wdg_set_background(widget: pygame_menu.widgets.Widget, bg_color, trg_size: (int, int) = None) -> None:
	"""Set the background for the given widget to the given bg_color and inflate it to the given trg_size."""
	if trg_size:
		widget.set_background_color(bg_color)
		delta = utils.subtract_tuples_int(trg_size, widget.get_size())
		delta = (max(delta[0], 0), max(delta[1], 0))
		widget.set_background_color(bg_color, delta)
	else:
		widget.set_background_color(bg_color, inflate=None)


# region Side Classes
# ----- Classes ------
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


@dataclass
class MyRangeSlider:
	"""Class for customizable range slider parameters"""
	title: str
	default: float
	onchange: Callable
	id: str = None


@dataclass
class MyDropSelect:
	"""Class for customizable drop select parameters"""
	title: str
	items: [(str, int)]
	onchange: Callable
	default: int = 0
	id: str = None
	option_font: str = None


@dataclass
class MyButton:
	"""Class for customizable button parameters"""
	title: str
	action: Callable


@dataclass
class MySelector:
	"""Class for customizable selector parameters"""
	title: str
	items: [(str, int)]
	default: int
	onchange: Callable
	id: str = None


@dataclass
class MyTextInput:
	"""Class for customizable text input parameters"""
	title: str
	default: str
	maxchar: int
	onreturn: Callable
	id: str = None


MyWidget = Union[MyRangeSlider, MyDropSelect, MyButton, MySelector, MyTextInput]


# endregion


class Menu:
	"""Class for the menu in the game"""

	def __init__(self, main_surface: pygame.Surface, rect: pygame.Rect, bg_img: pygame.Surface = None, scaling_factor: float = None,
				 lang: utils.Language = utils.Language.ENGLISH, button_texts: [str] = None, level_names: [str] = None, highscores: [[(str, str)]] = None, has_submenu_levels: bool = True, enable_controls_change: bool = True):
		"""
        Initialize the menu.

        :param main_surface: Surface to draw the menu onto
        :param rect: Rectangle for the menu (positioned w.r.t. the main surface)
        :param bg_img: Image to be used as the background of the menu
        :param scaling_factor: Factor for scaling positions and sizes from the benchmark screen to the actual screen
        :param lang: Language for the menu
        :param button_texts: Texts for the menu buttons
        :param level_names: Names of the levels
        :param highscores: Highscores of all levels in a displayable format
        :param has_submenu_levels: True if the menu should contain a submenu for selecting the level
        :param enable_controls_change: True if the changing of controls should be enabled in this menu
        """
		self.main_surface = main_surface
		self.start_game = False
		self.exit = False
		self.lang = lang
		self.num_players = 2
		self.level_idx = 0
		self.button_texts = button_texts if button_texts else TEXTS_BUTTON_START_MENU[self.lang]
		self.snake_colors = [GREEN, BLUE, CYAN, PINK]
		self.snake_controls = [
			[pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT],
			[pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d],
			[pygame.K_KP8, pygame.K_KP4, pygame.K_KP5, pygame.K_KP6],
			[pygame.K_i, pygame.K_j, pygame.K_k, pygame.K_l]]
		self.scaling_factor = scaling_factor if scaling_factor else main_surface.get_height() / BENCHMARK_HEIGHT
		# Background
		self.bg_img = bg_img
		# Initialize the menu - 1st, define all the areas, rects, images, etc.
		#   Menu area
		self.menu_rect = rect
		self.menu_surf = self.main_surface.subsurface(self.menu_rect)
		self.menu_frame_img = pygame.transform.scale(pygame.image.load(FILENAME_MENU_FRAME).convert_alpha(), self.menu_rect.size)
		#   Button area inside the menu area
		buttons_area_start = utils.mult_tuple_to_int(BUTTON_AREA_START, self.scaling_factor)
		buttons_area_size = utils.mult_tuple_to_int(BUTTON_AREA_SIZE, self.scaling_factor)
		self.buttons_area_rect = pygame.Rect(buttons_area_start, buttons_area_size)
		self.buttons_surf = self.menu_surf.subsurface(self.buttons_area_rect)
		#   Buttons inside the button area
		num_buttons = len(self.button_texts)
		self.button_size = (self.buttons_area_rect.w, int(self.scaling_factor * BUTTON_HEIGHT))
		free_space = int((self.buttons_area_rect.h - num_buttons * self.button_size[1]) / (num_buttons - 1))
		self.button_rects = [pygame.Rect((0, i * (self.button_size[1] + free_space)), self.button_size) for i in range(num_buttons)]
		self.button_imgs_orig = {state: pygame.image.load(FILENAMES_BUTTON[state]).convert_alpha() for state in WidgetState}
		self.button_imgs = {state: pygame.transform.scale(img_orig, self.button_size) for state, img_orig in self.button_imgs_orig.items()}
		self.button_base_imgs = {state: pygame_menu.BaseImage(image_path=FILENAMES_BUTTON[state], drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL) for state in WidgetState}
		#   Texts for the buttons
		self.font_size = int(BUTTON_FONT_SIZE * self.scaling_factor)
		self.button_font_name = FONT_SNAKE_CHAN
		self.button_std_font = pygame.font.Font(self.button_font_name, self.font_size)
		self.button_texts_rend = [self.button_std_font.render(text, True, WHITE) for text in self.button_texts]
		#   2nd, define the sprites for the objects
		self.on_click_functions = [self.click_on_play_button, self.click_on_highscore_button, self.click_on_controls_button, self.click_on_options_button, self.click_on_exit_button]
		self.buttons = [Clickable(self.button_imgs[WidgetState.NORMAL], rect, func) for rect, func in zip(self.button_rects, self.on_click_functions)]
		self.button_group = ClickableGroup(*self.buttons)
		self.clock = pygame.time.Clock()
		# Variables for submenu options
		self.music_volume = pygame.mixer_music.get_volume()
		self.sound_volume = 1.0
		self.sel_music_track_name = FILENAMES_MUSIC_TRACKS[0][0]
		self.sel_bg_name = FILENAMES_GAME_BGS[0][0]
		self.submenu_options = self.init_submenu_options()
		# Variables for submenu controls
		self.controls_bg_img = pygame_menu.BaseImage(image_path=FILENAME_CONTROLS_BG, drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL).resize(*(utils.mult_tuple_to_int(CONTROL_BG_IMG_SIZE, self.scaling_factor)))
		self.sel_player_id_in_submenu_controls = 0
		trg_w, trg_h = utils.mult_tuple_to_int(SNAKE_COLOR_IMG_SIZE, self.scaling_factor)
		self.snake_color_imgs = {color: pygame_menu.BaseImage(image_path=FILENAMES_SNAKE_COLORS[color], drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL).resize(trg_w, trg_h) for color in self.snake_colors}
		self.submenu_controls = self.init_submenu_controls(enable_controls_change)
		self.mini_menu_change_controls = self.init_mini_menu_change_controls()
		# Variables for submenu levels
		self.level_prev_imgs = None
		self.submenu_levels = None
		self.level_names = level_names
		if has_submenu_levels:
			trg_w, trg_h = utils.mult_tuple_to_int(LEVEL_PREV_IMG_SIZE, self.scaling_factor)
			self.level_prev_imgs = [pygame_menu.BaseImage(image_path=FILENAME_LVL_PREV.format(i), drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL).resize(trg_w, trg_h) for i in range(len(level_names))]
			self.submenu_levels = self.init_submenu_level_selection()
		# Variables for submenu highscore
		self.highscores = highscores
		self.cur_level_id_for_highscore = 0
		self.submenu_highscore = self.init_submenu_highscore()
		# Variables for mini menu new highscore
		self.team_name = ""
		self.has_entered_team_name = False
		self.mini_menu_new_highscore = self.init_mini_menu_new_highscore()

	def init_submenu_options(self) -> pygame_menu.Menu:
		"""Initialize and return the submenu for the options."""
		my_widgets = [MyRangeSlider("Music volume", self.music_volume, self.change_music_volume),
					  MyRangeSlider("Sound volume", self.sound_volume, self.change_sound_volume),
					  MyDropSelect("Music Track", FILENAMES_MUSIC_TRACKS, self.change_music_track, option_font=FONT_COURIER_NEW),
					  MyDropSelect("Background", FILENAMES_GAME_BGS, self.change_background, option_font=FONT_COURIER_NEW)]
		menu_theme = pygame_menu.Theme(background_color=(0, 0, 0, 0), title=False, widget_alignment=pygame_menu.locals.ALIGN_CENTER, widget_font=self.button_std_font, widget_font_antialias=True, widget_font_color=WHITE)
		buttons_offset = self.buttons_surf.get_abs_offset()
		submenu_options = pygame_menu.Menu("Options", self.buttons_area_rect.w, self.buttons_area_rect.h, position=(buttons_offset[0], buttons_offset[1], False), enabled=False, theme=menu_theme)
		free_space = int((self.buttons_area_rect.h - (len(my_widgets) + 1) * self.button_size[1]) / len(my_widgets))
		block_height = self.button_size[1] + free_space
		top_margin = OPTIONS_TOP_MARGIN * self.scaling_factor
		options_frame = submenu_options.add.frame_v(self.buttons_area_rect.w, int(5 * block_height + top_margin), padding=0)
		options_frame.pack(submenu_options.add.vertical_margin(top_margin))
		red_block_rate = 0.875
		red_block_height = red_block_rate * block_height
		for my_wdg in my_widgets:
			cur_wdg = self.add_widget_from_mywidget(my_wdg, submenu_options)
			self.set_std_params(cur_wdg, self.button_size)
			options_frame.pack(cur_wdg, align=pygame_menu.locals.ALIGN_CENTER)
			options_frame.pack(submenu_options.add.vertical_margin(red_block_height - cur_wdg.get_height()))
		self.add_back_button(submenu_options, options_frame, int((1 - red_block_rate) * len(my_widgets) * block_height))
		submenu_options.resize(options_frame.get_width(), options_frame.get_height())
		return submenu_options

	def init_submenu_controls(self, enable_controls_change: bool) -> pygame_menu.Menu:
		"""Init the submenu for the controls"""
		menu_theme = pygame_menu.Theme(background_color=(0, 0, 0, 0), title=False, widget_alignment=pygame_menu.locals.ALIGN_CENTER, widget_font=self.button_std_font, widget_font_antialias=True, widget_font_color=WHITE)
		buttons_offset = self.buttons_surf.get_abs_offset()
		submenu_controls = pygame_menu.Menu("Controls", self.buttons_area_rect.w, self.buttons_area_rect.h, position=(buttons_offset[0], buttons_offset[1], False), enabled=False, theme=menu_theme)
		sel_player = self.add_widget_from_mywidget(MySelector("", PLAYER_ITEMS, self.sel_player_id_in_submenu_controls, self.change_player_in_submenu_controls, id=PLAYER_SEL_ID), submenu_controls)
		control_bg_img = submenu_controls.add.image(self.controls_bg_img, image_id=CONTROLS_BG_IMG_ID, padding=0)
		control_labels = [submenu_controls.add.label(utils.get_descr_from_pygame_key(pygame_key), label_id=lbl_id, padding=0, font_name=FONT_COURIER_NEW, font_size=int(CONTROLS_FONT_SIZE * self.scaling_factor), float=True)
						  for pygame_key, lbl_id in zip(self.snake_controls[self.sel_player_id_in_submenu_controls], CONTROLS_LABEL_IDS)]
		change_button = self.add_widget_from_mywidget(MyButton("Change", self.change_controls), submenu_controls)

		sel_color = self.add_widget_from_mywidget(MyDropSelect("", COLOR_ITEMS, self.change_color, default=self.sel_player_id_in_submenu_controls, id=SNAKE_COLOR_SEL_ID, option_font=FONT_COURIER_NEW), submenu_controls)
		snake_img = submenu_controls.add.image(self.snake_color_imgs[self.snake_colors[self.sel_player_id_in_submenu_controls]], image_id=SNAKE_COLOR_IMG_ID, padding=0)
		self.set_std_params(sel_color, sel_color.get_size(), FONT_COURIER_NEW, self.font_size, True)

		self.set_std_params(sel_player, self.button_size, self.button_font_name, self.font_size, True)
		self.set_std_params(change_button, utils.mult_tuple_to_int(change_button.get_size(), 1.1), FONT_COURIER_NEW, self.font_size, True)
		free_space = int((submenu_controls.get_height() - 3 * self.button_size[1] - control_bg_img.get_height()) / 3)
		block_height = self.button_size[1] + free_space
		top_margin = int(OPTIONS_TOP_MARGIN * self.scaling_factor)
		main_frame = submenu_controls.add.frame_v(self.buttons_area_rect.w, self.buttons_area_rect.h + 2 * top_margin, padding=0)

		vert_margin_right = int(0.5 * (block_height - change_button.get_height()))
		hor_frame_height = max(sel_color.get_height() + snake_img.get_height(), control_bg_img.get_height() + change_button.get_height()) + 2 * vert_margin_right
		hor_frame = submenu_controls.add.frame_h(main_frame.get_width(), hor_frame_height, padding=0)
		vert_frames = [submenu_controls.add.frame_v(0.5 * hor_frame.get_width(), hor_frame.get_height(), padding=0) for _ in range(2)]
		main_frame.pack(submenu_controls.add.vertical_margin(top_margin))
		main_frame.pack(sel_player, align=pygame_menu.locals.ALIGN_CENTER)
		main_frame.pack(submenu_controls.add.vertical_margin(max(1, block_height - sel_player.get_height())))
		vert_frames[1].pack(control_bg_img, align=pygame_menu.locals.ALIGN_CENTER)
		vert_frames[1].pack(submenu_controls.add.vertical_margin(max(1, vert_margin_right)))
		vert_frames[1].pack(change_button, align=pygame_menu.locals.ALIGN_CENTER)
		vert_margin_left = int((control_bg_img.get_height() - snake_img.get_height()) / 2)
		vert_frames[0].pack(submenu_controls.add.vertical_margin(vert_margin_left))
		vert_frames[0].pack(snake_img, align=pygame_menu.locals.ALIGN_CENTER)
		vert_frames[0].pack(submenu_controls.add.vertical_margin(max(1, vert_margin_left + vert_margin_right)))
		vert_frames[0].pack(sel_color, align=pygame_menu.locals.ALIGN_CENTER)
		# The center of a label part is [156/442 * image_width] away from the center of the image
		img_centerx, img_centery = control_bg_img.get_rect().center
		diff = int(CONTROL_LBL_TO_BG_RATIO * control_bg_img.get_width())
		trg_centers = [(img_centerx, img_centery - diff), (img_centerx - diff, img_centery), (img_centerx, img_centery + diff), (img_centerx + diff, img_centery)]
		for lbl, trg_center in zip(control_labels, trg_centers):
			vert_frames[1].pack(lbl, align=pygame_menu.locals.ALIGN_CENTER)
			lbl.translate(*utils.subtract_tuples_int(trg_center, lbl.get_rect().center))
		hor_frame.pack(vert_frames)
		main_frame.pack(hor_frame)
		self.add_back_button(submenu_controls, main_frame, max(1, int(0.9 * (block_height - change_button.get_height()))))
		if not enable_controls_change:
			assert isinstance(sel_player, pygame_menu.widgets.Selector), f"Expected selector, got {type(sel_player)} instead."
			sel_player.update_items(PLAYER_ITEMS[:self.num_players])
			change_button.hide()
			sel_color.hide()
		submenu_controls.resize(*main_frame.get_size())
		return submenu_controls

	def init_submenu_highscore(self) -> pygame_menu.Menu:
		"""Init the submenu for viewing the highscores"""
		menu_theme = pygame_menu.Theme(background_color=(0, 0, 0, 0), title=False, widget_alignment=pygame_menu.locals.ALIGN_CENTER, widget_font=self.button_std_font, widget_font_antialias=True, widget_font_color=WHITE)
		buttons_offset = self.buttons_surf.get_abs_offset()
		submenu_highscore = pygame_menu.Menu("Highscore", self.buttons_area_rect.w, self.buttons_area_rect.h, position=(buttons_offset[0], buttons_offset[1], False), enabled=False, theme=menu_theme)
		level_items = [(name, idx) for idx, name in enumerate(self.level_names)]
		sel_level = self.add_widget_from_mywidget(MySelector("Level: ", level_items, 0, self.change_level_in_submenu_highscore), submenu_highscore)
		self.set_std_params(sel_level, self.button_size, self.button_font_name, self.font_size, True)
		labels_highscore = [self.set_std_params(submenu_highscore.add.label("", label_id=lbl_id), self.button_size, FONT_COURIER_NEW, self.font_size, False) for lbl_id in HIGHSCORE_LBL_IDS]
		free_space = int((submenu_highscore.get_height() - 5 * self.button_size[1]) / 4)
		block_height = self.button_size[1] + free_space
		top_margin = int(OPTIONS_TOP_MARGIN * self.scaling_factor)
		main_frame = submenu_highscore.add.frame_v(self.buttons_area_rect.w, int(5 * block_height + 2 * top_margin), padding=0)
		main_frame.pack(submenu_highscore.add.vertical_margin(top_margin))
		main_frame.pack(sel_level, align=pygame_menu.locals.ALIGN_CENTER)
		main_frame.pack(submenu_highscore.add.vertical_margin(block_height - sel_level.get_height()))
		red_block_rate = 0.875
		highscores = self.get_highscore_strings()
		for lbl, text in zip(labels_highscore, highscores):
			lbl.set_title(text)
			self.set_wdg_background(lbl, self.button_size)
			main_frame.pack(lbl, align=pygame_menu.locals.ALIGN_CENTER)
			main_frame.pack(submenu_highscore.add.vertical_margin(red_block_rate * block_height - lbl.get_height()))
		self.add_back_button(submenu_highscore, main_frame, int((1 - red_block_rate) * 3 * block_height))
		submenu_highscore.resize(*main_frame.get_size())
		return submenu_highscore

	def init_submenu_level_selection(self) -> pygame_menu.Menu:
		"""Init the submenu for the level and player number selection screen"""
		menu_theme = pygame_menu.Theme(background_color=(0, 0, 0, 0), title=False, widget_alignment=pygame_menu.locals.ALIGN_CENTER, widget_font=self.button_font_name, widget_font_antialias=True, widget_font_color=WHITE)
		buttons_offset = self.buttons_surf.get_abs_offset()
		menu_w, menu_h = utils.mult_tuple_to_int(self.buttons_area_rect.size, LEVEL_MENU_SIZE_FACTOR)
		submenu_levels = pygame_menu.Menu("Level Selection", menu_w, menu_h, position=(buttons_offset[0], buttons_offset[1], False), enabled=False, theme=menu_theme)
		play_button = self.add_widget_from_mywidget(MyButton("Play", self.start_new_game), submenu_levels)
		sel_num_players = self.add_widget_from_mywidget(MySelector("Player Count: ", NUM_PLAYER_ITEMS, self.num_players - 1, self.change_num_players), submenu_levels)
		level_items = [(name, idx) for idx, name in enumerate(self.level_names)]
		sel_level = self.add_widget_from_mywidget(MySelector("Level: ", level_items, self.level_idx, self.change_level), submenu_levels)
		level_img = submenu_levels.add.image(self.level_prev_imgs[self.level_idx], image_id=LEVEL_PREV_IMG_ID, padding=0)
		free_space = (submenu_levels.get_height() - 4 * self.button_size[1] - level_img.get_height()) / 4
		block_height = self.button_size[1] + free_space
		top_margin = int(OPTIONS_TOP_MARGIN * self.scaling_factor)
		main_frame = submenu_levels.add.frame_v(submenu_levels.get_width(), int(4 * block_height + level_img.get_height() + 2 * top_margin), padding=0)
		main_frame.pack(submenu_levels.add.vertical_margin(top_margin))
		red_block_rate = 0.875
		# Pack widgets into the frame and add an appropriate vertical margin between them
		wdg_params = [(play_button, True, 1.1 * block_height),
					  (sel_num_players, True, red_block_rate * block_height),
					  (sel_level, True, red_block_rate * block_height - 13 * self.scaling_factor),
					  (level_img, False, 0)]
		for (wdg, set_std, block_trg_h) in wdg_params:
			if set_std:
				wdg = self.set_std_params(wdg, self.button_size, self.button_font_name, self.font_size, True)
			main_frame.pack(wdg, align=pygame_menu.locals.ALIGN_CENTER)
			if (diff := block_trg_h - wdg.get_height()) > 0:
				main_frame.pack(submenu_levels.add.vertical_margin(diff))
		self.add_back_button(submenu_levels, main_frame, int(block_height - play_button.get_height()))
		submenu_levels.resize(main_frame.get_width(), main_frame.get_height())
		return submenu_levels

	def init_mini_menu_change_controls(self) -> pygame_menu.Menu:
		"""Initialize the mini submenu for changing a snakes controls"""
		menu_theme = pygame_menu.Theme(background_color=(0, 0, 0, 0), title=False, widget_alignment=pygame_menu.locals.ALIGN_CENTER, widget_font_antialias=True, widget_font_color=WHITE)
		mini_menu = pygame_menu.Menu("Change Controls", 500, 500, position=(500, 500, False), enabled=False, theme=menu_theme)
		text_label = mini_menu.add.label("", label_id="TextLabel", align=pygame_menu.locals.ALIGN_CENTER)
		msg_label = mini_menu.add.label("Key not supported. Try again.", label_id="MsgLabel", align=pygame_menu.locals.ALIGN_CENTER)
		self.set_std_params(text_label, self.button_size, FONT_COURIER_NEW, int(CONTROLS_FONT_SIZE * self.scaling_factor), False)
		vert_marg = mini_menu.add.vertical_margin(15 * self.scaling_factor)
		self.set_std_params(msg_label, self.button_size, FONT_COURIER_NEW, int(0.75 * self.font_size), False)
		main_frame = mini_menu.add.frame_v(mini_menu.get_rect().w, text_label.get_height() + msg_label.get_height() + vert_marg.get_height(), padding=0)
		main_frame.pack(text_label, align=pygame_menu.locals.ALIGN_CENTER)
		main_frame.pack(vert_marg)
		main_frame.pack(msg_label, align=pygame_menu.locals.ALIGN_CENTER)
		msg_label.hide()
		mini_menu.resize(*main_frame.get_size())
		return mini_menu

	def init_mini_menu_new_highscore(self) -> pygame_menu.Menu:
		"""Initialize the mini menu for entering a new highscore"""
		menu_theme = pygame_menu.Theme(background_color=(0, 0, 0, 0), title=False, widget_alignment=pygame_menu.locals.ALIGN_CENTER, widget_font_antialias=True, widget_font_color=WHITE)
		mini_menu = pygame_menu.Menu("Change Controls", self.buttons_area_rect.w, self.buttons_area_rect.h, position=(500, 500, False), enabled=False, theme=menu_theme)
		text_label = mini_menu.add.label("New highscore!", label_id="TextLabel", align=pygame_menu.locals.ALIGN_CENTER)
		text_input_team_name = self.add_widget_from_mywidget(MyTextInput("Teamname: ", "", MAX_LEN_FOR_TEAM_NAME, self.change_team_name), mini_menu)
		self.set_std_params(text_label, self.button_size, FONT_COURIER_NEW, int(CONTROLS_FONT_SIZE * self.scaling_factor), False)
		vert_marg = mini_menu.add.vertical_margin(15 * self.scaling_factor)
		self.set_std_params(text_input_team_name, self.button_size, FONT_COURIER_NEW, self.font_size, False)
		main_frame = mini_menu.add.frame_v(mini_menu.get_rect().w, text_label.get_height() + text_input_team_name.get_height() + vert_marg.get_height(), padding=0)
		main_frame.pack(text_label, align=pygame_menu.locals.ALIGN_CENTER)
		main_frame.pack(vert_marg)
		main_frame.pack(text_input_team_name, align=pygame_menu.locals.ALIGN_CENTER)
		main_frame.set_border(1, WHITE)
		mini_menu.resize(*utils.add_two_tuples(main_frame.get_size(), (2, 2)))
		mini_menu.translate(*utils.subtract_tuples_int(self.main_surface.get_rect().center, self.mini_menu_change_controls.get_rect().center))
		return mini_menu

	def add_widget_from_mywidget(self, my_wdg: MyWidget, menu: pygame_menu.Menu) -> pygame_menu.widgets.Widget:
		"""
        Add a pygame widget to the menu based on the information in my_wdg.

        :param my_wdg: The MyWidget object containing the information for the widget
        :param menu: The menu to add the widget to
        :return: The widget that was added to the menu
        """
		wdg_id = my_wdg.id if hasattr(my_wdg, "id") and my_wdg.id else my_wdg.title
		if isinstance(my_wdg, MyRangeSlider):
			wdg = menu.add.range_slider(my_wdg.title, my_wdg.default, (0, 1), 0.01, rangeslider_id=wdg_id, range_text_value_enabled=False, slider_text_value_enabled=False, value_format=lambda x: str(int(x * 100)), onchange=my_wdg.onchange)
		elif isinstance(my_wdg, MyButton):
			wdg = menu.add.button(my_wdg.title, my_wdg.action)
		elif isinstance(my_wdg, MyDropSelect):
			wdg = menu.add.dropselect(my_wdg.title, my_wdg.items, default=my_wdg.default, dropselect_id=wdg_id, placeholder=my_wdg.items[0][0], placeholder_add_to_selection_box=False, onchange=my_wdg.onchange,
									  selection_option_font=my_wdg.option_font, selection_option_font_color=WHITE, selection_option_selected_font_color=WHITE, selection_box_border_color=WHITE,
									  selection_box_bgcolor=COLOR_WIDGETS[WidgetState.NORMAL], selection_option_selected_bgcolor=COLOR_WIDGETS[WidgetState.NORMAL])
		elif isinstance(my_wdg, MySelector):
			wdg = menu.add.selector(my_wdg.title, my_wdg.items, my_wdg.default, selector_id=wdg_id, onchange=my_wdg.onchange, style=pygame_menu.widgets.SELECTOR_STYLE_CLASSIC)
		elif isinstance(my_wdg, MyTextInput):
			wdg = menu.add.text_input(my_wdg.title, my_wdg.default, textinput_id=wdg_id, maxchar=my_wdg.maxchar, maxwidth=int(MAX_WIDTH_FOR_TEXT_INPUT * self.scaling_factor), onreturn=my_wdg.onreturn, copy_paste_enable=True)
		else:
			raise TypeError(f"Expected {type(MyWidget)}, got {type(my_wdg)} instead")
		wdg = wdg.add_self_to_kwargs()
		return wdg

	def add_back_button(self, menu: pygame_menu.Menu, frame: pygame_menu.widgets.Frame = None, margin: float = 0) -> pygame_menu.widgets.Button:
		"""Add a back button to the given menu in the given frame with the given vertical margin on top."""
		button = self.set_std_params(self.add_widget_from_mywidget(MyButton("Back", self.click_on_back_button), menu), self.button_size)
		assert isinstance(button, pygame_menu.widgets.Button)
		if frame:
			if margin > 0:
				frame.pack(menu.add.vertical_margin(int(margin)))
			frame.pack(button, align=pygame_menu.locals.ALIGN_CENTER)
		return button

	def set_std_params(self, wdg: pygame_menu.widgets.Widget, size: (int, int), font: pygame_menu.font.FontType = None, font_size: int = -1, enable_mouse_over_leave: bool = True) -> pygame_menu.widgets.Widget:
		"""Set some standard parameters for the given widget and return it."""
		wdg.set_padding(0)
		if enable_mouse_over_leave:
			wdg.set_onmouseover(self.mouse_over_widget)
			wdg.set_onmouseleave(self.mouse_leave_widget)
		wdg.set_selection_effect()
		wdg.set_font(font if font else self.button_std_font, font_size if font_size > 0 else self.font_size, WHITE, WHITE, WHITE, WHITE, None, True)
		self.set_wdg_background(wdg, size)
		return wdg

	def set_wdg_background(self, wdg: pygame_menu.widgets.Widget, size: (int, int)):
		"""Set a widgets background in a standard way."""
		if isinstance(wdg, pygame_menu.widgets.Button):
			wdg_set_background(wdg, self.button_base_imgs[WidgetState.NORMAL], size)
		else:
			wdg_set_background(wdg, COLOR_WIDGETS[WidgetState.NORMAL], size)
		return wdg

	def adjust_font_size_to_fit_trg_wdg_size(self, wdg: pygame_menu.widgets.Widget, trg_size: (int, int)) -> pygame_menu.widgets.Widget:
		"""Adjust the font size of the given widget until it fits into the given target size."""
		cur_font_size = self.font_size
		if wdg.get_font_info()["size"] != cur_font_size:
			wdg.update_font({"size": cur_font_size})
		while wdg.get_width() > trg_size[0] or wdg.get_height() > trg_size[1]:
			cur_font_size -= 1
			wdg.update_font({"size": cur_font_size})
		return wdg

	def reset(self):
		"""Reset the menu."""
		self.start_game = False
		self.exit = False
		self.has_entered_team_name = False
		self.music_volume = pygame.mixer_music.get_volume()
		self.submenu_options.get_widget("Music volume").set_default_value(self.music_volume)

	def slide_in(self) -> None:
		"""Slide the menu in from the left edge."""
		assert self.bg_img, "Background image must exist for slide_in method"
		speed = 10
		cur_topleft = (-self.menu_rect.w, self.menu_rect.top)
		while cur_topleft[0] <= 0:
			self.main_surface.blit(self.bg_img, (0, 0))
			for rect, text in zip(self.button_rects, self.button_texts_rend):
				button_topleft = utils.add_tuples([cur_topleft, rect.topleft, self.buttons_area_rect.topleft])
				cur_button_rect = pygame.Rect(button_topleft, self.button_size)
				self.main_surface.blit(self.button_imgs[WidgetState.NORMAL], button_topleft)
				self.main_surface.blit(text, text.get_rect(center=cur_button_rect.center))
			self.main_surface.blit(self.menu_frame_img, cur_topleft)
			cur_topleft = (cur_topleft[0] + speed, cur_topleft[1])
			pygame.display.update()
		self.main_surface.blit(self.bg_img, (0, 0))
		self.update_display()

	def handle_events(self) -> bool:
		"""Handle the events in the start menu. Returns True if the user starts a new game or False if they want to exit."""
		button_pushed = False
		submenus = [self.submenu_options, self.submenu_controls, self.submenu_highscore, self.mini_menu_new_highscore] + ([self.submenu_levels] if self.submenu_levels else [])
		while not self.start_game and not self.exit and not self.has_entered_team_name:
			events = pygame.event.get()
			active_submenu = [menu for menu in submenus if menu.is_enabled()]
			if active_submenu:
				active_submenu[0].update(events)
			else:
				for event in events:
					if event.type == pygame.MOUSEMOTION and not button_pushed:
						# Check for hovering over buttons
						prev_pos = utils.subtract_tuples(event.pos, event.rel)
						self.button_group.collide_update_img(prev_pos, self.button_imgs[WidgetState.NORMAL], self.buttons_surf)
						self.button_group.collide_update_img(event.pos, self.button_imgs[WidgetState.HOVERED], self.buttons_surf)
					if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
						# Check for click on button
						self.button_group.collide_update_img(event.pos, self.button_imgs[WidgetState.PUSHED], self.buttons_surf)
						button_pushed = True
					if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
						# Execute on click function if cursor is on a button
						self.button_group.collide_update_img(event.pos, self.button_imgs[WidgetState.NORMAL], self.buttons_surf)
						self.button_group.collide_click(event.pos, self.buttons_surf)
						button_pushed = False
			self.update_display()
			self.clock.tick(FPS)
		self.has_entered_team_name = False
		return self.start_game

	def change_controls(self, **kwargs) -> None:
		"""Change keys for controlling a snake. Standard callback function of the respective button widget."""
		self.submenu_controls.disable()
		self.mini_menu_change_controls.enable()
		directions = ["Up", "Left", "Down", "Right"]
		text_label = self.mini_menu_change_controls.get_widget("TextLabel")
		msg_label = self.mini_menu_change_controls.get_widget("MsgLabel")
		keys = []
		for direction in directions:
			text_label.set_title(f"Player {self.sel_player_id_in_submenu_controls + 1}: Press key for <{direction}>")
			self.set_std_params(text_label, self.button_size, FONT_COURIER_NEW, self.font_size, False)
			if direction == "Up":
				if (cur_center := self.mini_menu_change_controls.get_rect().center) != (trg_center := self.main_surface.get_rect().center):
					self.mini_menu_change_controls.translate(*utils.subtract_tuples_int(trg_center, cur_center))
			self.update_display()
			pressed_key = False
			while not pressed_key:
				for event in pygame.event.get():
					if event.type == pygame.KEYDOWN and (is_allowed := utils.check_allowed_keys(event.key)):
						keys.append(event.key)
						pressed_key = True
						if msg_label.is_visible():
							msg_label.hide()
					elif event.type == pygame.KEYDOWN and not is_allowed:
						if not msg_label.is_visible():
							msg_label.show()
					self.update_display()
		self.snake_controls[self.sel_player_id_in_submenu_controls] = keys
		self.update_submenu_controls(True, False)
		self.mini_menu_change_controls.disable()
		self.submenu_controls.enable()

	def change_color(self, sel_item_and_index, sel_value, **kwargs) -> None:
		"""Change the color in the submenu controls. Standard callback function of the resp. dropselect widget."""
		pre_color = self.snake_colors[self.sel_player_id_in_submenu_controls]
		post_color = sel_value
		self.snake_colors = [pre_color if color == post_color else post_color if color == pre_color else color for color in self.snake_colors]
		self.update_submenu_controls(False, True)

	def update_submenu_controls(self, update_controls: bool = True, update_color: bool = True) -> None:
		"""Update the key representation and/or the snake color in the controls submenu when new controls for a snake got defined."""
		if hasattr(self, "submenu_controls"):
			if update_controls:
				# Update controls part
				bg_img = self.submenu_controls.get_widget(CONTROLS_BG_IMG_ID)
				img_centerx, img_centery = bg_img.get_rect().center
				diff = int(CONTROL_LBL_TO_BG_RATIO * bg_img.get_width())
				trg_centers = [(img_centerx, img_centery - diff), (img_centerx - diff, img_centery), (img_centerx, img_centery + diff), (img_centerx + diff, img_centery)]
				for lbl_id, pygame_key, trg_center in zip(CONTROLS_LABEL_IDS, self.snake_controls[self.sel_player_id_in_submenu_controls], trg_centers):
					lbl = self.submenu_controls.get_widget(lbl_id)
					lbl.set_title(utils.get_descr_from_pygame_key(pygame_key))
					if (cur_center := lbl.get_rect().center) != trg_center:
						cur_translate = lbl.get_translate()
						add_translate = utils.subtract_tuples_int(trg_center, cur_center)
						lbl.translate(*utils.add_two_tuples(cur_translate, add_translate))
			if update_color:
				# Update color part
				color_img = self.submenu_controls.get_widget(SNAKE_COLOR_IMG_ID)
				assert isinstance(color_img, pygame_menu.widgets.Image), f"Expected Image type, got {type(color_img)} instead."
				color = self.snake_colors[self.sel_player_id_in_submenu_controls]
				color_img.set_image(self.snake_color_imgs[color])
				sel_color = self.submenu_controls.get_widget(SNAKE_COLOR_SEL_ID)
				sel_color.set_value([color_item[0] for color_item in COLOR_ITEMS if color_item[1] == color][0])

	def update_submenu_highscore(self) -> None:
		"""Update the highscores in the resp. submenu when the level to be displayed got changed."""
		if hasattr(self, "submenu_highscore"):
			for lbl_id, score in zip(HIGHSCORE_LBL_IDS, self.get_highscore_strings()):
				cur_label = self.submenu_highscore.get_widget(lbl_id)
				assert isinstance(cur_label, pygame_menu.widgets.Label), f"Expected Label, got {type(cur_label)} instead."
				cur_label.set_title(score)
				self.set_wdg_background(cur_label, self.button_size)

	def change_music_volume(self, new_volume: float, **kwargs) -> None:
		"""Change the music volume. The input param new_volume must be between 0.0 and 1.0."""
		pygame.mixer_music.set_volume(new_volume)
		self.music_volume = new_volume

	def change_sound_volume(self, new_volume: float, **kwargs) -> None:
		"""Change the sound volume. The input param new_volume must be between 0.0 and 1.0."""
		self.sound_volume = new_volume

	def start_new_game(self, **kwargs) -> None:
		"""Start a new game."""
		self.exit = False
		self.start_game = True
		if self.submenu_levels:
			self.submenu_levels.disable()

	def click_on_play_button(self) -> None:
		"""Start a new game."""
		if self.submenu_levels:
			self.submenu_levels.enable()
		else:
			self.start_new_game()

	def click_on_highscore_button(self) -> None:
		self.submenu_highscore.enable()

	def click_on_controls_button(self) -> None:
		self.submenu_controls.enable()

	def click_on_options_button(self) -> None:
		self.submenu_options.enable()

	def click_on_exit_button(self) -> None:
		"""Exit the application."""
		self.start_game = False
		self.exit = True

	def click_on_back_button(self, *args, **kwargs) -> None:
		for submenu in [self.submenu_options, self.submenu_controls, self.submenu_highscore]:
			submenu.disable()
		if self.submenu_levels:
			self.submenu_levels.disable()

	def mouse_over_widget(self, widget: pygame_menu.widgets.Widget, event: pygame.event.Event) -> None:
		"""Handle a mouseover on the given widget."""
		bg_color = self.button_base_imgs[WidgetState.HOVERED] if isinstance(widget, pygame_menu.widgets.Button) else COLOR_WIDGETS[WidgetState.HOVERED]
		wdg_set_background(widget, bg_color)
		widget.select(True, True)

	def mouse_leave_widget(self, widget: pygame_menu.widgets.Widget, event: pygame.event.Event) -> None:
		"""Handle a mouse leave on the given widget."""
		bg_color = self.button_base_imgs[WidgetState.NORMAL] if isinstance(widget, pygame_menu.widgets.Button) else COLOR_WIDGETS[WidgetState.NORMAL]
		wdg_set_background(widget, bg_color)

	def change_music_track(self, sel_item_and_index, sel_value, **kwargs) -> None:
		if sel_item_and_index[0][0] != self.sel_music_track_name:
			utils.play_music_track(sel_item_and_index[0][1], self.music_volume)
			self.sel_music_track_name = sel_item_and_index[0][0]

	def change_background(self, sel_item_and_index, sel_value, **kwargs) -> None:
		"""Change the in-game background. Standard callback function of the respective dropselect widget."""
		self.sel_bg_name = sel_item_and_index[0][0]

	def change_num_players(self, sel_item_and_index, sel_value, **kwargs) -> None:
		"""Change the number of players. Standard Callback function of the resp. selector widget."""
		self.num_players = sel_value
		sel_player = self.submenu_controls.get_widget(PLAYER_SEL_ID)
		assert isinstance(sel_player, pygame_menu.widgets.Selector), f"Expected selector, got {type(sel_player)} instead."
		sel_player.update_items(PLAYER_ITEMS[:self.num_players])
		if "widget" in kwargs and isinstance(wdg := kwargs["widget"], pygame_menu.widgets.Widget):
			self.adjust_font_size_to_fit_trg_wdg_size(wdg, self.button_size)
			self.set_wdg_background(wdg, self.button_size)

	def change_level(self, sel_item_and_index, sel_value, **kwargs) -> None:
		"""Change the level. Callback function for the resp. selector widget"""
		self.level_idx = sel_value
		if "widget" in kwargs and isinstance(wdg := kwargs["widget"], pygame_menu.widgets.Widget):
			self.adjust_font_size_to_fit_trg_wdg_size(wdg, self.button_size)
			self.set_wdg_background(wdg, self.button_size)
		# Change level preview image
		img_wdg = self.submenu_levels.get_widget(LEVEL_PREV_IMG_ID)
		assert isinstance(img_wdg, pygame_menu.widgets.Image), f"Expected Image type, got {type(img_wdg)} instead."
		img_wdg.set_image(self.level_prev_imgs[self.level_idx])

	def change_player_in_submenu_controls(self, sel_item_and_index, sel_value, **kwargs) -> None:
		"""Change the player whose controls are displayed in the controls submenu. Callback function for the resp. selector widget"""
		self.sel_player_id_in_submenu_controls = sel_value
		self.update_submenu_controls(True, True)

	def change_level_in_submenu_highscore(self, sel_item_and_index, sel_value, **kwargs) -> None:
		"""Change the level in the highscore submenu. Callback function for the resp. selector widget"""
		self.cur_level_id_for_highscore = sel_value
		if "widget" in kwargs and isinstance(wdg := kwargs["widget"], pygame_menu.widgets.Widget):
			self.adjust_font_size_to_fit_trg_wdg_size(wdg, self.button_size)
			self.set_wdg_background(wdg, self.button_size)
		self.update_submenu_highscore()

	def set_sound_volume(self, volume: float) -> None:
		"""Set the given volume as the default value for the sound volume widget"""
		if 0 <= volume <= 1:
			self.sound_volume = volume
			self.submenu_options.get_widget("Sound volume").set_default_value(self.sound_volume)

	def set_controls(self, controls: [[int, int, int, int]]) -> None:
		"""Update the snake controls in the menu"""
		self.snake_controls = controls
		self.update_submenu_controls(True, False)

	def set_colors(self, colors: [(int, int, int)]):
		"""Update the snake colors in the menu"""
		self.snake_colors = colors
		self.update_submenu_controls(False, True)

	def set_bg_value(self, bg_name: str) -> None:
		"""Update the selected background in the dropselect widget"""
		self.sel_bg_name = bg_name
		self.submenu_options.get_widget("Background").set_value(bg_name)

	def set_music_track_value(self, track_name) -> None:
		"""Update the selected music track in the dropselect widget"""
		self.sel_music_track_name = track_name
		self.submenu_options.get_widget("Music Track").set_value(track_name)

	def set_highscore(self, level_idx: int, highscore: [(str, str)]) -> None:
		"""Set the highscore for the given level to the given score"""
		self.highscores[level_idx] = highscore
		self.update_submenu_highscore()

	def get_highscore_strings(self) -> [str]:
		"""Return the strings for the highscores of the currently displayed level"""
		scores = self.highscores[self.cur_level_id_for_highscore]
		return [f"{idx + 1}. {name:{MAX_LEN_FOR_TEAM_NAME}} {score.rjust(5)}" for idx, (name, score) in enumerate(scores)] + [""] * max(0, (3 - len(scores)))

	def change_team_name(self, current_text: str, **kwargs) -> None:
		"""Change the team name for a new highscore. Standard callback function of the resp. text input widget"""
		self.team_name = current_text
		self.has_entered_team_name = True

	def get_infos(self) -> (int, int, float, [[int, int, int, int]]):
		"""
        Return the params needed for outside the menu that might have been changed in the menu

        :return: Tuple containing [0] the index of the selected level, [1] the number of players, [2] the sound volume, [3] the snake controls, [4] the snake colors, [5] the name of the selected background, [6] the name of the selected music track
        """
		if self.submenu_levels:
			return self.level_idx, self.num_players, self.sound_volume, self.snake_controls, self.snake_colors, self.sel_bg_name, self.sel_music_track_name
		else:
			return None, None, self.sound_volume, self.snake_controls, self.snake_colors, self.sel_bg_name, self.sel_music_track_name

	def update_display(self) -> None:
		"""Display the current state on the screen"""
		self.main_surface.blit(self.bg_img, (0, 0)) if self.bg_img else self.main_surface.fill(BG_COLOR)
		submenus = [self.submenu_options, self.submenu_controls, self.submenu_highscore, self.mini_menu_change_controls, self.mini_menu_new_highscore] + ([self.submenu_levels] if self.submenu_levels else [])
		active_submenu = active[0] if (active := [menu for menu in submenus if menu.is_enabled()]) else None
		if active_submenu:
			active_submenu.draw(self.main_surface)
			if active_submenu is self.mini_menu_change_controls:
				self.submenu_controls.enable()
				self.submenu_controls.draw(self.main_surface)
				self.submenu_controls.disable()
		else:
			self.button_group.draw(self.buttons_surf)
			for rect, text in zip(self.button_rects, self.button_texts_rend):
				self.buttons_surf.blit(text, text.get_rect(center=rect.center))
		if active_submenu is not self.mini_menu_new_highscore:
			self.main_surface.blit(self.menu_frame_img, self.menu_rect)
		pygame.display.update()
