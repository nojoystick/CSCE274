import serial
import state_interface
import connection_interface
from time import sleep
import threading;

L = 235 #distance wheels are apart in mm
#connection = ""

def straightTime(velocity, distance):
  time = (float(distance*10))/float(velocity)
  return time

def turnTime(velocity, angle):
  omega = float(2*velocity)/float(L)
  time = angle/omega
  return time

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

DONE = False
moving = False
VERTEXES = 5
TOTAL = 0
CURRENT = 0

def pentagon():
  while moving:
    CURRENT = 0
    for i in range(VERTEXES-TOTAL):
      time = straightTime(200,32)
      connection.drive(200,0)
      sleep(time)

      time = turnTime(200,1.2265)
      connection.drive(200,1)
      sleep(time)
      CURRENT = CURRENT+1
  #TOTAL = CURRENT

connection = state_interface.Interface()

while not DONE:
  ret = connection.read_button(connection.getClean())
  if ret:
    if not moving:
      TOTAL = CURRENT
      myThread = threading.Thread(target=pentagon)
      moving = True
      myThread.start()
    else:
      TOTAL = CURRENT
      moving = False
      connection.stop()
    sleep(0.015)
  elif TOTAL is 5:
    myThread.stop()
    break
  sleep(0.015)

connection.stop()
connection.close()
