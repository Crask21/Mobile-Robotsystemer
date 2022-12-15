from Protocol.Physical.Class_DTMF import SEND

from Protocol.Physical.Threadprog4 import LISTEN

class DTMF:
    def __init__(self, baud, sync=10, mono_robot=False):
        # DTMF Settings
        fs = 44100
        amplitude = 15000
        media = 'PyGame' # 'SD'
        fade_P = 0.006667
        baud_rate = baud
        syn = sync
        # SYNC

        
        self.send = SEND(fs, amplitude, fade_P, baud_rate,syn, media,mono=mono_robot)
        self.listen=LISTEN(baud_rate)


#robot=DTMF(10)
#robot.listen.startListen()
#robot.send.send_package([0xc,0xa,0xa,0xa,0xa,0xb])
# helo

    

