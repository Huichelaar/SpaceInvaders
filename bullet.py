from entity import *

# Bullets can be shot from weapons
# bullets can also kill weapons of opposing faction
# if they move to the same space as weapon.
class Bullet(Entity):

  # Velocity is given as time (in seconds) required for bullet to move one tile.
  # Velocity also determines direction bullet fires in.
  # Negative velocity bullets move up.
  # Positive velocity bullets move down.
  def __init__(self, field, x, y, velocity, faction):
    super().__init__(field, x, y)
    self.velocity = velocity
    self.faction = faction
  
  # Move bullet based on velocity & faction/direction.
  def move(self):
    super().move()
    
    # Don't move bullet if not enough time has passed.
    # Do kill invaders/tanks if same spot is occupied.
    if abs(self.velocity) > self.moveTimer:
      if (self.faction == FACTION_TANK):
        if (self.field.invaderMapNext[self.y][self.x]):
          self.kill(self.field.invaderMapNext[self.y][self.x])  # Kill invader.
        else:
          self.field.tankBulletMapNext[self.y][self.x] = self
        pass
      elif (self.faction == FACTION_INVADER):
        if (self.field.tankMapNext[self.y][self.x]):
          self.kill(self.field.tankMapNext[self.y][self.x])     # Kill tank.
        else:
          self.field.invaderBulletMapNext[self.y][self.x] = self
        pass
      return
    
    # Move bullet and kill first thing that crosses its path.
    distance = round(self.moveTimer / self.velocity)      # TODO handle zerodivision error
    incr = distance / abs(distance)                       # TODO handle zerodivision error
    deltaY = 0                                            # Currently travelled distance.
    while deltaY != distance:
      deltaY += incr
      
      if (deltaY + self.y < 0):
        return    # Bullet travelled offscreen.
      if (deltaY + self.y > self.field.height - 1):
        return    # Bullet travelled offscreen.
      
      if (self.faction == FACTION_TANK) and (self.field.invaderMapNext[self.y][self.x] != None):
        self.kill(self.field.invaderMapNext[self.y][self.x])  # Kill invader.
        return
      elif (self.faction == FACTION_INVADER) and (self.field.tankMapNext[self.y][self.x] != None):
        self.kill(self.field.tankMapNext[self.y][self.x])     # Kill tank.
        return
    
    # Nothing to kill, place bullet.
    if self.faction == FACTION_TANK:
      self.field.tankBulletMapNext[self.y + distance][self.x] = self
    else:
      self.field.invaderBulletMapNext[self.y + distance][self.x] = self
    
    # Reset movetimer.
    self.moveTimer -= abs(self.velocity)
    
    # Update position.
    super().updatePos(self.x, self.y + distance)
  
  # Bullets can kill weapons.
  def kill(self, weapon):
    self.field.bullets.remove(self)   # Bullet is consumed when it kills.
    weapon.die()