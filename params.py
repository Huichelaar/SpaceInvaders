# Parameters.
import math

# Change as desired.
FIELD_WIDTH = 50
FIELD_HEIGHT = 15
SWARM_WIDTH = math.floor(FIELD_WIDTH / 5 * 2)
SWARM_HEIGHT = math.floor(FIELD_HEIGHT / 3 * 2)
SWARM_SIZE = 80#(SWARM_WIDTH * SWARM_HEIGHT) >> 3

INVADER_SYMBOL = 'S'
INVADER_BULLET_SYMBOL = '|'
INVADER_PLUS_BULLET_SYMBOL = '$'
TANK_SYMBOL = 'U'
TANK_BULLET_SYMBOL = '^'
BOTH_BULLET_SYMBOL = '#'
EMPTY_SYMBOL = ' '
FRAME_SYMBOL = '|'

TIME_OUT = 300                  # Game ends automatically after this many seconds have passed.

SCREEN_REFRESH = 0.1            # Re-draw screen every SCREEN_REFRESH seconds.
GAMELOGIC_REFRESH = 0.1         # Re-run game logic, including reading input, every GAMELOGIC_REFRESH seconds.

TANK_BULLET_VELOCITY = -0.2     # Time in seconds for bullet to move 1 tile. Negative for moving up.
INVADER_VELOCITY = 0.25         # Time in seconds for invader swarm to move.
INVADER_BULLET_VELOCITY = 0.5   # Time in seconds for bullet to move 1 tile. Positive for moving down.
INVADER_SHOOT_FREQUENCY = 2     # Time in seconds for another bullet to be shot by an invader.


# Enums, don't touch these!
FACTION_NEUTRAL = 0             # Default faction.
FACTION_TANK = 1
FACTION_INVADER = 2

INPUT_LEFT = 1 << 0
INPUT_RIGHT = 1 << 1
INPUT_UP = 1 << 2

GAME_ONGOING = 0
GAME_VICTORY = 1
GAME_DEFEAT = 2
GAME_TIMEOUT = 3