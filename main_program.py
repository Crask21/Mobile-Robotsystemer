from DTMF.DTMF_overclass import DTMF
import time


robot=DTMF(20)
robot.listen.startListen()
pack=[0, 1, 1, 10, 2, 0, 3, 0, 1, 0, 1, 2, 13, 4, 7, 0, 0, 1, 0, 1, 3, 9, 13, 10, 4, 0, 1, 0, 1, 4, 7, 0, 6, 9, 2, 0, 3, 13, 2, 0, 3, 3, 0, 1]

time.sleep(2)
#robot.send.send_package([*robot.send.synchroniazation(150,'mute'),*pack])







#print(pack)

time.sleep(10)
robot.send.compare(pack,robot.listen.outputList)