"""A helper module"""

import itertools
import pygame
from enum import Enum, Flag, auto

pygame.init()


class Language(Enum):
	GERMAN = 0
	ENGLISH = 1


class Backgrounds(Enum):
	NONE = 0
	DESERT = 1


class Goals(Enum):
	NONE = 0
	HIGHSCORE = 1
	SURVIVE = 2


class SnakeParts(Enum):
	HEAD = 0
	BODY_STRAIGHT = 1
	BODY_CORNER = 2
	TAIL = 3


class Cntble(Enum):
	DROP_ITEM = 0
	BOMB = 1


class Objects(Flag):
	NONE = auto()
	WALL = auto()
	APPLE = auto()
	MELON = auto()
	COFFEE = auto()
	TEA = auto()
	BEER = auto()
	CHILI = auto()
	BOMB = auto()
	EXPLOSION = auto()
	FIRE_SPIT = auto()


Eatable = Objects.APPLE | Objects.MELON | Objects.COFFEE | Objects.TEA | Objects.BEER | Objects.CHILI
Growing = Objects.APPLE | Objects.MELON
Speeding = Objects.COFFEE | Objects.TEA
Complex = Objects.BEER | Objects.BOMB | Objects.CHILI
Hurting = Objects.WALL | Objects.EXPLOSION
Indestructible = Objects.WALL
MoveStopper = Objects.WALL | Objects.BOMB


def string_to_object(string: str) -> Objects:
	"""Translate a string to the respective Object (wall etc.)"""
	match string:
		case "w":
			return Objects.WALL
		case "a":
			return Objects.APPLE
		case "m":
			return Objects.MELON
		case "c":
			return Objects.COFFEE
		case "t":
			return Objects.TEA
		case "b":
			return Objects.BEER
		case "o":
			return Objects.BOMB
		case "h":
			return Objects.CHILI
		case _:
			return Objects.NONE


def strings_to_objects(strings: [str], sep: str = ",") -> [[Objects]]:
	"""Translate a whole map of strings to the corresponding objects"""
	return [[string_to_object(string) for string in line.split(sep)] for line in strings]


def add_tuples(tuple_list: list[tuple[float, ...]]) -> tuple[float, ...]:
	"""Add all tuples in the list itemwise"""
	return tuple([sum(items) for items in zip(*tuple_list)])


def add_two_tuples(tuple1, tuple2) -> tuple:
	"""Add two tuples itemwise"""
	return add_tuples([tuple1, tuple2])


def subtract_tuples(tuple1: tuple[float, ...], tuple2: tuple[float, ...]) -> tuple[float, ...]:
	"""Subtract tuples itemwise"""
	return tuple([a - b for a, b in itertools.zip_longest(tuple1, tuple2, fillvalue=0)])


def subtract_tuples_int(tuple1: tuple[float, ...], tuple2: tuple[float, ...]) -> tuple[int, ...]:
	"""Subtract tuples itemwise and cast to int"""
	return tuple([int(a - b) for a, b in itertools.zip_longest(tuple1, tuple2, fillvalue=0)])


def multiply_tuple(tuple1: tuple[float, ...], scalar: float) -> tuple[float, ...]:
	"""Multiply tuple with a scalar itemwise"""
	return tuple([a * scalar for a in tuple1])


def mult_tuple_to_int(tuple1: tuple[float, ...], scalar: float) -> tuple[int, ...]:
	"""Multiply tuple with a scalar itemwise and cast the result to integer"""
	return tuple([int(a * scalar) for a in tuple1])


def tuple_to_int(tuple1: tuple[float, ...]) -> tuple[int, ...]:
	"""Cast all elements of the tuple to int"""
	return tuple([int(a) for a in tuple1])


def get_tuple_signs(tuple1: tuple[float, ...]) -> tuple[int, ...]:
	"""Map a tuple of numbers to a tuple of 1, 0 or -1, based on the sign of each integer"""
	return tuple([1 if a > 0 else -1 if a < 0 else 0 for a in tuple1])


def get_next_squares(pos: (int, int), direction: (int, int), num_squares: int) -> [(int, int)]:
	"""Return the next squares, starting from the given pos in the given direction"""
	return [add_two_tuples(pos, mult_tuple_to_int(direction, i)) for i in range(1, num_squares + 1)]


def get_spit_fire_squares(pos: (int, int), direction: (int, int), num_squares: int, map: [[Objects]]) -> [(int, int)]:
	"""Return the next squares, starting from the given pos in the given direction,
	but stop if an indestructible Object is in the way"""
	next_squares = get_next_squares(pos, direction, num_squares)
	for idx, square in enumerate(next_squares):
		row, col = square
		if row >= len(map) or col >= len(map[row]) or map[row][col] in Indestructible:
			return next_squares[0:idx]
	return next_squares


def play_music_track(filename: str, volume: float = 1.0) -> None:
	"""
	Change the music track and play it.

	:param filename: Filename of the music track
	:param volume: Music volume
	"""
	pygame.mixer_music.load(filename)
	pygame.mixer_music.set_volume(volume)
	pygame.mixer_music.play(loops=-1)


def check_allowed_keys(pygame_key: int) -> bool:
	"""Transform an int representing a pygame key constant to the corresponding char"""
	# Check pygame_key against allowed keys
	allowed_keys = [
		pygame.K_a,
		pygame.K_b,
		pygame.K_c,
		pygame.K_d,
		pygame.K_e,
		pygame.K_f,
		pygame.K_g,
		pygame.K_h,
		pygame.K_i,
		pygame.K_j,
		pygame.K_k,
		pygame.K_l,
		pygame.K_m,
		pygame.K_n,
		pygame.K_o,
		pygame.K_p,
		pygame.K_q,
		pygame.K_r,
		pygame.K_s,
		pygame.K_t,
		pygame.K_u,
		pygame.K_v,
		pygame.K_w,
		pygame.K_x,
		pygame.K_y,
		pygame.K_z,
		228,
		246,
		252,
		pygame.K_LESS,
		pygame.K_COMMA,
		pygame.K_PERIOD,
		pygame.K_MINUS,
		pygame.K_HASH,
		pygame.K_PLUS,
		pygame.K_CARET,
		pygame.K_1,
		pygame.K_2,
		pygame.K_3,
		pygame.K_4,
		pygame.K_5,
		pygame.K_6,
		pygame.K_7,
		pygame.K_8,
		pygame.K_9,
		pygame.K_0,
		223,
		180,
		pygame.K_RIGHT,
		pygame.K_DOWN,
		pygame.K_LEFT,
		pygame.K_UP,
		pygame.K_KP_1,
		pygame.K_KP_2,
		pygame.K_KP_3,
		pygame.K_KP_4,
		pygame.K_KP_5,
		pygame.K_KP_6,
		pygame.K_KP_7,
		pygame.K_KP_8,
		pygame.K_KP_9,
		pygame.K_KP_0,
		pygame.K_KP_PERIOD,
		pygame.K_KP_PLUS,
		pygame.K_KP_DIVIDE,
		pygame.K_KP_MULTIPLY,
		pygame.K_KP_MINUS
	]
	return pygame_key in allowed_keys


def get_descr_from_pygame_key(pygame_key: int) -> str:
	"""Replace some pygame descriptions with smaller ones for a better visual"""
	replace = {pygame.K_UP: "↑", pygame.K_DOWN: "↓", pygame.K_LEFT: "←", pygame.K_RIGHT: "→",
			   pygame.K_KP_1: "KP1", pygame.K_KP_2: "KP2", pygame.K_KP_3: "KP3", pygame.K_KP_4: "KP4", pygame.K_KP_5: "KP5", pygame.K_KP_6: "KP6", pygame.K_KP_7: "KP7", pygame.K_KP_8: "KP8", pygame.K_KP_9: "KP9", pygame.K_KP_0: "KP0",
			   pygame.K_KP_PERIOD: "KP.", pygame.K_KP_PLUS: "KP+", pygame.K_KP_DIVIDE: "KP/", pygame.K_KP_MULTIPLY: "KP*", pygame.K_KP_MINUS: "KP-",
			   pygame.K_a: "A", pygame.K_b: "B", pygame.K_c: "C", pygame.K_d: "D", pygame.K_e: "E", pygame.K_f: "F", pygame.K_g: "G", pygame.K_h: "H", pygame.K_i: "I", pygame.K_j: "J", pygame.K_k: "K", pygame.K_l: "L", pygame.K_m: "M",
			   pygame.K_n: "N", pygame.K_o: "O", pygame.K_p: "P", pygame.K_q: "Q", pygame.K_r: "R", pygame.K_s: "S", pygame.K_t: "T", pygame.K_u: "U", pygame.K_v: "V", pygame.K_w: "W", pygame.K_x: "X", pygame.K_y: "Y", pygame.K_z: "Z"}
	return replace[pygame_key] if pygame_key in replace else pygame.key.name(pygame_key)


def get_time_string_for_ms(ms: int) -> str:
	"""Return a time string in format mm:ss for the given number of milliseconds"""
	seconds = int(ms / 1000)
	return "{}:{}".format(int(seconds / 60), str(seconds % 60).zfill(2))
