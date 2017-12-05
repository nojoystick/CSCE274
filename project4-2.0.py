#Imports
import serial
import time
import struct
import threading
import sys
import random

Integrator_max = 200
Integrator_min = 1

class Robot:

    #establishes a connection to the robot through the USB0 port, throw exception if no
    #Instance variables for PID controller with a setpoint of 250 and our trial and error
    #values for PID(1, .07, .02)
    #Integrator max and min are the values to keep PID in range
    def __init__(self):
        self.connection = serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=1)
        self.Kp = 1
        self.Ki = .067
        self.Kd = 0.02
        self.Derivator = 1
        self.Integrator = 1
        self.Integrator_max=Integrator_max
        self.Integrator_min=Integrator_min

        self.set_point = 250
        self.error = 0
        
    #Takes in the current value or the rightsensor reading and commutes the PID    
    def update(self, current_value):
        self.error = self.set_point - current_value
        self.P_value = self.Kp * self.error
        self.D_value = self.Kd *(self.error - self.Derivator)
        self.Derivator = self.error
        
        self.Integrator = self.Integrator + self.error
        
        if self.Integrator > self.Integrator_max:
            self.Integrator = self.Integrator_max
            
        elif self.Integrator < self.Integrator_min:
            self.Integrator = self.Integrator_min

        self.I_value = self.Integrator * self.Ki
        PID = self.P_value + self.I_value + self.D_value
        
        return PID

    #set and get functions incase we wanted to change in our script
    def setIntegrator(self, Integrator):
        self.Integrator = Integrator

    def setDerivator(self, Derivator):
        self.Derivator = Derivator

    def setKp(self,P):
        self.Kp=P

    def setKi(self,I):
        self.Ki=I

    def setKd(self,D):
        self.Kd=D

    def getPoint(self):
        return self.set_point

    def getError(self):
        return self.error

    def getIntegrator(self):
        return self.Integrator

    def getDerivator(self):  
        return self.Derivator   
        
        
    #This checked to see whether a connection was established to the robot
    #This takes in a raw form of a command and then sends it to the robot
    def sendCommandRaw(self, command):
        self.connection.write(chr(command))

    #This send command is if the command sent in is already in chr format
    def sendCommand(self, command):
        self.connection.write(command)
            
    #Closes the serial connection/resets incase anything is going amist
    def portClose(self):
        self.connection.close()
        time.sleep(.25)

    #Reopens the connections
    def portOpen(self):
        self.connection.open()
        time.sleep(.25)

    #Puts the robot in passive mode if the command is sent while the robot is off        
    def start(self):
        print 'Starting Robot'
        self.sendCommandRaw(128)
        time.sleep(0.30)  

    #Puts the robot in passive mode if the command is sent while the robot is off        
    def passive():
        print 'Putting robot in passive mode'
        self.sendCommandRaw(128)
        time.sleep(0.30)


    #Acts as if the battery was removed and reinserted    

    def reset(self):
        print 'Resetting Robot'
        self.sendCommandRaw(7)
        time.sleep(0.30)

    #Modes for robot to be initialized in
    def safe(self):
        print 'Putting Robot in safe mode'
        self.sendCommandRaw(131)
        time.sleep(0.30)

    def full(self):
        print 'Putting Robot into full mode'
        self.sendCommandRaw(132)
        time.sleep(0.30)
        
        
    def clean(self):
        print 'Cleaning'
        self.sendCommandRaw(135)

    #This command controlled the drive wheels by sending the OPCODE 137 and by
    #Setting the values for the radius and velocity where 32767 is a special case
    #To drive straight    
       
    def drive(self):
        #print 'Driving Robot'
        cmd = struct.pack('!Bhh', 137, 120, 32767)
        self.sendCommand(cmd)
        time.sleep(0.030)


    #Haults the robot by setting velocity to 0
    def stopDrive(self):
        #print 'Stopping Robot'
        cmd = struct.pack('!Bhh', 137, 0, 32767)
        self.sendCommand(cmd)

    #Allows the user to see button presses on the robot
    def getButtons(self):
        self.sendCommandRaw(142)
        self.sendCommandRaw(18)
        x = self.connection.read(1)
        x = struct.unpack('B', x)[0]
        x = "{0:04b}".format(x)
        return x
       

    #Returns the 1 or 0 for the given bump/wheel
    def getBumpandWheel(self):
        self.sendCommandRaw(142)
        self.sendCommandRaw(7)
        x = self.connection.read(1)
        x = struct.unpack('B', x)[0]
        x = "{0:04b}".format(x)
        return x

    #These next 4 methods return 1 or 0 for each cliff sensor depending if it is activated or not
    def getCliffLeft(self):
        cmd = struct.pack('!BB', 142, 9)
        self.sendCommand(cmd)
        x = self.connection.read(1)
        data = struct.unpack('B', x)[0]
        return data 

    def getCliffFrontLeft(self):
        cmd = struct.pack('!BB', 142, 10)
        self.sendCommand(cmd)
        x = self.connection.read(1)
        data = struct.unpack('B', x)[0]
        return data

    def getCliffFrontRight(self):
        cmd = struct.pack('!BB', 142, 11)
        self.sendCommand(cmd)
        x = self.connection.read(1)
        data = struct.unpack('B', x)[0]
        #print data
        return data

    def getCliffRight(self):
        cmd = struct.pack('!BB', 142, 12)
        self.sendCommand(cmd)
        x = self.connection.read(1)
        data = struct.unpack('B', x)[0]
        #print data
        return data

    #The next 3 methods return Roombas receiver sensor value
    def getInfraredOmni(self):
        cmd = struct.pack('!BB', 142, 17)
        self.sendCommand(cmd)
        x = self.connection.read(1)
        data = struct.unpack('B', x)[0]
        return data
    
    def getInfraredLeft(self):
        cmd = struct.pack('!BB', 142, 52)
        self.sendCommand(cmd)
        x = self.connection.read(1)
        data = struct.unpack('B', x)[0]
        return data
    
    def getInfraredRight(self):
        cmd = struct.pack('!BB', 142, 53)
        self.sendCommand(cmd)
        x = self.connection.read(1)
        data = struct.unpack('B', x)[0]
        return data
    
    #check if any of the cliffs have been activated
    def checkCliff(self):
        cliff = 0
        cliff = (self.getCliffFrontLeft() + self.getCliffFrontRight() + self.getCliffLeft() + self.getCliffRight())
        if(cliff > 0):
            return 1
        else:
            return 0

    #Reads data from the distance sensor(sends 142 to request) allowing the robot to know how far it traveled
    def getDistance(self):
        cmd = struct.pack('!BB', 142, 19)
        self.sendCommand(cmd)
        x = self.connection.read(2)
        time.sleep(.25)
        return struct.unpack('!h', x)[0]


    #Sends 142 to request sensor data, then read in 2 bytes
    #Since clockwise is negative times it by -1 and divides it by .324056 to get degrees
    def getCWAngle(self):
        cmd = struct.pack('!BB', 142, 25)
        self.sendCommand(cmd)
        x = self.connection.read(2)
        return (struct.unpack('!h', x)[0] * -1)/(0.324056)

    def getCCWAngle(self):
        cmd = struct.pack('!BB', 142, 25)
        self.sendCommand(cmd)
        x = self.connection.read(2)
        return (struct.unpack('!h', x)[0])/(0.324056)

    #rotates in place ClockWise at a random velocity between 50 - 220
    def rotateCW(self):
        cmd = struct.pack('!Bhh', 137, 50, -1)
        self.sendCommand(cmd)
        time.sleep(.25)

    #rotates in place CounterClockWise at a random velocity between 50 - 220
    def rotateCCW(self):
        cmd = struct.pack('!Bhh', 137, 80, 1)
        self.sendCommand(cmd)
        #time.sleep(.25)
        
    def rotateCWInput(self,velocity):
        cmd = struct.pack('!Bhh', 137, velocity, -1)
        self.sendCommand(cmd)
        time.sleep(.25)

    #rotates in place CounterClockWise at a random velocity between 50 - 220
    def rotateCCWInput(self,velocity):
        cmd = struct.pack('!Bhh', 137, velocity, 1)
        self.sendCommand(cmd)
        #time.sleep(.25)

    #Returns the virtual wall sensor value
    def getVirtualWall(self):
        cmd = struct.pack('!BB', 142, 13)
        x = self.connection.read(1)
        x = struct.unpack('B', x)
        return x
        #time.sleep(.25)

    

    #Returns all the light bumpers index 0-5
    def getLightBumper(self):
        cmd = struct.pack('!BB', 142, 45)
        self.sendCommand(cmd)
        x = self.connection.read(1)
        x = struct.unpack('B', x)[0]
        x = "{0:04b}".format(x)
        return x

    #Returns left bump Signal strength
    def getLBS(self):
        cmd = struct.pack('!BB', 142, 46)
        self.sendCommand(cmd)
        x = self.connection.read(2)
        return struct.unpack('!H', x)[0]

    #Returns Right bump signal strength 
    def getRBS(self):
        cmd = struct.pack('!BB', 142, 51)
        self.sendCommand(cmd)
        x = self.connection.read(2)
        return struct.unpack('!H', x)[0]

    #Returns light bumper center left signal strength
    def getLBCS(self):
        cmd = struct.pack('!BB', 142, 48)
        self.sendCommand(cmd)
        x = self.connection.read(2)
        return struct.unpack('!H', x)[0]

    #Returns right bumper center signal strength
    def getRBCS(self):
        cmd = struct.pack('!BB', 142, 49)
        self.sendCommand(cmd)
        x = self.connection.read(2)
        return struct.unpack('!H', x)[0]

    #Returns Right front bump signal strength
    def getRFBS(self):
        cmd = struct.pack('!BB', 142, 50)
        self.sendCommand(cmd)
        x = self.connection.read(2)
        return struct.unpack('!H', x)[0]

    #Returns left front bump signal strength
    def getLFBS(self):
        cmd = struct.pack('!BB', 142, 51)
        self.sendCommand(cmd)
        x = self.connection.read(2)
        return struct.unpack('!H', x)[0]
    

    #Warning song playing some of the mario theme
    #takes in a structure of bytes and sends command to store, then sends command
    #to play song 0 or 1.
    def setMario(self):
        cmd = struct.pack('!BBBBBBBBBBBBBBBBBBB', 140, 0 ,16 , 88, 8, 88, 16, 88, 16, 88, 16, 84, 8, 88, 16, 91, 32, 79, 16)
        self.connection.write(cmd)
        time.sleep(.2)
        return

    def playMario(self):
        cmd2 = struct.pack('!BB', 141, 0)
        self.connection.write(cmd2)
        time.sleep(.4)
        return
    
    def setZelda(self):
        cmd = struct.pack('!BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',140,1,8,71,36,74,18,69,36,67,9,69,9,71,36,74,18,69,54,71,36,74,18,81,36,79,18,74,36,72,9,71,9,69,54)
        self.connection.write(cmd)
        time.sleep(.015)
        return

    def playZelda(self):
        cmd2 = struct.pack('!BB', 141, 1)
        self.connection.write(cmd2)
        print "Song playing"
        time.sleep(.025)
        return
    
    def setSong(self):
        cmd = struct.pack("BBBBBBBBBBBBBBBBBBBBBBBBB", 140, 2, 11, 71, 34, 69, 34, 65, 34, 71, 34, 69, 34, 65, 34, 71, 34, 69, 34,64, 17, 62, 17, 64, 51)
        self.connection.write(cmd)
        time.sleep(.015)
        return

    def playSong(self):
        cmd = struct.pack('!BB', 141, 2)
        self.connection.write(cmd)
        time.sleep(.025)
        return

    def setRocky(self):
        cmd = struct.pack('!BBBBBBBBBBB', 140, 3, 8, 73,8,71,8,73,32,66,32)
        self.connection.write(cmd)
        time.sleep(.015)
        return

    def playRocky(self):
        cmd = struct.pack('!BB', 141, 3)
        self.connection.write(cmd)
        time.sleep(.025)
        return
        
    #Random walk using drive direct, with velocities ranging from 100 to 200
    def randomWalk(self):
        #index 0 is high byte 1 is low byte
        x = random.randint(100,200)
        cmd = struct.pack('!Bhh', 145, x, x)
        self.connection.write(cmd)
        return

    #Controlled walk taking in directly left and right velocities
    def controlledWalk(self,left,right):
        cmd = struct.pack('!Bhh', 145, left, right)
        self.connection.write(cmd)
        return

    #Returns the charging state of robot, mainly to check if the robot is docked
    def chargingState(self):
        cmd = struct.pack('!BB', 142, 34)
        self.sendCommand(cmd)
        x = self.connection.read(1)
        data = struct.unpack('B', x)[0]
        return data

    #Prints if there are any bytes that were in waiting and clears in case
    #there are so they don't interfere with code
    def clear(self):
        x = self.connection.inWaiting()
        print 'Bytes in waiting:'
        print x
        if(x > 0):
            print 'Clearing ' +str(x)+ ' byte(s)'
            for i in range(0,x): self.connection.read(1)
        return



    

           

