# Field upon which invaders and tank clash.
# Contains a three-dimensional array of entities.

# NOTE. Should put weapons on one map and list bullets, this should make movement of weapons and bullets & impact of bullets easy to keep track of. Likewise, victory & loss conditions should be easy to check this way.

import math
from params import *
from weapon import *

class MultipleInvadersOnTileError(Exception):
  pass

class MultipleTanksOnTileError(Exception):
  pass

class Field:

  def __init__(self, width = DEFAULT_FIELD_WIDTH, height = DEFAULT_FIELD_HEIGHT):
    self.width = width
    self.height = height
    
    # Maps for each entity.
    self.invaderMap = [[None for x in range(width)] for y in range(height)]
    self.tankMap = [[None for x in range(width)] for y in range(height)]
    self.invaderBulletMap = [[None for x in range(width)] for y in range(height)]
    self.tankBulletMap = [[None for x in range(width)] for y in range(height)]

  def spawnInvader(self, x, y):
    try:
      if self.invaderMap[y][x] != None:
        raise MultipleInvadersOnTileError("Attempted to generate invader on a tile already occupied by an invader.")
      else:
        self.invaderMap[y][x] = Invader(x, y)
    except Exception as e:
      print("An error occurred: ", e)
      print("Exiting program due to error: ", e)
      exit()
    
  def spawnTank(self, x, y):
    try:
      if self.tankMap[y][x] != None:
        raise MultipleTanksOnTileError("Attempted to generate tank on a tile already occupied by a tank.")
      else:
        self.tankMap[y][x] = Tank(x, y)
    except Exception as e:
      print("An error occurred: ", e)
      print("Exiting program due to error: ", e)
      exit()

  # Generate entities at the start of game.
  def initEntities(self):
  
    # Generate invaders.
    # We attempt to spread invaders evenly in their territory,
    # Whilst leaving room left and right for them to move to.
    invaderTerritoryStart = (DEFAULT_FIELD_WIDTH - DEFAULT_SWARM_WIDTH) >> 1
    invaderTerritoryEnd = invaderTerritoryStart + DEFAULT_SWARM_WIDTH
    invaderTerritorySize = DEFAULT_SWARM_WIDTH * DEFAULT_SWARM_HEIGHT
    step = math.floor(invaderTerritorySize / DEFAULT_SWARM_SIZE)
    
    x = invaderTerritoryStart
    y = 0
    self.invaderCount = 0
    while y < DEFAULT_SWARM_HEIGHT:
      while x < invaderTerritoryEnd:
        self.spawnInvader(x, y)
        self.invaderCount += 1
        x += step
      x -= DEFAULT_SWARM_WIDTH
      y += 1
    
    # Generate tank.
    # We generate one tank.
    # FUTURE PROOFING: trying to keep in mind the
    # option to generate more tanks for multiplayer.
    # Bottom row of field is tank territory.
    self.spawnTank(self.width >> 1, self.height - 1)
  
  # Draw the field to the terminal by outputting characters.
  def drawField(self):
  
    # Header.
    header = ''.join([FRAME_SYMBOL for x in range(self.width + 2)])
    print(header, end='')
    
    # Main screen
    y = 0
    while y < self.height:
      print('\n' + FRAME_SYMBOL, end='')
      x = 0
      while x < self.width:
        symbol = EMPTY_SYMBOL
        
        # Draw invaders.
        if self.invaderMap[y][x] != None:
          symbol = INVADER_SYMBOL
          if not self.invaderMap[y][x].isAlive:
            symbol = EXPLOSION_SYMBOL
        
        # Draw tanks.
        elif self.tankMap[y][x] != None:
          symbol = TANK_SYMBOL
          if not self.tankMap[y][x].isAlive:
            symbol = EXPLOSION_SYMBOL
        
        # Draw bullets.
        elif self.invaderBulletMap[y][x] != None:
          symbol = INVADER_BULLET_SYMBOL
          if self.tankBulletMap[y][x] != None:
            symbol = BOTH_BULLET_SYMBOL
        elif self.tankBulletMap[y][x] != None:
          symbol = TANK_BULLET_SYMBOL
        
        print(symbol, end='')
        x += 1
        
      print(FRAME_SYMBOL, end='')
      y += 1
    
    # Footer.
    print('\n' + header)