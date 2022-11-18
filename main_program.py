from DTMF.DTMF_overclass import DTMF
import time


robot=DTMF(10)
#robot.listen.startListen()
pack=[0, 1, 1, 10, 2, 0, 3, 0, 1, 0, 1, 2, 13, 4, 7, 0, 0, 1, 0, 1, 3, 9, 13, 10, 4, 0, 1, 0, 1, 4, 7, 0, 6, 9, 2, 0, 3, 13, 2, 0, 3, 3, 0, 1]

robot.send.send_package([*robot.send.synchroniazation(14,'mute'),*pack])
robot.listen.startListen()
print(pack)

time.sleep(10)
print(robot.listen.outputList==pack)