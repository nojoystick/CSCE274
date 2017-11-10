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
    elif cliff != 0 or bumpRight or bumpLeft:
      connection.stop()
      connection.obstacle()

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
