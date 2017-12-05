#***NOTE THERE ARE MANY PRINT STATEMENTS COMMENTED OUT FOR DEBUGGING
#PURPOSES***

import Project4
import time
import struct
import threading
import sys
import random


#Initializes a new instance of the Robot
Robot = Project4.Robot()

#Initializes Lock which is a method apart of Threading to control other threads
#Global values to be used in threads
lock = threading.Lock()

#will keep track of how many times the clean/power is pressed
button = 0

#Main global value used in each thread to communicated with the other threads to
#initially set to 0, and is reset to 0, in which 0 indicated no state change of the robot
data = 0

#The first thread is going to be the basic running commands of this project
def wallFollow():
    global data
    global button
    global lock
    global dock
    dock = 0
    while(dock == 0):
        #print 'gogoroomba'
        #Randomwalk of Roomba
        if(data == 1):
            #print 'Starting Robot'
            lock.acquire()
            value = Robot.getRBS()
            PID = Robot.update(value)
            centerLeft = Robot.getLBCS()
            centerRight = Robot.getRBCS()
            
            #Checks our left and right center sensors to see if there is an
            #object sense our right bump sensor is only checking the right
            #if so rotates
            if(centerLeft > 200 or centerRight > 145):
                Robot.rotateCCW()
            #Checks our PID output and commutes wheel velocity occurdingly    
            elif(0 < PID < 230):
                #print 'adjusting +'
                Robot.controlledWalk(PID, 200)
            elif(PID < 0):
                #print ' adjusting -'
                Robot.controlledWalk(200, 200+PID)
            elif(PID > 237):
                Robot.controlledWalk(PID-200,200)
            

            #Quits the thread entirely by executing a sys exit
            if(data == 2):
                lock.acquire()
                print 'Qutting program'
                sys.exit('Exiting Sript')
            lock.release()

def randomJitter():
    global data                
    global button
    global lock
    global dock 
    while True:
        #print 'random jitter'
        lock.acquire()
        right = Robot.getInfraredRight()
        left = Robot.getInfraredLeft()
        omni = Robot.getInfraredOmni()
        #if the robot is in the force field of the dock
        #checks 
        if((data == 1 and (left == 161 and data != 3)) or
            (data == 1 and (right == 161 and data != 3)) or
            (data == 1 and (omni == 161 and data != 3))):
            print 'In docks forcefield'
            dock = 1
            print 'stopping robot'
            data = 3
            Robot.stopDrive()
            
        #Jitter until Dock is straight ahead
        #Checks if right or left sensor is out of the forcefield of the dock
        #Corrects itself if not
        if(data == 3):
            if(left != 161 and right != 161):
                print 'Both Sensors lost, fast error correcting'
                Robot.controlledWalk(-120, 120)
            elif(right != 161):
               print 'Right sensor lost, error correcting' 
               Robot.rotateCW()
            elif(left != 161):
                print 'Left sensor lost, error correcting'
                Robot.rotateCCW()
        lock.release()

def dockAhead():
    global data
    global button
    global lock
    while True:
        lock.acquire()
        #Sensor readings to be used in ifs
        state = Robot.chargingState()
        omni = Robot.getInfraredOmni()
        left = Robot.getInfraredLeft()
        right = Robot.getInfraredRight()
        bumpRight = Robot.getBumpandWheel()[3]
        bumpLeft = Robot.getBumpandWheel()[2]
        possibilities = [5, 0, 1]
        bumpPossibilities = [1 ,0]
        #If the robots has found the dock and is charging, we stop play a song and exit script
        if(state == 2):
            print 'found dock'
            Robot.stopDrive()
            Robot.playSong()
            data = 0
            sys.exit()
        #These are tested instances in which the sensors are directly in front of
        #the dock, or very close because of the oscillation where 161(the force field) would return
        #instead of the buoy, these cases were added in for a better sense of direction
        #We stop driving wants robot hits dock(data = 5) or when we press the button press(data = 0)
        if(((left == 172 and right == 168) and data not in possibilities) or
           ((left == 164 and right == 172) and data not in possibilities)or
           ((left == 168 and right == 168) and data not in possibilities)):
            data = 6
            Robot.stopDrive()
            print 'driving to dock'
            Robot.controlledWalk(50,50)

        #Since we are taking in these three instanes, Robot may hit the dock without being on the charge port
        #So we are checking the robots bumps to back up and adjust itself until it is docked
            
        #If the robots left bump is activated, we need to back up and then rotate CCW.
        #Also for priority reasons, we don't want this to be active while the wall following
        #is still in effect so we make sure data != 1 (wall follow is not active)
        if((bumpLeft == '1' and bumpRight == '1') and data not in bumpPossibilities):
            Robot.stopDrive()
            time.sleep(.15)
            Robot.controlledWalk(-100,-100)
            print 'hit dock, rotating CW for error correction'
            time.sleep(.015)
            print 'both bumpers hit random CW'
            Robot.stopDrive()
            Robot.controlledWalk(-50,-50)
            Robot.controlledWalk(50,50)
            data = 5
            
        if(bumpLeft == '1' and data not in bumpPossibilities):
            Robot.stopDrive()
            time.sleep(.15)
            Robot.controlledWalk(-100,-100)
            print 'hit dock, rotating CCW for error correction'
            x = random.randint(50,75)
            Robot.rotateCCWInput(x)
            data = 5
            
        #If the robots right bump is activated, we need to back up and then rotate CW
        if(bumpRight == '1' and data not in bumpPossibilities):
            Robot.stopDrive()
            time.sleep(.15)
            Robot.controlledWalk(-100,-100)
            print 'hit dock, rotating CW for error correction'
            x = random.randint(50,175)
            Robot.rotateCWInput(x)
            data = 5
        lock.release()

#This thread will check the button press and correspond with thread 1 to tell
#Roomba to do what he/she needs to do
def checkButtons():
    global data
    global button
    global lock
    prvButton = 0
    while True:
        #print 'checking buttons'
        lock.acquire()
        #print 'checking buttons after lock'
        power1 = Robot.getButtons()
        power = power1[3]
        
        if(prvButton  == '0' and power == '1'):
            if(button == 0):
                print 'Starting Robot'
                #Robot.controlledWalk(left,right)
                data = 1
                button = 1  
            else:
                print 'Button pressed after Robot started'
                Robot.controlledWalk(0,0)
                data = 0
                button = 0
        lock.release()
        prvButton = power

#First we want to want to reset Roomba, start it and then put into full mode
time.sleep(1)
Robot.clear()
Robot.setSong()
Robot.start()
Robot.full()


#print Robot.getBumpandWheel
#Sets up the threads to be ran
t1 = threading.Thread(name = 'wallFollow', target = wallFollow)
t2 = threading.Thread(name = 'CheckButtons', target = checkButtons)
t3 = threading.Thread(name = 'randomJitter', target = randomJitter)
t4 = threading.Thread(name = 'dockAhead', target = dockAhead)


#starts the threads
t1.start()
t2.start()
t3.start()
t4.start()
