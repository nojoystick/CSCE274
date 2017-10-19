DRIVE_COMMAND=137
def drive(velocity, radius):
    v1, v2, r1, r2 = drive_formatting(velocity, radius)
    command = str(DRIVE_COMMAND)+" "+str(v1)+" "+str(v2)+" "+str(r1)+" "+str(r2)
    #send_command(command)
    return command

def drive_formatting(velocity, radius):
  # Check boundary conditions
    #if velocity > MAX_VELOCITY:
     # velocity = MAX_VELOCITY
    #if velocity < MIN_VELOCITY:
     # velocity = MIN_VELOCITY
    #if radius > MAX_RADIUS:
     # radius = MAX_RADIUS
    #if radius < MIN_RADIUS:
     # radius = MIN_RADIUS
    # Format radius into hex
    #if radius != STRAIGHT and radius != TURN_CLOCKWISE and radius != TURN_COUNTERCLOCKWISE:
      # Return radius as a 32 bit hex value w/out 0x
    velocity = hex(velocity & (2**16-1))[2:]
    radius = hex(radius & (2**16-1))[2:]
    # store as a 4 character string
    velocity = str(velocity).zfill(4)
    radius = str(radius).zfill(4)
    # parse low and high bit back into decimal
    v1 = int(velocity[:2],16)
    v2 = int(velocity[2:],16)
    r1= int(radius[:2],16)
    r2= int(radius[2:],16)

    return (v1,v2,r1,r2)

def send_command(command):
    encoded = ""
    command = str.split(command)
    for i in range(0,len(command)):
      encoded += chr(int(command[i]))
    self.connection.write(encoded)

    #Friend who got all projects working said this is all you need.
    #self.connection.write(command)
    #sleep(.015) #Must wait 15 ms in between command sends.

command = drive(-200,500)
send_command(command)
