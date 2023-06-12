"""A multiplayer cooperative snake game

import structure:

friendly_snakes
|-- communicator (incl. the main game loop)
|	|-- menu
|	|-- game
|	|	|-- graphics
|	|	|	|-- snake
|	|	|	|-- level
Additionally, the utils and constants class are widely used and imported in almost every module.
"""

# ----- Imports --------
import sys
from communicator import Communicator

# ----- Main script ----
if __name__ == "__main__":
	comm = Communicator()
	sys.exit(comm.start())
