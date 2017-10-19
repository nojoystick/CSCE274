import state_interface
import threading
import random

#Global Constants
MOVING = False #Robots current state
LOWANG = -30 #Lowest number in range
HIGHANG = 30 #Highest number in range
TURNANG = 180 #Default angle for robot to turn when it bumbs/detects a cliff

# Function randomAngle takes in two integers in a range from low to high 
# and generates a random number N such that low <= N <= high
def randomAngle(low, high):
  return random.randint(low, high)

# Function randomDirection generates either 0 or 1 to determine 
# which direction the roomba should rotate. 0 indicates turn left, 
# 1 indicates turn right.
def randomDirection():
  return random.randint(0,1)

# Function that tells the robot to turn clockwise for 180 + (-30,30) degrees
def turnClockwise():
  connection.drive(200,1)
  connection.pause(connection.turnTime(200, (TURNANG + randomAngle(LOWANG, HIGHAND))))

# Function that tells the robot to turn counterclockwise for 180 + (-30,30) degrees
def turnCounterClockwise():
  connection.drive(200,-1)
  connection.pause(connection.turnTime(200, (TURNANG + randomAngle(LOWANG, HIGHANG))))
  
def cantStopWontStop():
  global MOVING

  while MOVING:
  	connection.pause()
    connection.drive_direct(200,200)
    connection.pause()
    wheelDrop,bumpLeft,bumpRight = connection.bump_wheel_drop()
    connection.pause()
    cliffLeft, cliffFrontLeft, cliffFrontRight, cliffRight = connection.read_cliff()
    connection.pause()

    if wheelDrop:
      connection.stop()
      connection.pause()
      #connection.song()
      connection.pause()
      MOVING = False
      break
    elif ((cliffLeft or cliffFrontLeft) and (cliffRight or cliffFrontRight)):
      if randomDirection() == 0:
        turnClockwise()
        connection.pause()
      else
        turnCounterClockwise()
        connection.pause()
    elif cliffLeft or cliffFrontLeft
      turnClockwise()
      connection.pause()
    elif cliffRight or cliffFrontRight
      turnCounterClockwise()
      connection.pause()
    elif bumpLeft and bumpRight:
      if randomDirection() == 0
        turnClockwise()
        connection.pause()
      else
        turnCounterClockwise()
        connection.pause()
	elif bumpLeft:
      turnClockwise()
      connection.pause()
    elif bumpRight:
      turnCounterClockwise()
      connection.pause()

connection = state_interface.Interface()
#connection.set_Full()

while True: 
  connection.pause()
  cleanDetect = connection.read_button(connection.getClean())
  connection.pause()
  wheelDrop, bumpLeft, bumpRight = connection.bump_wheel_drop()
  connection.pause()
  cliffLeft, cliffFrontLeft, cliffFrontRight, cliffRight = connection.read_cliff()
  connection.pause()

  if not MOVING and not wheelDrop and not (cliffLeft or cliffFrontLeft or cliffFrontRight or cliffRight) and cleanDetect:
    myThread = threading.Thread(target=cantStopWontStop)
    MOVING = True
    myThread.start()
  elif MOVING and cleanDetect:
    MOVING = False
    connection.pause()

  connection.pause()

connection.stop()
connection.pause()
connection.close()
