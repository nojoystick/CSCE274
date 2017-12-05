import state_interface
import threading
import random

#Global Constants
MOVING = False # Is the robot currently moving
LSPEED = 0
RSPEED = 0

###############################################################################
# FOLLOW WALL
#
def FollowWall():
  global MOVING
  global LSPEED
  global RSPEED

  while 1:
   # Reset driving speed to drive straight every iteration after the correction.
    LSPEED = 50
    RSPEED = 50
    # Case: wheel drop detected
    if wheelDrop:
      connection.stop()
      connection.song()
      MOVING = False
      break
    # Case: cliff detected
    elif cliff != 0:
      connection.stop()
      connection.obstacle()
    # Case: Bump sensed left, right, or both
    # Bump sensor is turned off if the dock has been found
    elif bumpLeft:
      connection.stop()
      connection.turnClockwise()
    elif bumpRight:
      connection.stop()
      connection.turnCounterClockwise()
    elif bumpLeft and bumpRight:
      connection.stop()
      connection.obstacle()
    
    # Case: Dock has not been found; execute wall following PD 
    u = connection.pd()
    if u > 14:
      LSPEED = 30
      RSPEED = 20
    elif (u >= 9 and u <= 11):
      LSPEED = 150 + u
      RSPEED = 35 - u
    else:
      LSPEED = 35 + u
      RSPEED = 35 - u
    if MOVING:
      connection.drive_direct(RSPEED,LSPEED)
      connection.tpause(st)

###############################################################################
# DOCKING THREAD
# This thread is triggered by detection of the RG or RGFIELD by the omni
# It runs until the dock is found or charging is detected.
#
def FindDock():
  while 1:
    print "OMNI IS REDGREEN"
    # Read dock sensors
    is_omni_rg = connection.is_omni_rg()
    print "OM"+str(is_omni_rg)
    is_right_red = connection.is_right_red()
    print "R"+str(ir_omni_red)
    is_left_green = connection.read_is_left_green()
    print "L"+str(ir_omni_left)

    while(is_left_green and is_right_red):
      print "STRAIGHT"
      connection.drive_direct(30,30)
      connection.stop()
      is_left_green = connection.is_left_green()
      is_right_red = connection.is_right_red()
    while(not is_left_green and not is_left_red):
      print "CIRCLE"
      # maybe include some randomness here to make it do more of a zigzag
      connection.drive_direct(100,30)
      dock = connection.read_charge_source_available()
      is_left_green = connection.is_left_green()
      is_right_red = connection.is_right_red()  
      print "OUTSIDE IFs"

###############################################################################
# THREAD MANAGEMENT

# Connect to state interface and set to full mode
connection = state_interface.Interface()
connection.set_full()

# Initialize threads
while True: 
  cleanDetect = connection.read_button(connection.getClean())
  wheelDrop, bumpLeft, bumpRight = connection.bump_wheel_drop()
  cliff = connection.read_cliff()
  ir_omni_is_rg = connection.is_omni_rg()
  charging = connection.read_charging_state()
  dock = connection.read_charging_source_available()

# Case: not moving and clean button is pressed
# Start wall following thread
  if not MOVING and not wheelDrop and cliff == 0 and cleanDetect:
    wallThread = threading.Thread(target=FollowWall)
    MOVING = True
    wallThread.start()

# Case: omni sensor detects red and green beams 
# Stop wall following thread
# Start dock finding thread
  elif ir_omni_is_rg:
    wallThread.stop()
    dockThread = threading.Thread(target=FindDock)
    dockThread.start()

# Case: moving and clean button is pressed
# Stop any active threads  
  elif MOVING and cleanDetect:
    MOVING = False
    wallThread.stop()
    dockThread.stop()
    connection.stop()

# Case: charging or dock are detected
# Stop finding dock thread
# Quit program
  elif charging is not 0 or dock is not 0:
    MOVING = False
    dockThread.stop()
    connection.stop()
    quit()

