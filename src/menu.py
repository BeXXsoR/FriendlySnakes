"""Classes for all the menus in the game"""

import utils
import pygame

pygame.init()

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
BG_COLOR = GREEN
FILENAMES_SNAKE_IMGS = {GREEN: "../res/snake_head_green.png", BLUE: "../res/snake_head_blue.png",
			  			CYAN: "../res/snake_head_cyan.png",	PINK: "../res/snake_head_pink.png"}
FILENAME_BUTTON = "../res/button.png"
FPS = 60
MAP_TO_SCREEN_RATIO = 0.9
TITLE_FONT_SIZE = 200
SNAKE_NAME_FONT_SIZE = 80
BENCHMARK_HEIGHT = 1440
TITLE_HEIGHT = 0.1
SNAKE_SETTINGS_HEIGHT = 0.4
# Heights of elements inside the snake settings areas
SNAKE_NAME_HEIGHT = 0.2
FREE_SPACE_HEIGHT = 0.2
SNAKE_COLOR_HEIGHT = 0.3
# endregion


class Clickable(pygame.sprite.Sprite):
	"""Sprite subclass for the buttons in the start menu"""
	def __init__(self, image: pygame.Surface, rect: pygame.Rect, on_click_function):
		super().__init__()
		self.image = image
		self.rect = rect
		self.on_click_function = on_click_function

	def on_click(self):
		self.on_click_function()


class ClickableGroup(pygame.sprite.Group):
	"""Sprites group for the buttons in the start menu"""
	def __init__(self, *sprites):
		super().__init__(*sprites)

	def collide_click(self, point: (int, int)):
		"""Call the on click method of the sprites that collide with the given point"""
		for sprite in self.sprites():
			if sprite.rect.collidepoint(point):
				try:
					sprite.on_click()
				except AttributeError:
					continue


class StartMenu:
	def __init__(self, main_surface: pygame.Surface):
		"""Initialize the start menu"""
		self.main_surface = main_surface
		self.snake_names = ["Kokosnuss", "Tiger", "Muh", "Mausi"]
		self.snake_colors = [GREEN, BLUE, CYAN, PINK]
		# snake_controls = [
		# 	{pygame.K_UP: ORIENT_UP, pygame.K_LEFT: ORIENT_LEFT, pygame.K_DOWN: ORIENT_DOWN, pygame.K_RIGHT: ORIENT_RIGHT},
		# 	{pygame.K_w: ORIENT_UP, pygame.K_a: ORIENT_LEFT, pygame.K_s: ORIENT_DOWN, pygame.K_d: ORIENT_RIGHT},
		# 	{pygame.K_KP8: ORIENT_UP, pygame.K_KP4: ORIENT_LEFT, pygame.K_KP5: ORIENT_DOWN, pygame.K_KP6: ORIENT_RIGHT},
		# 	{pygame.K_i: ORIENT_UP, pygame.K_j: ORIENT_LEFT, pygame.K_k: ORIENT_DOWN, pygame.K_l: ORIENT_RIGHT}]
		usable_rect = pygame.rect.Rect(int((1 - MAP_TO_SCREEN_RATIO) * self.main_surface.get_width() / 2),
									   int((1 - MAP_TO_SCREEN_RATIO) * self.main_surface.get_height() / 2),
									   MAP_TO_SCREEN_RATIO * self.main_surface.get_width(),
									   MAP_TO_SCREEN_RATIO * self.main_surface.get_height())
		self.scaling_factor = main_surface.get_height() / BENCHMARK_HEIGHT
		# Title
		self.title_font = pygame.font.Font(None, int(TITLE_FONT_SIZE * self.scaling_factor))
		self.title_rendered = self.title_font.render("Friendly Snakes", True, BLUE)
		self.title_rect = pygame.rect.Rect(usable_rect.topleft, (usable_rect.w, TITLE_HEIGHT * usable_rect.h))
		# Free space rect
		self.free_space_rect = pygame.rect.Rect(self.title_rect.bottomleft, (self.title_rect.w, FREE_SPACE_HEIGHT * usable_rect.h))
		# snake settings
		self.snake_settings_rects = [pygame.rect.Rect(usable_rect.left + int(i / 4 * usable_rect.w), self.free_space_rect.bottom, int(usable_rect.w / 4), SNAKE_SETTINGS_HEIGHT * usable_rect.h) for i in range(4)]
		self.snake_settings_surfs = [self.main_surface.subsurface(rect) for rect in self.snake_settings_rects]
		self.snake_name_rect = pygame.rect.Rect(0, 0, self.snake_settings_rects[0].w, SNAKE_NAME_HEIGHT * self.snake_settings_rects[0].h)
		self.snake_color_rect = pygame.rect.Rect(self.snake_name_rect.bottomleft, tuple([SNAKE_COLOR_HEIGHT * self.snake_settings_rects[0].h] * 2))
		self.snake_color_rect.centerx = self.snake_name_rect.centerx
		self.snake_name_font = pygame.font.Font(None, int(SNAKE_NAME_FONT_SIZE * self.scaling_factor))
		# prepare images
		self.snake_imgs = {k: pygame.transform.scale(pygame.image.load(v).convert_alpha(), utils.mult_tuple_to_int(self.snake_color_rect.size, 0.9)) for k,v in FILENAMES_SNAKE_IMGS.items()}
		self.name_button_img = pygame.transform.scale(pygame.image.load(FILENAME_BUTTON).convert_alpha(), utils.mult_tuple_to_int(self.snake_name_rect.size, 0.9))
		self.color_button_img = pygame.transform.scale(pygame.image.load(FILENAME_BUTTON).convert_alpha(), utils.mult_tuple_to_int(self.snake_color_rect.size, 1))
		# prepare buttons
		self.name_button = Clickable(self.name_button_img, self.name_button_img.get_rect(center=self.snake_name_rect.center), self.click_on_name_button())
		self.color_button = Clickable(self.color_button_img, self.color_button_img.get_rect(center=self.snake_color_rect.center), self.click_on_color_button())
		self.name_button_grp = ClickableGroup(self.name_button, self.color_button)
		# rest
		self.clock = pygame.time.Clock()
		self.update_display()

	def handle_events(self):
		"""Handle the events in the start menu"""
		is_running = True
		while is_running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
					# Quit
					is_running = False
			self.clock.tick(FPS)
			self.update_display()

	def click_on_name_button(self):
		pass

	def click_on_color_button(self):
		pass

	def update_display(self) -> None:
		"""Display the current state on the screen"""
		self.main_surface.fill(BG_COLOR)
		self.main_surface.blit(self.title_rendered, self.title_rendered.get_rect(center=self.title_rect.center))
		# Draw snake settings edges
		for rect in self.snake_settings_rects:
			pygame.draw.rect(self.main_surface, RED, rect, 5)
		# Draw button style backgrounds for the snake settings elements
		for surf in self.snake_settings_surfs:
			self.name_button_grp.draw(surf)
		# Draw snake settings
		for surf, name, color in zip(self.snake_settings_surfs, self.snake_names, self.snake_colors):
			cur_name_rendered = self.snake_name_font.render(name, True, WHITE)
			surf.blit(cur_name_rendered, cur_name_rendered.get_rect(center=self.snake_name_rect.center))
			surf.blit(self.snake_imgs[color], self.snake_imgs[color].get_rect(center=self.snake_color_rect.center))
		pygame.display.update()

