from time import sleep
import serial
import struct
from threading import Thread, Lock

#-------------------------------------------------------------------------------------------------------------
# - Setup - Automatically connects to the robot and creates and instance of Lock() when the program starts
#-------------------------------------------------------------------------------------------------------------

lock = Lock()  #Locks are used to make sure sensor data is only read from one place at a time
connection = serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=1)

#-------------------------------------------------------------------------------------------------------------
# - Variables - Important Variables
#-------------------------------------------------------------------------------------------------------------

SPD = 100	    #Default Speed
SLP = .001

#-------------------------------------------------------------------------------------------------------------
# - COMMAND VALUES - ASCII Values for Different Functions
#-------------------------------------------------------------------------------------------------------------
                    
ON = chr(128)       #Turn on/Passive Mode
OFF = chr(133)      #Turn off
RESET = chr(7)      #Changes mode to off, then on
SAFE = chr(131)     #Safe mode
FULL = chr(132)     #Full mode
STOP = chr(173)     #Stops the robot, unresponsive
CLEAN = chr(135)    #"Cleans"
SPOT = chr(134)     #Spot clean
DOCK = chr(143)     #Docks
DRIVE = chr(145)    #Movement command
ADRIVE = chr(137)   #Alternate drive, uses turn radius
MOTOR = chr(144)    #Controls motors
CLED = chr(162)     #Clean button's LED
BLED = chr(163)     #Individual Digit LED Bits
ALED = chr(164)     #Digit LEDs using ASCII values
PUSH = chr(165)     #Push a button
SENSE = chr(142)    #Read from a sensor
STREAM = chr(148)   #Returns data every 15 ms, Don't use
STATE = chr(150)    #Stream State
SONG = chr(140)     #Make a song
PLAY = chr(141)     #Play a song

#-------------------------------------------------------------------------------------------------------------
# - SENSOR VALUES - Values for Different Sensor Packs
#-------------------------------------------------------------------------------------------------------------
CHARGE = chr(21)    #Charge or no charge
CHARGES = chr(34)   #Charge or no charge
BUMPS = chr(7)      #Bumps and wheel Drops
WALL = chr(8)	    #Infrared wall sensor
LCLIFF = chr(9)	    #Left cliff sensor
FLCLIFF = chr(10)   #Front left cliff sensor
FRCLIFF = chr(11)   #Front right cliff sensor
RCLIFF = chr(12)    #Right cliff sensor
LWALL = chr(46)     #Left Light bump sensor
CLWALL = chr(48)    #Center Left light bump sensor
FLWALL = chr(47)    #Front Left light bump
RWALL = chr(51)     #Right Light bump sensor
CRWALL = chr(49)    #Center Right light bump sensor
FRWALL = chr(50)    #Front Right light bump sensor
WALL = chr(27)      #Crap wall sensor
BUTTON = chr(18)    #Button sensors
DIST = chr(19)      #Distance travelled since on
ANGLE = chr(20)     #Angle the roomba has turned
LENC = chr(43)	    #Left wheel encoder
RENC = chr(44)      #Right wheel encoder
LINF = chr(52)	    #Left infrared sensor
RINF = chr(53)      #Right infrared sensor
OMNI = chr(17)
#-------------------------------------------------------------------------------------------------------------
# - BUTTON VALUES - Values returned when readButton() is called
#-------------------------------------------------------------------------------------------------------------

CLN = 1             #Clean
SPT = 2             #Spot
DCK = 4		    #Dock
MNT = 8		    #Minute
HOU = 16	    #Hour
DAY = 32	    #Day
SCH = 64	    #Schedule
CLK = 128	    #Clock
                    #Other buttons return nothing

#-------------------------------------------------------------------------------------------------------------
# - CONNECTION COMMANDS - Commands to connect and send data to the robot
#-------------------------------------------------------------------------------------------------------------

#Connects the raspberry pi to the robot
#You need to use connection.close() and connection.open() in order to receive correct sensor data
def connect():
        global connection
        connection = serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=1)

#Sends the given command
def send(cmd):
	lock.acquire
	connection.write(cmd)
	lock.release()	

#-------------------------------------------------------------------------------------------------------------
# - STATE COMMANDS - Commands to change the state of the robot
#-------------------------------------------------------------------------------------------------------------

#Turns the robot on, also puts it into passive mode
def turnOn():
	lock.acquire()
        connection.write(ON)
	lock.release()

#Turns the robot off
def turnOff():
	lock.acquire()
        connection.write(OFF)
	lock.release()

#Resets the robot
def reset():
	lock.acquire()
	connection.write(RESET)
	lock.release()

#Changes the robot to safe mode
def safeMode():
	lock.acquire()
        connection.write(SAFE)
	lock.release()

#Changes the robot to full mode
def fullMode():
	lock.acquire()
        connection.write(FULL)
	print "In Full Mode"
	lock.release()

#Stops the robot. It will not respond to commands
def Stop():
	lock.acquire()
        connection.write(STOP)
	lock.release()

#-------------------------------------------------------------------------------------------------------------
# - DEFAULT MOVEMENT COMMANDS - Movement commands using default values
#-------------------------------------------------------------------------------------------------------------

#Goes forward at default speed
def go():
	lock.acquire()
	cmd = struct.pack(">hh", SPD, SPD)
	connection.write(DRIVE+cmd)
	lock.release()

#Turns left at default speed
def left():
	lock.acquire()
	cmd = struct.pack(">hh", -1*SPD, SPD)
	connection.write(DRIVE+cmd)
	lock.release()

#Turns right at default speed
def right():
	lock.acquire()
	cmd = struct.pack(">hh", SPD, -1*SPD)
	connection.write(DRIVE+cmd)
	lock.release()

#-------------------------------------------------------------------------------------------------------------
# - BASIC MOVEMENT COMMANDS - Simple commands to move the robot
#-------------------------------------------------------------------------------------------------------------

#Go Forward at a given speed, may need to be adjusted for individual robots
def forward(speed):
	lock.acquire()
	cmd = struct.pack(">hh", speed, speed)
        connection.write(DRIVE+cmd)
	lock.release()

#Goes forward at a given speed for a given time
def forwardFor(speed, t):
	forward(speed)
	sleep(t)
	forward(0)

#Drives, independently control left and right wheel velocities
def move(vl, vr):
	lock.acquire()	
	cmd = struct.pack(">hh", vr, vl)
	connection.write(DRIVE+cmd)
	lock.release()

#Drive command using speed and turn radius
def aDrive(s, r):
	lock.acquire()	
	cmd = struct.pack(">Bhh", ADRIVE, s, r)
	connection.write(cmd)
	lock.release()

#Turns left at a given speed
def turnLeft(speed):
	lock.acquire()
        cmd = struct.pack(">hh", speed, -1*speed)
        connection.write(DRIVE+cmd)
	lock.release()

#Turns left at a given speed for a given time
def leftFor(speed, t):
	turnLeft(speed)
	sleep(t)
	forward(0)

#Moves in a square; turns left
def leftSquare():
	for a in range(4):
		forward(250)
		sleep(1)
		turnLeft(200)
		sleep(.95)
	forward(0)

#Turns right at a given speed
def turnRight(speed):
	lock.acquire()
        cmd = struct.pack(">hh", -1*speed, speed)
        connection.write(DRIVE+cmd)
	lock.release()

#Turns right at a given speed for a given time
def rightFor(speed, t):
	turnRight(speed)
	sleep(t)
	forward(0)

#Moves in a square; turns right
def rightSquare():
        for a in range(4):
                forward(250)
                sleep(1)
                turnRight(200)
                sleep(1)
        forward(0)

#Stops the robot
def stop():
	forward(0)

#-------------------------------------------------------------------------------------------------------------
# - ADVANCED MOVEMENT COMMANDS - Movement commands that rely on sensor data
#-------------------------------------------------------------------------------------------------------------

#Goes forward for a given distance
def forwardDis(speed, dis):
	retDistance()
	i = 0	
	forward(speed)
	while i < dis:
		i += retDistance()
	forward(0)

#Goes forward until a bump sensor is triggered, returns bump sensor
def forwardUntilBump(speed):
	forward(speed)
	while True:
		bump = retBump()
		if bump is not 0:
			forward(0)
			return bump

#Turns left to a given degree
def leftDeg(speed, deg):
	retAngle()
	angle = 0
	turnLeft(speed)
	while angle < deg:
		angle += abs(retAngle())
	forward(0)

#Turns right to a given degree
def rightDeg(speed, deg):
	retAngle()
	angle = 0
	turnRight(speed)
	while angle < deg:
		angle += abs(retAngle())
	forward(0)

#-------------------------------------------------------------------------------------------------------------
# - GENERIC SENSOR COMMANDS - Commands to return data from the robot
#-------------------------------------------------------------------------------------------------------------

#Reads the state of a given sensor
def readSensor(pack, nbit):
	lock.acquire()
	sleep(SLP)
        connection.write(SENSE+pack)
        bit = struct.unpack('B', connection.read(nbit))[0]
	lock.release()
	return bit

#Prints the current sensor data
def printData():
	lock.acquire()
	bit = struct.unpack("h", connection.read(2))[0]
	lock.release()
	print bit

#Stream returns sensor data every 15 ms, don't use at the moment
def stream(pack):
	lock.acquire()
        connection.write(STREAM+pack)
	lock.release()

#Turns the stream on or off
def streamState(state):
	lock.acquire()
        connection.write(STATE+state)
	lock.release()

#-------------------------------------------------------------------------------------------------------------
# - SPECIFIC SENSOR COMMANDS - Read in from specific sensors
#-------------------------------------------------------------------------------------------------------------

def retCharges():
	lock.acquire()
	sleep(SLP)
	connection.write(SENSE+CHARGES)
	bit = struct.unpack('>B',connection.read(1))[0]
	lock.release()
	return bit

#Returns whether or not its charging
def retCharge():
	lock.acquire()
	sleep(SLP)
	connection.write(SENSE+CHARGE)
	bit = struct.unpack('>B',connection.read(1))[0]
	lock.release()
	return bit

#Reads the state of the buttons
def readButton():
	lock.acquire()
	sleep(SLP)
        connection.write(SENSE+BUTTON)
        bit = struct.unpack('>B', connection.read(1))[0]
	lock.release()
	return bit

#Returns the distance travelled since it was turned on
def retDistance():
	lock.acquire()
	sleep(SLP)
	bit = struct.unpack('>h', connection.read(2))[0]
	lock.release()
	return bit

#Returns the angle turned since turned on
def retAngle():
	lock.acquire()
	connection.write(SENSE+ANGLE)
	bit = struct.unpack('>h', connection.read(2))[0]
	lock.release()
	return bit

#Returns bump/wheel drop sensors
def retBump():
	lock.acquire()
	connection.write(SENSE+BUMPS)
	bit = struct.unpack('>B', connection.read(1))[0]
	lock.release()
	return bit

#Returns the value of all the cliff sensors, returns 4 bits
def retCliff():
	lock.acquire()
	connection.write(SENSE+LCLIFF)
	connection.write(SENSE+RCLIFF)
	connection.write(SENSE+FLCLIFF)
	connection.write(SENSE+FRCLIFF)
	bit = struct.unpack('I', connection.read(4))[0]
	lock.release()
	return bit

#Returns the left lighthouse beacon
def retLinf():
	lock.acquire()
	connection.write(SENSE+LINF)
	bit = struct.unpack('>B', connection.read(1))[0]
	lock.release()
	return bit

#Returns the right lighthouse beacon
def retRinf():
	lock.acquire()
	connection.write(SENSE+RINF)
	bit = struct.unpack('>B', connection.read(1))[0]
	lock.release()
	return bit

#Returns the omnidirectional infrared beacon
def retOmni():
	lock.acquire()
	connection.write(SENSE+OMNI)
	bit = struct.unpack('>B', connection.read(1))[0]
	lock.release()
	return bit

#Returns right light bump sensor (Farthest right)
def retRWall():
	lock.acquire()
	sleep(SLP)
	connection.write(SENSE+RWALL)
	bit = struct.unpack('>H', connection.read(2))[0]
	lock.release()
	return bit

#Returns front right light bump sensor (In between right and center)
def retFRWall():
	sleep(SLP)
	lock.acquire()
	connection.write(SENSE+FRWALL)
	bit = struct.unpack('>H', connection.read(2))[0]
	lock.release()
	return bit

#Returns center right light bump sensor (Closest to the front)
def retCRWall():
	sleep(SLP)
	lock.acquire()
	connection.write(SENSE+CRWALL)
	bit = struct.unpack('>H', connection.read(2))[0]
	lock.release()
	return bit

#Returns state of four lightbump sensors
def retWalls():
	lock.acquire()
	connection.write(SENSE+RWALL)
	connection.write(SENSE+LWALL)
	connection.write(SENSE+CLWALL)
	connection.write(SENSE+CRWALL)
	bit = struct.unpack('>I', connection.read(4))[0]
	lock.release()
	return bit

#Reads and prints out the state of all buttons
def readButtonState():
	cln = "False"
	spt = "False"
	dck = "False"
	mnt = "False"
	hou = "False"
	day = "False"
	bstate = readButton()
	if(bstate >= DAY):
		day = "True"
		bstate = bstate - DAY
	if(bstate >= HOU):
		hou = "True"
		bstate = bstate - HOU
	if(bstate >= MNT):
		mnt = "True"
		bstate = bstate - MNT
	if(bstate >= DCK):
		dck = "True"
		bstate = bstate - DCK
	if(bstate >= SPT):
		spt = "True"
		bstate = bstate - SPT
	if(bstate == CLN):
		cln = "True"
	print "Clean: "+cln+"\nSpot: "+spt+"\nDock: "+dck+"\nMinute: "+mnt+"\nHour: "+hou+"\nDay: "+day	

#-------------------------------------------------------------------------------------------------------------
# - MISC CONTROL COMMANDS - Other commands, Simulate button presses, control motors and LEDS, play songs
#-------------------------------------------------------------------------------------------------------------

#Same as pressing the clean button
def clean():
	lock.acquire()
        connection.write(CLEAN)
	lock.release()

#Same as pressing the spot button
def spotClean():
	lock.acquire()
        connection.write(SPOT)
	lock.release()

#Finds the nearest dock
def dock():
	lock.acquire()
        connection.write(DOCK)
	lock.release()

#Controls the individual motors for the vacuum
def motors(main,side,vac):
        if main > 127 or main < -127 or side > 127 or side < -127:
                print "Main/Side cannot be above 127 or below -127"
                return
        if vac > 127 or vac < 0:
                print "vac cannot be greater than 127 or less than 0"
                return
	lock.acquire()
        cmd = struct.pack("BBB", main, side, vac)
        connection.write(MOTOR+cmd)
	lock.release()

#Plays a song (Downwards chromatic scale)
def Song():
	lock.acquire()
	connection.write(SONG+chr(0)+chr(6)+struct.pack('BBBBBBBBBBBB', 70, 8, 69, 8, 68, 8, 67, 8, 66, 8, 65, 8))
	sleep(.1)
	lock.release()

#Plays an existing song
def playSong(s):
	lock.acquire()
        connection.write(PLAY+chr(s))
	lock.release()

#Controls the LED lights
def LED(bit,color,power):
	lock.acquire()
        cmd = struct.pack("BBB", bit, color, power)
        connection.write(ClED+cmd)
	lock.release()

#Controls the LED display using bits (It's a doozie)
def bLED(b0,b1,b2,b3):
	lock.acquire()
        cmd = struct.pack("hhhh", b0, b1, b2, b3)
        connection.write(BLED+cmd)
	lock.release()

#Controls the LED display with ASCII values
def aled(a0,a1,a2,a3):
	lock.acquire()
        cmd = struct.pack("BBBB", a0, a1, a2, a3)
        connection.write(ALED+cmd)
	lock.release()

#0=clean, 1=spot, 2=dock, 3=minute, 4=hour, 5=day, 6=schedule, 7=clock
#Same as pushing the given button
def pushButton(but):
	lock.acquire()
        connection.write(PUSH+but)
	lock.release()

#-------------------------------------------------------------------------------------------------------------
# - Time Commands - Wait
#-------------------------------------------------------------------------------------------------------------

#Waits .1 seconds - minimum time between sent commands
def wait():
	sleep(.1)

#Stops the method until (only) a specific button is pressed
def stopUntilButton(con):
        while True:
                if readButton() == con:
                        break

#Stops the method until a given sensor is pressed
def stopUntilSensor(pack):
        while True:
		data = readSensor(pack, 2)
                if data > 0:
			return data

#-------------------------------------------------------------------------------------------------------------
# - Variable Mutators - Change Certain Variables
#-------------------------------------------------------------------------------------------------------------

#Sets default speed
def setSpeed(speed):
	SPD = speed

#-------------------------------------------------------------------------------------------------------------
# - NOTE - To use these methods outside of this file use 'from FILENAME import *'
#-------------------------------------------------------------------------------------------------------------
