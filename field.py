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

  def __init__(self, width=FIELD_WIDTH, height=FIELD_HEIGHT):
    self.width = width
    self.height = height
    self.tank = None
    self.bullets = list()
    self.swarm = None
    
    # Maps for each entity.
    # 'Next' maps are used whilst entities move
    # during game logic.
    self.invaderMapCurr = [[None for x in range(width)] for y in range(height)]
    self.invaderMapNext = list()
    self.tankMapCurr = [[None for x in range(width)] for y in range(height)]
    self.tankMapNext = list()
    self.invaderBulletMapCurr = [[None for x in range(width)] for y in range(height)]
    self.invaderBulletMapNext = list()
    self.tankBulletMapCurr = [[None for x in range(width)] for y in range(height)]
    self.tankBulletMapNext = list()

  def spawnInvaderSwarm(self, width=SWARM_WIDTH, height=SWARM_HEIGHT):
  
    # We attempt to spread invaders evenly in their territory,
    # Whilst leaving room left and right for them to move to.
    invaderTerritoryStart = (self.width - width) >> 1
    invaderTerritoryEnd = invaderTerritoryStart + width
    invaderTerritorySize = width * height
    step = math.floor(invaderTerritorySize / SWARM_SIZE)
    
    self.swarm = Swarm(self, invaderTerritoryStart, 0, INVADER_VELOCITY, width, height)
    x = invaderTerritoryStart
    y = 0
    self.invaderCount = 0
    while y < height:
      while x < invaderTerritoryEnd:
        self.spawnInvader(x, y)
        self.invaderCount += 1
        x += step
      x -= SWARM_WIDTH
      y += 1

  def spawnInvader(self, x, y):
    try:
      if self.invaderMapCurr[y][x] != None:
        raise MultipleInvadersOnTileError("Attempted to generate invader on a tile already occupied by an invader.")
      else:
        invader = Invader(self, self.swarm, x, y)
        self.invaderMapCurr[y][x] = invader
        self.swarm.invaders.append(invader)
    except Exception as e:
      print("An error occurred: ", e)
      print("Exiting program due to error: ", e)
      exit()
    
  def spawnTank(self, x, y):
    try:
      if self.tankMapCurr[y][x] != None:
        raise MultipleTanksOnTileError("Attempted to generate tank on a tile already occupied by a tank.")
      else:
        self.tank = Tank(self, x, y)
        self.tankMapCurr[y][x] = self.tank
    except Exception as e:
      print("An error occurred: ", e)
      print("Exiting program due to error: ", e)
      exit()

  # Generate entities at the start of game.
  def initEntities(self):
    
    # Generate invaders.
    self.spawnInvaderSwarm(SWARM_WIDTH, SWARM_HEIGHT)
    
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
        if self.invaderMapCurr[y][x] != None:
          symbol = INVADER_SYMBOL
          if not self.invaderMapCurr[y][x].isAlive:
            symbol = EXPLOSION_SYMBOL
        
        # Draw tanks.
        elif self.tankMapCurr[y][x] != None:
          symbol = TANK_SYMBOL
          if not self.tankMapCurr[y][x].isAlive:
            symbol = EXPLOSION_SYMBOL
        
        # Draw bullets.
        elif self.invaderBulletMapCurr[y][x] != None:
          symbol = INVADER_BULLET_SYMBOL
          if self.tankBulletMapCurr[y][x] != None:
            symbol = BOTH_BULLET_SYMBOL
        elif self.tankBulletMapCurr[y][x] != None:
          symbol = TANK_BULLET_SYMBOL
        
        print(symbol, end='')
        x += 1
        
      print(FRAME_SYMBOL, end='')
      y += 1
    
    # Footer.
    print('\n' + header)
  
  # Empties 'Next' buffer tilemaps.
  def clearNextMaps(self):
    self.invaderMapNext = [[None for x in range(self.width)] for y in range(self.height)]
    self.tankMapNext = [[None for x in range(self.width)] for y in range(self.height)]
    self.invaderBulletMapNext = [[None for x in range(self.width)] for y in range(self.height)]
    self.tankBulletMapNext = [[None for x in range(self.width)] for y in range(self.height)]
  
  # Moves next tilemaps into current tilemaps.
  def updateMaps(self):
    self.invaderMapCurr = self.invaderMapNext
    self.tankMapCurr = self.tankMapNext
    self.invaderBulletMapCurr = self.invaderBulletMapNext
    self.tankBulletMapCurr = self.tankBulletMapNext