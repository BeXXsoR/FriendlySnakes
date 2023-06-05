"""Module for the communicator class in the friendly snakes package"""

# ----- Imports --------
import utils
import json
from menu import Menu
from game import Game
from level import Level
from graphics import Graphics
from constants import *
import pygame

pygame.init()

# ----- Constants ------
FILENAME_LEVEL_INFO = "../res/levels.json"
FILENAME_ITEM_SOUNDS = {utils.Objects.APPLE: "../res/eat.ogg", utils.Objects.MELON: "../res/eat.ogg", utils.Objects.CHILI: "../res/eat.ogg",
                        utils.Objects.COFFEE: "../res/slurp.ogg", utils.Objects.TEA: "../res/slurp.ogg", utils.Objects.BEER: "../res/burp.ogg",
                        utils.Objects.BOMB: "../res/bomb.ogg", utils.Objects.EXPLOSION: "../res/explosion.ogg"}
FILENAME_CRASH_SOUND = "../res/crash.ogg"
UPDATE_SNAKES = [pygame.event.custom_type() for _ in range(4)]
REOCC_TIMER = pygame.event.custom_type()
START_MENU_TOPLEFT = (0, 300)
START_MENU_SIZE = (670, 705)
PAUSE_MENU_TOPLEFT = (0, 300)
PAUSE_MENU_SIZE = (670, 705)
FILENAME_START_BG = "../res/menu_bg.png"
FILENAME_PAUSE_MENU_BG = "../res/menu_bg.png"


# ----- Classes --------
class Communicator:
    """Class for interacting between different parts of the game, e.g. start menu and game engine"""

    def __init__(self):
        snake_names = ["Kokosnuss", "Tiger", "Muh", "Mausi"]
        snake_colors = [GREEN, BLUE, CYAN, PINK]
        snake_controls = [
            {pygame.K_UP: ORIENT_UP, pygame.K_LEFT: ORIENT_LEFT, pygame.K_DOWN: ORIENT_DOWN, pygame.K_RIGHT: ORIENT_RIGHT},
            {pygame.K_w: ORIENT_UP, pygame.K_a: ORIENT_LEFT, pygame.K_s: ORIENT_DOWN, pygame.K_d: ORIENT_RIGHT},
            {pygame.K_KP8: ORIENT_UP, pygame.K_KP4: ORIENT_LEFT, pygame.K_KP5: ORIENT_DOWN, pygame.K_KP6: ORIENT_RIGHT},
            {pygame.K_i: ORIENT_UP, pygame.K_j: ORIENT_LEFT, pygame.K_k: ORIENT_DOWN, pygame.K_l: ORIENT_RIGHT}]
        self.snake_controls_all = []
        for controls in snake_controls:
            self.snake_controls_all.extend(controls.keys())
        self.main_surface = pygame.display.set_mode((0, 0))
        self.lang = utils.Language.ENGLISH
        self.levels = []
        self.read_level_infos()
        self.level = self.levels[7]
        utils.play_music_track(FILENAMES_MUSIC_TRACKS[0], 0.1)
        self.scaling_factor = self.main_surface.get_height() / BENCHMARK_HEIGHT
        self.start_bg_img = pygame.transform.scale(pygame.image.load(FILENAME_START_BG).convert_alpha(), self.main_surface.get_size())
        self.start_menu = Menu(self.main_surface,
                               pygame.Rect(utils.mult_tuple_to_int(START_MENU_TOPLEFT, self.scaling_factor), utils.mult_tuple_to_int(START_MENU_SIZE, self.scaling_factor)),
                               self.start_bg_img,
                               self.scaling_factor,
                               self.lang)
        self.pause_menu = Menu(self.main_surface,
                               pygame.Rect(utils.mult_tuple_to_int(PAUSE_MENU_TOPLEFT, self.scaling_factor), utils.mult_tuple_to_int(PAUSE_MENU_SIZE, self.scaling_factor)),
                               None,
                               self.scaling_factor,
                               self.lang)
        self.set_start_screen()
        self.init_start_menu()
        # self.game = Game(snake_names, snake_colors, snake_controls, self.level, self.main_surface)
        self.game = Game(snake_names[:1], snake_colors[:1], snake_controls[:1], self.level, self.main_surface)
        # self.game = Game(snake_names[:2], snake_colors[:2], snake_controls[:2], self.level, self.main_surface)
        self.graphics = Graphics(self.main_surface, self.level.num_rows, self.level.num_cols)
        self.upd_snake_events = [pygame.event.Event(event_id, {"snake_idx": idx}) for idx, event_id in enumerate(UPDATE_SNAKES[:len(self.game.snakes)])]
        self.reocc_event = pygame.event.Event(REOCC_TIMER, {"duration": REOCC_DUR})
        self.item_sounds = {k: pygame.mixer.Sound(v) for k, v in FILENAME_ITEM_SOUNDS.items()}
        self.crash_sound = pygame.mixer.Sound(FILENAME_CRASH_SOUND)
        self.paused = False
        self.quit = False
        self.pause_start_time = 0
        self.paused_time = 0
        self.clock = pygame.time.Clock()

    def set_start_screen(self):
        self.main_surface.blit(self.start_bg_img, (0, 0))
        msg_font = pygame.font.SysFont("Snake Chan", 40)
        msg_rendered = msg_font.render("Press any key", True, WHITE)
        self.main_surface.blit(msg_rendered, msg_rendered.get_rect(center=(self.main_surface.get_rect().centerx, 0.95 * self.main_surface.get_height())))
        pygame.display.update()

    def read_level_infos(self) -> None:
        """Reads the level infos from the json file"""
        with (open(FILENAME_LEVEL_INFO)) as file_level_info:
            level_infos = json.load(file_level_info)
        for level_info in level_infos:
            self.levels.append(Level(level_info))

    def init_start_menu(self):
        # Wait for user pressing key
        key_pressed = False
        while not key_pressed:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    key_pressed = True
        self.start_menu.slide_in()

    def start(self):
        """Start the execution"""
        if self.start_menu.handle_events():
            self.start_game()

    def start_game(self):
        """Start or resume the game"""
        self.paused_time += pygame.time.get_ticks()
        while not self.quit:
            self.game_loop()

    def pause_game(self) -> bool:
        """Pause the game. Return True if user wants to resume and False for exit."""
        self.pause_start_time = pygame.time.get_ticks()
        self.reset_timer(True)
        self.pause_menu.reset()
        # Use current state as the background for the pause menu
        self.pause_menu.bg_img = self.main_surface.copy()
        resume = self.pause_menu.handle_events()
        if resume:
            self.paused = False
        else:
            self.quit = True
        self.paused_time += (pygame.time.get_ticks() - self.pause_start_time)
        return resume

    def reset_timer(self, deactivate=False):
        """
        Reset the timer for the reoccurring events.

        :param deactivate: If set to True, all reoccurring events will be deactivated.
        """
        for snake in self.game.snakes:
            pygame.time.set_timer(self.upd_snake_events[snake.idx], 0 if deactivate else int(1000 / snake.speed))
        pygame.time.set_timer(self.reocc_event, 0 if deactivate else REOCC_DUR)

    def game_loop(self) -> None:
        """Main game loop"""
        self.reset_timer()
        self.graphics.update_display(*self.game.get_infos_for_updating_display(), paused_time=self.paused_time)
        # start game loop
        crashed = False
        while not self.paused and not self.quit:
            snake_ids_to_update = []
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Quit
                    self.quit = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    # Pause the game
                    self.paused = True
                elif event.type == pygame.KEYDOWN and event.key in self.snake_controls_all and not crashed:
                    # Update orientation of snake
                    self.game.update_snake_orientation(event.key)
                elif event.type in UPDATE_SNAKES and not crashed:
                    # Update position of snake (only add to list here, real updating is done later)
                    snake_ids_to_update.append(event.snake_idx)
                elif event.type == REOCC_TIMER and not crashed:
                    # update all counting elements
                    new_objs = self.game.update_counting()
                    self.play_sounds(new_objs)
            # Update position of snakes
            if snake_ids_to_update:
                items = self.game.update_snakes(snake_ids_to_update)
                self.play_sounds(items)
                for _id in snake_ids_to_update:
                    pygame.time.set_timer(self.upd_snake_events[_id], int(1000 / self.game.snakes[_id].speed))
            # Update display
            self.graphics.update_display(*self.game.get_infos_for_updating_display(), paused_time=self.paused_time)
            if self.game.crashes and not crashed:
                self.crash_sound.play()
                crashed = True
                self.paused = True
            self.clock.tick(FPS)
        if self.paused:
            self.pause_game()

    def play_sounds(self, items: [utils.Objects]) -> None:
        """Play the sounds for the given items"""
        for item in items:
            if item in self.item_sounds:
                self.item_sounds[item].play()
