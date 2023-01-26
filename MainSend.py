import sys
#import Turtlebot.Turtlebot_Python.moveClass as moveClass
from Protocol.DataLink.protocol_class import protocolClass
from Protocol.Physical.DTMF_overclass import DTMF
import time



def main():
    baudrate = 50
    sync = 10

    robot=DTMF(baudrate,sync)
    
    
    move = [[-90,0],[-90,70],[90,30],[-90,50],[-30,100],[30,100]]   

   
    
    

    pack = protocolClass(['0xd','0x0','0x8'],move,robot,'output.txt')

    pack.DataLinkDown()

    
    pack.PhysicalDown()
    
   

if __name__ == "__main__":
    main()