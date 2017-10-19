import serial
import state_interface
import connection_interface
import time
import threading;

L = 235 #distance wheels are apart in mm

# We should figure out how to make this prettier
# I suspect we can take the globals out
global DONE 
DONE = False
global moving 
moving = False
global VERTEXES 
VERTEXES = 5
global TOTAL 
TOTAL = 0
global CURRENT 
CURRENT= 0
global PRESS
PRESS = False

# Functions to calculate drive times needed
# to travel a specific distance or turn a 
# specific angle
def straightTime(velocity, distance):
  time = (float(distance*10))/float(velocity)
  return time

def turnTime(velocity, angle):
  omega = float(2*velocity)/float(L)
  drive_time = angle/omega
  return drive_time

def pentagon():
  global moving
  global VERTEXES
  global CURRENT
  global TOTAL
  global PRESS

  while moving:
    CURRENT = 0
    # We should see if it still works when we take out
    # the clock stuff
    for i in range(VERTEXES-TOTAL):
      clock = 0
      connection.pause()
      drive_time = straightTime(200,32)
      connection.drive(200,0)
      isTurning = False
      clock = time.clock()
      time.sleep(drive_time)

      drive_time = turnTime(200,1.2265)
      connection.drive(200,1)
      isTurning = True
      clock = time.clock()
      time.sleep(drive_time)
      TOTAL+=1
      if PRESS:
        connection.pause()
        clock2 = time.clock()
        rem_time = clock2-clock
        if not isTurning:
          connection.drive(200,0)
        if isTurning:
          connection.drive(200,1)
        time.sleep(rem_time)
        PRESS = False
        break
      connection.pause()
    moving = False  
    connection.stop()

connection = state_interface.Interface()

while not DONE:
  connection.pause()
  ret = connection.read_button(connection.getClean())
  connection.pause()
  if ret:
    if not moving:
      print "A"
      myThread = threading.Thread(target=pentagon)
      moving = True
      myThread.start()
    else:
      print "B"
      PRESS = True
      moving = False
    connection.pause()
  elif TOTAL is 5:
    print "C"
    break
  connection.pause()

connection.stop()
connection.close()
