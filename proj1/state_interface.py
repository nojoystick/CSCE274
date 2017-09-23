import serial
connection = serial.Serial(‘/dev/ttyUSB0’, baudrate=115200);
#Control the state of the robot (Start, Reset, Stop, Passive, Safe).


#Read the state of the buttons.

velocity = 200
radius = 500
#Send a Drive command to set the velocity and the radius of the
#wheels, given the two as arguments.
#I think the radius refers to turning radius, because the 
#radius of the wheels is constant
def Drive(velocity, radius):
  #convert velocity and radius into hex
  velocity =  hex(velocity)[2:]
  radius = hex(radius)[2:]
  #store velocity and radius hex in an array of bytes
  v = bytearray(velocity)
  r = bytearray(radius)
  #send command to robot
  #137 is drive command, followed by two bytes velocity and
  #two bytes radius
  connection.write(chr(137),v[0],v[1],r[0],r[1])  
