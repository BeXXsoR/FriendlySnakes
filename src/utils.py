"""A helper module"""

import itertools
from enum import Enum, Flag, auto


class SnakeParts(Enum):
	HEAD = 0
	BODY_STRAIGHT = 1
	BODY_CORNER = 2
	TAIL = 3


class Objects(Flag):
	NONE = auto()
	WALL = auto()
	APPLE = auto()
	MELON = auto()
	COFFEE = auto()
	TEA = auto()
	BEER = auto()


Eatable = Objects.APPLE | Objects.MELON | Objects.COFFEE | Objects.TEA | Objects.BEER
Growing = Objects.APPLE | Objects.MELON
Speeding = Objects.COFFEE | Objects.TEA
Complex = Objects.BEER


def string_to_object(string: str) -> Objects:
	"""Translate a string to the respective Object (wall etc.)"""
	match string:
		case "w": return Objects.WALL
		case "a": return Objects.APPLE
		case "m": return Objects.MELON
		case "c": return Objects.COFFEE
		case "t": return Objects.TEA
		case "b": return Objects.BEER
		case _: return Objects.NONE


def strings_to_objects(strings: [str], sep: str = ",") -> [[Objects]]:
	"""Translate a whole map of strings to the corresponding objects"""
	return [[string_to_object(string) for string in line.split(sep)] for line in strings]


def add_tuples(tuple_list: list[tuple[float, ...]]) -> tuple[float, ...]:
	"""Add all tuples in the list itemwise"""
	return tuple([sum(items) for items in zip(*tuple_list)])


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
