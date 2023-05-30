"""Module for the graphics class in the friendly snakes package"""

# ----- Imports --------
import utils
from level import Level
from snake import Snake
from constants import *
import animations
import pygame

pygame.init()


# ----- Classes --------
class Graphics:
	"""The class for displaying all graphics on the screen"""

	def __init__(self, main_surface: pygame.Surface, num_rows: int, num_cols: int):
		self.main_surface = main_surface
		self.bg = pygame.transform.scale(pygame.image.load(FILENAMES_BG[utils.Backgrounds.DESERT]).convert_alpha(), self.main_surface.get_size())
		self.edge_size = int(min(self.main_surface.get_width() * MAP_TO_SCREEN_RATIO / num_cols, self.main_surface.get_height() * MAP_TO_SCREEN_RATIO / num_rows))
		self.square_size = (self.edge_size, self.edge_size)
		map_size = (self.edge_size * num_cols, self.edge_size * num_rows)
		# Field surface
		self.map_rect = pygame.rect.Rect((0, 0), map_size)
		self.map_rect.center = self.main_surface.get_rect().center
		self.map_surface = self.main_surface.subsurface(self.map_rect)
		self.square_posis = [[(j * self.edge_size, i * self.edge_size) for j in range(num_cols)] for i in range(num_rows)]
		# snake status surfaces
		status_rect_size = (int((MAP_TO_SCREEN_RATIO * self.main_surface.get_width() - self.map_rect.width) / 2), int(self.map_rect.height / 4))
		status_rect = pygame.rect.Rect((0, 0), status_rect_size)
		self.snake_status_rects = []
		for i in range(4):
			cur_rect = status_rect.copy()
			cur_rect.top = self.snake_status_rects[-1].bottom if self.snake_status_rects else self.map_rect.top
			cur_rect.left = int((1 - MAP_TO_SCREEN_RATIO) / 2 * self.main_surface.get_width())
			# 	if i % 2 == 0 else self.map_rect.right
			self.snake_status_rects.append(cur_rect)
		self.status_surfaces = [self.main_surface.subsurface(rect) for rect in self.snake_status_rects]
		# Rects inside a snake status surface
		num_rows = 6
		num_cols = 6
		edge_size = int(min(status_rect.width / num_cols, status_rect.height / num_rows))
		rect_size = (edge_size, edge_size)
		self.snake_head_img_rect = pygame.rect.Rect((0, 0), rect_size)
		self.snake_name_rect = pygame.rect.Rect(self.snake_head_img_rect.topright, (3 * edge_size, edge_size))
		self.snake_body_img_rect = pygame.rect.Rect(self.snake_head_img_rect.bottomleft, rect_size)
		self.snake_size_rect = pygame.rect.Rect(self.snake_body_img_rect.topright, rect_size)
		self.snake_speed_img_rect = pygame.rect.Rect(self.snake_size_rect.topright, rect_size)
		self.snake_speed_rect = pygame.rect.Rect(self.snake_speed_img_rect.topright, rect_size)
		self.snake_drunk_rect = pygame.rect.Rect(self.snake_body_img_rect.bottomleft, rect_size)
		self.snake_chili_rect = pygame.rect.Rect(self.snake_speed_img_rect.bottomleft, rect_size)
		self.snake_burger_rects = [pygame.rect.Rect((i * edge_size, self.snake_drunk_rect.bottom), rect_size) for i in range(3)]
		# Prepare images
		self.items_orig = {obj: pygame.image.load(filename).convert_alpha() for obj, filename in FILENAME_ITEMS.items()}
		self.items = {obj: pygame.transform.scale(img_orig, self.square_size)
					  for obj, img_orig in self.items_orig.items()}
		self.fire = pygame.transform.scale(pygame.image.load(FILENAME_FIRE_SPIT).convert_alpha(), (SPIT_FIRE_RANGE * self.edge_size, self.edge_size))
		self.bomb_anim = animations.Animation(FILENAME_BOMB, self.square_size)
		self.explosion_anim = animations.Animation(FILENAME_EXPLOSION, (3 * self.edge_size, 3 * self.edge_size))
		self.drunk_anim = animations.Animation(FILENAME_DRUNK, self.square_size)
		self.piqu_rising_anim = animations.Animation(FILENAME_PIQU_RISING, self.square_size)
		# self.explosions = {}
		self.snake_parts_orig = {k: [pygame.image.load(filename).convert_alpha() for filename in v] for k, v in FILENAME_SNAKE_PARTS.items()}
		self.snake_parts = {k: [pygame.transform.scale(img_orig, self.square_size) for img_orig in v] for k, v in self.snake_parts_orig.items()}
		status_img_size = utils.mult_tuple_to_int(rect_size, 1)
		self.snake_status_imgs = {k: [pygame.transform.scale(img_orig, status_img_size) for img_orig in v] for k, v in self.snake_parts_orig.items() if k != utils.SnakeParts.TAIL}
		self.speedo_img = pygame.transform.scale(pygame.image.load(FILENAME_SPEEDO).convert_alpha(), utils.mult_tuple_to_int(rect_size, 0.8))
		self.drunk_img = pygame.transform.scale(self.items_orig[utils.Objects.BEER], utils.mult_tuple_to_int(rect_size, 0.8))
		# Prepare fonts
		self.snake_name_font = pygame.font.Font(None, SNAKE_NAME_FONT_SIZE)
		self.snake_info_font = pygame.font.Font(None, SNAKE_INFO_FONT_SIZE)

	def update_display(self, level: Level, snakes: [Snake], crashes: [((int, int), (int, int))], bombs: {(int, int): int}, explosions: {(int, int): int}) -> None:
		"""Draw everything onto the screen"""
		# Draw background
		# self.main_surface.fill(BG_COLOR)
		self.main_surface.blit(self.bg, (0, 0))
		# Draw level
		wall_color = GREY
		for row, obj_row in enumerate(level.map):
			for col, obj in enumerate(obj_row):
				grid_pos = (row, col)
				screen_pos = self.grid_to_screen_pos(grid_pos)
				if obj == utils.Objects.WALL:
					pygame.draw.rect(self.map_surface, wall_color, pygame.rect.Rect(screen_pos, self.square_size))
				elif obj == utils.Objects.BOMB:
					cur_frame_id = self.bomb_anim.num_frames - bombs[grid_pos]
					cur_frame = self.bomb_anim.pygame_frames[cur_frame_id]
					self.map_surface.blit(cur_frame, screen_pos)
				elif obj == utils.Objects.EXPLOSION:
					# Do nothing here, explosions are handled seperately later (so that for explosions at the edge,
					# the explosions are only drawn after the wall has been drawn)
					pass
				elif obj != utils.Objects.NONE:
					self.map_surface.blit(self.items[obj], screen_pos)
		# Draw explosions
		for grid_pos in explosions:
			screen_pos = self.grid_to_screen_pos(grid_pos)
			cur_frame_id = self.explosion_anim.num_frames - explosions[grid_pos]
			cur_frame = self.explosion_anim.pygame_frames[cur_frame_id]
			self.map_surface.blit(cur_frame, utils.subtract_tuples(screen_pos, self.square_size))
		# Draw snakes
		for snake in snakes:
			head_orientation = utils.subtract_tuples(snake.pos[0], snake.pos[1])
			for idx, pos in enumerate(snake.pos):
				screen_pos = self.grid_to_screen_pos(pos)
				if idx == 0 and snake.color in self.snake_parts:
					# snake head (incl. piquancy and drunk animation)
					self.map_surface.blit(pygame.transform.rotate(self.snake_parts[snake.color][utils.SnakeParts.HEAD.value], ROTATIONS_STRAIGHT[head_orientation]), screen_pos)
					if snake.piquancy_growing > 0:
						cur_frame_id = self.piqu_rising_anim.num_frames - snake.piquancy_growing
						cur_frame = self.piqu_rising_anim.pygame_frames[cur_frame_id]
						self.map_surface.blit(pygame.transform.rotate(cur_frame, ROTATIONS_STRAIGHT[head_orientation]), screen_pos)
					if snake.is_drunk > 0:
						cur_frame_id = self.drunk_anim.num_frames - snake.is_drunk
						cur_frame = self.drunk_anim.pygame_frames[cur_frame_id]
						self.map_surface.blit(pygame.transform.rotate(cur_frame, ROTATIONS_STRAIGHT[head_orientation] % 180), screen_pos)
				elif idx == len(snake.pos) - 1 and snake.color in self.snake_parts:
					# snake tail
					tail_orientation = utils.subtract_tuples_int(snake.pos[idx - 1], pos)
					self.map_surface.blit(pygame.transform.rotate(self.snake_parts[snake.color][utils.SnakeParts.TAIL.value], ROTATIONS_STRAIGHT[tail_orientation]), screen_pos)
				elif idx != len(snake.pos) - 1 and snake.color in self.snake_parts:
					# snake body
					orientation_front = utils.subtract_tuples_int(snake.pos[idx - 1], pos)
					orientation_back = utils.subtract_tuples_int(pos, snake.pos[idx + 1])
					if orientation_front == orientation_back:
						snake_part_idx = utils.SnakeParts.BODY_STRAIGHT.value if orientation_front == orientation_back else utils.SnakeParts.BODY_CORNER.value
						rotation = ROTATIONS_STRAIGHT[orientation_front] if orientation_front == orientation_back else ROTATIONS_CORNER[(orientation_front, orientation_back)]
					else:
						snake_part_idx = utils.SnakeParts.BODY_CORNER.value
						rotation = ROTATIONS_CORNER[(orientation_front, orientation_back)]
					self.map_surface.blit(pygame.transform.rotate(self.snake_parts[snake.color][snake_part_idx], rotation), screen_pos)
				else:
					pygame.draw.rect(self.map_surface, snake.color, pygame.rect.Rect(screen_pos, self.square_size))
			# Draw spit fire
			if snake.spit_fire_posis:
				screen_pos = self.grid_to_screen_pos(snake.spit_fire_posis[0 if head_orientation in [ORIENT_RIGHT, ORIENT_DOWN] else -1])
				# The spit fire range might be cut because of obstacles, so we have to check for that and only show
				# the image partially in that case
				factor = len(snake.spit_fire_posis) / SPIT_FIRE_RANGE
				trg_area = (0, 0, factor * self.fire.get_width(), self.fire.get_height())
				trg_image = self.fire.subsurface(trg_area)
				self.map_surface.blit(pygame.transform.rotate(trg_image, ROTATIONS_STRAIGHT[head_orientation]), screen_pos)
		# Draw crashes
		radius1 = self.edge_size / 2.0 * 0.7
		radius2 = self.edge_size / 2.0 * 0.8
		crashes_centers = tuple([utils.multiply_tuple(utils.add_tuples([self.grid_to_screen_pos(crash[0]), self.grid_to_screen_pos(crash[1]), self.square_size]), 0.5) for crash in crashes])
		for center in crashes_centers:
			pygame.draw.circle(self.map_surface, ORANGE, center, radius2)
			pygame.draw.circle(self.map_surface, RED, center, radius1)
		# Draw snake status
		for surf, snake in zip(self.status_surfaces, snakes):
			# surf.fill((random.randrange(255), random.randrange(255), random.randrange(255)))
			to_be_added_rects = [self.snake_chili_rect]
			to_be_added_rects.extend(self.snake_burger_rects)
			# Draw status images
			surf.blit(self.snake_status_imgs[snake.color][utils.SnakeParts.HEAD.value], self.snake_status_imgs[snake.color][utils.SnakeParts.HEAD.value].get_rect(center=self.snake_head_img_rect.center))
			surf.blit(self.snake_status_imgs[snake.color][utils.SnakeParts.BODY_STRAIGHT.value], self.snake_status_imgs[snake.color][utils.SnakeParts.HEAD.value].get_rect(center=self.snake_body_img_rect.center))
			surf.blit(self.speedo_img, self.speedo_img.get_rect(center=self.snake_speed_img_rect.center))
			# Display status texts
			name_font = self.snake_name_font.render(snake.name, True, snake.color)
			surf.blit(name_font, name_font.get_rect(center=self.snake_name_rect.center))
			len_font = self.snake_info_font.render(str(len(snake.pos)), True, BLACK)
			surf.blit(len_font, len_font.get_rect(center=self.snake_size_rect.center))
			speed_font = self.snake_info_font.render(str(snake.speed), True, BLACK)
			surf.blit(speed_font, speed_font.get_rect(center=self.snake_speed_rect.center))
			if snake.is_drunk:
				surf.blit(self.drunk_img, self.drunk_img.get_rect(center=self.snake_drunk_rect.center))
				drunk_font = self.snake_info_font.render(str(int(snake.is_drunk / REOCC_PER_SEC)), True, BLACK if snake.is_drunk > 3 else RED)
				surf.blit(drunk_font, drunk_font.get_rect(center=self.snake_drunk_rect.center))
			# for rect in to_be_added_rects:
				# pygame.draw.rect(surf, (random.randrange(255), random.randrange(255), random.randrange(255)), rect)
				# pygame.draw.rect(surf, GREY, rect)
		pygame.display.update()

	def grid_to_screen_pos(self, grid_pos: (int, int)) -> (int, int):
		"""Translates coordinates in the grid to the screen position of the topleft corner of the corresponding rect"""
		return self.square_posis[grid_pos[0]][grid_pos[1]]

	def display_map(self, level: Level):
		self.main_surface.fill(BG_COLOR)
		# Draw level
		wall_color = GREY
		for row, obj_row in enumerate(level.map):
			for col, obj in enumerate(obj_row):
				screen_pos = self.grid_to_screen_pos((row, col))
				if obj == utils.Objects.WALL:
					pygame.draw.rect(self.map_surface, wall_color, pygame.rect.Rect(screen_pos, self.square_size))
		pygame.display.update()
