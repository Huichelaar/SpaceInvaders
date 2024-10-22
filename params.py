# Parameters.
import math

# Change as desired.
DEFAULT_FIELD_WIDTH = 50
DEFAULT_FIELD_HEIGHT = 15
DEFAULT_SWARM_WIDTH = math.floor(DEFAULT_FIELD_WIDTH / 5 * 2)
DEFAULT_SWARM_HEIGHT = math.floor(DEFAULT_FIELD_HEIGHT / 3 * 2)
DEFAULT_SWARM_SIZE = 80#(DEFAULT_SWARM_WIDTH * DEFAULT_SWARM_HEIGHT) >> 3

INVADER_SYMBOL = 'A'
INVADER_BULLET_SYMBOL = 'v'
TANK_SYMBOL = 'U'
TANK_BULLET_SYMBOL = '^'
BOTH_BULLET_SYMBOL = '|'
EXPLOSION_SYMBOL = '@'
EMPTY_SYMBOL = ' '
FRAME_SYMBOL = '|'

SCREEN_REFRESH = 0.1            # Re-draw screen every SCREEN_REFRESH seconds.
GAMELOGIC_REFRESH = 0.1         # Re-run game logic, including reading input, every GAMELOGIC_REFRESH seconds.

TANK_BULLET_VELOCITY = -0.2     # Time in seconds for bullet to move 1 tile. Negative for moving up.
INVADER_BULLET_VELOCITY = 0.5   # Time in seconds for bullet to move 1 tile. Positive for moving down.


# Enums, don't touch these!
FACTION_TANK = 0
FACTION_INVADER = 1

INPUT_LEFT = 1 << 0
INPUT_RIGHT = 1 << 1
INPUT_UP = 1 << 2