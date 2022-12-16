import sys
#import Turtlebot.Turtlebot_Python.moveClass as moveClass
from Protocol.DataLink.protocol_class import protocolClass

from Protocol.Physical.DTMF_overclass import DTMF
import time



def main():
    baudrate = 50
    sync = 30

    robot=DTMF(baudrate,sync)
    
    #moveObj = moveClass.bot()
    
    #move = [
    #[0,20],[90,15]]
    move = [[90,0],[90,0],[0,110],[0,123],[-90,0],[0,46],[90,0],[0,35],[-90,0],[0,100],[0,67]]

    testpack=[0, 1, 1, 0, 8, 3, 11, 13, 0, 1, 0, 1, 2, 5, 3, 7, 5, 6, 3, 6, 3, 6, 5, 7, 3, 8, 6, 15, 0, 1, 0, 1, 3, 6, 6, 7, 5, 6, 12, 2, 0, 7, 2, 6, 15, 14, 10, 7, 0, 1, 0, 1, 4, 7, 5, 7, 4, 6, 5, 6, 11, 7, 0, 1]

    robot.send.send_package(testpack)



    pack = protocolClass(['0x7','0x0','0x8'],move,robot,'output.txt')

    pack.DataLinkDown()

    print(pack.data_list)
    pack.PhysicalDown()
    
    #robot.send.send_package(pack.data_list)
    #robot.send.send_package([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],False)


    
    #moveObj.move(ang, dist)
    #moveObj.stop()

if __name__ == "__main__":
    main()