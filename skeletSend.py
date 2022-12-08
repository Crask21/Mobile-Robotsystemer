import sys
#import Turtlebot.Turtlebot_Python.moveClass as moveClass
from protocol_class import protocolClass
from Protocol.Physical.DTMF_overclass import DTMF
import time


def main():
    baudrate = 50
    sync = 30

    robot=DTMF(baudrate,sync)
    
    #moveObj = moveClass.bot()
    
    move = [[0,80],[90,80]]

    pack = protocolClass(move,'output.txt')

    pack.DataLinkDown()
    #pack.print()
    
    print(pack.data_list)


    robot.send.send_package(pack.data_list)

    
    #moveObj.move(ang, dist)
    #moveObj.stop()

if __name__ == "__main__":
    main()