import time
from Turtlebot.moveClass import moveClass
from Protocol.DataLink.protocol_class import protocolClass
from Protocol.Physical.DTMF_overclass import DTMF


def main():
    pack= [0, 1, 10, 11, 12, 1, 8, 0, 14, 4, 6, 0, 13, 0, 1, 0, 1, 10, 11, 12, 2, 13, 10, 14, 4, 6, 15, 15, 0, 1, 0, 1, 0, 1, 10, 11, 12, 3, 4, 4, 6, 5, 6, 5, 7, 10, 2, 0, 6, 14, 2, 8, 9, 0, 1, 0, 1, 10, 11, 12, 4, 7, 5, 7, 4, 7, 3, 12, 10, 10, 0, 1]
    #print(len(pack))
    global robot
    robot=DTMF(50,10)
    # for testing
    #data_prot = protocolClass(moves=pack,robot=robot)
    #data_prot.DataLinkUp()  
    #data_prot.print()
    #time.sleep(100)
    
    moveObj = moveClass()
    data = robot.listen.startListen()
    robot.send.compare(pack, robot.listen.outputList)
    data_prot = protocolClass(moves=data,robot=robot)

    data_prot.DataLinkUp()  
    data_prot.print()
    for i in range(len(data_prot.data_list)-1):
        moveObj.move(data_prot.data_list[i][0],data_prot.data_list[i][1])
    moveObj.stop()

if __name__ == "__main__":
    main()