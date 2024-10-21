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
INPUT_LEFT = False
INPUT_KEY_LEFT_PRESS = False
INPUT_RIGHT = False
INPUT_KEY_RIGHT_PRESS = False
INPUT_UP = False
INPUT_KEY_UP_PRESS = False

def setKeyPressFlags(key):
  global INPUT_KEY_LEFT_PRESS
  global INPUT_LEFT
  global INPUT_KEY_RIGHT_PRESS
  global INPUT_RIGHT
  global INPUT_KEY_UP_PRESS
  global INPUT_UP

  if (not INPUT_KEY_RIGHT_PRESS) and (key == Key.right):
    #print("right pressed")
    INPUT_KEY_RIGHT_PRESS = True
    INPUT_RIGHT = True
  elif (not INPUT_KEY_LEFT_PRESS) and (key == Key.left):
    #print("left pressed")
    INPUT_KEY_LEFT_PRESS = True
    INPUT_LEFT = True
  elif (not INPUT_KEY_UP_PRESS) and (key == Key.up):
    INPUT_KEY_UP_PRESS = True
    INPUT_UP = True

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
    endTime = time.time() + 0.1
    
    clearScreen()
    field.drawField()
    
    curTime = time.time()
    if curTime < endTime:
      time.sleep(endTime - curTime)

# Adjusts entities' position based on key input.
def handlePlayerInput(field):
  global INPUT_LEFT
  global INPUT_RIGHT
  global INPUT_UP
  
  x = field.tank.x
  y = field.tank.y
  
  # Left key input.
  if INPUT_LEFT:
    INPUT_LEFT = False    # Consume input regardless of effect.
    if x > 0:
      INPUT_LEFT = False
      field.tankMap[y][x] = None
      field.tankMap[y][x-1] = field.tank
      field.tank.x -= 1
  
  # Right key input.
  if INPUT_RIGHT:
    INPUT_RIGHT = False   # Consume input regardless of effect.
    if x < field.width - 1:
      field.tankMap[y][x] = None
      field.tankMap[y][x+1] = field.tank
      field.tank.x += 1
  
  # Up key input.
  if INPUT_UP:
    INPUT_UP = False      # Consume input regardless of effect.
    # TODO

def runGameLogic(field):
  timeOut = time.time() + 20
  curTime = time.time()
  
  while curTime < timeOut:
    endTime = time.time() + 0.05
    
    # Logic here.
    # End thread if game is over.
    
    handlePlayerInput(field)
    #inputThread = Thread(target=readPlayerInput, args=(field,), daemon=True)
    #inputThread.start()
    
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