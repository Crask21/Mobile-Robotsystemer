import sys
from Turtlebot.moveClass import moveClass
from Protocol.DataLink.protocol_class import protocolClass
from Protocol.Physical.DTMF_overclass import DTMF
import time

def main():
    baud = 20
    robot=DTMF(baud,30, mono_robot = True)
    
    moveObj = moveClass()
    pack = protocolClass('0x0',[],robot)
    
    pack.PhysicalUp()
    print("After physicalUp: ")
    pack.print()
    print("even more after physical up")
    
    pack.DataLinkUp()
    print("After DataLinkUp:")
    pack.print()
    
    #fix the length of following range
    for i in range(len(pack.data_list)-1):
        moveObj.move(pack.data_list[i][0],pack.data_list[i][1])
    moveObj.stop()
    
    
    #delete the moves
    pack.data_list = pack.data_list[len(pack.data_list)-1]
    print("before datalink down:")
    pack.print()
    #dataLink down
    pack.DataLinkDown()
    print("After DataLinkDown:")
    pack.print()
    
    #physical down
    pack.PhysicalDown()
    print("After PhysicalDown")
    pack.print()

if __name__ == "__main__":
    main()