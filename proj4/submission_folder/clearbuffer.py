import serial

c = serial.Serial('/dev/ttyUSB0/', 115200)
c.write(chr(7))
c.write(chr(128))
c.write(chr(132))
c.read(10000)
c.close()



