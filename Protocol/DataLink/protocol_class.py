import numpy as np
import Protocol.DataLink.protocol as protocol
from Protocol.Physical.DTMF_overclass import DTMF
import Protocol.DataLink.ErrorCorrection as ec
import Protocol.DataLink.ErrorCorrection as ErrorCorrection
move = [[10,20],[-10,30]]

class protocolClass:
    data_list = []
    n = 4  #Data package size
    def __init__(self, moves, robot, filename=0):
        if filename != 0:
            self.data_list=moves+[[open(filename).read()]]
        else:
            for i in range(len(moves)):
                self.data_list.append(moves[i])
        self.robot=robot

    def setMoves(self, moves):
         self.data_list=moves
    
    def setPackage(self, value):
        self.data_list = value

    def set(self, fileName):
        self.data_list += [[open(fileName).read()]]

    def DataLinkDown(self):
        self.data_list=protocol.convert_to_hexa(self.data_list)
        self.data_list=protocol.data_seg(self.data_list,6)
        self.data_list=protocol.hexa_devide(self.data_list)
        self.data_list=protocol.add_seq(self.data_list)
        self.data_list=protocol.add_address(self.data_list)
        self.data_list=protocol.add_CRC(self.data_list)
        self.data_list=protocol.add_esc(self.data_list)
        self.data_list=protocol.add_StartStop(self.data_list)
        self.dataListEC = self.data_list
        self.data_list=protocol.one_list(self.data_list)
    
    def DataLinkUp(self):
        self.data_list=protocol.organize(self.data_list)
        self.data_list=protocol.esc_check(self.data_list)
        self.data_list=protocol.decode_CRC(self.data_list)
        self.data_list = ErrorCorrection.errorCorrectionUp(self.data_list, self.robot)
        self.data_list=protocol.decode_address(self.data_list)
        self.data_list=protocol.remove_seq(self.data_list)
        self.data_list=protocol.data_comb(self.data_list)
        self.data_list=protocol.convert_to_decimal(self.data_list)
    
    def SendBack(self):
        print()
    
    def PhysicalDown(self):
        self.robot.send.send_package(self.data_list)
        ec.errorCorrectionDown(self.dataListEC,self.robot)
        #ved ikke hvad det er eller hvad 40 kommer fra
        #ec.errorCorrectionDown(self.dataListEC,40)
        
        
    def PhysicalUp(self):
        self.data_list = self.robot.listen.startListen()
    
    
    def print(self):
        print(self.data_list)

#l1=protocolClass(move,'test.txt')
#l1.DataLinkDown()
##l1.DataLinkUp()
#l1.print()
#l2=protocolClass(['0x0', '0x1', '0xa', '0xb', '0xc', '0x1', '0x8', '0xa', '0x9', '0x4', '0x7', '0x0', '0x1', '0x0', '0x1', '0xa', '0xb', '0xc', '0x2', '0x7', '0x6', '0x9', '0xe', '0x5', '0x0', '0x1', '0x0', '0x1', '0xa', '0xb', '0xc', '0x3', '0x4', '0x4', '0x6', '0x5', '0x6', '0x5', '0x7', '0xa', '0x2', '0x0', '0x6', '0xe', '0x7', '0x5', '0x7', '0x4', '0x7', '0x3', '0x0', '0x0', '0x1'])
#l2.DataLinkUp()
#l2.print()
#
#idk
#<<<<<<< HEAD:protocol_class.py
#    n = 4  #Data package size
#    def __init__(self, moves, filename=0):
#=======
#    dataListEC= []
#    #dtmf = DTMF(40)
#    def __init__(self, baud, sync = 10, moves = [], filename=0):
#        self.dtmf = DTMF(int(baud),sync)
#>>>>>>> be6d5aa4e7ef76ea77dd1a582f5a96fea946d556:Protocol/DataLink/protocol_class.py