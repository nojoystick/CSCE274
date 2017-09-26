import serial

import connection_interface

# Define a bunch of important constants
# Right now there are global but later  on we
# could organize them into classes
  port = "'/dev/ttyUSB0'"
  baudrate = 115200

# Values relating to state
  START = "128"
  RESET = "7"
  STOP = "173"
  SAFE = "131"
  FULL = "132"

# Values relating to buttons
  # These are the read values from the OI Spec
  CLOCK = 0x80
  SCHEDULE = 0x40
  DAY = 0x20
  HOUR = 0x10
  MINUTE = 0x08
  DOCK = 0x04
  SPOT = 0x02
  CLEAN = 0x01

  PACKET = "18"
  
# Commands relating to driving
  # radii for common commands
  STRAIGHT = 0x8000
  TURN_CLOCKWISE = 0xFFFF
  TURN_COUNTERCLOCKWISE = 0x0001
  
  # Boundary conditions
  MAX_VELOCITY = 500
  MIN_VELOCITY = -500
  MAX_RADIUS = 2000
  MIN_RADIUS = -2000

  DRIVE_COMMAND = "137"

class Interface:

  state = None

  def init(self):
    # Set up serial connection
    self.connection = connection_interface.SerialInterface(port, baudrate)
    #Change state to passive, then safe
    self.state = START
    self.control_state(SAFE)
  #Control the state of the robot (Start, Reset, Stop, Passive, Safe).
  def control_state(self, next_state):
    if next_state != self.state:
      self.connection.write(chr(next_state))
 
  def read_buttons(self)
    #TODO Read the state of the buttons

  #Send a Drive command to set the velocity and the radius of the
  #wheels, given the two as arguments.
  def drive(self, velocity, radius):
    #TODO THESE CONVERSIONS SHOULD BE THEIR OWN FUNCTION
    #convert velocity and radius into hex
    velocity =  hex(velocity & (2**32-1))[2:] #returns 32 bit without 0x
    radius = hex(radius & (2**32-1))[2:]
    #store velocity and radius hex in an array of bytes
    v = bytearray(velocity)
    r = bytearray(radius)
    connection.send_command("DRIVE_COMMAND v[0] v[1] r[0] r[1]")
  
  
