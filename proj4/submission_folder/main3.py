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

  # Execute wall following algorithm in while loop 
  elif dock is 0 or charging is 0:
    while MOVING:
   # Reset driving speed to drive straight every iteration after the correction.
      LSPEED = 50
      RSPEED = 50

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
# DOCKING THREAD
# This thread is triggered by detection of the RG or RGFIELD by the omni
# It runs until the dock is found or charging is detected.
#
def FindDock()
  while 1:
    # Read dock sensors
    ir_omni = connection.read_ir_omni()
    print "OM"+str(ir_omni)
    ir_right = connection.read_ir_right()
    print "R"+str(ir_right)
    ir_left = connection.read_ir_left()
    print "L"+str(ir_left)

    # Case: detects dock
    if ir_omni is RED_GREEN or ir_omni is RGFIELD:
      print "OMNI IS REDGREEN"
      while charging is 0 or dock is 0:
        print "WHILE"
      while(ir_left is GREEN and ir_right is RED) and dock is 0:
        print "STRAIGHT"
        connection.drive_direct(30,30)
        #connection.stop()
        dock = connection.read_charge_source_available()
        #ir_left = connection.read_ir_left()
        #ir_right = connection.read_ir_right()
        #print "RIGHT"+str(ir_right)
        #print ""
        #print "LEFT"+str(ir_left)
        #print ""
      while(ir_left is not GREEN or ir_right is not RED) and dock is 0:
         print "CIRCLE"
         connection.drive_direct(100,30)
         dock = connection.read_charge_source_available()
         ir_left = connection.read_ir_left()
         ir_right = connection.read_ir_right()
         print "RIGHT" + str(ir_right)
         print ""
         print "LEFT" +str(ir_left)
         print ""
         print "OUTSIDE IFs"
         charging = connection.read_charging_state();
         dock = connection.read_charge_source_available();


###############################################################################


# Connect to state interface and set to full mode
connection = state_interface.Interface()
connection.set_full()

# Initialize thread
while True: 
  cleanDetect = connection.read_button(connection.getClean())
  wheelDrop, bumpLeft, bumpRight = connection.bump_wheel_drop()
  cliff = connection.read_cliff()
  ir_omni = connection.read_ir_omni()
  charging = connection.read_charging_state()
  dock = connection.read_charging_source_available()

  if not MOVING and not wheelDrop and cliff == 0 and cleanDetect:
    myThread = threading.Thread(target=FollowWall)
    MOVING = True
    myThread.start()
  elif ir_omni = RED_GREEN or ir_omni = RGFIELD:
    dockThread = threading.Thread(target=FindDock)
    dockThread.start()   
  elif MOVING and cleanDetect:
    MOVING = False
    connection.stop()
  elif MOVING and charging is not 0 or dock is not 0:
    Moving = False
    connection.stop()
    quit()

