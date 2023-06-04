"""Classes for all the menus in the game"""

import utils
from enum import Enum
from dataclasses import dataclass
from typing import Callable
from constants import *
import pygame
import pygame_menu

pygame.init()


class WidgetState(Enum):
    NORMAL = 0
    PUSHED = 1
    HOVERED = 2


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
BG_COLOR = (167, 226, 247)
FILENAMES_SNAKE = {GREEN: "../res/menu_snake_green.png", BLUE: "../res/menu_snake_blue.png",
                   CYAN: "../res/menu_snake_cyan.png", PINK: "../res/menu_snake_pink.png"}
FILENAME_BUTTON = "../res/button.png"
FILENAME_KEY_BG = "../res/key_bg.png"
FILENAME_ROOT_LVL_PREV = "../res/level_prev_{}.png"
# FILENAME_MENU_SIDE_BAR = "../res/menu_side_bar.png"
FILENAME_MENU_FRAME = "../res/menu_frame.png"
FILENAMES_BUTTON = {WidgetState.NORMAL: "../res/menu_button_normal.png", WidgetState.PUSHED: "../res/menu_button_pushed.png", WidgetState.HOVERED: "../res/menu_button_hovered.png"}
COLOR_WIDGETS = {WidgetState.NORMAL: (76, 123, 209), WidgetState.HOVERED: (111, 164, 255)}
TEXTS_BUTTON = {utils.Language.GERMAN: ["Spielen", "Profil wählen", "Steuerung", "Optionen", "Verlassen"],
                utils.Language.ENGLISH: ["Play", "Choose profile", "Controls", "Options", "Exit"]}
BG_ITEMS = [("Desert", 0)]
MUSIC_TRACK_ITEMS = [("Bells Song", 0)]
FADE_MS = 1
FPS = 60
# benchmark screen: 2560x1440
BUTTON_AREA_START = (36, 267)
# BUTTON_AREA_SIZE = (424, 369)
BUTTON_AREA_SIZE = (520, 369)
BUTTON_HEIGHT = 50
OPTIONS_TOP_MARGIN = 13
MENU_AREA_START = (0.01, 0.3)
# MENU_AREA_SIZE = (0.2, 1 - 2 * MENU_AREA_START[1])
MENU_SIDE_BAR_SIZE = (0.1, 1)
# BUTTON_SIZE = (1, 0.15)
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


# ----- Methods ------
def wdg_set_background(widget: pygame_menu.widgets.Widget, bg_color, trg_size: (int, int)) -> None:
    """Set the background for the given widget to the given bg_color and inflate it to the given trg_size"""
    widget.set_background_color(bg_color)
    delta = utils.subtract_tuples_int(trg_size, widget.get_size())
    delta = (max(delta[0], 0), max(delta[1], 0))
    widget.set_background_color(bg_color, delta)


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


# def init_submenu_options(widget_area_size: (int, int), widgets_offset: (int, int), music_volume: float, sound_volume: float):
# 	"""
# 	Initialize the submenu for the options.
#
# 	:param widget_area_size: Size of the widget area
# 	:param widgets_offset: Absolute offset of the topleft corner of the first widget
# 	"""
# 	menu_theme = pygame_menu.Theme(background_color=(0, 0, 0, 0), title=False, widget_alignment=pygame_menu.locals.ALIGN_CENTER, widget_font=button_font, widget_font_antialias=True, widget_font_color=WHITE)
# 	submenu_options = pygame_menu.Menu("Options", widget_area_size[0], widget_area_size[1], position=(widgets_offset[0], widgets_offset[1], False), enabled=False, theme=menu_theme)
# 	slider_music_vol = submenu_options.add.range_slider("Music volume:", music_volume, (0, 1), 0.01, rangeslider_id="MusicVolumeSlider", range_text_value_enabled=False, slider_text_value_enabled=False, value_format=lambda x: str(int(x * 100)), onchange=change_music_volume)
# 	slider_sound_vol = submenu_options.add.range_slider("Sound volume:", sound_volume, (0, 1), 0.01, rangeslider_id="SoundVolumeSlider", range_text_value_enabled=False, slider_text_value_enabled=False, value_format=lambda x: str(int(x * 100)), onchange=change_sound_volume)
# 	sel_music_track = submenu_options.add.dropselect("Music Track:", MUSIC_TRACK_ITEMS, default=0, placeholder=MUSIC_TRACK_ITEMS[0][0], placeholder_add_to_selection_box=False)
# 	sel_bg = submenu_options.add.dropselect("Background:", BG_ITEMS, default=0, placeholder=BG_ITEMS[0][0], placeholder_add_to_selection_box=False)
# 	button_back = submenu_options.add.button("Back", click_on_back_button)
# 	for wdg in [slider_music_vol, slider_sound_vol, sel_music_track, sel_bg, button_back]:
# 		wdg.set_padding(0)
# 		wdg.set_onmouseover(mouse_over_widget)
# 		wdg.set_onmouseleave(mouse_leave_widget)
# 		wdg.set_selection_effect()
# 		wdg.set_font(button_font, int(BUTTON_FONT_SIZE * scaling_factor), WHITE, WHITE, WHITE, WHITE, None, True)
# 		if wdg is button_back:
# 			wdg_set_background(wdg, button_base_imgs[WidgetState.NORMAL], button_size)
# 		else:
# 			wdg_set_background(wdg, COLOR_WIDGETS[WidgetState.NORMAL], button_size)
# 			wdg.set_border(0, WHITE)
# 	options_texts = ["Music volume: ", "Sound volume: ", "Music Track: ", "Background: "]
# 	options_widgets = [slider_music_vol, slider_sound_vol, sel_music_track, sel_bg]
# 	block_height = button_size[1] + free_space
# 	options_frame = submenu_options.add.frame_v(widget_area_size[0], 5 * block_height + OPTIONS_TOP_MARGIN, padding=0)
# 	options_frame.pack(submenu_options.add.vertical_margin(OPTIONS_TOP_MARGIN))
# 	for wdg in options_widgets:
# 		options_frame.pack(wdg, align=pygame_menu.locals.ALIGN_CENTER)
# 		options_frame.pack(submenu_options.add.vertical_margin(0.875 * block_height - wdg.get_height()))
# 	options_frame.pack(submenu_options.add.vertical_margin(0.5 * block_height))
# 	options_frame.pack(button_back, align=pygame_menu.locals.ALIGN_CENTER)
# 	submenu_options.resize(options_frame.get_width(), options_frame.get_height())
# 	submenu_options_pos = submenu_options.get_position()
# 	return submenu_options
@dataclass
class MyRangeSlider:
    """Class for customizable range slider parameters"""
    title: str
    default: float
    onchange: Callable


@dataclass
class MyDropSelect:
    """Class for customizable drop select parameters"""
    title: str
    items: [(str, int)]
    onchange: Callable


@dataclass
class MyButton:
    """Class for customizable button parameters"""
    title: str
    action: Callable


class Menu:
    """Class for the menu in the game"""
    def __init__(self, main_surface: pygame.Surface, rect: pygame.Rect, bg_img: pygame.Surface = None, scaling_factor: float = None, lang: utils.Language = utils.Language.ENGLISH):
        """
        Initialize the menu.

        :param main_surface: Surface to draw the menu onto
        :param rect: Rectangle for the menu (positioned w.r.t. the main surface)
        :param bg_img: Image to be used as the background of the menu
        :param scaling_factor: Factor for scaling positions and sizes from the benchmark screen to the actual screen
        """
        self.main_surface = main_surface
        self.start_game = False
        self.exit = False
        self.lang = lang
        self.button_texts = TEXTS_BUTTON[self.lang]
        self.snake_names = ["Kokosnuss", "Tiger", "Muh", "Mausi"]
        self.snake_colors = [GREEN, BLUE, CYAN, PINK]
        self.snake_controls = [["↑", "←", "↓", "→"], ["W", "A", "S", "D"], ["8", "4", "5", "6"], ["I", "J", "K", "L"]]
        self.level = 0
        usable_rect = pygame.rect.Rect(int((1 - MAP_TO_SCREEN_RATIO) * self.main_surface.get_width() / 2),
                                       int((1 - MAP_TO_SCREEN_RATIO) * self.main_surface.get_height() / 2),
                                       MAP_TO_SCREEN_RATIO * self.main_surface.get_width(),
                                       MAP_TO_SCREEN_RATIO * self.main_surface.get_height())
        self.scaling_factor = scaling_factor if scaling_factor else main_surface.get_height() / BENCHMARK_HEIGHT
        # Background
        # self.bg_img = pygame.transform.scale(pygame.image.load(FILENAME_BG).convert_alpha(), self.main_surface.get_size())
        self.bg_img = bg_img
        # Initialize the menu - 1st, define all the areas, rects, images, etc.
        #   Menu area
        # self.menu_rect = pygame.Rect(utils.mult_tuple_to_int(MENU_FRAME_START, self.scaling_factor), utils.mult_tuple_to_int(MENU_FRAME_SIZE, self.scaling_factor))
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
        self.button_size = (self.buttons_area_rect.w, self.scaling_factor * BUTTON_HEIGHT)
        free_space = int((self.buttons_area_rect.h - num_buttons * self.button_size[1]) / (num_buttons - 1))
        self.button_rects = [pygame.Rect((0, i * (self.button_size[1] + free_space)), self.button_size) for i in range(num_buttons)]
        self.button_imgs_orig = {state: pygame.image.load(FILENAMES_BUTTON[state]).convert_alpha() for state in WidgetState}
        self.button_imgs = {state: pygame.transform.scale(img_orig, self.button_size) for state, img_orig in self.button_imgs_orig.items()}
        self.button_base_imgs = {state: pygame_menu.BaseImage(image_path=FILENAMES_BUTTON[state], drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL) for state in WidgetState}
        #   Texts for the buttons
        self.button_font = pygame.font.SysFont("Snake Chan", int(BUTTON_FONT_SIZE * self.scaling_factor))
        self.button_texts_rend = [self.button_font.render(text, True, WHITE) for text in self.button_texts]
        #   2nd, define the sprites for the objects
        self.on_click_functions = [self.click_on_new_game_button, self.click_on_profile_button, self.click_on_controls_button, self.click_on_options_button, self.click_on_exit_button]
        self.buttons = [Clickable(self.button_imgs[WidgetState.NORMAL], rect, func) for rect, func in zip(self.button_rects, self.on_click_functions)]
        self.button_group = ClickableGroup(*self.buttons)
        self.music_volume = pygame.mixer_music.get_volume()
        self.sound_volume = 1.0
        self.cur_track_idx = 0
        self.cur_bg_idx = 0
        self.clock = pygame.time.Clock()
        # Submenu Options
        self.submenu_options = self.init_submenu_options()
        self.submenu_controls = self.init_submenu_controls()
        self.mini_menu_change_controls = self.init_mini_menu_change_controls()
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
        # # LEVEL SELECT AREA
        # self.level_previews = [pygame.transform.scale(pygame.image.load(FILENAME_ROOT_LVL_PREV.format(str(i))).convert_alpha(), ) for i in range(1)]
        # rest
        # self.clock = pygame.time.Clock()
        # self.play_music_track(0)
        # self.main_surface.blit(self.bg_img, (0, 0))
        # msg_font = pygame.font.SysFont("Snake Chan", 40)
        # msg_rendered = msg_font.render("Press any key", True, WHITE)
        # self.main_surface.blit(msg_rendered, msg_rendered.get_rect(center=(self.main_surface.get_rect().centerx, 0.95 * self.main_surface.get_height())))
        # pygame.display.update()

    def init_submenu_options(self) -> pygame_menu.Menu:
        """Initialize and return the submenu for the options."""
        # self.menu_base_image = pygame_menu.BaseImage(image_path=FILENAME_MENU_FRAME, drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL)
        my_widgets = [MyRangeSlider("Music volume", self.music_volume, self.change_music_volume),
                      MyRangeSlider("Sound volume", self.sound_volume, self.change_sound_volume),
                      MyDropSelect("Music Track", MUSIC_TRACK_ITEMS, self.change_music_track),
                      MyDropSelect("Background", BG_ITEMS, self.change_background)]
        menu_theme = pygame_menu.Theme(background_color=(0, 0, 0, 0), title=False, widget_alignment=pygame_menu.locals.ALIGN_CENTER, widget_font=self.button_font, widget_font_antialias=True, widget_font_color=WHITE)
        buttons_offset = self.buttons_surf.get_abs_offset()
        submenu_options = pygame_menu.Menu("Options", self.buttons_area_rect.w, self.buttons_area_rect.h, position=(buttons_offset[0], buttons_offset[1], False), enabled=False, theme=menu_theme)
        free_space = int((self.buttons_area_rect.h - (len(my_widgets) + 1) * self.button_size[1]) / len(my_widgets))
        block_height = self.button_size[1] + free_space
        options_frame = submenu_options.add.frame_v(self.buttons_area_rect.w, 5 * block_height + OPTIONS_TOP_MARGIN, padding=0)
        options_frame.pack(submenu_options.add.vertical_margin(OPTIONS_TOP_MARGIN))
        red_block_rate = 0.875
        red_block_height = red_block_rate * block_height
        for my_wdg in my_widgets:
            if isinstance(my_wdg, MyRangeSlider):
                cur_wdg = submenu_options.add.range_slider(my_wdg.title, my_wdg.default, (0, 1), 0.01, rangeslider_id=my_wdg.title, range_text_value_enabled=False, slider_text_value_enabled=False, value_format=lambda x: str(int(x * 100)), onchange=my_wdg.onchange)
            elif isinstance(my_wdg, MyDropSelect):
                cur_wdg = submenu_options.add.dropselect(my_wdg.title, my_wdg.items, default=0, placeholder=my_wdg.items[0][0], placeholder_add_to_selection_box=False, onchange=my_wdg.onchange)
            elif isinstance(my_wdg, MyButton):
                cur_wdg = submenu_options.add.button(my_wdg.title, my_wdg.action)
            else:
                raise TypeError(f"Expected one of [MyRangeSlider, MyDropSelect, MyButton], got {type(my_wdg)} instead")
            cur_wdg = self.set_std_params(cur_wdg)
            options_frame.pack(cur_wdg, align=pygame_menu.locals.ALIGN_CENTER)
            options_frame.pack(submenu_options.add.vertical_margin(red_block_height - cur_wdg.get_height()))
        options_frame.pack(submenu_options.add.vertical_margin((1 - red_block_rate) * len(my_widgets) * block_height))
        options_frame.pack(self.set_std_params(submenu_options.add.button("Back", self.click_on_back_button)), align=pygame_menu.locals.ALIGN_CENTER)
        submenu_options.resize(options_frame.get_width(), options_frame.get_height())
        return submenu_options

    def set_std_params(self, wdg: pygame_menu.widgets.Widget) -> pygame_menu.widgets.Widget:
        """Set some standard parameters for the given widget and return it"""
        wdg.set_padding(0)
        wdg.set_onmouseover(self.mouse_over_widget)
        wdg.set_onmouseleave(self.mouse_leave_widget)
        wdg.set_selection_effect()
        wdg.set_font(self.button_font, int(BUTTON_FONT_SIZE * self.scaling_factor), WHITE, WHITE, WHITE, WHITE, None, True)
        if isinstance(wdg, pygame_menu.widgets.Button):
            wdg_set_background(wdg, self.button_base_imgs[WidgetState.NORMAL], self.button_size)
        else:
            wdg_set_background(wdg, COLOR_WIDGETS[WidgetState.NORMAL], self.button_size)
        return wdg

    def init_submenu_controls(self) -> pygame_menu.Menu:
        """Initialize and return the submenu for the controls"""
        menu_theme = pygame_menu.Theme(background_color=(0, 0, 0, 0), title=False, widget_alignment=pygame_menu.locals.ALIGN_CENTER, widget_font=pygame.font.SysFont("segoeuisymbol", int(BUTTON_FONT_SIZE * self.scaling_factor)), widget_font_antialias=True, widget_font_color=WHITE)
        buttons_offset = self.buttons_surf.get_abs_offset()
        submenu_controls = pygame_menu.Menu("Controls", self.menu_rect.w, self.menu_rect.h, position=(buttons_offset[0], buttons_offset[1], False), enabled=False, theme=menu_theme)
        main_frame = submenu_controls.add.frame_v(submenu_controls.get_width(), submenu_controls.get_height(), padding=0)
        cols_frame = submenu_controls.add.frame_h(main_frame.get_width(), 0.8 * main_frame.get_height(), padding=0)
        rows_frames = [submenu_controls.add.frame_v(int(cols_frame.get_width() / 5), cols_frame.get_height(), padding=0) for _ in range(4)]
        first_col = submenu_controls.add.frame_v(int(cols_frame.get_width() / 5), cols_frame.get_height(), padding=0)
        for idx, text in enumerate(["Player", "Up", "Down", "Left", "Right", ""]):
            label = submenu_controls.add.label(text)
            row_height = label.get_height()
            help_frame = self.set_help_frame_around_wdg(submenu_controls, label, (first_col.get_width(), row_height))
            # help_frame = submenu_controls.add.frame_h(first_col.get_width(), row_height, padding=0)
            # help_frame.pack(label, align=pygame_menu.locals.ALIGN_CENTER)
            # help_frame.set_border(1, WHITE)
            first_col.pack(help_frame, align=pygame_menu.locals.ALIGN_CENTER)
        cols_frame.pack(first_col, align=pygame_menu.locals.ALIGN_CENTER)
        for snake_id, (frame, controls, name) in enumerate(zip(rows_frames, self.snake_controls, self.snake_names)):
            name_entry = submenu_controls.add.text_input("", default=name, maxchar=0, maxwidth=8)
            self.set_std_params_controls(name_entry)
            help_frame = self.set_help_frame_around_wdg(submenu_controls, name_entry, (frame.get_width(), row_height))
            # help_frame = submenu_controls.add.frame_v(frame.get_width(), row_height, padding=0)
            # help_frame.pack(name_entry, align=pygame_menu.locals.ALIGN_CENTER)
            # help_frame.set_border(1, WHITE)
            frame.pack(help_frame, align=pygame_menu.locals.ALIGN_CENTER)
            # button = submenu_controls.add.button(name, self.change_control, accept_kwargs=True, snake_id=snake_id)
            # self.set_std_params(button)
            # frame.pack(button, align=pygame_menu.locals.ALIGN_CENTER)
            for key_id, key in enumerate(controls):
                # key_entry = submenu_controls.add.text_input("", default=key, maxchar=1, maxwidth=10)
                # self.set_std_params_controls(key_entry)
                label = submenu_controls.add.label(key, label_id=f"Widget{key_id + 1}{snake_id + 1}")
                help_frame = self.set_help_frame_around_wdg(submenu_controls, label, (frame.get_width(), row_height))
                # help_frame = submenu_controls.add.frame_v(frame.get_width(), row_height, padding=0)
                # help_frame.pack(label, align=pygame_menu.locals.ALIGN_CENTER)
                # help_frame.set_border(1, WHITE)
                frame.pack(help_frame, align=pygame_menu.locals.ALIGN_CENTER)
                # button = submenu_controls.add.button(key, self.change_control, accept_kwargs=True, snake_id=snake_id, dir_id=dir_id, key=key)
                # self.set_std_params(button)
                # frame.pack(button, align=pygame_menu.locals.ALIGN_CENTER)
            change_button = submenu_controls.add.button("Change", action=self.change_controls, accept_kwargs=True, snake_id=snake_id)
            help_frame = self.set_help_frame_around_wdg(submenu_controls, change_button, (frame.get_width(), row_height))
            frame.pack(help_frame, align=pygame_menu.locals.ALIGN_CENTER)
            cols_frame.pack(frame, align=pygame_menu.locals.ALIGN_CENTER)
        main_frame.pack(cols_frame, align=pygame_menu.locals.ALIGN_CENTER)
        main_frame.pack(self.set_std_params(submenu_controls.add.button("Back", self.click_on_back_button)), align=pygame_menu.locals.ALIGN_CENTER)
        submenu_controls.resize(main_frame.get_width(), main_frame.get_height())
        return submenu_controls

    def set_help_frame_around_wdg(self, menu: pygame_menu.Menu, wdg: pygame_menu.widgets.Widget, size: (int, int)) -> pygame_menu.widgets.Frame:
        """Set a frame containing just the single widget and add it to the menu"""
        help_frame = menu.add.frame_v(size[0], size[1], padding=0)
        help_frame.pack(wdg, align=pygame_menu.locals.ALIGN_CENTER)
        help_frame.set_border(1, WHITE)
        return help_frame

    def set_std_params_controls(self, wdg: pygame_menu.widgets.Widget) -> pygame_menu.widgets.Widget:
        """Set some standard parameters for the given widget and return it"""
        wdg.set_padding(0)
        # wdg.set_onmouseover(self.mouse_over_widget)
        # wdg.set_onmouseleave(self.mouse_leave_widget)
        wdg.set_selection_effect()
        # wdg.set_font(self.button_font, int(BUTTON_FONT_SIZE * self.scaling_factor), WHITE, WHITE, WHITE, WHITE, None, True)
        return wdg

    def init_mini_menu_change_controls(self) -> pygame_menu.Menu:
        """Initialize the mini submenu for changing a snakes controls"""
        menu_theme = pygame_menu.Theme(background_color=(0, 0, 0, 0), title=False, widget_alignment=pygame_menu.locals.ALIGN_CENTER, widget_font=pygame.font.SysFont("segoeuisymbol", int(BUTTON_FONT_SIZE * self.scaling_factor)), widget_font_antialias=True, widget_font_color=WHITE)
        mini_menu = pygame_menu.Menu("Change Controls", 500, 500, position=(500, 500, False), enabled=False, theme=menu_theme)
        label = mini_menu.add.label("", label_id="TextLabel")
        return mini_menu

    def reset(self):
        """Reset menu"""
        self.start_game = False
        self.exit = False
        self.bg_img = None
        self.music_volume = pygame.mixer_music.get_volume()
        self.submenu_options.get_widget("Music volume").set_default_value(self.music_volume)

    def slide_in(self) -> None:
        """Slide the menu in from the left edge"""
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
        """Handle the events in the start menu. Returns True if the user starts a new game or False if they want to exit"""
        button_pushed = False
        while not self.start_game and not self.exit:
            events = pygame.event.get()
            if self.submenu_options.is_enabled():
                self.submenu_options.update(events)
            elif self.submenu_controls.is_enabled():
                self.submenu_controls.update(events)
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
        return self.start_game

    # def handle_submenu_options(self):
    #     """Handle the submenu for the options"""
    #     self.submenu_options.enable()
        # menu = pygame_menu.Menu("Options", self.menu_rect.w, self.menu_rect.h, theme=pygame_menu.themes.THEME_BLUE)
        # menu.add.text_input("Name: ", default="Kokosnuss")
        # menu.add.range_slider("Music volume", 100, (0, 100), 1, rangeslider_id="MusicVolumeSlider", value_format=lambda x: str(int(x)), onchange=self.change_music_volume)
        # menu.add.button("Back", pygame_menu.events.CLOSE)
        # menu.mainloop(self.menu_surf)
        # pass

    def change_controls(self, **kwargs) -> None:
        """Change keys for controlling a snake"""
        snake_id = kwargs["snake_id"]
        self.submenu_controls.disable()
        self.mini_menu_change_controls.enable()
        directions = ["Up", "Down", "Left", "Right"]
        keys = []
        label = self.mini_menu_change_controls.get_widget("TextLabel")
        for direction in directions:
            label.set_title(f"Player {snake_id + 1}: Press key for <{direction}>")
            self.set_std_params(label)
            self.update_display()
            pressed_key = False
            while not pressed_key:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and (char := utils.get_char_for_pygame_key(event.key)):
                        keys.append(char)
                        pressed_key = True
        self.snake_controls[snake_id] = keys
        self.update_submenu_controls(snake_id)
        self.mini_menu_change_controls.disable()
        self.submenu_controls.enable()

    def update_submenu_controls(self, snake_id: int) -> None:
        """Update the key representation in the controls submenu when new controls for a snake got defined"""
        for key_id, key in enumerate(self.snake_controls[snake_id]):
            self.submenu_controls.get_widget(f"Widget{key_id + 1}{snake_id + 1}").set_title(key)

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
        self.submenu_controls.enable()

    def click_on_options_button(self) -> None:
        self.submenu_options.enable()

    def click_on_exit_button(self) -> None:
        """Exit the application"""
        self.start_game = False
        self.exit = True

    def click_on_back_button(self, *args, **kwargs) -> None:
        for submenu in [self.submenu_options, self.submenu_controls]:
            submenu.disable()

    def mouse_over_widget(self, widget: pygame_menu.widgets.Widget, event: pygame.event.Event) -> None:
        """Handle a mouseover on the given widget"""
        bg_color = self.button_base_imgs[WidgetState.HOVERED] if isinstance(widget, pygame_menu.widgets.Button) else COLOR_WIDGETS[WidgetState.HOVERED]
        wdg_set_background(widget, bg_color, self.button_size)
        widget.select(True, True)

    def mouse_leave_widget(self, widget: pygame_menu.widgets.Widget, event: pygame.event.Event) -> None:
        """Handle a mouse leave on the given widget"""
        bg_color = self.button_base_imgs[WidgetState.NORMAL] if isinstance(widget, pygame_menu.widgets.Button) else COLOR_WIDGETS[WidgetState.NORMAL]
        wdg_set_background(widget, bg_color, self.button_size)

    def change_music_track(self, sel_item_and_index, sel_value, **kwargs) -> None:
        utils.play_music_track(FILENAMES_MUSIC_TRACKS[sel_value], self.music_volume)
        self.cur_track_idx = sel_value

    def change_background(self, sel_item_and_index, sel_value, **kwargs) -> None:
        pass

    def update_display(self) -> None:
        """Display the current state on the screen"""
        if self.bg_img:
            self.main_surface.blit(self.bg_img, (0, 0))
        else:
            self.main_surface.fill(BG_COLOR)
        if self.submenu_options.is_enabled():
            self.submenu_options.draw(self.main_surface)
        elif self.submenu_controls.is_enabled():
            self.submenu_controls.draw(self.main_surface)
        elif self.mini_menu_change_controls.is_enabled():
            self.mini_menu_change_controls.draw(self.main_surface)
        else:
            self.button_group.draw(self.buttons_surf)
            for rect, text in zip(self.button_rects, self.button_texts_rend):
                self.buttons_surf.blit(text, text.get_rect(center=rect.center))
        self.main_surface.blit(self.menu_frame_img, self.menu_rect)

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
        # pygame.display.update(self.menu_rect)
        pygame.display.update()
