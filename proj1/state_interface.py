import serial
#connection = serial.Serial('/dev/ttyUSB0', baudrate=115200)
#Control the state of the robot (Start, Reset, Stop, Passive, Safe).


#Read the state of the buttons.

#Send a Drive command to set the velocity and the radius of the
#wheels, given the two as arguments.
#I think the radius refers to turning radius, because the 
#radius of the wheels is constant
def Drive(velocity, radius):
  #convert velocity and radius into hex
  velocity =  hex(velocity & (2**32-1))[2:] #returns 32 bit without 0x
  radius = hex(radius & (2**32-1))[2:]
  #store velocity and radius hex in an array of bytes
  v = bytearray(velocity)
  r = bytearray(radius)
  print hex(v[0])
  print hex(v[1])
  print hex(r[0])
  print hex(r[1])
  #send command to robot
  #137 is drive command, followed by two bytes velocity and
  #two bytes radius. I'm not sure if this formatting is right
  connection.write(chr(137),v[0],v[1],r[0],r[1])
  
