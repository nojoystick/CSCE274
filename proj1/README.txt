README.txt

Header.pdf contains the required project submission information.

connection_interface.py will contain the first interface required
by the assignment. It connects to the serial interface, sends and
reads data, and then closes the connection.

state_interface.py will contain the second interface required by
the assignment. This interface will control the state of the
robot, read the buttons, and send a drive command if a velocity
and wheel radius are passed in as arguments.

main.py initializes the robot, and if the button is pressed, it 
moves it along a pentagon with 30cm sides, listening continuously
for button presses, and stops it when it covers the pentagon. Or
if the button is pressed while the robot is moving, it stops the
robot when it reaches the current goal vertex.
