import serial
import struct

import connection_interface

# Define a bunch of important constants
# Right now these are global but later  on we
# could organize them into classes
port = '/dev/ttyUSB0'
baudrate = 115200
SENSORS_OPCODE = 142
# Values relating to state
START = 128
RESET = 7
STOP = 173
SAFE = 131
FULL = 132

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
DATA_SIZE = "1" # in bytes
  
# Commands relating to driving
  # radii for common commands
STRAIGHT = "8000"
TURN_CLOCKWISE = "FFFF"
TURN_COUNTERCLOCKWISE = "0001"
  
  # Boundary conditions
MAX_VELOCITY = 500
MIN_VELOCITY = -500
MAX_RADIUS = 2000
MIN_RADIUS = -2000

DRIVE_COMMAND = 137

class Interface:

  state = None

  def __init__(self):
    # Set up serial connection
    self.connection = connection_interface.SerialInterface(port, baudrate)
    # Change state to passive, then safe
    self.state = START
    self.control_state(SAFE)

  # Control the state of the robot (Start, Reset, Stop, Passive, Safe).
  def control_state(self, next_state):
    if next_state != self.state:
      #self.connection.write(chr(next_state)) For consistency lets use send_command
      self.connection.send_command(next_state)
 
  def read_buttons(self):
    # Read packet
    self.connection.send_command(SENSORS_OPCODE+PACKET) #This should work fine im told.
    button_data = self.connection.read_data(DATA_SIZE)
    # Check that size of input matches expected size
    if len(button_data) == DATA_SIZE:
      byte = struct.unpack('B', button_data)[0]
      return {
      #if this doesnt work change Globals to binary
        CLEAN: bool(byte & CLEAN),
        SPOT: bool(byte & SPOT),
        DOCK: bool(byte & DOCK),
        MINUTE: bool(byte & MINUTE),
        HOUR: bool(byte & HOUR),
        DAY: bool(byte & DAY),
        SCHEDULE: bool(byte & SCHEDULE),
        CLOCK: bool(byte & CLOCk)
        }
    # If there's a data size mismatch
    else:
      return {
        CLEAN: False, SPOT: False, DOCK: False, MINUTE: False,
        HOUR: False, DAY: False, SCHEDULE: False, CLOCK: False
        }

  # Send a Drive command to set the velocity and the radius of the
  # wheels, given the two as arguments.
  def drive(self, velocity, radius):
    v, r = self.drive_formatting(velocity, radius)
    # Convert velocity and radius into hex
    #connection.send_command("DRIVE_COMMAND v[0] v[1] r[0] r[1]")
    #unsure about above
    command = str(DRIVE_COMMAND+v[0]+v[1]+r[0]+r[1])
    connection.send_command(command)
    
  def drive_formatting(self, velocity, radius):
  # Check boundary conditions
    if velocity > MAX_VELOCITY:
      velocity = MAX_VELOCITY
    if velocity < MIN_VELOCITY:
      velocity = MIN_VELOCITY
    if radius > MAX_RADIUS:
      radius = MAX_RADIUS
    if radius < MIN_RADIUS:
      radius = MIN_RADIUS
    # Format radius into hex
    if radius != STRAIGHT and radius != TURN_CLOCKWISE and radius != TURN_COUNTERCLOCKWISE:
      # Return radius as a 32 bit hex value w/out 0x
      raddius = hex(radius & (2**32-1))[2:]
    velocity = hex(velocity & (2**32-1))[2:]
    #now add to a byte array so individual bytes can be accessed
    v = bytearray(velocity)
    r = bytearray(radius)
    return (v, r)
