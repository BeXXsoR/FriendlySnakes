"""Classes for all the menus in the game"""

# import utils
from enum import Enum
from dataclasses import dataclass
from typing import Callable, Union
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
# FILENAMES_SNAKE = {GREEN: "../res/menu_snake_green.png", BLUE: "../res/menu_snake_blue.png",
#                    CYAN: "../res/menu_snake_cyan.png", PINK: "../res/menu_snake_pink.png"}
FILENAME_LVL_PREV = "../res/level_prev_{}.png"
FILENAME_MENU_FRAME = "../res/menu_frame.png"
FILENAMES_BUTTON = {WidgetState.NORMAL: "../res/menu_button_normal.png", WidgetState.PUSHED: "../res/menu_button_pushed.png", WidgetState.HOVERED: "../res/menu_button_hovered.png"}
COLOR_WIDGETS = {WidgetState.NORMAL: (76, 123, 209), WidgetState.HOVERED: (111, 164, 255)}
BG_ITEMS = [("Desert", 0)]
MUSIC_TRACK_ITEMS = [("Bells Song", 0)]
NUM_PLAYER_ITEMS = [("1", 1), ("2", 2), ("3", 3), ("4", 4)]
LEVEL_PREV_IMG_ID = "Level_Prev_Img"
FPS = 60
# benchmark screen: 2560x1440
BUTTON_AREA_START = (36, 267)
BUTTON_AREA_SIZE = (520, 370)
BUTTON_HEIGHT = 50
OPTIONS_TOP_MARGIN = 13
MENU_AREA_START = (0.01, 0.3)
BUTTON_FONT_SIZE = 25
LEVEL_PREV_IMG_SIZE = (200, 200)
# endregion


# ----- Methods ------
def wdg_set_background(widget: pygame_menu.widgets.Widget, bg_color, trg_size: (int, int) = None) -> None:
    """Set the background for the given widget to the given bg_color and inflate it to the given trg_size"""
    if trg_size:
        widget.set_background_color(bg_color)
        delta = utils.subtract_tuples_int(trg_size, widget.get_size())
        delta = (max(delta[0], 0), max(delta[1], 0))
        widget.set_background_color(bg_color, delta)
    else:
        widget.set_background_color(bg_color, inflate=None)


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


@dataclass
class MySelector:
    """Class for customizable selector parameters"""
    title: str
    items: [(str, int)]
    default: int
    onchange: Callable


MyWidget = Union[MyRangeSlider, MyDropSelect, MyButton, MySelector]


class Menu:
    """Class for the menu in the game"""
    def __init__(self, main_surface: pygame.Surface, rect: pygame.Rect, bg_img: pygame.Surface = None, scaling_factor: float = None,
                 lang: utils.Language = utils.Language.ENGLISH, button_texts: [str] = None, level_names: [str] = None):
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
        self.num_players = 2
        self.level_idx = 0
        self.button_texts = button_texts if button_texts else TEXTS_BUTTON_START_MENU[self.lang]
        # self.snake_names = ["Kokosnuss", "Tiger", "Muh", "Mausi"]
        self.snake_names = ["Ko", "Ti", "Mu", "Ma"]
        self.snake_colors = [GREEN, BLUE, CYAN, PINK]
        self.snake_controls = [["↑", "←", "↓", "→"], ["W", "A", "S", "D"], ["8", "4", "5", "6"], ["I", "J", "K", "L"]]
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
        self.on_click_functions = [self.click_on_play_button, self.click_on_profile_button, self.click_on_controls_button, self.click_on_options_button, self.click_on_exit_button]
        self.buttons = [Clickable(self.button_imgs[WidgetState.NORMAL], rect, func) for rect, func in zip(self.button_rects, self.on_click_functions)]
        self.button_group = ClickableGroup(*self.buttons)
        self.music_volume = pygame.mixer_music.get_volume()
        self.sound_volume = 1.0
        self.cur_track_idx = 0
        self.cur_bg_idx = 0
        self.clock = pygame.time.Clock()
        # Submenu Options
        self.submenu_options = self.init_submenu_options()
        # self.submenu_controls = self.init_submenu_controls()
        self.submenu_controls = self.init_submenu_options()
        self.level_prev_imgs = None
        self.submenu_levels = None
        if level_names:
            trg_w, trg_h = utils.mult_tuple_to_int(LEVEL_PREV_IMG_SIZE, self.scaling_factor)
            self.level_prev_imgs = [pygame_menu.BaseImage(image_path=FILENAME_LVL_PREV.format(i), drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL).resize(trg_w, trg_h) for i in range(len(level_names))]
            self.submenu_levels = self.init_submenu_level_selection(level_names)
        self.mini_menu_change_controls = self.init_mini_menu_change_controls()

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
        top_margin = OPTIONS_TOP_MARGIN * self.scaling_factor
        options_frame = submenu_options.add.frame_v(self.buttons_area_rect.w, int(5 * block_height + top_margin), padding=0)
        options_frame.pack(submenu_options.add.vertical_margin(top_margin))
        red_block_rate = 0.875
        red_block_height = red_block_rate * block_height
        for my_wdg in my_widgets:
            cur_wdg = self.add_widget_from_mywidget(my_wdg, submenu_options, self.button_size)
            options_frame.pack(cur_wdg, align=pygame_menu.locals.ALIGN_CENTER)
            options_frame.pack(submenu_options.add.vertical_margin(red_block_height - cur_wdg.get_height()))
        options_frame.pack(submenu_options.add.vertical_margin((1 - red_block_rate) * len(my_widgets) * block_height))
        options_frame.pack(self.set_std_params(submenu_options.add.button("Back", self.click_on_back_button), self.button_size), align=pygame_menu.locals.ALIGN_CENTER)
        submenu_options.resize(options_frame.get_width(), options_frame.get_height())
        return submenu_options

    def init_submenu_controls(self) -> pygame_menu.Menu:
        """Initialize and return the submenu for the controls"""
        font = pygame.font.SysFont("segoeuisymbol", int(BUTTON_FONT_SIZE * self.scaling_factor))
        menu_theme = pygame_menu.Theme(background_color=(0, 0, 0, 0), title=False, widget_alignment=pygame_menu.locals.ALIGN_CENTER, widget_font=font, widget_font_antialias=True, widget_font_color=WHITE)
        buttons_offset = self.buttons_surf.get_abs_offset()
        submenu_controls = pygame_menu.Menu("Controls", self.buttons_area_rect.w, self.buttons_area_rect.h, position=(buttons_offset[0], buttons_offset[1], False), enabled=False, theme=menu_theme)
        main_frame = submenu_controls.add.frame_v(submenu_controls.get_width(), submenu_controls.get_height(), padding=0)
        cols_frame = submenu_controls.add.frame_h(main_frame.get_width(), 0.9 * main_frame.get_height(), padding=0)
        rows_frames = [submenu_controls.add.frame_v(int(cols_frame.get_width() / 5), cols_frame.get_height(), padding=0) for _ in range(4)]
        first_col = submenu_controls.add.frame_v(int(cols_frame.get_width() / 5), cols_frame.get_height(), padding=0)
        margin = 20
        for text in ["Player", "Up", "Left", "Down", "Right"]:
            label = submenu_controls.add.label(text, padding=0)
            row_height = label.get_height()
            self.set_std_params(label, (first_col.get_width(), row_height), font=font, enable_mouse_over_leave=False)
            help_frame = self.set_help_frame_around_wdg(submenu_controls, label, (first_col.get_width(), row_height))
            first_col.pack(help_frame, align=pygame_menu.locals.ALIGN_CENTER)
            if text == "Player":
                first_col.pack(submenu_controls.add.vertical_margin(margin))
        cols_frame.pack(first_col, align=pygame_menu.locals.ALIGN_CENTER)
        for snake_id, (frame, controls, name) in enumerate(zip(rows_frames, self.snake_controls, ["Pl. 1", "Pl. 2", "Pl. 3", "Pl. 4"])):
            label = submenu_controls.add.label(name, padding=0)
            self.set_std_params(label, (frame.get_width(), row_height), font=font)
            help_frame = self.set_help_frame_around_wdg(submenu_controls, label, (frame.get_width(), row_height))
            frame.pack(help_frame, align=pygame_menu.locals.ALIGN_CENTER)
            frame.pack(submenu_controls.add.vertical_margin(margin))
            for key_id, key in enumerate(controls):
                label = submenu_controls.add.label(key, label_id=f"Widget{key_id + 1}{snake_id + 1}")
                self.set_std_params(label, (frame.get_width(), row_height), font=font, enable_mouse_over_leave=False)
                help_frame = self.set_help_frame_around_wdg(submenu_controls, label, (frame.get_width(), row_height))
                frame.pack(help_frame, align=pygame_menu.locals.ALIGN_CENTER)
            change_button = submenu_controls.add.button("Change", action=self.change_controls, accept_kwargs=True, snake_id=snake_id)
            self.set_std_params(change_button, (frame.get_width(), row_height), font=font)
            help_frame = self.set_help_frame_around_wdg(submenu_controls, change_button, (frame.get_width(), row_height))
            frame.pack(submenu_controls.add.vertical_margin(margin))
            frame.pack(help_frame, align=pygame_menu.locals.ALIGN_CENTER)
            cols_frame.pack(frame, align=pygame_menu.locals.ALIGN_CENTER)
        main_frame.pack(cols_frame, align=pygame_menu.locals.ALIGN_CENTER)
        main_frame.pack(self.set_std_params(submenu_controls.add.button("Back", self.click_on_back_button), self.button_size), align=pygame_menu.locals.ALIGN_CENTER)
        submenu_controls.resize(main_frame.get_width(), main_frame.get_height())
        return submenu_controls

    def init_submenu_level_selection(self, level_names: [str]) -> pygame_menu.Menu:
        """Init the submenu for the level and player number selection screen"""
        font = pygame.font.SysFont("segoeuisymbol", int(BUTTON_FONT_SIZE * self.scaling_factor))
        menu_theme = pygame_menu.Theme(background_color=(0, 0, 0, 0), title=False, widget_alignment=pygame_menu.locals.ALIGN_CENTER, widget_font=font, widget_font_antialias=True, widget_font_color=WHITE)
        buttons_offset = self.buttons_surf.get_abs_offset()
        submenu_levels = pygame_menu.Menu("Level Selection", self.buttons_area_rect.w, self.buttons_area_rect.h, position=(buttons_offset[0], buttons_offset[1], False), enabled=False, theme=menu_theme)
        main_frame = submenu_levels.add.frame_v(submenu_levels.get_width(), submenu_levels.get_height(), padding=0)
        play_button = self.add_widget_from_mywidget(MyButton("Play", self.start_new_game), submenu_levels, self.button_size)
        sel_num_players = self.add_widget_from_mywidget(MyDropSelect("Number Of Players:", NUM_PLAYER_ITEMS, self.change_num_players), submenu_levels, self.button_size)
        level_items = [(name, idx) for idx, name in enumerate(level_names)]
        sel_level = self.add_widget_from_mywidget(MySelector("Level:", level_items, self.level_idx, self.change_level), submenu_levels, self.button_size)
        level_img = submenu_levels.add.image(self.level_prev_imgs[self.level_idx], image_id=LEVEL_PREV_IMG_ID)
        back_button = self.add_widget_from_mywidget(MyButton("Back", self.start_new_game), submenu_levels, self.button_size)
        for wdg in [play_button, sel_num_players, sel_level, level_img, back_button]:
            main_frame.pack(wdg, align=pygame_menu.locals.ALIGN_CENTER)
            # main_frame.pack(submenu_levels.add.vertical_margin(20))
        return submenu_levels

    def add_widget_from_mywidget(self, my_wdg: MyWidget, menu: pygame_menu.Menu, trg_size: (int, int)) -> pygame_menu.widgets.Widget:
        """
        Add a pygame widget to the menu based on the information in my_wdg

        :param my_wdg: The MyWidget object containing the information for the widget
        :param menu: The menu to add the widget to
        :return: The widget that was added to the menu
        """
        if isinstance(my_wdg, MyRangeSlider):
            wdg = menu.add.range_slider(my_wdg.title, my_wdg.default, (0, 1), 0.01, rangeslider_id=my_wdg.title, range_text_value_enabled=False, slider_text_value_enabled=False, value_format=lambda x: str(int(x * 100)), onchange=my_wdg.onchange)
        elif isinstance(my_wdg, MyDropSelect):
            wdg = menu.add.dropselect(my_wdg.title, my_wdg.items, default=0, dropselect_id=my_wdg.title, placeholder=my_wdg.items[0][0], placeholder_add_to_selection_box=False, onchange=my_wdg.onchange)
        elif isinstance(my_wdg, MyButton):
            wdg = menu.add.button(my_wdg.title, my_wdg.action)
        elif isinstance(my_wdg, MySelector):
            wdg = menu.add.selector(my_wdg.title, my_wdg.items, my_wdg.default, selector_id=my_wdg.title, onchange=my_wdg.onchange, style=pygame_menu.widgets.SELECTOR_STYLE_CLASSIC)
        else:
            raise TypeError(f"Expected {type(MyWidget)}, got {type(my_wdg)} instead")
        wdg = self.set_std_params(wdg, trg_size)
        return wdg

    def set_std_params(self, wdg: pygame_menu.widgets.Widget, size: (int, int), font: pygame.font.Font = None, font_size: int = -1, enable_mouse_over_leave: bool = True) -> pygame_menu.widgets.Widget:
        """Set some standard parameters for the given widget and return it"""
        wdg.set_padding(0)
        if enable_mouse_over_leave:
            wdg.set_onmouseover(self.mouse_over_widget)
            wdg.set_onmouseleave(self.mouse_leave_widget)
        wdg.set_selection_effect()
        wdg.set_font(font if font else self.button_font, font_size if font_size > 0 else int(BUTTON_FONT_SIZE * self.scaling_factor), WHITE, WHITE, WHITE, WHITE, None, True)
        if isinstance(wdg, pygame_menu.widgets.Button):
            wdg_set_background(wdg, self.button_base_imgs[WidgetState.NORMAL], size)
        else:
            wdg_set_background(wdg, COLOR_WIDGETS[WidgetState.NORMAL], size)
        return wdg

    def set_help_frame_around_wdg(self, menu: pygame_menu.Menu, wdg: pygame_menu.widgets.Widget, size: (int, int)) -> pygame_menu.widgets.Frame:
        """Set a frame containing just the single widget and add it to the menu"""
        help_frame = menu.add.frame_v(size[0], size[1], padding=0)
        help_frame.pack(wdg, align=pygame_menu.locals.ALIGN_CENTER)
        help_frame.set_border(1, WHITE)
        return help_frame

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
            elif self.submenu_levels and self.submenu_levels.is_enabled():
                self.submenu_levels.update(events)
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

    def change_controls(self, **kwargs) -> None:
        """Change keys for controlling a snake"""
        snake_id = kwargs["snake_id"]
        self.submenu_controls.disable()
        self.mini_menu_change_controls.enable()
        directions = ["Up", "Left", "Down", "Right"]
        keys = []
        label = self.mini_menu_change_controls.get_widget("TextLabel")
        for direction in directions:
            label.set_title(f"Player {snake_id + 1}: Press key for <{direction}>")
            self.set_std_params(label, label.get_size())
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

    def start_new_game(self) -> None:
        """Start a new game"""
        self.exit = False
        self.start_game = True

    def click_on_play_button(self) -> None:
        """Start a new game"""
        if self.submenu_levels:
            self.submenu_levels.enable()
        else:
            self.start_new_game()

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
        wdg_set_background(widget, bg_color)
        widget.select(True, True)

    def mouse_leave_widget(self, widget: pygame_menu.widgets.Widget, event: pygame.event.Event) -> None:
        """Handle a mouse leave on the given widget"""
        bg_color = self.button_base_imgs[WidgetState.NORMAL] if isinstance(widget, pygame_menu.widgets.Button) else COLOR_WIDGETS[WidgetState.NORMAL]
        wdg_set_background(widget, bg_color)

    def change_music_track(self, sel_item_and_index, sel_value, **kwargs) -> None:
        utils.play_music_track(FILENAMES_MUSIC_TRACKS[sel_value], self.music_volume)
        self.cur_track_idx = sel_value

    def change_background(self, sel_item_and_index, sel_value, **kwargs) -> None:
        pass

    def change_num_players(self, sel_item_and_index, sel_value, **kwargs) -> None:
        """Change the number of players. Callback function for the resp. dropdown widget"""
        self.num_players = sel_value

    def change_level(self, sel_item_and_index, sel_value, **kwargs) -> None:
        """Change the level. Callback function for the resp. selector widget"""
        self.level_idx = sel_value
        wdg = self.submenu_levels.get_widget(LEVEL_PREV_IMG_ID)
        assert isinstance(wdg, pygame_menu.widgets.Image), f"Expected Image type, got {type(wdg)} instead."
        wdg.set_image(self.level_prev_imgs[self.level_idx])

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
        elif self.submenu_levels and self.submenu_levels.is_enabled():
            self.submenu_levels.draw(self.main_surface)
        elif self.mini_menu_change_controls.is_enabled():
            self.mini_menu_change_controls.draw(self.main_surface)
        else:
            self.button_group.draw(self.buttons_surf)
            for rect, text in zip(self.button_rects, self.button_texts_rend):
                self.buttons_surf.blit(text, text.get_rect(center=rect.center))
        self.main_surface.blit(self.menu_frame_img, self.menu_rect)
        pygame.display.update()
