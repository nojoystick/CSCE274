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
begins driving. If the button is pressed again, it stops, and
waits for another button press to start again. As it drives it
detects for cliffs, bumps, and wheel drops. If it reaches a cliff
or detects a bump, it turns 180±30 degrees and continues driving.
For a bump on the left, it turns clockwise, and a bump on the
right causes a counterclockwise turn. If it detects a wheel drop,
it stops, plays a warning song (All Star by Smash Mouth) and then
waits for the button to be pressed to continue driving.
