import serial
from time import sleep

class SerialInterface:
  #Some constants
  port = '/dev/ttyUSB0'
  baudrate = 115200
  connection = None
  
  #Constructor
  def __init__(self, port, baudrate):
    self.connect(port,baudrate)
    #Should close and reopen connection because of weirdness in values upon init
    self.connection.close()
    sleep(.015)
    self.connection.open()

  #a. Connection to the serial interface.
  def connect(self, port, baudrate): 
    self.connection = serial.Serial(port, baudrate)
  
  #b. Sending of commands.
  #this can take in a string of commands separated by spaces
  #and split and encode the command
  def send_command(self, command):
    #print command
    encoded = ""
    command = str.split(command)
    for i in range(0,len(command)):
      encoded += chr(int(command[i]))
    self.connection.write(encoded)
    #Friend who got all projects working said this is all you need.
    #self.connection.write(command)
    sleep(.015) #Must wait 15 ms in between command sends.

  #c. Reading of data.
  def read_data(self, size):
    #size should give the number of bytes
    return self.connection.read(int(size))

  #d. Close the connection.
  def close(self):
    self.connection.close()
