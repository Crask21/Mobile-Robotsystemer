import sys
sys.path.append('../Mobile-Robotsystems')
import Protocol.DataLink.crc as crc
import Protocol.DataLink.protocol as protocol
from Protocol.Physical.DTMF_overclass import DTMF
import numpy as np
import time


#Der skal kommenteres alle SeqNo skal have samme hexadecimal længde
#Errorhandle: 0x96

def errorCorrectionUp(pack, robot):
    #dtmf = DTMF(baud)
    errorList = []
    errorList = range(len(pack))
    #three lines are the real lines
   # for i in range(len(pack)):
   #     if (pack[i][1]=="error"):
   #         errorList += [i]
    errorMessage = []
    #changed from len(errorList>0) to len(errorList)>0 this looks more right
    if len(errorList)>0:
        for i in range(len(errorList)):
            errorMessage += [0, 1, 9, 6, errorList[i], errorList[i], errorList[i], 0, 1]
            print([0, 1, 9, 6, errorList[i], errorList[i], errorList[i], 0, 1])
        print("ECUP errorMessage: ")
        print(errorMessage)
        robot.send.send_package(errorMessage)
        #time.sleep(5)
        
        dataNew = robot.listen.startListen()
        dataNew = protocol.organize(dataNew)
        dataNew = protocol.esc_check(dataNew)
        dataNew = protocol.decode_CRC(dataNew)
        #dataNew = errorCorrectionUp(dataNew,baud) #Recursive intergration is complicated
        if(len(dataNew) == len(errorList)):
            for i in range(len(errorList)):
                pack[errorList[i]] = dataNew[i]
        else:
            print("Fatal error at error correction")
        return pack
    else:
        return pack
    
def errorCorrectionDown(pack, robot):
    #dtmf = DTMF(baud)
    resend = []
    errorMessage = robot.listen.startListen()
    print('ECDown listened finished')
    errorMessage = protocol.organize(errorMessage)
    errorMessage = protocol.hexa_to_msg(errorMessage)
    print(errorMessage)

    for i in range(len(errorMessage)):
        if(errorMessage[i][0:1]==[9,6]):
            print(np.std(errorMessage[i][2:4]))
            if(np.std(errorMessage[i][2:4])==0):
                resend+=pack[errorMessage[i][3]]
            else:
                print("Error in error message similarity") # a minor bandaid solution
                resend+=pack[errorMessage[i][3]]
    resend = protocol.one_list(resend)
    print("ECDown prossessed. Resend length:")
    print(len(resend))
    if len(resend) != 0:
        print("ECDown sending")
        robot.send.send_package(resend)
    
    
#errorCorrection([[0x0,0x1,0x9],"error",[0x1,0xa],"error", "error", [0x1,0x4,0x9,0xf]],50)