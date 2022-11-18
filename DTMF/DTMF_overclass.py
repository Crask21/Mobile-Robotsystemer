from DTMF.Class_DTMF import SEND
from DTMF.Threadprog import LISTEN

class DTMF:
    def __init__(self, baud):
        # DTMF Settings
        fs = 44100
        amplitude = 5000
        media = 'PyGame' # 'SD'
        fade_P = 0.02
        baud_rate = baud

        self.send = SEND(fs, amplitude, fade_P, baud_rate, media)
        self.listen=LISTEN(baud_rate)


#robot=DTMF(10)
#robot.listen.startListen()
#robot.send.send_package([0xc,0xa,0xa,0xa,0xa,0xb])

    

