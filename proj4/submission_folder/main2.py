import state_interface
import threading
import random
import logging

#Global Constants
MOVING = False # Is the robot currently moving
LSPEED = 0
RSPEED = 0

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
  D = kd*( e - le )/st      			# Derivative Controller
  u = P  + D     	  			# Controller Output
  le = e					# Updates last error
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
      is_omni_rg = connection.is_omni_rg()
      print "OM"+str(ir_omni)
      is_right_red = connection.is_right_red()
      print "R"+str(ir_right)
      is_left_green = connection.is_left_green()
      print "L"+str(ir_left)

    # Read for charging and dock

      connection.drive_direct(RSPEED,LSPEED)
      wheelDrop,bumpRight,bumpLeft = connection.bump_wheel_drop()
      logger.info("Infrared O/R/L: %s/%s/%s",ir_omni,ir_right,ir_left)
      logger.info("Charging and Docking C/D: %s/%s", charging, dock)
    
    # Case: detects dock
      if connection.is_omni_rg():
        print "OMNI IS REDGREEN"
        while charging is 0 or dock is 0:
          print "WHILE"
          while(is_left_green and is_left_red) and dock is 0:
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
          while(not is_left_green and not is_right_red) and dock is 0:
            print "CIRCLE"
            connection.drive_direct(100,30)
            dock = connection.read_charge_source_available()
            is_left_green = connection.is_left_green()
            is_right_red = connection.is_right_red()
            print "RIGHT" + str(ir_right)
            print ""
            print "LEFT" +str(ir_left)
            print ""
          print "OUTSIDE IFs"
          charging = connection.read_charging_state();
          dock = connection.read_charge_source_available();

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
