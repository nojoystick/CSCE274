import serial
#1. Write an interface for the serial communication, that includes:

#a. Connection to the serial interface.
connection = serial.Serial(‘/dev/ttyUSB0’, baudrate=115200);

#b. Sending of commands.
#sends START command
connection.write(chr(128));

#c. Reading of data.
#reads 1 byte
connection.read(1);

#d. Close the connection.
connection.close();
