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
  print "in random direction"
  return random.randint(0,1)

# Function that tells the robot to turn clockwise for 180 + (-30,30) degrees
def turnClockwise():
  print "in clockwise turn"
  connection.drive(200,1)
  totalAngle = TURNANG + randomAngle(LOWANG, HIGHANG)
  print str(totalAngle)
  waitTime = connection.turnTime(200, totalAngle)
  print str(waitTime)
  connection.tpause(waitTime)

# Function that tells the robot to turn counterclockwise for 180 + (-30,30) degrees
def turnCounterClockwise():
  print "in cc turn"
  connection.drive(200,-1)
  totalAngle = TURNANG + randomAngle(LOWANG, HIGHANG)
  print str(totalAngle)
  waitTime = connection.turnTime(200, totalAngle)
  print str(waitTime)
  connection.tpause(waitTime)
  
def cantStopWontStop():
  global MOVING

  while MOVING:
    wheelDrop = False
    bumpLeft = False
    bumpRight = False
    cliff = 0
    print "In CSWT while loop"
    connection.pause()
    connection.drive_direct(200,200)
    connection.pause()
    wheelDrop,bumpLeft,bumpRight = connection.bump_wheel_drop()
    print str(wheelDrop)+ " "+str(bumpLeft)+" "+str(bumpRight)
    connection.pause()
    #cliffLeft, cliffFrontLeft, cliffFrontRight, cliffRight = connection.read_cliff()
    cliff = connection.read_cliff()
    print str(cliff)
    connection.pause()

    if wheelDrop:
      connection.stop()
      connection.pause()
      connection.song()
      connection.pause()
      MOVING = False
      break
    elif cliff != 0: #((cliffLeft or cliffFrontLeft) and (cliffRight or cliffFrontRight)):
      print "In cliff"
      connection.stop()
      connection.pause()
      if randomDirection() == 0:
        turnClockwise()
        connection.pause()
      else:
        turnCounterClockwise()
        connection.pause()
    #elif cliffLeft or cliffFrontLeft:
     # turnClockwise()
      #connection.pause()
    #elif cliffRight or cliffFrontRight:
     # turnCounterClockwise()
      #connection.pause()
    elif bumpLeft and bumpRight:
      print "In l and r bump"
      connection.stop()
      connection.pause()
      if randomDirection() == 0:
        turnClockwise()
        connection.pause()
      else:
        turnCounterClockwise()
        connection.pause()
    elif bumpLeft:
      print "In l bump"
      connection.stop()
      connection.pause()
      turnClockwise()
      connection.pause()
    elif bumpRight:
      print "In r bump"
      connection.stop()
      connection.pause()
      turnCounterClockwise()
      connection.pause()

connection = state_interface.Interface()
#connection.set_Full()
connection.song()
print "Started moving"
while True: 
  #print "in infinite loop"
  connection.pause()
  cleanDetect = connection.read_button(connection.getClean())
  connection.pause()
  wheelDrop, bumpLeft, bumpRight = connection.bump_wheel_drop()
  #print str(wheelDrop)
  #print str(bumpLeft)
  #print str(bumpRight)
  connection.pause()
  #cliffLeft, cliffFrontLeft, cliffFrontRight, cliffRight = connection.read_cliff()
  cliff = connection.read_cliff()
  #print str(cliff)
  connection.pause()

  if not MOVING and not wheelDrop and cliff==0 and cleanDetect: #(cliffLeft or cliffFrontLeft or cliffFrontRight or cliffRight) and cleanDetect:
    myThread = threading.Thread(target=cantStopWontStop)
    #print "In not moving"
    MOVING = True
    myThread.start()
  elif MOVING and cleanDetect:
    MOVING = False
    connection.pause()

  connection.pause()

connection.stop()
connection.pause()
connection.close()
