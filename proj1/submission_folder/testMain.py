import state_interface
import time
import threading
import math

#Global Constants
MOVING = False #Robots current state
VERTEXES = 5 #Total number of vertexes the robot should hit
TOTAL = 0 #How many vertexes the robot has hit
ANGLE = 72 #Pentagons angle in degrees
DISTANCE = 320 #Length of each pentagons side in mm
L = 235 #distance wheels are apart in mm

# Functions to calculate drive times needed
# to travel a specific distance or turn a 
# specific angle

def straightTime(velocity, distance):
  time = (float(distance))/float(velocity)
  return time

def turnTime(velocity, angle):
  angle = float(math.radians(angle)) #Convert angle to radians
  omega = float(2*velocity)/float(L)
  drive_time = angle/omega
  return drive_time

def pentagon():
  global MOVING
  global VERTEXES
  global TOTAL

  while MOVING:
    for i in range(VERTEXES-TOTAL):
      connection.pause()
      drive_time = straightTime(200,DISTANCE)
      connection.drive(200,0)
      time.sleep(drive_time)

      drive_time = turnTime(200,ANGLE)
      connection.drive(200,1)
      time.sleep(drive_time)
      TOTAL+=1
      if not MOVING:
        connection.stop()
        break
      connection.pause()
    MOVING = False

connection = state_interface.Interface()

while True: 
  connection.pause()
  ret = connection.read_button(connection.getClean())
  connection.pause()
  if ret:
    if not MOVING:
      myThread = threading.Thread(target=pentagon)
      MOVING = True
      myThread.start()
    else:
      MOVING = False
    connection.pause()
  elif TOTAL is 5:
    break
  connection.pause()

connection.stop()
connection.close()
