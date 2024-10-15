from entity import *

# Bullets can be shot from weapons
# bullets can also kill weapons of opposing faction
# if they move to the same space as weapon.
class Bullet(Entity):

  # This simplifies things such that faction determines direction bullet moves in.
  # This means that invaders will always start ABOVE tank and
  # tank will always start BELOW invaders.
  def __init__(self, x, y, velocity, faction):
    super().__init__(x, y)
    self.velocity = velocity
    self.faction = faction
  
  def move(self)
    # TODO move bullet based on velocity & faction/direction
    return