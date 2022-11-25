import sys
from Turtlebot.moveClass import moveClass
from Protocol.DataLink.protocol_class import protocolClass
import time

def main():
    baud = 20
    moveObj = moveClass()
    pack = protocolClass(40)
    
    pack.PhysicalUp()
    pack.DataLinkUp()
    
    for i in range(len(pack.data_list)-1):
        moveObj.move(pack.data_list[i][0],pack.data_list[i][1])
    moveObj.stop()

if __name__ == "__main__":
    main()