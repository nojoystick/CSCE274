import serial
import state_interface
import connection_interface

connection = state_interface.Interface()
connection.drive(500,500)
