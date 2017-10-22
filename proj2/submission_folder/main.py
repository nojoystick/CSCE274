import state_interface
import threading
import random
import logging

#Global Constants
MOVING = False # Is the robot currently moving
LOWANG = -30 # Lowest number in range
HIGHANG = 30 # Highest number in range
TURNANG = 180 # Default angle for robot to turn when it bumbs/detects a cliff
SPEED = 100 # Speed to use for all robot movements

# Creating a logger to log Roomba events
logger = logging.getLogger('Roomba_Events')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('Roomba_Events.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s, %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

# Function randomAngle takes in two integers in a range from low to high 
# and generates a random number N such that low <= N <= high
def randomAngle(low, high):
  return random.randint(low, high)

# Function randomDirection generates either 0 or 1 to determine 
# which direction the roomba should rotate. 0 indicates turn left, 
# 1 indicates turn right.
def randomDirection():
  print "in random direction"
  return random.randint(0,1)

# Function that tells the robot to turn clockwise for 180 + (-30,30) degrees
def turnClockwise():
  connection.drive_direct(SPEED,-SPEED)
  totalAngle = TURNANG + randomAngle(LOWANG, HIGHANG)
  logger.info('CLOCKWISE ANGLE: %s', totalAngle)
  waitTime = connection.turnTime(SPEED, totalAngle)
  connection.tpause(waitTime)

# Function that tells the robot to turn counterclockwise for 180 + (-30,30) degrees
def turnCounterClockwise():
  connection.drive_direct(-SPEED,SPEED)
  totalAngle = TURNANG + randomAngle(LOWANG, HIGHANG)
  logger.info('COUNTERCLOCKWISE ANGLE: %S', totalAngle)
  waitTime = connection.turnTime(SPEED, totalAngle)
  connection.tpause(waitTime)
  
def cantStopWontStop():
  global MOVING

  while MOVING:
    wheelDrop = False
    bumpLeft = False
    bumpRight = False
    cliff = 0
    connection.drive_direct(SPEED,SPEED)
    wheelDrop,bumpLeft,bumpRight = connection.bump_wheel_drop()
    #cliffLeft, cliffFrontLeft, cliffFrontRight, cliffRight = connection.read_cliff()
    cliff = connection.read_cliff()

    if wheelDrop:
      logger.warning('UNSAFE')
      connection.stop()
      connection.song()
      MOVING = False
      break
    elif cliff != 0: #((cliffLeft or cliffFrontLeft) and (cliffRight or cliffFrontRight)):
      logger.warning('UNSAFE')
      connection.stop()
      if randomDirection() == 0:
        turnClockwise()
      else:
        turnCounterClockwise()
    #elif cliffLeft or cliffFrontLeft:
     # turnClockwise()
    #elif cliffRight or cliffFrontRight:
     # turnCounterClockwise()
    elif bumpLeft and bumpRight:
      connection.stop()
      if randomDirection() == 0:
        turnClockwise()
      else:
        turnCounterClockwise()
    elif bumpLeft:
      connection.stop()
      turnClockwise()
    elif bumpRight:
      connection.stop()
      turnCounterClockwise()

connection = state_interface.Interface()
connection.set_full()
connection.song()
while True: 
  cleanDetect = connection.read_button(connection.getClean())
  wheelDrop, bumpLeft, bumpRight = connection.bump_wheel_drop()
  #cliffLeft, cliffFrontLeft, cliffFrontRight, cliffRight = connection.read_cliff()
  cliff = connection.read_cliff()

  if not MOVING and not wheelDrop and cliff==0 and cleanDetect: #(cliffLeft or cliffFrontLeft or cliffFrontRight or cliffRight) and cleanDetect:
    logger.info('BUTTON')
    myThread = threading.Thread(target=cantStopWontStop)
    MOVING = True
    myThread.start()
  elif MOVING and cleanDetect:
    logger.info('BUTTON')
    MOVING = False
    connection.stop()
