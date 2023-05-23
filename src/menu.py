"""Classes for all the menus in the game"""

import utils
from enum import Enum
import pygame
import pygame_menu

pygame.init()


class ButtonState(Enum):
	NORMAL = 0
	PUSHED = 1
	HOVERED = 2


class Language(Enum):
	GERMAN = 0
	ENGLISH = 1


# ----- Constants ------
# region Constants
GREEN = (0, 153, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
PINK = (255, 51, 255)
CYAN = (51, 255, 255)
ORANGE = (255, 128, 0)
GREY = (192, 192, 192)
BLACK = (0, 0, 0)
BLACK_TP = (0, 0, 0, 0)
BG_COLOR = GREEN
FILENAMES_SNAKE = {GREEN: "../res/menu_snake_green.png", BLUE: "../res/menu_snake_blue.png",
				   CYAN: "../res/menu_snake_cyan.png", PINK: "../res/menu_snake_pink.png"}
FILENAME_BUTTON = "../res/button.png"
FILENAME_KEY_BG = "../res/key_bg.png"
FILENAME_ROOT_LVL_PREV = "../res/level_prev_{}.png"
FILENAME_BG = "../res/menu_bg.png"
FILENAMES_MUSIC_TRACKS = ["../res/title_theme.ogg"]
# FILENAME_MENU_SIDE_BAR = "../res/menu_side_bar.png"
FILENAME_MENU_FRAME = "../res/menu_frame.png"
FILENAMES_BUTTON = {ButtonState.NORMAL: "../res/menu_button_normal.png", ButtonState.PUSHED: "../res/menu_button_pushed.png", ButtonState.HOVERED: "../res/menu_button_hovered.png"}
TEXTS_BUTTON = {Language.GERMAN: ["Neues Spiel", "Profil wählen", "Steuerung", "Optionen", "Verlassen"],
				Language.ENGLISH: ["New game", "Choose profile", "Controls", "Options", "Exit"]}
BG_ITEMS = [("Desert", 0)]
MUSIC_TRACK_ITEMS = [("Bells Song", 0)]
FADE_MS = 1
FPS = 60
# benchmark screen: 2560x1440
BENCHMARK_HEIGHT = 1440
MENU_FRAME_START = (0, 300)
MENU_FRAME_SIZE = (554, 705)
BUTTON_AREA_START = (36, 267)
BUTTON_AREA_SIZE = (424, 369)
BUTTON_HEIGHT = 50
MENU_AREA_START = (0.01, 0.3)
MENU_AREA_SIZE = (0.2, 1 - 2 * MENU_AREA_START[1])
MENU_SIDE_BAR_SIZE = (0.1, 1)
BUTTON_SIZE = (1, 0.15)
BUTTON_FONT_SIZE = 25
MAP_TO_SCREEN_RATIO = 0.9
TITLE_FONT_SIZE = 200
SNAKE_NAME_FONT_SIZE = 80
CONTROLS_FONT_SIZE = 30
TITLE_HEIGHT = 0.1
SNAKE_SETTINGS_HEIGHT = 0.4
# Heights of elements inside the snake settings areas
SNAKE_NAME_HEIGHT = 0.2
FREE_SPACE_HEIGHT = 0.1
SNAKE_COLOR_HEIGHT = 0.4
SNAKE_CONTROLS_HEIGHT = 0.15
# endregion

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

	def collide_update_img(self, point: (int, int), img: pygame.Surface, surf: pygame.Surface=None) -> [BasicSprite]:
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


class StartMenu:
	def __init__(self, main_surface: pygame.Surface):
		"""Initialize the start menu"""
		self.main_surface = main_surface
		self.start_game = False
		self.exit = False
		self.lang = Language.ENGLISH
		self.button_texts = TEXTS_BUTTON[self.lang]
		self.snake_names = ["Kokosnuss", "Tiger", "Muh", "Mausi"]
		self.snake_colors = [GREEN, BLUE, CYAN, PINK]
		self.snake_controls = [["↑", "←", "↓", "→"], ["W", "A", "S", "D"], ["8", "4", "5", "6"], ["I", "J", "K", "L"]]
		self.level = 0
		usable_rect = pygame.rect.Rect(int((1 - MAP_TO_SCREEN_RATIO) * self.main_surface.get_width() / 2),
									   int((1 - MAP_TO_SCREEN_RATIO) * self.main_surface.get_height() / 2),
									   MAP_TO_SCREEN_RATIO * self.main_surface.get_width(),
									   MAP_TO_SCREEN_RATIO * self.main_surface.get_height())
		self.scaling_factor = main_surface.get_height() / BENCHMARK_HEIGHT
		# Background
		self.bg_img = pygame.transform.scale(pygame.image.load(FILENAME_BG).convert_alpha(), self.main_surface.get_size())
		# Initialize the menu - 1st, define all the areas, rects, images, etc.
		#   Menu area
		self.menu_rect = pygame.Rect(utils.mult_tuple_to_int(MENU_FRAME_START, self.scaling_factor), utils.mult_tuple_to_int(MENU_FRAME_SIZE, self.scaling_factor))
		self.menu_surf = self.main_surface.subsurface(self.menu_rect)
		self.menu_frame_img = pygame.transform.scale(pygame.image.load(FILENAME_MENU_FRAME).convert_alpha(), self.menu_rect.size)
		#   Button area inside the menu area
		buttons_area_start = utils.mult_tuple_to_int(BUTTON_AREA_START, self.scaling_factor)
		buttons_area_size = utils.mult_tuple_to_int(BUTTON_AREA_SIZE, self.scaling_factor)
		self.buttons_area_rect = pygame.Rect(buttons_area_start, buttons_area_size)
		self.buttons_surf = self.menu_surf.subsurface(self.buttons_area_rect)
		#   Buttons inside the button area
		num_buttons = len(self.button_texts)
		self.button_size = (self.buttons_area_rect.w, self.scaling_factor * BUTTON_HEIGHT)
		free_space = int((self.buttons_area_rect.h - num_buttons * self.button_size[1]) / (num_buttons - 1))
		self.button_rects = [pygame.Rect((0, i * (self.button_size[1] + free_space)), self.button_size) for i in range(num_buttons)]
		self.button_imgs_orig = {state: pygame.image.load(FILENAMES_BUTTON[state]).convert_alpha() for state in ButtonState}
		self.button_imgs = {state: pygame.transform.scale(img_orig, self.button_size) for state, img_orig in self.button_imgs_orig.items()}
		#   Texts for the buttons
		self.button_font = pygame.font.SysFont("Snake Chan", int(BUTTON_FONT_SIZE * self.scaling_factor))
		self.button_texts_rend = [self.button_font.render(text, True, WHITE) for text in self.button_texts]
		#   2nd, define the sprites for the objects
		self.on_click_functions = [self.click_on_new_game_button, self.click_on_profile_button, self.click_on_controls_button, self.click_on_options_button, self.click_on_exit_button]
		self.buttons = [Clickable(self.button_imgs[ButtonState.NORMAL], rect, func) for rect, func in zip(self.button_rects, self.on_click_functions)]
		self.button_group = ClickableGroup(*self.buttons)
		# Submenu Options
		self.menu_base_image = pygame_menu.BaseImage(image_path=FILENAME_MENU_FRAME, drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL)
		self.menu_theme = pygame_menu.Theme(background_color=(0, 0, 0, 0), title=False, widget_alignment=pygame_menu.locals.ALIGN_LEFT, widget_font=self.button_font, widget_font_antialias=True, widget_font_color=WHITE)
		self.music_volume = 0.1
		self.sound_volume = 1
		self.cur_track_idx = 0
		self.cur_bg_idx = 0
		buttons_offset = self.buttons_surf.get_abs_offset()
		self.submenu_options = pygame_menu.Menu("Options", self.buttons_area_rect.w, self.buttons_area_rect.h, position=(buttons_offset[0], buttons_offset[1], False), enabled=False, theme=self.menu_theme)
		# self.submenu_options = pygame_menu.Menu("Options", self.menu_rect.w, self.menu_rect.h, enabled=False, theme=self.menu_theme)
		# self.submenu_options.add.range_slider("Music volume", self.music_volume, (0, 1), 0.01, rangeslider_id="MusicVolumeSlider", value_format=lambda x: str(int(x * 100)), onchange=self.change_music_volume, margin=(0, free_space))
		# self.submenu_options.add.range_slider("Sound volume", self.sound_volume, (0, 1), 0.01, rangeslider_id="SoundVolumeSlider", value_format=lambda x: str(int(x * 100)), onchange=self.change_sound_volume, margin=(0, free_space))
		sel_music_track = self.submenu_options.add.selector("Music Track: ", MUSIC_TRACK_ITEMS, margin=(0, free_space), font_size=int(BUTTON_FONT_SIZE / 2))
		sel_music_track.set_margin(0, self.button_size[1] + free_space - sel_music_track.get_height())
		slider_music_vol = self.submenu_options.add.range_slider("Music volume", self.music_volume, (0, 1), 0.01, rangeslider_id="MusicVolumeSlider", range_text_value_enabled=False, slider_text_value_enabled=False, value_format=lambda x: str(int(x * 100)), onchange=self.change_music_volume)
		slider_music_vol.set_margin(0, self.button_size[1] + free_space - slider_music_vol.get_height())
		slider_sound_vol = self.submenu_options.add.range_slider("Sound volume", self.sound_volume, (0, 1), 0.01, rangeslider_id="SoundVolumeSlider", range_text_value_enabled=False, slider_text_value_enabled=False, value_format=lambda x: str(int(x * 100)), onchange=self.change_sound_volume)
		slider_sound_vol.set_margin(0, self.button_size[1] + free_space - slider_sound_vol.get_height())
		sel_bg = self.submenu_options.add.selector("Background: ", BG_ITEMS, margin=(0, free_space), font_size=int(BUTTON_FONT_SIZE / 2))
		sel_bg.set_margin(0, self.button_size[1] + free_space - sel_bg.get_height())
		button_back = self.submenu_options.add.button("Back", self.click_on_back_button, align=pygame_menu.locals.ALIGN_CENTER)
		button_back.set_margin(0, self.button_size[1] + free_space - button_back.get_height())
		self.submenu_options.center_content()




		# Title
		# self.title_font = pygame.font.Font(None, int(TITLE_FONT_SIZE * self.scaling_factor))
		# self.title_rendered = self.title_font.render("Friendly Snakes", True, BLUE)
		# self.title_rect = pygame.rect.Rect(usable_rect.topleft, (usable_rect.w, TITLE_HEIGHT * usable_rect.h))
		# # Free space rect
		# self.free_space_rect = pygame.rect.Rect(self.title_rect.bottomleft, (self.title_rect.w, FREE_SPACE_HEIGHT * usable_rect.h))
		# # SNAKE SETTINGS AREA
		# ## fonts
		# self.snake_name_font = pygame.font.Font(None, int(SNAKE_NAME_FONT_SIZE * self.scaling_factor))
		# self.snake_controls_font = pygame.font.SysFont("segoeuisymbol", int(CONTROLS_FONT_SIZE * self.scaling_factor))
		# ## rects
		# area_w, area_h = int(usable_rect.w / 4), int(SNAKE_SETTINGS_HEIGHT * usable_rect.h)
		# self.snake_settings_rects = [pygame.rect.Rect(usable_rect.left + int(i / 4 * usable_rect.w), self.free_space_rect.bottom, area_w, area_h) for i in range(4)]
		# self.snake_settings_surfs = [self.menu_surface.subsurface(rect) for rect in self.snake_settings_rects]
		# ## inner rects
		# BORDER_DIST = 0.1
		# self.snake_name_rect = pygame.rect.Rect(BORDER_DIST * area_w, 0, (1 - 2 * BORDER_DIST) * area_w, SNAKE_NAME_HEIGHT * area_h)
		# self.snake_color_rect = pygame.rect.Rect(utils.add_tuples([self.snake_name_rect.bottomleft, (0, int(0.05 * area_h))]), tuple([SNAKE_COLOR_HEIGHT * area_h] * 2))
		# # self.snake_color_rect.centerx = self.snake_name_rect.centerx
		# controls_rect_size = tuple([SNAKE_CONTROLS_HEIGHT * min(area_w, area_h)] * 2)
		# # self.controls_rects = [pygame.rect.Rect(utils.add_tuples([self.snake_color_rect.bottomleft]), controls_rect_size)]
		# self.controls_rects = [pygame.rect.Rect((self.snake_name_rect.centerx + controls_rect_size[0], self.snake_color_rect.top), controls_rect_size)]
		# self.controls_rects[0].bottom = self.snake_color_rect.centery
		# # self.controls_rects[0].centerx = self.snake_color_rect.centerx
		# # self.controls_rects[0].top += 0.02 * self.snake_settings_rects[0].h
		# other_rects = [pygame.rect.Rect(utils.add_tuples([self.controls_rects[0].bottomleft, ((i - 1) * controls_rect_size[0], 0)]), controls_rect_size) for i in range(3)]
		# self.controls_rects.extend(other_rects)
		# # prepare images
		# self.snake_imgs = {k: pygame.transform.scale(pygame.image.load(v).convert_alpha(), utils.mult_tuple_to_int(self.snake_color_rect.size, 0.8)) for k,v in FILENAMES_SNAKE.items()}
		# self.name_button_img = pygame.transform.scale(pygame.image.load(FILENAME_KEY_BG).convert_alpha(), utils.mult_tuple_to_int(self.snake_name_rect.size, 1))
		# # self.name_button_img = pygame.transform.scale(pygame.image.load(FILENAME_BUTTON).convert_alpha(), utils.mult_tuple_to_int(self.snake_name_rect.size, 1))
		# self.color_button_img = pygame.transform.scale(pygame.image.load(FILENAME_KEY_BG).convert_alpha(), utils.mult_tuple_to_int(self.snake_color_rect.size, 1))
		# # self.color_button_img = pygame.transform.scale(pygame.image.load(FILENAME_BUTTON).convert_alpha(), utils.mult_tuple_to_int(self.snake_color_rect.size, 1))
		# self.controls_bg_img = pygame.transform.scale(pygame.image.load(FILENAME_KEY_BG).convert_alpha(), utils.mult_tuple_to_int(controls_rect_size, 1))
		# # prepare buttons
		# self.name_button = Clickable(self.name_button_img, self.name_button_img.get_rect(center=self.snake_name_rect.center), self.click_on_name_button())
		# self.color_button = Clickable(self.color_button_img, self.color_button_img.get_rect(center=self.snake_color_rect.center), self.click_on_color_button())
		# self.control_buttons = [Clickable(self.controls_bg_img, rect, None) for rect in self.controls_rects]
		# # self.button_grp = ClickableGroup(self.control_buttons + [self.name_button])
		# self.button_grp = ClickableGroup(self.control_buttons + [self.name_button,  self.color_button])
		# prepare controls
		# self.controls_sprites =
		## LEVEL SELECT AREA
		# self.level_previews = [pygame.transform.scale(pygame.image.load(FILENAME_ROOT_LVL_PREV.format(str(i))).convert_alpha(), ) for i in range(1)]
		# rest
		self.clock = pygame.time.Clock()
		self.play_music_track(0)
		self.main_surface.blit(self.bg_img, (0, 0))
		msg_font = pygame.font.SysFont("Snake Chan", 40)
		msg_rendered = msg_font.render("Press any key", True, WHITE)
		self.main_surface.blit(msg_rendered, msg_rendered.get_rect(center=(self.main_surface.get_rect().centerx, 0.95 * self.main_surface.get_height())))
		pygame.display.update()

	def slide_menu_in(self) -> None:
		"""Slide the menu in from the left edge"""
		speed = 10
		cur_topleft = (-self.menu_rect.w, self.menu_rect.top)
		while cur_topleft[0] <= 0:
			self.main_surface.blit(self.bg_img, (0, 0))
			for rect, text in zip(self.button_rects, self.button_texts_rend):
				button_topleft = utils.add_tuples([cur_topleft, rect.topleft, self.buttons_area_rect.topleft])
				cur_button_rect = pygame.Rect(button_topleft, self.button_size)
				self.main_surface.blit(self.button_imgs[ButtonState.NORMAL], button_topleft)
				self.main_surface.blit(text, text.get_rect(center=cur_button_rect.center))
			self.main_surface.blit(self.menu_frame_img, cur_topleft)
			cur_topleft = (cur_topleft[0] + speed, cur_topleft[1])
			pygame.display.update()
		self.update_display()

	def handle_events(self) -> bool:
		"""Handle the events in the start menu. Returns True if the user starts a new game or False if they want to exit"""
		button_pushed = False
		while not self.start_game and not self.exit:
			events = pygame.event.get()
			if self.submenu_options.is_enabled():
				self.submenu_options.update(events)
			else:
				for event in events:
					if event.type == pygame.MOUSEMOTION and not button_pushed:
						# Check for hovering over buttons
						prev_pos = utils.subtract_tuples(event.pos, event.rel)
						self.button_group.collide_update_img(prev_pos, self.button_imgs[ButtonState.NORMAL], self.buttons_surf)
						self.button_group.collide_update_img(event.pos, self.button_imgs[ButtonState.HOVERED], self.buttons_surf)
					if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
						# Check for click on button
						self.button_group.collide_update_img(event.pos, self.button_imgs[ButtonState.PUSHED], self.buttons_surf)
						button_pushed = True
					if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
						# Execute on click function if cursor is on a button
						self.button_group.collide_update_img(event.pos, self.button_imgs[ButtonState.NORMAL], self.buttons_surf)
						self.button_group.collide_click(event.pos, self.buttons_surf)
						button_pushed = False
			self.update_display()
			self.clock.tick(FPS)
		return self.start_game

	def handle_submenu_options(self):
		"""Handle the submenu for the options"""
		self.submenu_options.enable()
		# menu = pygame_menu.Menu("Options", self.menu_rect.w, self.menu_rect.h, theme=pygame_menu.themes.THEME_BLUE)
		# menu.add.text_input("Name: ", default="Kokosnuss")
		# menu.add.range_slider("Music volume", 100, (0, 100), 1, rangeslider_id="MusicVolumeSlider", value_format=lambda x: str(int(x)), onchange=self.change_music_volume)
		# menu.add.button("Back", pygame_menu.events.CLOSE)
		# menu.mainloop(self.menu_surf)
		pass

	def change_music_volume(self, new_volume: float) -> None:
		"""Change the music volume. The input param new_volume must be between 0.0 and 1.0."""
		pygame.mixer_music.set_volume(new_volume)
		self.music_volume = new_volume

	def change_sound_volume(self, new_volume: float) -> None:
		"""Change the sound volume. The input param new_volume must be between 0.0 and 1.0."""
		self.sound_volume = new_volume

	def click_on_new_game_button(self) -> None:
		"""Start a new game"""
		self.exit = False
		self.start_game = True

	def click_on_profile_button(self) -> None:
		pass

	def click_on_controls_button(self) -> None:
		pass

	def click_on_options_button(self) -> None:
		self.handle_submenu_options()

	def click_on_exit_button(self) -> None:
		"""Exit the application"""
		self.start_game = False
		self.exit = True

	def click_on_back_button(self, *args, **kwargs) -> None:
		self.submenu_options.disable()

	def change_music_track(self, sel_item_and_index, sel_value, **kwargs) -> None:
		self.play_music_track(sel_value)
		self.cur_track_idx = sel_value

	def play_music_track(self, track_index: int) -> None:
		"""Change the music track and play it"""
		pygame.mixer_music.load(FILENAMES_MUSIC_TRACKS[track_index])
		pygame.mixer_music.set_volume(self.music_volume)
		pygame.mixer_music.play(loops=-1)

	def update_display(self) -> None:
		"""Display the current state on the screen"""
		self.main_surface.blit(self.bg_img, (0, 0))
		# self.menu_surf.blit(self.side_bar_img, self.side_bar_rect)
		self.button_group.draw(self.buttons_surf)
		pygame.draw.rect(self.main_surface, RED, self.submenu_options.get_rect(), width=5)
		if self.submenu_options.is_enabled():
			self.submenu_options.draw(self.main_surface)
		else:
			for rect, text in zip(self.button_rects, self.button_texts_rend):
				self.buttons_surf.blit(text, text.get_rect(center=rect.center))
		self.main_surface.blit(self.menu_frame_img, self.menu_rect)
		# pygame.draw.rect(self.main_surface, RED, self.menu_rect, width=1)
		# pygame.draw.rect(self.menu_surf, GREY, self.side_bar_rect, width=1)
		# pygame.draw.rect(self.menu_surf, ORANGE, self.button_area_rect, width=1)
		# self.main_surface.blit(self.title_rendered, self.title_rendered.get_rect(center=self.title_rect.center))
		# # Draw button style backgrounds for the snake settings elements
		# for surf in self.snake_settings_surfs:
		# 	self.button_grp.draw(surf)
		# # Draw snake settings
		# for surf, name, color, controls in zip(self.snake_settings_surfs, self.snake_names, self.snake_colors, self.snake_controls):
		# 	cur_name_rendered = self.snake_name_font.render(name, True, color)
		# 	surf.blit(cur_name_rendered, cur_name_rendered.get_rect(center=self.snake_name_rect.center))
		# 	for key, rect in zip(controls, self.controls_rects):
		# 		cur_key_rendered = self.snake_controls_font.render(key, True, color)
		# 		surf.blit(cur_key_rendered, cur_key_rendered.get_rect(center=rect.center))
		# 	surf.blit(self.snake_imgs[color], self.snake_imgs[color].get_rect(center=self.snake_color_rect.center))
		pygame.display.update()


