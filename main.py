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

def refreshGameScreen(field):
  timeOut = time.time() + 20
  curTime = time.time()
  
  while curTime < timeOut:
    endTime = time.time() + SCREEN_REFRESH
    
    clearScreen()
    field.drawField()
    
    curTime = time.time()
    if curTime < endTime:
      time.sleep(endTime - curTime)

# Adjusts entities' position based on key input.
# Shoots bullets based on key input.
def handlePlayerInput(tank):
  global INPUT_BITFIELD

  INPUT_BITFIELD = tank.move(INPUT_BITFIELD)
  INPUT_BITFIELD = tank.shoot(INPUT_BITFIELD)

# Moves bullets.
def moveBullets(field):
  for bullet in field.bullets:
    bullet.move()

def runGameLogic(field):
  timeOut = time.time() + 20
  curTime = time.time()
  
  while curTime < timeOut:
    endTime = time.time() + GAMELOGIC_REFRESH
    
    # Logic here.
    # End thread if game is over.
    
    # Clear next maps.
    field.clearNextMaps()
    
    # Handle entities.
    handlePlayerInput(field.tank)   # Tank
    # TODO                          # Invaders
    moveBullets(field)              # Bullets
    
    # Copy next maps to current maps.
    field.updateMaps()
    
    curTime = time.time()
    if curTime < endTime:
      time.sleep(endTime - curTime)
  
  print("\n")

def main():

  # Potential expansion: allow user to input params.
  field = Field(DEFAULT_FIELD_WIDTH, DEFAULT_FIELD_HEIGHT)
  field.initEntities()
  
  gameLogicThread = Thread(target=runGameLogic, args=(field,), daemon=True)
  gameLogicThread.start()
  
  listener = keyboard.Listener(on_press=setKeyPressFlags, on_release=setKeyReleaseFlags)
  listener.start()
  
  gameRefreshThread = Thread(target=refreshGameScreen, args=(field,), daemon=True)
  gameRefreshThread.start()
  
  while gameRefreshThread.is_alive():
    time.sleep(0.5)
  
  return

main()