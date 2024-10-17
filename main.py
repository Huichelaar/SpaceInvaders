# Space Invaders. No walls, to keep things simple.
from params import *
from field import *

def main():

  # Potential expansion: allow user to input params.
  field = Field(DEFAULT_FIELD_WIDTH, DEFAULT_FIELD_HEIGHT)
  field.initEntities()
  
  field.drawField()
  
  return

main()