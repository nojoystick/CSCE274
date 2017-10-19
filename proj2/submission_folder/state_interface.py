import serial
import struct
from time import sleep

import connection_interface

# Values relating to state
START = "128"
RESET = "7"
STOP = "173"
SAFE = "131"
FULL = "132"

# Values relating to buttons
SENSORS_OPCODE = "142"
CLOCK = 0x80
SCHEDULE = 0x40
DAY = 0x20
HOUR = 0x10
MINUTE = 0x08
DOCK = 0x04
SPOT = 0x02
CLEAN = 0x01
PACKET = "18"
DATA_SIZE = 1 # in bytes
  
# Commands relating to driving
STRAIGHT = "8000"
TURN_CLOCKWISE = "FFFF"
TURN_COUNTERCLOCKWISE = "0001"
MAX_VELOCITY = 500
MIN_VELOCITY = -500
MAX_RADIUS = 2000
MIN_RADIUS = -2000
DRIVE_COMMAND = "137"

class Interface:

  state = None

  def __init__(self):
    # Set up serial connection
    self.connection = connection_interface.SerialInterface()
    # Change state to passive, then safe
    self.state = START
    self.control_state(SAFE)

  # Control the state of the robot (Start, Reset, Stop, Passive, Safe).
  def control_state(self, next_state):
    if next_state != self.state:
      self.connection.send_command(next_state)

  def read_button(self, button):
    self.connection.send_command(str(SENSORS_OPCODE)+" "+str(PACKET))
    data = self.connection.read_data(DATA_SIZE)
    if len(data)==DATA_SIZE:
      byte = struct.unpack("B", data)[0]
      return bool(byte & button)
    else:
      return False  

  # Send a Drive command to set the velocity and the radius of the
  # wheels, given the two as arguments.
  def drive(self, velocity, radius):
    v1, v2, r1, r2 = self.drive_formatting(velocity, radius)
    command = str(DRIVE_COMMAND)+" "+str(v1)+" "+str(v2)+" "+str(r1)+" "+str(r2)
    self.connection.send_command(command)

  def drive_formatting(self, velocity, radius):
  #Check boundary conditions
    if velocity > MAX_VELOCITY:
      velocity = MAX_VELOCITY
    if velocity < MIN_VELOCITY:
      velocity = MIN_VELOCITY
    if radius > MAX_RADIUS:
      radius = MAX_RADIUS
    if radius < MIN_RADIUS:
      radius = MIN_RADIUS
    # If it isn't already hex, format the radius into hex
    if radius != STRAIGHT and radius != TURN_CLOCKWISE and radius != TURN_COUNTERCLOCKWISE:
      # Return radius as a 32 bit hex value without leading 0x
      velocity = hex(velocity & (2**16-1))[2:]
      radius = hex(radius & (2**16-1))[2:]
    # Store as a 4 character string
    velocity = str(velocity).zfill(4)
    radius = str(radius).zfill(4)
    # Parse low and high bit back into decimal
    v1 = int(velocity[:2],16)
    v2 = int(velocity[2:],16)
    r1= int(radius[:2],16)
    r2= int(radius[2:],16)
    return (v1,v2,r1,r2)

  def close(self):
    self.connection.close()

  def stop(self):
    self.drive(0,0)

  def pause(self):
    sleep(0.015)

  def getClean(self): #This method is necessary in order to access the CLEAN variable. Should we store the CLEAN etc variables in main??
    return CLEAN
