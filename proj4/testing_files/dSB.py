import serial
import time
import state_interface
import time
import threading
global moving
moving = False
global VERTEXES
VERTEXES = 5
global TOTAL
TOTAL = 0

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
      connection.pause()
      connection.drive(200,0)
      time.sleep(1000)
      if PRESS:
        print("PRESS")
    connection.stop()

connection = state_interface.Interface()

while True:
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
