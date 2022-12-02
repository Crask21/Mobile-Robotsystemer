from Protocol.Physical.Class_DTMF import SEND
from Protocol.Physical.Threadprog import LISTEN

class DTMF:
    def __init__(self, baud, sync=10):
        # DTMF Settings
        fs = 44100
        amplitude = 5000
        media = 'PyGame' # 'SD'
        fade_P = 0.1
        baud_rate = baud
        syn = sync
        # SYNC

        #heyo
        self.send = SEND(fs, amplitude, fade_P, baud_rate,syn, media)
        self.listen=LISTEN(baud_rate)


#robot=DTMF(10)
#robot.listen.startListen()
#robot.send.send_package([0xc,0xa,0xa,0xa,0xa,0xb])

    

