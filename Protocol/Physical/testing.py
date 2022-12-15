from Class_DTMF import SEND
import sys
sys.path.append('../Mobile-Robotsystems')
#from Turtlebot.moveClass import moveClass
from Protocol.DataLink.protocol_class import protocolClass
from Protocol.Physical.DTMF_overclass import DTMF
import time

dtmf_freq = [[1209,697], # 0
            [1336,697],  # 1
            [1477,697],  # 2
            [1633,697],  # 3
            [1209,770],  # 4
            [1336,770],  # 5
            [1477,770],  # 6
            [1633,770],  # 7
            [1209,852],  # 8
            [1336,852],  # 9
            [1477,852],  # A
            [1633,852],  # B
            [1209,941],  # C
            [1336,941],  # D
            [1477,941],  # E
            [1633,941]]  # F




# DTMF Settings
fs = 44100
amplitude = 6000
fade_P = 0.003
baud_rate = 160
sync = 70
send = SEND(fs, amplitude, fade_P, baud_rate,sync)
pack = [0, 1, 1, 0, 8, 3, 11, 13, 0, 1, 0, 1, 2, 4, 4, 6, 5, 6, 5, 7, 10, 2, 0, 6, 14, 4, 10, 2, 0, 1, 0, 1, 3, 7, 5, 7, 4, 7, 3, 14, 7, 0, 0, 1]

pack = [*pack,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]



pakke = [0, 1, 1, 7, 0, 8, 6, 10, 2, 0, 1, 0, 1, 2, 14, 7, 15, 14, 0, 0, 1, 0, 1, 3, 10, 13, 12, 3, 8, 7, 4, 0, 1, 0, 1, 4, 5, 3, 8, 8, 13, 0, 1, 0, 1, 5, 7, 6, 0, 3, 8, 0, 1, 0, 1, 6, 4, 4, 6, 5, 6, 5, 7, 10, 2, 0, 6, 14, 5, 5, 4, 0, 1, 0, 1, 7, 7, 5, 7, 4, 7, 3, 4, 2, 11, 0, 1]
robot=DTMF(50,30, mono_robot = True)
pack = protocolClass('0x0',[],robot)

pack.setPackage(pakke)
pack.DataLinkUp()

#send.send_package(pack)

#send.send_package([0,15],False)


print(pack)








