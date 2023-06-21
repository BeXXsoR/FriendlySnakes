"""Setup file for cx_Freeze"""

from cx_Freeze import setup, Executable

build_exe_options = {
	"packages": ["pygame"],
	"includes": ["animations", "communicator", "constants", "game", "graphics", "level", "menu", "snake", "utils"],
	"build_exe": "../build_win64",
	"silent_level": 1
}

setup(
	name="Friendly Snakes",
	options={"build_exe": build_exe_options},
	executables=[Executable("friendly_snakes.py")]
)
