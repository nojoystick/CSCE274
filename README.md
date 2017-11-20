# CSCE274

This repository will contain all the code for four group project assignments programing the iRobot Create 2 using pySerial.

Project 1 involved creating two interfaces which are used to control the state of the robot and send commands. The main.py implements these interfaces to make the robot drive in a pentagon when the "Clean" button is pressed. The robot also listens for button presses as it drives its course and responds by stopping at the next vertex of the pentagon. It then completes the pentagon when the button is pressed again.


Project 2 implemented a random walk algorithm for the robot. Once the "Clean" button was pressed, the robot would travel through the room, and if it encountered a bump or cliff, it would stop, turn 180±30 degrees, and continue driving.
If the wheel drop was detected, it would play a warning song and stop until the "Clean" button was pressed again.

Project 3 implemented a PD controller to follow a wall. The robot would maintain a set point using the light sensors to detect distance from the wall. If a wall approached from the front, a multiplier was used to ensure that the robot would turn quickly enough to avoid the oncoming corner. Aspects of Project 2 were maintained to handle obtsacles.
