"""Module for the start menu class in the friendly snakes package"""

import utils
from constants import FPS, WHITE
from menus import *
import pygame
import pygame_menu


# ----- Constants ------
MENU_FRAME_START = (0, 300)
MENU_FRAME_SIZE = (670, 705)
BUTTON_AREA_START = (36, 267)
BUTTON_AREA_SIZE = (520, 369)
OPTIONS_TOP_MARGIN = 13
TEXTS_BUTTON = {Language.GERMAN: ["Neues Spiel", "Profil wählen", "Steuerung", "Optionen", "Verlassen"],
				Language.ENGLISH: ["New game", "Choose profile", "Controls", "Options", "Exit"]}


# ----- Classes --------
class StartMainMenu(MainMenu):
	"""Class for the start menu"""

	def __init__(self, main_surface: pygame.Surface):
		"""Initialize the start menu"""
		super().__init__(main_surface)
		# Background
		self.bg_img = pygame.transform.scale(pygame.image.load(FILENAME_BG).convert_alpha(), self.parent_surface.get_size())
		# Initialize the menu - 1st, define all the areas, rects, images, etc.
		# #   Menu area
		# self.menu_rect = pygame.Rect(utils.mult_tuple_to_int(MENU_FRAME_START, self.scaling_factor), utils.mult_tuple_to_int(MENU_FRAME_SIZE, self.scaling_factor))
		# self.menu_surf = self.main_surface.subsurface(self.menu_rect)
		# self.menu_frame_img = pygame.transform.scale(pygame.image.load(FILENAME_MENU_FRAME).convert_alpha(), self.menu_rect.size)
		# #   Button area inside the menu area
		# self.buttons_area_start = utils.mult_tuple_to_int(BUTTON_AREA_START, self.scaling_factor)
		# self.buttons_area_size = utils.mult_tuple_to_int(BUTTON_AREA_SIZE, self.scaling_factor)
		# self.buttons_area_rect = pygame.Rect(self.buttons_area_start, self.buttons_area_size)
		# self.buttons_surf = self.menu_surf.subsurface(self.buttons_area_rect)
		# #   Buttons inside the button area
		# self.button_texts = TEXTS_BUTTON[self.lang]
		# self.button_texts_rend = [self.button_font.render(text, True, WHITE) for text in self.button_texts]
		# num_buttons = len(self.button_texts)
		# free_space = int((self.buttons_area_rect.h - num_buttons * self.button_size[1]) / (num_buttons - 1))
		# self.button_rects = [pygame.Rect((0, i * (self.button_size[1] + free_space)), self.button_size) for i in range(num_buttons)]
		#   2nd, define the sprites for the objects
		self.on_click_functions = [self.click_on_new_game_button, self.click_on_profile_button, self.click_on_controls_button, self.click_on_options_button, self.click_on_exit_button]
		self.buttons = [Clickable(self.button_imgs[WidgetState.NORMAL], rect, func) for rect, func in zip(self.button_rects, self.on_click_functions)]
		self.button_group = ClickableGroup(*self.buttons)
		# Predefine the submenu "Options"
		self.menu_base_image = pygame_menu.BaseImage(image_path=FILENAME_MENU_FRAME, drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL)
		self.menu_theme = pygame_menu.Theme(background_color=(0, 0, 0, 0), title=False, widget_alignment=pygame_menu.locals.ALIGN_CENTER, widget_font=self.button_font, widget_font_antialias=True, widget_font_color=WHITE)
		buttons_offset = self.buttons_surf.get_abs_offset()
		self.submenu_options = pygame_menu.Menu("Options", self.buttons_area_rect.w, self.buttons_area_rect.h, position=(buttons_offset[0], buttons_offset[1], False), enabled=False, theme=self.menu_theme)
		slider_music_vol = self.submenu_options.add.range_slider("Music volume:", self.music_volume, (0, 1), 0.01, rangeslider_id="MusicVolumeSlider", range_text_value_enabled=False, slider_text_value_enabled=False, value_format=lambda x: str(int(x * 100)), onchange=self.change_music_volume)
		slider_sound_vol = self.submenu_options.add.range_slider("Sound volume:", self.sound_volume, (0, 1), 0.01, rangeslider_id="SoundVolumeSlider", range_text_value_enabled=False, slider_text_value_enabled=False, value_format=lambda x: str(int(x * 100)), onchange=self.change_sound_volume)
		sel_music_track = self.submenu_options.add.dropselect("Music Track:", MUSIC_TRACK_ITEMS, default=0, placeholder=MUSIC_TRACK_ITEMS[0][0], placeholder_add_to_selection_box=False)
		sel_bg = self.submenu_options.add.dropselect("Background:", BG_ITEMS, default=0, placeholder=BG_ITEMS[0][0], placeholder_add_to_selection_box=False)
		button_back = self.submenu_options.add.button("Back", self.click_on_back_button)
		for wdg in [slider_music_vol, slider_sound_vol, sel_music_track, sel_bg, button_back]:
			wdg.set_padding(0)
			wdg.set_onmouseover(self.mouse_over_widget)
			wdg.set_onmouseleave(self.mouse_leave_widget)
			wdg.set_selection_effect()
			wdg.set_font(self.button_font, int(BUTTON_FONT_SIZE * self.scaling_factor), WHITE, WHITE, WHITE, WHITE, None, True)
			if wdg is button_back:
				wdg_set_background(wdg, self.button_base_imgs[WidgetState.NORMAL], self.button_size)
			else:
				wdg_set_background(wdg, COLOR_WIDGETS[WidgetState.NORMAL], self.button_size)
				wdg.set_border(0, WHITE)
		options_widgets = [slider_music_vol, slider_sound_vol, sel_music_track, sel_bg]
		block_height = self.button_size[1] + self.free_space
		options_frame = self.submenu_options.add.frame_v(self.buttons_area_rect.w, 5 * block_height + OPTIONS_TOP_MARGIN, padding=0)
		options_frame.pack(self.submenu_options.add.vertical_margin(OPTIONS_TOP_MARGIN))
		for wdg in options_widgets:
			options_frame.pack(wdg, align=pygame_menu.locals.ALIGN_CENTER)
			options_frame.pack(self.submenu_options.add.vertical_margin(0.875 * block_height - wdg.get_height()))
		options_frame.pack(self.submenu_options.add.vertical_margin(0.5 * block_height))
		options_frame.pack(button_back, align=pygame_menu.locals.ALIGN_CENTER)
		self.submenu_options.resize(options_frame.get_width(), options_frame.get_height())
		# Start clock and music and display the initial screen
		self.clock = pygame.time.Clock()
		self.play_music_track(0)
		self.parent_surface.blit(self.bg_img, (0, 0))
		msg_font = pygame.font.SysFont("Snake Chan", 40)
		msg_rendered = msg_font.render("Press any key", True, WHITE)
		self.parent_surface.blit(msg_rendered, msg_rendered.get_rect(center=(self.parent_surface.get_rect().centerx, 0.95 * self.parent_surface.get_height())))
		pygame.display.update()

	def set_button_size(self) -> (int, int):
		"""Return the size of a button"""
		return utils.mult_tuple_to_int((BUTTON_AREA_SIZE[0], BUTTON_HEIGHT), self.scaling_factor)

	def set_button_area_start_and_size(self) -> ((int, int), (int, int)):
		"""
		Return the button area start position and size w.r.t. the benchmark screen

		:return: Tuple containing [0] the button area start position and [1] the button area size
		"""
		return utils.mult_tuple_to_int(BUTTON_AREA_START, self.scaling_factor), utils.mult_tuple_to_int(BUTTON_AREA_SIZE, self.scaling_factor)

	def set_menu_area_start_and_size(self) -> ((int, int), (int, int)):
		"""
		Return the menu area start position and size w.r.t. the benchmark screen

		:return: Tuple containing [0] the menu area start position and [1] the menu area size
		"""
		return utils.mult_tuple_to_int(MENU_FRAME_START, self.scaling_factor), utils.mult_tuple_to_int(MENU_FRAME_SIZE, self.scaling_factor)

	def set_button_texts(self) -> [str]:
		"""Return the texts for the buttons"""
		return TEXTS_BUTTON[self.lang]

	def slide_menu_in(self) -> None:
		"""Slide the menu in from the left edge"""
		speed = 10
		cur_topleft = (-self.menu_rect.w, self.menu_rect.top)
		while cur_topleft[0] <= 0:
			self.parent_surface.blit(self.bg_img, (0, 0))
			for rect, text in zip(self.button_rects, self.button_texts_rend):
				button_topleft = utils.add_tuples([cur_topleft, rect.topleft, self.buttons_area_rect.topleft])
				cur_button_rect = pygame.Rect(button_topleft, self.button_size)
				self.parent_surface.blit(self.button_imgs[WidgetState.NORMAL], button_topleft)
				self.parent_surface.blit(text, text.get_rect(center=cur_button_rect.center))
			self.parent_surface.blit(self.menu_frame_img, cur_topleft)
			cur_topleft = (cur_topleft[0] + speed, cur_topleft[1])
			pygame.display.update()
		self.update_display()

	def handle_events(self) -> bool:
		"""
		Handle the events in the menu.

		:return: True if play should start/ resume, False for exit
		"""
		pushed_button = None
		while not self.play_game and not self.exit:
			events = pygame.event.get()
			if self.submenu_options.is_enabled():
				self.submenu_options.update(events)
			else:
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

	def handle_submenu_options(self):
		"""Handle the submenu for the options"""
		self.submenu_options.enable()

	def click_on_new_game_button(self) -> None:
		"""Start a new game"""
		self.exit = False
		self.play_game = True

	def click_on_profile_button(self) -> None:
		pass

	def click_on_controls_button(self) -> None:
		pass

	def click_on_options_button(self) -> None:
		self.handle_submenu_options()

	def click_on_exit_button(self) -> None:
		"""Exit the application"""
		self.play_game = False
		self.exit = True

	def click_on_back_button(self, *args, **kwargs) -> None:
		self.submenu_options.disable()

	def update_display(self) -> None:
		"""Display the current state on the screen"""
		self.parent_surface.blit(self.bg_img, (0, 0))
		if self.submenu_options.is_enabled():
			self.submenu_options.draw(self.parent_surface)
		else:
			self.button_group.draw(self.buttons_surf)
			for rect, text in zip(self.button_rects, self.button_texts_rend):
				self.buttons_surf.blit(text, text.get_rect(center=rect.center))
		self.parent_surface.blit(self.menu_frame_img, self.menu_rect)

		# pygame.draw.rect(self.main_surface, RED, self.submenu_options.get_rect(), width=5)
		# options_frame_rect = self.submenu_options.get_widget("options_frame").get_rect()
		# options_frame_rect.top += self.submenu_options.get_rect().top
		# options_frame_rect.left += self.submenu_options.get_rect().left
		# pygame.draw.rect(self.main_surface, YELLOW, options_frame_rect, width=5)
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


