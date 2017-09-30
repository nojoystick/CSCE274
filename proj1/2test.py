import serial
import state_interface
import connection_interface
from time import sleep
import threading;


L = 235 #distance wheels are apart in mm
connection = ""

def straightTime(velocity, distance):
  time = (float(distance*10))/float(velocity)
  return time

def turnTime(velocity, angle):
  omega = float(2*velocity)/float(L)
  time = angle/omega
  return time

def start_control():
  connection = state_interface.Interface()
  while True:
    if connection.read_button(connection.CLEAN):
      pentagon().start()

def pentagon(threading.Thread):
  
  for i in range(0,5):
    time = straightTime(200,32)
    connection.drive(200,0)
    sleep(time)

  time = turnTime(200,1.225)
  connection.drive(200, -1)
  sleep(time)

start_control()
connection.stop()
connection.close()


