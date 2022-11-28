import sys
from Turtlebot.Turtlebot_Python.moveClass import bot
import protocol
from DTMF.DTMF_overclass import DTMF
import time

def main():
    pack=[0, 1, 10, 11, 12, 1, 9, 4, 8, 10, 4, 0, 1, 0, 1, 10, 11, 12, 2, 7, 6, 9, 14, 5, 0, 1, 0, 1, 10, 11, 12, 3, 9, 4, 
8, 10, 8, 0, 1, 0, 1, 10, 11, 12, 4, 7, 6, 9, 14, 2, 0, 1, 0, 1, 10, 11, 12, 5, 9, 4, 8, 10, 15, 0, 1, 0, 1, 10, 11, 12, 6, 7, 6, 9, 14, 14, 0, 1, 0, 1, 10, 11, 12, 7, 4, 4, 6, 5, 6, 5, 7, 10, 2, 0, 6, 14, 7, 5, 7, 4, 7, 3, 8, 0, 1]
    #print(len(pack))
    robot=DTMF(40,10)
    moveObj = bot()
    list = robot.listen.startListen()
    robot.send.compare(pack, robot.listen.outputList)
    list = protocol.organize(list)
    print(list)
    list = protocol.esc_check(list)
    list = protocol.decode_CRC(list)
    list = protocol.remove_seq(list)
    list = protocol.convert_to_decimal(list)
    
    print(list)
    for i in range(len(list)-1):
        moveObj.move(list[i][0],list[i][1])
    moveObj.stop()

if __name__ == "__main__":
    main()