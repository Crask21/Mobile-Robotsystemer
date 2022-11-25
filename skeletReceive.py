import sys
import Turtlebot.Turtlebot_Python.moveClass
import protocol
from DTMF.DTMF_overclass import DTMF
import time

def main():
    pack=[0, 1, 10, 11, 12, 1, 9, 4, 8, 10, 4, 0, 1, 0, 1, 10, 11, 12, 2, 7, 6, 9, 14, 5, 0, 1, 0, 1, 10, 11, 12, 3, 4, 4, 4, 5, 4, 5, 5, 10, 2, 0, 4, 14, 5, 5, 5, 4, 5, 3, 11, 0, 1]
    #print(len(pack))
    robot=DTMF(20,10)
    moveObj = moveClass.bot()
    list = robot.listen.startListen()
    list = protocol.organize(list)
    list = protocol.esc_check(list)
    list = protocol.decode_CRC(list)
    list = protocol.remove_seq(list)
    list = protocol.convert_to_decimal(list)
    robot.send.compare(pack, robot.listen.outputList)
    print()
    for i in range(len(list)-1):
        moveObj.move(list[i][0],list[i][1])
    moveObj.stop()

if __name__ == "__main__":
    main()