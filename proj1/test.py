import serial
import threading
import state_interface
import connection_interface
from time import sleep
L = 235 #distance wheels are apart in mm

def straightTime(velocity, distance):
  time = (float(distance*10))/float(velocity)
  return time

def turnTime(velocity, angle):
  omega = float(2*velocity)/float(L)
  time = angle/omega
  return time

connection = state_interface.Interface()
#background = threading.Thread(connection)

for i in range(0,5):
  time = straightTime(200,32)
  connection.drive(200,0)
  sleep(time)

  time = turnTime(200,1.2265)
  connection.drive(200, 1)
  sleep(time)

connection.stop()
connection.close()
