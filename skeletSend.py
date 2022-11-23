import sys
import Turtlebot.Turtlebot_Python.moveClass as moveClass
import signalProcessing.protocol as protocol
from DTMF.DTMF_overclass import DTMF
import time

def main():
    robot=DTMF(20)
    #moveObj = moveClass.bot()
    
    with open('file.txt') as f:
        contents = f.read()
    move = [[20,10],[-10,30]]
    list = move + [[contents]]
    #[[20,10],[-10,30],["Dees large Nuts"]]
    list = protocol.convert_to_hexa(list)
    list = protocol.hexa_devide(list)
    list = protocol.add_seq(list)
    list = protocol.add_address(list)
    list = protocol.add_CRC(list)
    list = protocol.add_esc(list)
    list = protocol.add_StartStop(list)
    list = protocol.one_list(list)
    
    robot.send.send_package([*robot.send.synchroniazation(150,'mute'),*list])
    
    #moveObj.move(ang, dist)
    #moveObj.stop()

if __name__ == "__main__":
    main()