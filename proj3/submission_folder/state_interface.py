import serial
import struct
import math
from time import sleep
from threading import Thread, Lock
import connection_interface

lock = Lock() #Used when reading input from the packets because threading is used in main
L = 235 #Distance between the wheels in mm

#************ STATE ****************** ****************************************#
#
#  Various opcodes for controlling the state of the robot. These can be passed
#  directly as arguments into control_state to change the operational state of
#  the robot.
#
#******************************************************************************#

START = "128"
RESET = "7"
STOP = "173"
SAFE = "131"
FULL = "132"

#*********** READING DATA *****************************************************#
#
#  Opcodes and packet info for reading button press, wheel drop, bump, cliff.
#  Hex strings used to compare against input to determine if there are button
#  presses, wheel drops, bumpers, or cliffs detected.
#  
#
#******************************************************************************#

SENSORS_OPCODE = "142"
DATA_SIZE = 1 # in bytes
TRUE = 1
DIST_PACK = "19"
ANGLE_PACK = "20"

# Buttons *********************************************************************#
#        
# BIT:   | 7     | 6        | 5    | 4    | 3      | 2    | 1    | 0     |
# VALUE: | CLOCK | SCHEDULE | DAY  | HOUR | MINUTE | DOCK | SPOT | CLEAN |
# 

BUTTONS_PACKET = "18"
CLOCK = 0x80
SCHEDULE = 0x40
DAY = 0x20
HOUR = 0x10
MINUTE = 0x08
DOCK = 0x04
SPOT = 0x02
CLEAN = 0x01

# Bumps and Wheel Drops *******************************************************#
#
# BIT:   | 7-6-5-4  | 3         | 2          | 1         | 0          |
# VALUE: | RESERVED | DROP LEFT | DROP RIGHT | BUMP LEFT | BUMP RIGHT |
#

BUMP_PACKET = 7
DROP_LEFT = 0x08
DROP_RIGHT = 0x04
BUMP_LEFT = 0x02
BUMP_RIGHT = 0x01

# Cliff Sensor ****************************************************************#
# Returns a single bit, 0 = false, 1 = true
# Packets
# Each location left, front left, right, front right, virtual wall has its own
# packet ID which must be called and a single bit to read

CLIFF = 0x01
LEFT = 9
FRONT_LEFT = 10
RIGHT = 12
FRONT_RIGHT = 11
VIRTUAL_WALL = 13

  
#********* SENDING DATA *******************************************************#
#
#  Data for sending commands to the robot, including driving and song 
#  information.  
#
#******************************************************************************#


# Song ************************************************************************#
SONG_COMMAND = 140
PLAY_COMMAND = 141
SONG_NUMBER = 0
SONG_LENGTH = 12
As = 70
Fs = 66
Ds = 63
DQ = 48
Q = 32
E = 16
S = 8 



# Driving *********************************************************************#
STRAIGHT = "8000"
TURN_CLOCKWISE = "FFFF"
TURN_COUNTERCLOCKWISE = "0001"
MAX_VELOCITY = 500
MIN_VELOCITY = -500
MAX_RADIUS = 2000
MIN_RADIUS = -2000
DRIVE_COMMAND = "137"
DIRECT_COMMAND = "145"

#********* INTERFACE CLASS ****************************************************#
#
#  This interface is an expanded version of the state_interface from Project
#  1. It initializes the robot to any state, reads commands (button presses,
#  wheel drops, cliff sensor), and formats and sends commands.
#
#  New additions since the last project:
#    The robot can now be easily set to full mode using set_full
#    The robot reads the bump and wheel drop packets
#    The robot reads the cliff sensor packets
#    The calculation of angle/distance has been moved to the back end
#    The drive_direct function allows use of the robot's direct drive
#      feature, which takes in a specified velocity for each wheel as
#      arguments.
#    The drive_formatting function is now overloaded to handle arguments
#      for both standard and direct drive
#    The drive_formatting function was cleaned up by using helper functions
#      and now returns a simple string "command" rather than an array of
#      hex values
#    The robot can now play a song (All Star by Smash Mouth)
#
#******************************************************************************#


class Interface:
#****** CONSTRUCTORS AND SETTING THE STATE ************************************#
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
  
  def set_full(self):
    self.connection.send_command(FULL)
    
  def close(self):
    self.connection.close()

  def stop(self):
    self.drive(0,0)
    self.drive_direct(0,0)

  def pause(self):
    sleep(0.015)
  
  def tpause(self,time):
    sleep(time)

#****** READING DATA FROM THE ROBOT *******************************************#
#
#  Functions:
#    read_button: checks for pressing of the clean button
#      could be improved by debouncing the switch
#      returns a single boolean: true if the buttons is pressed
#    
#    bump_wheel_drop: checks for bumps and wheel drops:
#      returns three booleans:
#        wheel drop, bump left, bump right
#     
#    read_cliff: checks for cliff sensor.
#      returns five booleans:
#        left, front left, right, front right, virtual wall
#
#    read_angle: returns, in two bytes, the total degrees the robot 
#      has turned since the function was last called.
#
#    read_distance: returns, in two bytes, the total millimeters the robot
#      has traveled since the function was last called.
#
#    getClean: an accessor for the value of the clean button.
#
#
#   
#
#******************************************************************************#
  
  def read_button(self, button):
    lock.acquire()
    self.connection.send_command(str(SENSORS_OPCODE)+" "+str(BUTTONS_PACKET))
    data = self.connection.read_data(DATA_SIZE)
    byte = struct.unpack("B", data)[0]
    lock.release()
    return bool(byte & button)
  
  def bump_wheel_drop(self):
    lock.acquire()
    self.connection.send_command(str(SENSORS_OPCODE)+" "+str(BUMP_PACKET))
    data = self.connection.read_data(DATA_SIZE)
    byte = struct.unpack("B", data)[0]
    wheel_drop = False
    if bool(byte & DROP_LEFT) or bool(byte & DROP_RIGHT):
      wheel_drop = True
    bump_left = bool(byte & BUMP_LEFT)
    bump_right = bool(byte & BUMP_RIGHT)
    lock.release()
    return (wheel_drop, bump_right, bump_left)

  
  def read_cliff(self):
    lock.acquire()
    self.connection.send_command(str(SENSORS_OPCODE)+" "+str(LEFT))
    self.connection.send_command(str(SENSORS_OPCODE)+" "+str(FRONT_LEFT))
    self.connection.send_command(str(SENSORS_OPCODE)+" "+str(RIGHT))
    self.connection.send_command(str(SENSORS_OPCODE)+" "+str(FRONT_RIGHT))
    data = self.connection.read_data(4) #read 4 bytes
    byte = struct.unpack("I", data)[0]
    lock.release()
    return byte
      
  def read_angle(self):
    lock.acquire()
    self.connection.send_command(str(SENSORS_OPCODE)+" "+str(ANGLE_PACK))
    data = self.connection.read_data(2) # read 2 bytes
    byte = struct.unpack(">h", data)[0]
    lock.release()
    return byte



  def read_distance(self):
    lock.acquire()
    self.connection.send_command(str(SENSORS_OPCODE)+" "+str(DIST_PACK))
    data = self.connection.read_data(2) # read 2 bytes
    byte = struct.unpack(">h", data)[0]
    lock.release()
    return byte
  
  def getClean(self):
    return CLEAN


#******* SENDING DATA TO THE ROBOT ********************************************#
#
#  Functions:
#
#    song: sends a command to the robot to sing the song "All Star" by
#      Smash Mouth    
#
#    straightTime: given a velocity and distance as arguments, calculate
#      the time required to drive straight to reach that distance
#      returns a single integer time    
#
#    turnTime: given a velocity and angle as arguments, calculate the time
#      required to turn to reach that angle
#      returns a single integer time
#
#    drive: given a velocity and radius as arguments, send a drive command
#      for the robot to execute.
#      Calls the drive_formatting function to parse the velocity and radius
#        into a string "command".
#
#    drive_direct: given a velocity for each wheel as arguments, send a
#      drive command for the robot to execute.
#      Calls the drive_formatting function to parse the velocities
#        into a string "command".
#
#    drive_formatting: an overloaded function which takes in two arguments
#      and eventually returns a string with the appropriate drive command.
#     
#      Several helper functions are called: 
#        check_boundary: used to determine that the given arguments are within
#          the allowable range.
#
#        hexify: converts a decimal integer into a 4 bit string of hex with 
#          the "0x" prefix removed.
#
#        split_bits: splits two hex strings into two low bits and two high bits
#          each. Then parses those bits back into decimal.
#          returns four decimal integers; two for each argument passed
# 
#        stringify: combines the drive command and the four integeres from 
#          split_bits into a string "command"
#
#      returns: a string "command" which is a correctly formatted drive 
#        command for the robot, either in the drive or drive_direct case.
#
#
#******************************************************************************#

  def song(self):
    command = str(SONG_COMMAND)+" "+str(SONG_NUMBER)+" "+str(
              SONG_LENGTH)+" "+str(As)+" "+str(E)+" "+str(Fs)+" "+str(
              Q)+" "+str(Fs)+" "+str(S)+" "+str(Ds)+" "+str(S)+" "+str(
              Fs)+" "+str(E)+" "+str(Fs)+" "+str(Q)+" "+str(Fs)+" "+str(
              S)+" "+str(Ds)+" "+str(S)+" "+str(Fs)+" "+str(E)+" "+str(
              Fs)+" "+str(Q)+" "+str(Fs)+" "+str(Q)+" "+str(As)+" "+str(DQ)
    self.connection.send_command(command)
    command = str(PLAY_COMMAND)+" "+str(SONG_NUMBER)
    self.connection.send_command(command)
    

  def straightTime(self,velocity,distance): 
    time = (float(distance*10))/float(velocity)
    return time

  def turnTime(self, velocity, angle):
    angle = float(math.radians(angle))
    omega = float(2*velocity)/float(L)
    time = angle/omega
    return time

  # Send a Drive command to set the velocity and the radius of the
  # wheels, given the two as arguments.
  def drive(self, velocity, radius):
    command = self.drive_formatting(velocity, radius)
    self.connection.send_command(command)
  
  # Direct drive specifies the velocity of each wheel individually
  def drive_direct(self, R_Vel, L_Vel):
    command = self.drive_formatting(R_Vel, L_Vel) 
    self.connection.send_command(command)

  def drive_formatting(self, velocity, radius):
    # Check boundary conditions
    velocity = self.check_boundary(velocity, MAX_VELOCITY, MIN_VELOCITY)
    radius = self.check_boundary(radius, MAX_RADIUS, MIN_RADIUS)
    velocity = self.hexify(velocity)
    # If it isn't already hex, format the radius into hex
    if radius != STRAIGHT and radius != TURN_CLOCKWISE \
       and radius != TURN_COUNTERCLOCKWISE:
      radius = self.hexify(radius)
    # Parse low and high bit back into decimal
    v1,v2,r1,r2 = self.split_bits(velocity,radius)
    command = self.stringify(DRIVE_COMMAND, v1,v2,r1,r2)
    return command

  def drive_formatting(self, r_vel, l_vel):
    # Check boundary conditions
    r_vel = self.check_boundary(r_vel, MAX_VELOCITY, MIN_VELOCITY)
    l_vel = self.check_boundary(l_vel, MAX_VELOCITY, MIN_VELOCITY)
   # Hexify into a 4 bit string of hex
    r_vel = self.hexify(r_vel)
    l_vel = self.hexify(l_vel)
    # Split into two low and high bits and parse those back into decimal
    vr1, vr2, vl1, vl2 = self.split_bits(r_vel,l_vel)
    command = self.stringify(DIRECT_COMMAND, vr1,vr2,vl1,vl2)
    return command

  # HELPER FUNCTIONS CALLED BY DRIVE FORMATTING #
  def check_boundary(self,param, max_bound, min_bound):
    if param > max_bound:
      param = max_bound
    if param < min_bound:
      param = min_bound
    return param
  
  def hexify(self,param):
    param = hex(param & (2**16-1))[2:]
    param = str(param).zfill(4)
    return param
  
  def split_bits(self,param1, param2):
    high1 = int(param1[:2],16) 
    high2 = int(param2[:2],16)
    low1 = int(param1[2:],16) 
    low2 = int(param2[2:],16)
    return (high1, low1, high2, low2)

  def stringify(self,opcode, p1, p2, p3, p4):
    command = str((str(opcode)+" "+str(p1)+" "+str(
               p2)+" "+str(p3)+" "+str(p4)))
    return command
