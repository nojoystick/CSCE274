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
sp = 700 # Set point
pe = 0 # Past Error
le = 0 # Last Error
st = .5 # Sampling Time
kp = .016 # Proportional Gain
kd = .002 # Derivative Gain
LSPEED = 0
RSPEED = 0

FIELD = 161
GREEN = 164
GREEN_FIELD = 165
RED = 168
RED_FIELD = 169
RED_GREEN = 172
RGFIELD = 173

# Creating a logger to log Roomba events
logger = logging.getLogger('Roomba_Events')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('Roomba_Events.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s, %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

# - PID Controller - Returns a value based off of sensor data.  Returned value determines what to do
def pd():
  global le
  global pe
  e = sp - connection.read_light_right() - 10*connection.read_light_front_right() - 10*connection.read_light_center_right() #Error
  P = kp*e     					# Proportional Controller
  D = kd*( e - le )/st      	# Derivative Controller
  u = P  + D     	  			# Controller Output
  le = e						# Updates last error
  return int(u)			  	


def FollowWall():
  global MOVING
  global LSPEED
  global RSPEED
  charging = connection.read_charging_state()
  dock = connection.read_charge_source_available()

# Case: robot is not moving and on dock or charging
# Play a song and terminate the program 
  if dock is not 0 or charging is not 0:
    connection.stop()
    connection.song()
    print "Quitting"
    quit()

# Case: not on dock or charging
# Execute wall following algorithm in while loop 
  elif dock is 0 or charging is 0:
    while MOVING:
   # Reset driving speed to drive straight every iteration after the correction.
      LSPEED = 50
      RSPEED = 50
    # Read dock sensors
      ir_omni = connection.read_ir_omni()
      print "OM"+str(ir_omni)
      ir_right = connection.read_ir_right()
      print "R"+str(ir_right)
      ir_left = connection.read_ir_left()
      print "L"+str(ir_left)

    # Read for charging and dock

      connection.drive_direct(RSPEED,LSPEED)
      wheelDrop,bumpRight,bumpLeft = connection.bump_wheel_drop()
      logger.info("Infrared O/R/L: %s/%s/%s",ir_omni,ir_right,ir_left)
      logger.info("Charging and Docking C/D: %s/%s", charging, dock)
    
    # Case: detects dock
      if ir_omni is RED_GREEN or RGFIELD:
        while charging is 0 or dock is 0:
          if(ir_left is GREEN and ir_right is RED):
            connection.drive_direct(1,1)
          else:
            connection.drive_direct(10,1)
          charging = connection.read_charging_state();
          dock = connection.read_charging_source_available();

      # Case: robot was moving and is on dock or charging
      if charging is not 0 or dock is not 0:
        connection.stop()
        connection.song()
        print "Quitting 2"
        quit()
      # Case: wheel drop detected
      elif wheelDrop:
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
      u = pd()
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

# Connect to state interface and set to full mode
connection = state_interface.Interface()
connection.set_full()

# Initialize thread
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
