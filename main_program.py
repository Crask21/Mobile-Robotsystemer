from DTMF.DTMF_overclass import DTMF

robot=DTMF(10)
robot.listen.startListen()
robot.send.send_package([0xa,0xa])