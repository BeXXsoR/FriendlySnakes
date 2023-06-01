"""Module for the submenu classes in the friendly snakes package"""

# ----- Imports --------
import utils
from menus import Submenu, WidgetState, FILENAME_MENU_FRAME, BUTTON_FONT_SIZE, FILENAMES_BUTTON, FILENAMES_MUSIC_TRACKS
from constants import WHITE
import pygame
import pygame_menu

pygame.init()

# ----- Constants --------
COLOR_WIDGETS = {WidgetState.NORMAL: (76, 123, 209), WidgetState.HOVERED: (111, 164, 255)}
BG_ITEMS = [("Desert", 0)]
MUSIC_TRACK_ITEMS = [("Bells Song", 0)]
OPTIONS_TOP_MARGIN = 13


# ----- Methods --------
def wdg_set_background(widget: pygame_menu.widgets.Widget, bg_color, trg_size: (int, int)) -> None:
	"""Set the background for the given widget to the given bg_color and inflate it to the given trg_size"""
	widget.set_background_color(bg_color)
	delta = utils.subtract_tuples_int(trg_size, widget.get_size())
	delta = (max(delta[0], 0), max(delta[1], 0))
	widget.set_background_color(bg_color, delta)


# ----- Classes --------
class SubmenuOptions(Submenu):
	"""Class for the options submenu"""

	def __init__(self, parent_surface: pygame.Surface, buttons_area_topleft: (int, int), buttons_area_size: (int, int)):
		"""
		Initialize the options submenu.

		:param parent_surface: Surface to draw the menu onto.
		:param buttons_area_topleft: Position of topleft corner of the buttons area in the parent surface.
		:param buttons_area_size: Size of the buttons area
		"""
		super().__init__(parent_surface, buttons_area_topleft, buttons_area_size)
		self.music_volume = 0.1
		self.sound_volume = 1
		self.cur_track_idx = 0
		self.cur_bg_idx = 0
		self.menu_base_image = pygame_menu.BaseImage(image_path=FILENAME_MENU_FRAME, drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL)
		self.button_base_imgs = {state: pygame_menu.BaseImage(image_path=FILENAMES_BUTTON[state], drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL) for state in WidgetState}
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
		num_buttons = 5
		free_space = int((self.buttons_area_rect.h - num_buttons * self.button_size[1]) / (num_buttons - 1))
		block_height = self.button_size[1] + free_space
		options_frame = self.submenu_options.add.frame_v(self.buttons_area_rect.w, 5 * block_height + OPTIONS_TOP_MARGIN, padding=0)
		options_frame.pack(self.submenu_options.add.vertical_margin(OPTIONS_TOP_MARGIN))
		for wdg in options_widgets:
			options_frame.pack(wdg, align=pygame_menu.locals.ALIGN_CENTER)
			options_frame.pack(self.submenu_options.add.vertical_margin(0.875 * block_height - wdg.get_height()))
		options_frame.pack(self.submenu_options.add.vertical_margin(0.5 * block_height))
		options_frame.pack(button_back, align=pygame_menu.locals.ALIGN_CENTER)
		self.submenu_options.resize(options_frame.get_width(), options_frame.get_height())

	def handle_events(self) -> bool:
		"""
		Handle the events in the pygame event queue.

		:return: True if outer loop should be continued, False otherwise
		"""
		self.submenu_options.update(pygame.event.get())
		return self.click_on_back

	def change_music_volume(self, new_volume: float) -> None:
		"""
		Change the music volume.

		:param new_volume: New volume level, must be between 0.0 and 1.0.
		"""
		pygame.mixer_music.set_volume(new_volume)
		self.music_volume = new_volume

	def change_sound_volume(self, new_volume: float) -> None:
		"""
		Change the sound volume.

		:param new_volume: New volume level, must be between 0.0 and 1.0.
		"""
		self.sound_volume = new_volume

	def change_music_track(self, sel_item_and_index, sel_value, **kwargs) -> None:
		"""Change the music track. Standard callback method for the respective selectors in a menu.

		:param sel_item_and_index: part of the standard callback interface, not used here
		:param sel_value: Index of the chosen track
		:param kwargs: part of the standard callback interface, not used here
		"""
		utils.play_music_track(FILENAMES_MUSIC_TRACKS[sel_value], self.music_volume)
		self.cur_track_idx = sel_value
