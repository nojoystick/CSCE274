import serial
import state_interface
import connection_interface
import time
import threading;

L = 235 #distance wheels are apart in mm
#connection = ""

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


def straightTime(velocity, distance):
  time = (float(distance*10))/float(velocity)
  return time

def turnTime(velocity, angle):
  omega = float(2*velocity)/float(L)
  drive_time = angle/omega
  return drive_time

#def start_control():
 # connection = state_interface.Interface()
  #while True:
    #print connection.read_button(CLEAN)
   # if connection.read_button(connection.getClean()):
    #  print "almost at pentagon"
     # pentagon().start()

#class pentagon(threading.Thread):
 # def __init__(self):
  #  threading.Thread.__init__(self)
   # self.iterations = 0
    #self.daemon=True
    #self.paused=True
    #self.state=threading.Condition()

  #def run(self):
   # self.resume()
    #while True:
     # for i in range(0,5):
      #  time = straightTime(200,32)
       # connection.drive(200,0)
        #sleep(time)

        #time = turnTime(200,1.225)
        #connection.drive(200, -1)
        #sleep(time)

  #def reumse(self):
    #with self.state:
     # self.paused=False
      #self.state.notify()

 # def pause(self):
  #  with self.state:
   #   self.paused=True

def pentagon():
  global moving
  global VERTEXES
  global CURRENT
  global TOTAL
  global PRESS

  while moving:
    CURRENT = 0
    #connection.stop()
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
      print("HI HI")
      TOTAL+=1
      if PRESS:
        connection.pause()
        print("BITCH")
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
    print moving
    connection.stop()
#TOTAL = CURRENT

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
      #connection.stop()
    connection.pause()
  elif TOTAL is 5:
    print "C"
    break
  connection.pause()

connection.stop()
connection.close()
