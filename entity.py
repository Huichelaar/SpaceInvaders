# Entities are weapons and bullets;
# Basically, anything that moves.
from params import GAMELOGIC_REFRESH
from field import *

class Entity:

  def __init__(self, field, x, y):
    self.moveTimer = 0              # Used to limit how many movement actions
                                    # entity performs in a given period of time.
    self.field = field              # Entities are on a field.
    self.x = x
    self.y = y
    self.faction = FACTION_NEUTRAL  # Placeholder faction.
  
  # All entities can move.
  def move(self):
    self.moveTimer += GAMELOGIC_REFRESH
  
  # Change/Update position.
  def updatePos(self, x, y):
    self.x = x
    self.y = y