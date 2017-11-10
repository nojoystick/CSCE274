import state_interface
state = state_interface.Interface()

front_right = state.read_light_front_right()
center_right = state.read_light_center_right()
right = state.read_light_right()

print "FRONT RIGHT: "+str(front_right)
print "CENTER RIGHT: "+str(center_right)
print "RIGHT: "+str(center_right)


