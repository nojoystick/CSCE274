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
FOUND_DOCK = False

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
  global FOUND_DOCK
  FOUND_DOCK = False
  charging = connection.read_charging_state()
  dock = connection.read_charge_source_available()
  if dock is not 0 or charging is not 0:
    connection.drive_direct(0,0)
    #turn the robot off
    connection.song()
    print "Quitting"
    quit()
    #sleep?
  elif dock is 0 or charging is 0:
    while MOVING:
      print str(FOUND_DOCK)
      # Reset driving speed to drive straight every iteration after the correction.
      LSPEED = 50
      RSPEED = 50
      ir_omni = connection.read_ir_omni()
      print "OM"+str(ir_omni)
      ir_right = connection.read_ir_right()
      print "R"+str(ir_right)
      ir_left = connection.read_ir_left()
      print "L"+str(ir_left)
      if ir_omni is 172 or (ir_right is 168 and ir_left is 164):
        FOUND_DOCK = True

      charging2 = connection.read_charging_state()
      dock2 = connection.read_charge_source_available()
      print "C2"+str(charging2)
      print "D2" + str(dock2)
      connection.drive_direct(RSPEED,LSPEED)
      wheelDrop,bumpRight,bumpLeft = connection.bump_wheel_drop()
      logger.info("Infrared O/R/L: %s/%s/%s",ir_omni,ir_right,ir_left)
      logger.info("Charging and Docking C/D: %s/%s", charging2, dock2)
      if charging2 is not 0 or dock2 is not 0:
        connection.drive_direct(0,0)
        #turn the robot off
        connection.song()
        print "Quitting 2"
        quit()
        #sleep?
      #elif here checking infrared values are all 0 so use the PD controller?
      #elif ir_omni is 0 and ir_right is 0 and ir_left is 0 or FOUND_DOCK is False:
       # u = pd()
        #if u > 14:
         # LSPEED = 30
         # RSPEED = 20
        #elif (u >= 9 and u <= 11):
         # LSPEED = 150 + u
          #RSPEED = 35 - u
        #else:
         # LSPEED = 35 + u
         # RSPEED = 35 - u
        #if MOVING:
         # connection.drive_direct(RSPEED,LSPEED)
         # connection.tpause(st)
      elif wheelDrop:
        connection.stop()
        connection.song()
        MOVING = False
        break
      elif cliff != 0:
        connection.stop()
        connection.obstacle()
      elif bumpLeft and FOUND_DOCK is False:
        connection.stop()
        connection.turnClockwise()
      elif bumpRight and FOUND_DOCK is False:
        connection.stop()
        connection.turnCounterClockwise()
      elif bumpLeft and bumpRight and FOUND_DOCK is False:
        connection.stop()
        connection.obstacle()
      #elif something about checking infrared sensors
      elif FOUND_DOCK is False:
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
      elif ir_left is 164: #or ir_omni is 169:
        FOUND_DOCK = True
        print "TURN RIGHT"
        connection.drive_direct(5,85)
      elif ir_right is 168: #or ir_omni is 165:
        FOUND_DOCK = True
        print "TURN LEFT"
        connection.drive_direct(85,5)
      elif ir_omni is 172 or ir_omni is 173 or ir_right is 172 or ir_right is 173 or ir_left is 172 or ir_left is 173:
        FOUND_DOCK = True
        print "GO STRAIGHT"
        connection.drive_direct(1,1)
        connection.drive_direct(0,0)
      #elif something about diffeent infrared values

      #if wheelDrop:
       # connection.stop()
        #connection.song()
        #MOVING = False
        #break
      #if cliff != 0:
       # connection.stop()
        #connection.obstacle()
      #if bumpLeft:
       # connection.stop()
       # connection.turnClockwise()
      #if bumpRight:
       # connection.stop()
       # connection.turnCounterClockwise()
      #if bumpLeft and bumpRight:
       # connection.stop()
        #connection.obstacle()
    
      # Call to the PD controller. Most of these values have been tweaked using trial and error along multiple wall designs. USE THIS UNTIL INFARED IS DETECTED
      # Perhaps move this segment of code into an elif right after my comment above
      #u = pd()
      #if u > 14:
       # LSPEED = 30
        #RSPEED = 20
      #elif (u >= 9 and u <= 11):
       # LSPEED = 150 + u
        #RSPEED = 35 - u
     # else:
      #  LSPEED = 35 + u
       # RSPEED = 35 - u
      #if MOVING:
       # connection.drive_direct(RSPEED,LSPEED)
        #connection.tpause(st)

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
