# Space Invaders. No walls, to keep things simple.
import os
import time
from pynput import keyboard
from pynput.keyboard import Key
from threading import Thread
from params import *
from field import *

# Globals
# Keys, true if pressed, false otherwise.
INPUT_KEY_LEFT_PRESS = False
INPUT_KEY_RIGHT_PRESS = False
INPUT_KEY_UP_PRESS = False

# Input bitfield tracks input that still needs to be handled.
INPUT_BITFIELD = 0

# Bool, False if game is not over yet.
GAME_OVER = False

def setKeyPressFlags(key):
  global INPUT_KEY_LEFT_PRESS
  global INPUT_KEY_RIGHT_PRESS
  global INPUT_KEY_UP_PRESS
  global INPUT_BITFIELD

  if (not INPUT_KEY_LEFT_PRESS) and (key == Key.left):
    #print("left pressed")
    INPUT_KEY_LEFT_PRESS = True
    INPUT_BITFIELD |= INPUT_LEFT
  elif (not INPUT_KEY_RIGHT_PRESS) and (key == Key.right):
    #print("right pressed")
    INPUT_KEY_RIGHT_PRESS = True
    INPUT_BITFIELD |= INPUT_RIGHT
  elif (not INPUT_KEY_UP_PRESS) and (key == Key.up):
    #print("up pressed")
    INPUT_KEY_UP_PRESS = True
    INPUT_BITFIELD |= INPUT_UP

def setKeyReleaseFlags(key):
  global INPUT_KEY_RIGHT_PRESS
  global INPUT_KEY_LEFT_PRESS
  global INPUT_KEY_UP_PRESS

  if key == Key.right:
    #print("right released")
    INPUT_KEY_RIGHT_PRESS = False
  if key == Key.left:
    #print("left released")
    INPUT_KEY_LEFT_PRESS = False
  if key == Key.up:
    INPUT_KEY_UP_PRESS = False
  
# https://stackoverflow.com/a/684344
def clearScreen():
  os.system('cls' if os.name=='nt' else 'clear')

def displayEndState(field):
  if (field.state == GAME_VICTORY):
    print("Victory!")
  elif (field.state == GAME_DEFEAT):
    print("Defeat!")
  elif (field.state == GAME_TIMEOUT):
    print("Time out!")
  else:
    print("Game over!")

def refreshGameScreen(field):
  global GAME_OVER
  
  while not GAME_OVER:
    endTime = time.time() + SCREEN_REFRESH
    
    clearScreen()
    field.drawField()
    
    curTime = time.time()
    if curTime < endTime:
      time.sleep(endTime - curTime)
  
  # Display which faction has won if game has ended.
  displayEndState(field)

# Adjusts tank position based on key input.
# Shoots bullets based on key input.
def runTank(tank):
  global INPUT_BITFIELD

  # Nothing to return if no tank.
  if tank == None:
    return

  INPUT_BITFIELD = tank.move(INPUT_BITFIELD)
  INPUT_BITFIELD = tank.shoot(INPUT_BITFIELD)

# Moves invaders.
# Shoots bullets periodically.
def runInvaders(field):
  field.swarm.move()
  field.swarm.shoot()

# Moves bullets.
def moveBullets(field):
  # Moving bullets will be consumed if they kill a weapon,
  # Therefore we make a copy first.
  bulletsCopy = field.bullets.copy()

  for bullet in bulletsCopy:
    bullet.move()

def runGameLogic(field):
  global GAME_OVER

  timeOut = time.time() + TIME_OUT
  curTime = time.time()
  
  while True:
    endTime = time.time() + GAMELOGIC_REFRESH
    
    # Logic here.
    # End thread if game is over.
    
    # Clear next maps.
    field.clearNextMaps()
    
    # Handle entities.
    runTank(field.tank)             # Tank
    runInvaders(field)              # Invaders
    moveBullets(field)              # Bullets
    
    # Copy next maps to current maps.
    field.updateMaps()
    
    # End game if a faction has won.
    if field.state != GAME_ONGOING:
      break
    
    # End game if time-out has been reached.
    if curTime >= timeOut:
      field.state = GAME_TIMEOUT
      break
    
    curTime = time.time()
    if curTime < endTime:
      time.sleep(endTime - curTime)
  
  GAME_OVER = True

def main():

  # Potential expansion: allow user to input params.
  field = Field(FIELD_WIDTH, FIELD_HEIGHT)
  field.initEntities()
  
  gameLogicThread = Thread(target=runGameLogic, args=(field,), daemon=True)
  gameLogicThread.start()
  
  listener = keyboard.Listener(on_press=setKeyPressFlags, on_release=setKeyReleaseFlags)
  listener.start()
  
  gameRefreshThread = Thread(target=refreshGameScreen, args=(field,), daemon=True)
  gameRefreshThread.start()
  
  while gameLogicThread.is_alive():
    time.sleep(0.5)
  
  listener.stop()
  
  return

main()