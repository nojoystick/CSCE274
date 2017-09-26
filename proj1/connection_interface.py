import serial

class SerialInterface:
  #Some constants
  port = "'/dev/ttyUSB0'"
  baudrate = 115200
  connection = None
  
  #Constructor
  def __init__(self, port, baudrate):
    self.connect(port,baudrate)

  #a. Connection to the serial interface.
  def connect(self, port, baudrate): 
    self.connection = serial.Serial(port, baudrate)
  
  #b. Sending of commands.
  #this can take in a string of commands separated by spaces
  #and split and encode the command
  def send_command(self, command)
    encoded = ""
    command.split()
    for index in range(len(command))
      encoded += chr(int(index))
    return self.connection.write(chr(encoded))

  #c. Reading of data.
  def read_data(self, size)
    #size should give the number of bytes
    return self.connection.read(size)

  #d. Close the connection.
  def close(self)
    connection.close()
