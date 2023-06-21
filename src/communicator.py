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
UPDATE_SNAKES = [pygame.event.custom_type() for _ in range(4)]
REOCC_TIMER = pygame.event.custom_type()
START_MENU_TOPLEFT = (0, 300)
START_MENU_SIZE = (670, 705)
PAUSE_MENU_TOPLEFT = (0, 300)
PAUSE_MENU_SIZE = (670, 705)


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
        self.levels_as_json = self.read_level_infos()
        self.highscores = [level.highscore for level in self.levels]
        self.level = self.levels[self.level_idx]
        utils.play_music_track(FILENAMES_MUSIC_TRACKS[0][1], 0.1)
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
                               self.get_highscores_for_display(),
                               True,
                               True)
        self.pause_menu = Menu(self.main_surface,
                               pygame.Rect(utils.mult_tuple_to_int(PAUSE_MENU_TOPLEFT, self.scaling_factor), utils.mult_tuple_to_int(PAUSE_MENU_SIZE, self.scaling_factor)),
                               None,
                               self.scaling_factor,
                               self.lang,
                               TEXTS_BUTTON_PAUSE_MENU[self.lang],
                               [level.name for level in self.levels],
                               self.get_highscores_for_display(),
                               False,
                               False)
        self.game_over_menu = Menu(self.main_surface,
                                   pygame.Rect(utils.mult_tuple_to_int(PAUSE_MENU_TOPLEFT, self.scaling_factor), utils.mult_tuple_to_int(PAUSE_MENU_SIZE, self.scaling_factor)),
                                   None,
                                   self.scaling_factor,
                                   self.lang,
                                   TEXTS_BUTTON_GAME_OVER_MENU[self.lang],
                                   [level.name for level in self.levels],
                                   self.get_highscores_for_display(),
                                   False,
                                   False)
        self.set_start_screen()
        self.init_start_menu()
        self.game: Game
        self.graphics = Graphics(self.main_surface, self.level.num_rows, self.level.num_cols)
        self.upd_snake_events = [pygame.event.Event(event_id, {"snake_idx": idx}) for idx, event_id in enumerate(UPDATE_SNAKES)]
        self.reocc_event = pygame.event.Event(REOCC_TIMER, {"duration": REOCC_DUR})
        self.item_sounds = {k: pygame.mixer.Sound(v) for k, v in FILENAME_ITEM_SOUNDS.items()}
        self.crash_sound = pygame.mixer.Sound(FILENAME_CRASH_SOUND)
        self.sounds_all = list(self.item_sounds.values()) + [self.crash_sound]
        self.paused = False
        self.back_to_main_menu = False
        self.paused_time = 0
        self.clock = pygame.time.Clock()

    def update_param_from_menu(self, menu: Menu) -> None:
        """Get the relevant infos from the given menu and update the internal parameters"""
        level_idx, num_players, new_sound_volume, new_controls, new_colors = menu.get_infos()
        if level_idx is not None:
            self.level_idx = level_idx
            self.level = self.levels[self.level_idx]
        if num_players:
            for menu in [self.start_menu, self.pause_menu, self.game_over_menu]:
                menu.change_num_players(None, num_players)
            self.num_players = num_players
            self.upd_snake_events = [pygame.event.Event(event_id, {"snake_idx": idx}) for idx, event_id in enumerate(UPDATE_SNAKES[:self.num_players])]
        if new_sound_volume != self.sound_volume:
            for sound in self.sounds_all:
                sound.set_volume(new_sound_volume)
            for menu in [self.start_menu, self.pause_menu, self.game_over_menu]:
                menu.set_sound_volume(new_sound_volume)
            self.sound_volume = new_sound_volume
        if new_controls != self.snake_controls:
            for menu in [self.start_menu, self.pause_menu, self.game_over_menu]:
                menu.set_controls(new_controls)
            orientations = [ORIENT_UP, ORIENT_LEFT, ORIENT_DOWN, ORIENT_RIGHT]
            self.snake_controls = [{key: ori for key, ori in zip(controls, orientations)} for controls in new_controls]
            self.snake_controls_all = []
            for controls in self.snake_controls:
                self.snake_controls_all.extend(controls.keys())
        if new_colors != self.snake_colors:
            for menu in [self.start_menu, self.pause_menu, self.game_over_menu]:
                menu.set_colors(new_colors)
            self.snake_colors = new_colors

    def set_start_screen(self):
        self.main_surface.blit(self.start_bg_img, (0, 0))
        msg_font = pygame.font.Font(FONT_SNAKE_CHAN, 40)
        msg_rendered = msg_font.render("Press any key", True, WHITE)
        self.main_surface.blit(msg_rendered, msg_rendered.get_rect(center=(self.main_surface.get_rect().centerx, 0.95 * self.main_surface.get_height())))
        pygame.display.update()

    def read_level_infos(self) -> {}:
        """Reads the level infos from the json file"""
        with (open(FILENAME_LEVEL_INFO)) as file_level_info:
            level_infos = json.load(file_level_info)
        for level_info in level_infos:
            self.levels.append(Level(level_info))
        return level_infos

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
            self.start_game()
            self.start_menu.reset()
            cnt += 1
        # User ended game - save highscores to json file
        self.save_highscores_to_file()

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
        score = sum([snake.score for snake in self.game.snakes]) if self.level.goal == utils.Goals.HIGHSCORE else int((pygame.time.get_ticks() - self.paused_time) / 1000)
        cur_high = self.highscores[self.level_idx]
        if len(cur_high) < 3 or score > cur_high[2][1]:
            # New highscore
            self.game_over_menu.mini_menu_new_highscore.enable()
            self.game_over_menu.handle_events()
            team_name = self.game_over_menu.team_name
            place = 0
            while len(cur_high) > place and score <= cur_high[place][1]:
                place += 1
            self.highscores[self.level_idx] = cur_high[:place] + [(team_name, score)] + cur_high[place:2]
            for menu in [self.start_menu, self.pause_menu, self.game_over_menu]:
                menu.set_highscore(self.level_idx, self.get_highscore_for_display_for_single_level(self.level_idx))
            self.game_over_menu.mini_menu_new_highscore.disable()
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
        # let user press key to decide when to start
        cur_time = pygame.time.get_ticks()
        msg_font = pygame.font.Font(FONT_SNAKE_CHAN, 40)
        msg_rendered = msg_font.render("Press key to start", True, WHITE)
        self.main_surface.blit(msg_rendered, msg_rendered.get_rect(center=self.main_surface.get_rect().center))
        pygame.display.update()
        key_pressed = False
        while not key_pressed:
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    key_pressed = True
        self.paused_time += (pygame.time.get_ticks() - cur_time)
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

    def get_highscores_for_display(self) -> [[(str, str)]]:
        """Return the highscores for all levels in a displayable format"""
        return [self.get_highscore_for_display_for_single_level(level_idx) for level_idx in range(len(self.levels))]

    def get_highscore_for_display_for_single_level(self, level_idx) -> [(str, str)]:
        """Return the highscore for a single level in displayable format, i.e. for time-levels, change the score to a time format"""
        return [(name, str(score) if self.levels[level_idx].goal == utils.Goals.HIGHSCORE else utils.get_time_string_for_ms(score * 1000)) for (name, score) in self.highscores[level_idx]]

    def save_highscores_to_file(self) -> None:
        """Save the current highscores to the levels.json file"""
        for level_json, highscore in zip(self.levels_as_json, self.highscores):
            assert "highscore" in level_json, "Missing 'highscore' tag in level json dict."
            level_json["highscore"] = highscore
        with (open(FILENAME_LEVEL_INFO, "w")) as file_level_info:
            json.dump(self.levels_as_json, file_level_info)

    def show_map(self):
        is_running = True
        while is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    is_running = False
            self.graphics.display_map(self.level)
