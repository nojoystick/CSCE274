import state_interface
import time
import threading;

#DONE = False #Not necessary due to breaking loop
moving = False #Capitalize this when I have time
VERTEXES = 5
TOTAL = 0
#CURRENT = 0 #Remove not used
#PRESS = False #I think we can just stick with moving but we can test later
L = 235 #distance wheels are apart in mm

# We should figure out how to make this prettier
# I suspect we can take the globals out
# I did GG

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
  #Due to change in removing global tags this should work without the tags
  global moving
  global VERTEXES
  #global CURRENT
  global TOTAL
  #global PRESS

  while moving:
    #CURRENT = 0 #Take this out
    # We should see if it still works when we take out
    # the clock stuff
    for i in range(VERTEXES-TOTAL):
      #clock = 0 #Take this out as a test
      connection.pause()
      drive_time = straightTime(200,32)
      connection.drive(200,0)
      #isTurning = False
      #clock = time.clock()
      time.sleep(drive_time)

      drive_time = turnTime(200,1.2265)
      connection.drive(200,1)
      #isTurning = True
      #clock = time.clock()
      time.sleep(drive_time)
      TOTAL+=1
      if not moving:#if PRESS:
        connection.pause()
        #clock2 = time.clock()
        #rem_time = clock2-clock
        #if not isTurning:
         # connection.drive(200,0)
        #if isTurning:
         # connection.drive(200,1)
        #time.sleep(rem_time)
        #PRESS = False
        break
      connection.pause()
    moving = False  
    connection.stop()

connection = state_interface.Interface()

while True: #Same as while True: so remove global DONE
  connection.pause()
  ret = connection.read_button(connection.getClean())
  connection.pause()
  if ret:
    if not moving:
      print "A" #Remove prints when we get a chance
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
