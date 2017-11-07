import state_interface.py
import threading
import time

connection = state_interface.Interface()


def bumpTest:
while(1):
  connection.drive(200, 0)
  bump = connection.bump_wheel_drop()
  print bump
  if bump[1]:
    connection.stop()
    break


while not DONE:
  connection.pause()
  ret = connection.read_button(connection.getClean())
  connection.pause()
  if ret:
    if not moving:
      myThread = threading.Thread(target=bumpTest)
      moving = True
      myThread.start()
   else:
      PRESS = True
      moving = False
    connection.pause()
  elif TOTAL is 5:
    break
  connection.pause()
