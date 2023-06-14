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
                        utils.Objects.BOMB: "../res/bomb.ogg", utils.Objects.EXPLOSION: "../res/explosion.ogg", utils.Objects.FIRE_SPIT: "../res/fire_spit.ogg"}
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
        self.snake_names = ["Player 1", "Player 2", "Player 3", "Player 4"]
        self.snake_colors = [GREEN, BLUE, CYAN, PINK]
        self.snake_controls = [
            {pygame.K_UP: ORIENT_UP, pygame.K_LEFT: ORIENT_LEFT, pygame.K_DOWN: ORIENT_DOWN, pygame.K_RIGHT: ORIENT_RIGHT},
            {pygame.K_w: ORIENT_UP, pygame.K_a: ORIENT_LEFT, pygame.K_s: ORIENT_DOWN, pygame.K_d: ORIENT_RIGHT},
            {pygame.K_KP8: ORIENT_UP, pygame.K_KP4: ORIENT_LEFT, pygame.K_KP5: ORIENT_DOWN, pygame.K_KP6: ORIENT_RIGHT},
            {pygame.K_i: ORIENT_UP, pygame.K_j: ORIENT_LEFT, pygame.K_k: ORIENT_DOWN, pygame.K_l: ORIENT_RIGHT}]
        self.snake_controls_all = []
        for controls in self.snake_controls:
            self.snake_controls_all.extend(controls.keys())
        self.num_players = 2
        self.main_surface = pygame.display.set_mode((0, 0))
        self.lang = utils.Language.ENGLISH
        self.level_idx = 0
        self.levels = []
        self.read_level_infos()
        self.level = self.levels[self.level_idx]
        utils.play_music_track(FILENAMES_MUSIC_TRACKS[0], 0.1)
        self.sound_volume = 1.0
        self.scaling_factor = self.main_surface.get_height() / BENCHMARK_HEIGHT
        self.start_bg_img = pygame.transform.scale(pygame.image.load(FILENAME_START_BG).convert_alpha(), self.main_surface.get_size())
        self.start_menu = Menu(self.main_surface,
                               pygame.Rect(utils.mult_tuple_to_int(START_MENU_TOPLEFT, self.scaling_factor), utils.mult_tuple_to_int(START_MENU_SIZE, self.scaling_factor)),
                               self.start_bg_img,
                               self.scaling_factor,
                               self.lang,
                               TEXTS_BUTTON_START_MENU[self.lang],
                               [level.name for level in self.levels],
                               True)
        self.pause_menu = Menu(self.main_surface,
                               pygame.Rect(utils.mult_tuple_to_int(PAUSE_MENU_TOPLEFT, self.scaling_factor), utils.mult_tuple_to_int(PAUSE_MENU_SIZE, self.scaling_factor)),
                               None,
                               self.scaling_factor,
                               self.lang,
                               TEXTS_BUTTON_PAUSE_MENU[self.lang],
                               None,
                               False)
        self.game_over_menu = Menu(self.main_surface,
                                   pygame.Rect(utils.mult_tuple_to_int(PAUSE_MENU_TOPLEFT, self.scaling_factor), utils.mult_tuple_to_int(PAUSE_MENU_SIZE, self.scaling_factor)),
                                   None,
                                   self.scaling_factor,
                                   self.lang,
                                   TEXTS_BUTTON_GAME_OVER_MENU[self.lang],
                                   None,
                                   False)
        self.set_start_screen()
        self.init_start_menu()
        self.game: Game
        # self.game = Game(self.snake_names, self.snake_colors, self.snake_controls, self.level)
        # self.game = Game(self.snake_names[:1], self.snake_colors[:1], self.snake_controls[:1], self.level)
        # self.game = Game(self.snake_names[:2], self.snake_colors[:2], self.snake_controls[:2], self.level)
        self.graphics = Graphics(self.main_surface, self.level.num_rows, self.level.num_cols)
        self.upd_snake_events = [pygame.event.Event(event_id, {"snake_idx": idx}) for idx, event_id in enumerate(UPDATE_SNAKES)]
        self.reocc_event = pygame.event.Event(REOCC_TIMER, {"duration": REOCC_DUR})
        self.item_sounds = {k: pygame.mixer.Sound(v) for k, v in FILENAME_ITEM_SOUNDS.items()}
        self.crash_sound = pygame.mixer.Sound(FILENAME_CRASH_SOUND)
        self.sounds_all = list(self.item_sounds.values()) + [self.crash_sound]
        self.paused = False
        self.back_to_main_menu = False
        # self.pause_start_time = 0
        self.paused_time = 0
        self.clock = pygame.time.Clock()

    def update_param_from_menu(self, menu: Menu) -> None:
        """Get the relevant infos from the given menu and update the internal parameters"""
        level_idx, num_players, new_sound_volume, new_controls = menu.get_infos()
        if level_idx:
            self.level_idx = level_idx
            self.level = self.levels[self.level_idx]
        if num_players:
            self.num_players = num_players
            self.upd_snake_events = [pygame.event.Event(event_id, {"snake_idx": idx}) for idx, event_id in enumerate(UPDATE_SNAKES[:self.num_players])]
        if new_sound_volume != self.sound_volume:
            for sound in self.sounds_all:
                sound.set_volume(new_sound_volume)
            for menu in [self.start_menu, self.pause_menu, self.game_over_menu]:
                menu.set_sound_volume(new_sound_volume)
            self.sound_volume = new_sound_volume
        if new_controls:
            for menu in [self.start_menu, self.pause_menu, self.game_over_menu]:
                menu.set_controls(new_controls)
            orientations = [ORIENT_UP, ORIENT_LEFT, ORIENT_DOWN, ORIENT_RIGHT]
            self.snake_controls = [{key: ori for key, ori in zip(controls, orientations)} for controls in new_controls]
            for controls in self.snake_controls:
                self.snake_controls_all.extend(controls.keys())

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
                if event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONUP:
                    key_pressed = True
        self.start_menu.slide_in()

    def start(self):
        """Start the execution"""
        cnt = 0
        while self.start_menu.handle_events():
            self.update_param_from_menu(self.start_menu)
            # # Show map
            # self.show_map()
            # return
            # if cnt == 0:
            self.game = Game(self.snake_names[:self.num_players], self.snake_colors[:self.num_players], self.snake_controls[:self.num_players], self.level)
            if cnt > 0:
                self.reset()
                # self.game = Game(self.snake_names[:self.num_players], self.snake_colors[:self.num_players], self.snake_controls[:self.num_players], self.level)
            self.start_game()
            self.start_menu.reset()
            cnt += 1

    def start_game(self):
        """Start or resume the game"""
        self.paused_time = pygame.time.get_ticks()
        while not self.back_to_main_menu:
            self.game_loop()

    def pause_game(self) -> bool:
        """Pause the game. Return True if user wants to resume and False for exit."""
        pause_start_time = pygame.time.get_ticks()
        self.reset_timer(True)
        self.pause_menu.reset()
        # Use current state as the background for the pause menu
        self.pause_menu.bg_img = self.main_surface.copy()
        resume = self.pause_menu.handle_events()
        if resume:
            self.paused = False
        else:
            self.back_to_main_menu = True
            self.level.reset()
        self.update_param_from_menu(self.pause_menu)
        self.paused_time += (pygame.time.get_ticks() - pause_start_time)
        return resume

    def game_over(self) -> bool:
        """Handle the game over situation"""
        self.game_over_menu.reset()
        self.game_over_menu.bg_img = self.main_surface.copy()
        if play_again := self.game_over_menu.handle_events():
            self.reset()
        else:
            self.back_to_main_menu = True
        self.update_param_from_menu(self.game_over_menu)
        return play_again

    def reset(self) -> None:
        """Reset the game so that it can be played again"""
        # snake_names = [snake.name for snake in self.game.snakes]
        # snake_colors = [snake.color for snake in self.game.snakes]
        # snake_controls = [snake.controls for snake in self.game.snakes]
        # self.level.reset()
        # self.game = Game(snake_names, snake_colors, snake_controls, self.level, self.main_surface)
        self.game.reset()
        self.paused = False
        self.back_to_main_menu = False
        self.paused_time = pygame.time.get_ticks()

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
        while not self.paused and not self.back_to_main_menu and not crashed:
            snake_ids_to_update = []
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Quit
                    self.back_to_main_menu = True
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
            self.clock.tick(FPS)
        if crashed:
            self.stop_item_sounds()
            self.game_over()
        elif self.paused:
            self.pause_game()

    def play_sounds(self, items: [utils.Objects]) -> None:
        """Play the sounds for the given items"""
        for item in items:
            if item in self.item_sounds:
                self.item_sounds[item].play()

    def stop_item_sounds(self) -> None:
        """Stop all item sounds"""
        for sound in self.item_sounds.values():
            sound.stop()

    def show_map(self):
        is_running = True
        while is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    is_running = False
            self.graphics.display_map(self.level)
