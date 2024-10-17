from params import *
from entity import *

# Superclass of invader & tank.
class Weapon(Entity):
  
  def __init__(self, x, y):
    super().__init__(x, y)
    self.isAlive = True
  
  def shoot():
    # TODO Generate bullet
    return

# Player-controlled tank.
# Fends off invaders.
class Tank(Weapon):

  def __init__(self, x, y):
    super().__init__(x, y)
    self.faction = FACTION_TANK
  
  def move(self, input):
    # TODO, use given input
    return

# AI-controlled invader.
# Tries to get past tank.
class Invader(Weapon):

  def __init__(self, x, y):
    super().__init__(x, y)
    self.faction = FACTION_INVADER
  
  def move(self):
    # TODO, shimmy horizontally,
    # move down vertically if edge has been reached
    return