from random import seed, choice
from params import *
from entity import *
from bullet import *

# Every invader is part of a swarm.
class Swarm(Entity):
  
  def __init__(self, field, x, y, velocity=INVADER_VELOCITY, width=SWARM_WIDTH, height=SWARM_HEIGHT):
    super().__init__(field, x, y)
    self.width = width
    self.height = height
    self.velocity = velocity

    self.invaders = set()
    self.direction = -1
    self.shootTimer = 0
    seed()
  
  # Move entire swarm.
  # Shimmy horizontally,
  # move down vertically if edge has been reached.
  def move(self):
    super().move()
    
    # Don't move invaders if not enough time has passed.
    if self.velocity > self.moveTimer:
      for invader in self.invaders:
        invader.updatePos(invader.x, invader.y)
      return
  
    # Move down vertically if edge has been reached.
    if (((self.direction < 0) and (self.x == 0)) or
        ((self.direction > 0) and (self.x + self.width >= self.field.width - 1))):
      
      # Check if bottom has been reached.
      for invader in self.invaders:
        if invader.y >= self.field.height:
          # TODO Bottom reached, Invaders win
          break
      
      self.direction *= -1      # Change moving direction.
      self.y += 1
      for invader in self.invaders:
        invader.updatePos(invader.x, invader.y + 1)

    # Move horizontally.
    else:
      self.x += self.direction
      for invader in self.invaders:
        invader.updatePos(invader.x + self.direction, invader.y)
  
    # Reset movetimer.
    self.moveTimer -= self.velocity
    return
  
  # Have an invader shoot a bullet periodically.
  def shoot(self):
    self.shootTimer += GAMELOGIC_REFRESH
    
    # Don't shoot if not enough time has passed.
    if self.shootTimer < INVADER_SHOOT_FREQUENCY:
      return
    
    # Don't shoot if there're no invaders left.
    if not len(self.invaders):
      return
    
    # Shoot a bullet from a random invader.
    choice(list(self.invaders)).shoot()
    
    # Reset timer.
    self.shootTimer -= INVADER_SHOOT_FREQUENCY

# Superclass of invader & tank.
class Weapon(Entity):
  
  def __init__(self, field, x, y):
    super().__init__(field, x, y)
  
  def shoot(self):
    # TODO do we even need this?
    # hmm, we might be able to move this here:
    # self.field.bullets.append(bullet)
    pass
  
  # A weapon can die if a bullet hits it.
  def die(self):
    # Also seems superfluous; This routine doesn't do anything.
    pass

# Player-controlled tank.
# Fends off invaders.
class Tank(Weapon):

  def __init__(self, field, x, y):
    super().__init__(field, x, y)
    self.faction = FACTION_TANK
  
  def updatePos(self, x, y):
    self.field.tankMapNext[y][x] = self     # Occupy new coordinates.
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
      self.field.bullets.add(bullet)
    
    super().shoot()
    return input
  
  # Under certain circumstances, tanks can die.
  def die(self):
    super().die()
    self.field.tank = None

# AI-controlled invader.
# Tries to get past tank.
class Invader(Weapon):

  def __init__(self, field, swarm, x, y):
    super().__init__(field, x, y)
    self.swarm = swarm
    self.faction = FACTION_INVADER

  def updatePos(self, x, y):
    self.field.invaderMapNext[y][x] = self    # Occupy new coordinates.
    super().updatePos(x, y)
  
  # Generate bullet
  def shoot(self):
    
    # Don't shoot bullet if ally bullet ahead already.
    if self.field.invaderBulletMapCurr[self.y+1][self.x] != None:
      return
      
    bullet = Bullet(self.field, self.x, self.y+1, INVADER_BULLET_VELOCITY, FACTION_INVADER)
    self.field.invaderBulletMapCurr[self.y+1][self.x] = bullet
    self.field.bullets.add(bullet)
    super().shoot()
    
  # Under certain circumstances, invaders can die.
  def die(self):
    super().die()
    self.swarm.invaders.remove(self)