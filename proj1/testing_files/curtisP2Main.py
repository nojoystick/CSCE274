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

def cantStopWontStop():
  global MOVING
  global LOWANG
  global HIGHANG
  global TURNANG

  while MOVING:
  	connection.pause()
    #connection. direct drive 200,200?
    connection.pause()
    #wheelDrop,BumpLeft,BumpRight = connection. read wheelDrop sesor
    connection.pause()
    #cliffLeft, cliffFrontLeft, cliffRight, cliffFrontRight, cliffVWall = connection. read cliff sensors
    connection.pause()

    #if wheelDrop:
      #connection.stop()
      connection.pause()
      #connection. play warning song
      connection.pause()
      #MOVING = False
      #break
    #elif ((cliffLeft or cliffFrontLeft) and (cliffRight or cliffFrontRight)) or cliffVWall
      #if randomDirection() == 0:
        #left turn TURNANG + randomAngle(LOWANG, HIGHANG)
        connection.pause()
      #else
        #right turn TURNANG + randomAngle(LOWANG, HIGHANG)
        connection.pause()
    #elif cliffLeft or cliffFrontLeft
      #turn clockwise TURNANG + randomAngle(LOWANG, HIGHANG)
        connection.pause()
    #elif cliffRight or cliffFrontRight
      #turn counter clockwise TURNANG + randomAngle(LOWANG, HIGHANG)
        connection.pause()
    #elif bumpLeft and bumpRight:
      #if randomDirection() == 0
        #left turn TURNANG + randomAngle(LOWANG, HIGHANG)
        connection.pause()
      #else
          #right turn TURNANG + randomAngle(LOWANG, HIGHANG)
          connection.pause()
	#elif bumpLeft:
      #turn clockwise TURNANG + randomAngle(LOWANG, HIGHANG)
        connection.pause()
    #elif bumpRight:
      #turn counter clockwise TURNANG + randomAngle(LOWANG,HIGHANG)
        connection.pause()

connection = state_interface.Interface()
#connection.set_Full()

while True: 
  connection.pause()
  cleanDetect = connection.read_button(connection.getClean())
  connection.pause()
  #wheelDrop = connection. read wheelDrop sensor
  connection.pause()
  #cliffDetect = connection. read Cliff Sensors
  connection.pause()

  if not MOVING:#and not wheelDrop and not cliffDetect and cleanDetect:
    myThread = threading.Thread(target=cantStopWontStop)
    MOVING = True
    myThread.start()
  elif MOVING:#and cleanDetect
    MOVING = False
    connection.pause()

  connection.pause()

connection.stop()
connection.pause()
connection.close()
