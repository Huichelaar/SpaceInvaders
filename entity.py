# Entities are weapons and bullets;
# Basically, anything that moves.
class Entity:

  def __init__(self, x, y):
    self.x = x
    self.y = y
  
  # Change/Update position.
  def updatePos(self, x, y):
    self.x = x
    self.y = y