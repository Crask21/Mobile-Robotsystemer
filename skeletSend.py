import sys
#import Turtlebot.Turtlebot_Python.moveClass as moveClass
from protocol_class import protocolClass
from DTMF.DTMF_overclass import DTMF
import time

def main():
    robot=DTMF(50,30)
    #moveObj = moveClass.bot()
    
    move = [[20,10],[-10,30],[20,10],[-10,30],[20,10],[-10,30]]
    #[[20,10],[-10,30],["Dees large Nuts"]]
    pack = protocolClass(move,'output.txt')
    pack.DataLinkDown()
    pack.print()
    
    print(pack.data_list)

    #hej=[7,7,7,7,7,7,7,7,7,7,7,15,15,15]

    robot.send.send_package(pack.data_list, False)
    #robot.send.send_package(pack.data_list)
    
    #moveObj.move(ang, dist)
    #moveObj.stop()

if __name__ == "__main__":
    main()