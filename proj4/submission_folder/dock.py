# PSEUDOCODE
# If anything nonzero is read by the dock sensor
# While the robot is not charging or docked
# Turn clockwise until the right sensor reads red
# Turn counterclockwise until the left sensor reads green
# Turn clockwise again until the omni sensor reads both
# Drive forward a small distance and repeat

if ir_right is not 0 or ir_left is not 0 or ir_omni is not 0:
  while charging is not 0 or dock is not 0:
    while(ir_right is not RED):
      connection.drive_direct(-10,10) # arbitrary speed; adjust later
    while(ir_left is not GREEN):
      connection.drive_direct(10,-10)
    while(ir_omni is not RED_GREEN):
      connection.drive_direct(-10,10)
    connection.drive_direct(1,1)
    connection.tpause(1) # drive forward for 1 second; adjust later
   


