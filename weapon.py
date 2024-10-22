from params import *
from entity import *
from bullet import *

# Superclass of invader & tank.
class Weapon(Entity):
  
  def __init__(self, field, x, y):
    super().__init__(field, x, y)
    self.isAlive = True
  
  def shoot(self):
    # TODO do we even need this?
    # hmm, we might be able to move this here:
    # self.field.bullets.append(bullet)
    pass

# Player-controlled tank.
# Fends off invaders.
class Tank(Weapon):

  def __init__(self, field, x, y):
    super().__init__(field, x, y)
    self.faction = FACTION_TANK
  
  def updatePos(self, x, y):
    self.field.tankMapNext[y][x] = self.field.tank    # Occupy new coordinates.
    super().updatePos(x, y)
  
  def move(self, input):
    # Left key input.
    if input & INPUT_LEFT:
      input &= ~INPUT_LEFT    # Consume input regardless of effect.
      if self.x > 0:
        self.updatePos(self.x-1, self.y)
    
    # Right key input.
    elif input & INPUT_RIGHT:
      input &= ~INPUT_RIGHT   # Consume input regardless of effect.
      if self.x < self.field.width - 1:
        self.updatePos(self.x+1, self.y)
    
    else:
      self.updatePos(self.x, self.y)
    
    return input
  
  # Generate bullet.
  def shoot(self, input):
    # Up key input.
    if input & INPUT_UP:
      input &= ~INPUT_UP      # Consume input regardless of effect.
      if self.field.tankBulletMapCurr[self.y-1][self.x] != None:
        return input          # Space ahead already contains a bullet.
      bullet = Bullet(self.field, self.x, self.y-1, TANK_BULLET_VELOCITY, FACTION_TANK)
      self.field.tankBulletMapCurr[self.y-1][self.x] = bullet
      self.field.bullets.append(bullet)
    
    super().shoot()
    return input

# AI-controlled invader.
# Tries to get past tank.
class Invader(Weapon):

  def __init__(self, field, x, y):
    super().__init__(field, x, y)
    self.faction = FACTION_INVADER
  
  def move(self):
    # TODO, shimmy horizontally,
    # move down vertically if edge has been reached
    return