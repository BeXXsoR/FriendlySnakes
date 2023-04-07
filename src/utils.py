import itertools
from enum import Enum


class Objects(Enum):
	NONE = 0
	WALL = 1


def string_to_object(string: str) -> Objects:
	"""Translate a string to the respective Object (wall etc.)"""
	match string:
		case "w": return Objects.WALL
		case _: return Objects.NONE


def strings_to_objects(strings: [[str]], sep: str = ",") -> [[Objects]]:
	"""Translate a whole map of strings to the corresponding objects"""
	return [[string_to_object(string) for string in line.split(sep)] for line in strings]


def add_tuples(tuple_list: [()]) -> [()]:
	"""Add all tuples in the list itemwise"""
	return tuple([sum(items) for items in zip(*tuple_list)])


def subtract_tuples(tuple1: tuple, tuple2: tuple) -> tuple:
	"""Subtract tuples itemwise"""
	return tuple([a - b for a, b in itertools.zip_longest(tuple1, tuple2, fillvalue=0)])


def multiply_tuple(tuple1: tuple, scalar: float) -> tuple:
	"""Multiply tuple with a scalar itemwise"""
	return tuple([a * scalar for a in tuple1])


def mult_tuple_to_int(tuple1: tuple, scalar: float) -> tuple:
	"""Multiply tuple with a scalar itemwise and cast the result to integer"""
	return tuple([int(a * scalar) for a in tuple1])


def get_tuple_signs(tuple1: tuple) -> tuple:
	return tuple([1 if a > 0 else -1 if a < 0 else 0 for a in tuple1])
