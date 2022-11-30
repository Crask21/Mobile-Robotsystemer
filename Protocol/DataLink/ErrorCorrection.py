import sys
sys.path.append('../Mobile-Robotsystems')
import Protocol.DataLink.crc as crc
import Protocol.DataLink.protocol as protocol
from Protocol.Physical.DTMF_overclass import DTMF
import numpy as np


#Der skal kommenteres alle SeqNo skal have samme hexadecimal længde
#Errorhandle: 0x96

def errorCorrectionUp(pack,dtmf):
    #dtmf = DTMF(baud)
    errorList = []
    for i in range(len(pack)):
        if (pack[i]=="error"):
            errorList += [i]
    errorMessage = []
    if len(errorList>0):
        for i in range(len(errorList)):
            errorMessage += [0, 1, 9, 6, errorList[i], errorList[i], errorList[i], 0, 1]
            print([0, 1, 9, 6, errorList[i], errorList[i], errorList[i], 0, 1])
        dtmf.send.send_package(errorMessage)
        
        
        dataNew = dtmf.listen.startListen()
        dataNew = protocol.organize(dataNew)
        dataNew = protocol.esc_check(dataNew)
        dataNew = protocol.decode_CRC(dataNew)
        #dataNew = errorCorrectionUp(dataNew,baud) #Recursive intergration is complicated
        if(len(dataNew) == len(errorList)):
            for i in range(len(errorList)):
                pack[errorList[i]] = dataNew[i]
        else:
            print("Fatal error at error correction")
    
def errorCorrectionDown(pack,dtmf):
    #dtmf = DTMF(baud)
    resend = []
    errorMessage = dtmf.listen.startListen()
    errorMessage = protocol.organize(errorMessage)
    for i in range(len(errorMessage)):
        if(errorMessage[i][0:1]==[9,6]):
            if(np.std(errorMessage[i][2:4])==0):
                resend+=pack[errorMessage[i][3]]
            else:
                print("Error in error message similarity") # a minor bandaid solution
                resend+=pack[errorMessage[i][3]]
    resend = protocol.one_list(resend)
    dtmf.send.send_package(resend)
    
    
#errorCorrection([[0x0,0x1,0x9],"error",[0x1,0xa],"error", "error", [0x1,0x4,0x9,0xf]],50)