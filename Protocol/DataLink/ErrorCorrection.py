import sys
sys.path.append('../Mobile-Robotsystems')
import Protocol.DataLink.crc as crc
from Protocol.Physical.DTMF_overclass import DTMF


#Der skal kommenteres alle SeqNo skal have samme hexadecimal længde
def ErrorCorrection(pack,baud):
    dtmf = DTMF(baud)
    errorList = []
    for i in range(len(pack)):
        if (pack[i]=="error"):
            errorList += [i]
    
    for i in range(len(errorList)):
        dtmf.send.send_package([0, 1, 9, 6, errorList[i], errorList[i], errorList[i], 0, 1])
        print([0, 1, 9, 6, errorList[i], errorList[i], errorList[i], 0, 1])
    
    newData = dtmf.listen.startListen()
    
    
    #print()

ErrorCorrection([[0x0,0x1,0x9],"error",[0x1,0xa],"error", "error", [0x1,0x4,0x9,0xf]],50)