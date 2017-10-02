from Interface import *      #Imports all methods from interface
import sys
#-------------------------------------------------------------------------------------------------------------
# - Variables - Important variables
#-------------------------------------------------------------------------------------------------------------
charg = False #Charging?
m = False  #Moving?
sp = 900  #Set Point
pe = 0     #Past Error
le = 0     #Last Error
st = .1    #Sampling Time
kp = .016     #Proportional Gain
ki = .003     #Integral Gain
kd = .002    #Derivative Gain

#-------------------------------------------------------------------------------------------------------------
# - PID Controller - Returns a value based off of sensor data.  Returned value determines what to do
#-------------------------------------------------------------------------------------------------------------

def pid():
	global le
	global pe
	#frwall = retFRWall()
	#crwall = retCRWall()
	e = sp - retRWall() - 10*retFRWall() - 10*retCRWall()        #Error
	P = kp*e                  		#Proportional Controller
	I = ki*( pe + e )         		#Integral Controller
	D = kd*( e - le )/st      		#Derivative Controller
	u = P + I + D     	  		#Controller Output
	pe = I                    		#Updates past error
	le = e			  		#Updates last error
	return u                  		#Returns controller output

#-------------------------------------------------------------------------------------------------------------
# - Movement Function - Controls the motion of the robot, checks the bump and cliff sensors
#-------------------------------------------------------------------------------------------------------------

def go():
#	sys.exit()
	global charg
	global m
	ls = 50			#Left wheel speed
	rs = 50
	a = retCharges()
	b = retCharge()  
	if retCharges() is not 0 or a is not 0 or b is not 0:
		forward(0)
		turnOff()
		sys.exit()
		sleep(1)                      #Right wheel speed
	elif retCharges() is 0 and a is 0 and b is 0:
		while m:			#While moving
			bump = retBump()
			om = retOmni()
			om1 = retOmni()
			om2 = retOmni()
			c = retCharges()
			d = retCharge()
			wait()
			if c is not 0 or d is not 0:
				forward(0)
				sleep(1)
			#	turnOff()
				print "ASDFJKL;ASDFJKL;ASDFJKL;"
				m = False
				charg = True
				sys.exit()
			elif bump is 1:
				turnRight(19)
				sleep(1)
				forwardFor(-15,2)
			elif bump is 2:
				turnLeft(19)
				sleep(1)
				forwardFor(-15,2)
			elif bump is 3:
				turnLeft(11)
				sleep(.5)
				forwardFor(-15,2)
				wait()
			elif om is 164 or om is 169:
				print "Good"
				move(11,75)
			elif om is 168 or om is 165:
				move(75,11)
				print "OKk"
			elif om is 172 or om is 173 or om is 161:	
				forward(11)
				print "Correct"
			elif om is 0 and om1 is 0 and om2 is 0 and m:
				move(20,30)
				wait()
			#	if bump is 1:	#If bumped in the middle
			#		turnRight(19)
			#		wait()
			#	elif bump is 2:
			#		turnLeft(19)
			#		wait()
				
		#3		u = pid()
		#		print u
		#		if u > 14:
		#			ls = 30
		#			rs = 20
		#		else:
		#			ls = 35 + u
		#			rs = 35 - u	
		#		if m:
				#	print "LEFT: " + str(ls)
				#	print "RIGHT: " + str(rs)
		#			move(ls,rs)
		#			sleep(st)		
			
			wait()

#-------------------------------------------------------------------------------------------------------------
# - Main - Starts the robot and continuously checks for button presses
#-------------------------------------------------------------------------------------------------------------

connection.close()
wait()
connection.open()
turnOn()
wait()
safeMode()
wait()
while not charg:
	ret = readButton()
	if ret is 1:	 		#If Clean is pressed
		if not m:		#If NOT moving
			t = Thread(target=go)
			m = True	#Sets moving to true
			t.start()	#Starts the movement function
		else:			#If moving
			m = False	#Sets moving to false
			forward(0)	#Stops the robot
		wait()
	elif ret is 4:			#If Dock is pressed
		break			#Ends the loop
	wait()	
turnOff()	

#-------------------------------------------------------------------------------------------------------------
# - Note - Only follows walls on the right
#-------------------------------------------------------------------------------------------------------------
