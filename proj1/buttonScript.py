import serial
from time import sleep
import struct

c = serial.Serial('/dev/ttyUSB0', 115200)
sleep(0.015)
c.write(chr(128))
sleep(0.015)
c.write(chr(131))

while True:
  sleep(0.015)
  c.write(chr(142)+chr(18))
  sleep(0.015)
  data = c.read(1)
  print data
  byte = struct.unpack('B', data)[0]
  if bool(byte & 0x01):
    print "Clean this dick."
    break

