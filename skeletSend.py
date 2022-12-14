import sys
#import Turtlebot.Turtlebot_Python.moveClass as moveClass
from Protocol.DataLink.protocol_class import protocolClass

from Protocol.Physical.DTMF_overclass import DTMF
import time



def main():
    baudrate = 100
    sync = 30

    robot=DTMF(baudrate,sync)
    
    #moveObj = moveClass.bot()
    
    move = [[0,20],[90,15]]

    pack = protocolClass(['0x7','0x0','0x8'],move,robot,'output.txt')

    pack.DataLinkDown()
    #pack.print()
    #pack.DataLinkUp()
    print(pack.data_list)

    robot.send.send_package(pack.data_list)
    robot.send.send_package([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],False)


    
    #moveObj.move(ang, dist)
    #moveObj.stop()

if __name__ == "__main__":
    main()