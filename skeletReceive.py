import sys
from Turtlebot.Turtlebot_Python.moveClass import bot
from protocol_class import protocolClass
from DTMF.DTMF_overclass import DTMF
import time

def main():
    pack= [0, 1, 10, 11, 12, 1, 8, 10, 9, 4, 7, 0, 1, 0, 1, 10, 11, 12, 2, 7, 6, 9, 14, 5, 0, 1, 0, 1, 10, 11, 12, 3, 4, 4, 
6, 5, 6, 5, 7, 10, 2, 0, 6, 14, 7, 5, 7, 4, 7, 3, 0, 0, 1]
    #print(len(pack))
    robot=DTMF(40,10)
    moveObj = bot()
    data = robot.listen.startListen()
    robot.send.compare(pack, robot.listen.outputList)
    data_prot = protocolClass(data)
    data_prot.DataLinkUp()  
    data_prot.print()
    for i in range(len(data_prot.data_list)-1):
        moveObj.move(data_prot.data_list[i][0],data_prot.data_list[i][1])
    moveObj.stop()

if __name__ == "__main__":
    main()