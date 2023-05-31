"""Module for the submenu classes in the friendly snakes package"""

# ----- Imports --------
import utils
from menus import Submenu, WidgetState, FILENAME_MENU_FRAME, BUTTON_FONT_SIZE, FILENAMES_BUTTON
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

	def __init__(self, parent_surface: pygame.Surface):
		"""Initialize the options submenu"""
		super().__init__(parent_surface)
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
		block_height = self.button_size[1] + self.free_space
		options_frame = self.submenu_options.add.frame_v(self.buttons_area_rect.w, 5 * block_height + OPTIONS_TOP_MARGIN, padding=0)
		options_frame.pack(self.submenu_options.add.vertical_margin(OPTIONS_TOP_MARGIN))
		for wdg in options_widgets:
			options_frame.pack(wdg, align=pygame_menu.locals.ALIGN_CENTER)
			options_frame.pack(self.submenu_options.add.vertical_margin(0.875 * block_height - wdg.get_height()))
		options_frame.pack(self.submenu_options.add.vertical_margin(0.5 * block_height))
		options_frame.pack(button_back, align=pygame_menu.locals.ALIGN_CENTER)
		self.submenu_options.resize(options_frame.get_width(), options_frame.get_height())