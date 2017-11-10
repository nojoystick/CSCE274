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
sp = 0 # Set point
pe = 0 # Past Error
le = 0 # Last Error
st = 0 # Sampling Time
kp = 0 # Proportional Gain
ki = 0 # Integral  Gain
kd = 0 # Derivative Gain

# Creating a logger to log Roomba events
logger = logging.getLogger('Roomba_Events')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('Roomba_Events.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s, %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

#NOTE: Our Controller should only be a PD which means we do not have to worry about integral gains I think?
# I believe all we would do is take out the I and ki for the following equation.
# Also, it appears this only corrects for error on the right wall?

# - PID Controller - Returns a value based off of sensor data.  Returned value determines what to do
#def pd():
#	global le
#	global pe
#	#frwall = retFRWall()
#	#crwall = retCRWall()
#	e = sp - retRWall() - 10*retFRWall() - 10*retCRWall()        #Error
#	P = kp*e                  		#Proportional Controller
#	D = kd*( e - le )/st      		#Derivative Controller
#	u = P  + D     	  			#Controller Output
#	le = e			  		#Updates last error


# CAPS FOR VISIBILITY
# SHOULD WE MOVE THIS ANGLE/TURNING STUFF TO THE BACK END
# ALSO SINCE WE'RE FOLLOWING WALLS SHOULD WE ADJUST THE ANGLE TO BE SOMETHING
# LIKE 90 RATHER THAN 180?



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
  connection.drive_direct(SPEED,-SPEED)
  totalAngle = TURNANG + randomAngle(LOWANG, HIGHANG)
  waitTime = connection.turnTime(SPEED, totalAngle)
  logger.info("ANGLE: %s",connection.read_angle()) # Logs the angle the robot has turned since last checked
  connection.tpause(waitTime)

# Function that tells the robot to turn counterclockwise for 180 + (-30,30) degrees
def turnCounterClockwise():
  connection.drive_direct(-SPEED,SPEED)
  totalAngle = TURNANG + randomAngle(LOWANG, HIGHANG)
  waitTime = connection.turnTime(SPEED, totalAngle)
  logger.info("ANGLE: %s",connection.read_angle()) # Logs the angle the robot has turned since last checked
  connection.tpause(waitTime)
  
# After every moment the robot stops moving completely, the total distance it drove up until that point is logged.
def FollowWall():
  global MOVING

  while MOVING:
    connection.drive_direct(SPEED,SPEED)
    wheelDrop,bumpLeft,bumpRight = connection.bump_wheel_drop()


# NOT SURE IF WE DO THIS HERE OR IN THE PD
    # while left light sensor > x distance from the wall
      # drive diagonally left
    # while left light sensor < x distance from the wall
      # drive diagonally right
    # should we use infra/other sensors to check the front for corners?

    if wheelDrop:
      connection.stop()
      connection.song()
      MOVING = False
      break
    elif cliff != 0:
      connection.stop()
      if randomDirection() == 0:
        turnClockwise()
      else:
        turnCounterClockwise()
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

while True: 
  cleanDetect = connection.read_button(connection.getClean())
  wheelDrop, bumpLeft, bumpRight = connection.bump_wheel_drop()
  cliff = connection.read_cliff()

  if not MOVING and not wheelDrop and cliff == 0 and cleanDetect:
    myThread = threading.Thread(target=FollowWall)
    MOVING = True
    myThread.start()
  elif MOVING and cleanDetect:
    MOVING = False
    connection.stop()
