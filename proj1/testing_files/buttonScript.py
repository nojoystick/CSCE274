import serial
from time import sleep
import struct
import state_interface

c = state_interface.Interface()
sleep(0.015)

while True:
  sleep(0.015)
  c.drive(200, -1)
  sleep(0.015)
  data = c.read_button(1)
  #data = c.read(1)
  print data
  byte = struct.unpack('B', data)[0]
  if bool(byte & 0x01):
    print "Clean this dick."
    break

