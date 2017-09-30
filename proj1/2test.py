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

class pentagon(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    self.iterations = 0
    self.daemon=True
    self.paused=True
    self.state=threading.Condition()

  def run(self):
    self.resume()
    while True:
      for i in range(0,5):
        time = straightTime(200,32)
        connection.drive(200,0)
        sleep(time)

        time = turnTime(200,1.225)
        connection.drive(200, -1)
        sleep(time)

  def reumse(self):
    with self.state:
      self.paused=False
      self.state.notify()

  def pause(self):
    with self.state:
      self.paused=True

start_control()
connection.stop()
connection.close()




