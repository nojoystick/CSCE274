import serial
import time
connection = serial.Serial('/dev/ttyUSB0',115200)

SONG_COMMAND = 140
SONG_NUMBER = 1
SONG_LENGTH = 12
As = 70
Fs = 66
Ds = 63
DQ = 48
Q = 32
E = 16
S = 8

def send_command(command):
    encoded = ""
    command = str.split(command)
    for i in range(0,len(command)):
      encoded += chr(int(command[i]))
    connection.write(encoded)
    time.sleep(0.015)

def song():
  command = str(SONG_COMMAND)+" "+str(SONG_NUMBER)+" "+str(
              SONG_LENGTH)+" "+str(As)+" "+str(E)+" "+str(Fs)+" "+str(
              Q)+" "+str(Fs)+" "+str(S)+" "+str(Ds)+" "+str(S)+" "+str(
              Fs)+" "+str(E)+" "+str(Fs)+" "+str(Q)+" "+str(Fs)+" "+str(
              S)+" "+str(Ds)+" "+str(S)+" "+str(Fs)+" "+str(E)+" "+str(
              Fs)+" "+str(Q)+" "+str(Fs)+" "+str(Q)+" "+str(As)+" "+str(DQ)
  send_command(command)
  send_command(str(141) + " " + str(1))

song()
