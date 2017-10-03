import serial
from time import sleep

class SerialInterface:
  # Some constants
  port = '/dev/ttyUSB0'
  baudrate = 115200
  connection = None
  
  # Constructor
  def __init__(self):
    self.connect(port,baudrate)
    # Close and reopen connection
    self.connection.close()
    self.pause()
    self.connection.open()

  def connect(self, port, baudrate): 
    self.connection = serial.Serial(port, baudrate)
  
  # This function can take in a string of commands separated
  # by spaces and split and encode the command
  def send_command(self, command):
    encoded = ""
    command = str.split(command)
    for i in range(0,len(command)):
      encoded += chr(int(command[i]))
    self.connection.write(encoded)
    self.pause()

  def read_data(self, size):
    # Size: number of bytes to read
    return self.connection.read(int(size))

  def close(self):
    self.connection.close()
  
  def pause(self):
    sleep(0.015)
