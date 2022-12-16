from Protocol.Physical.Class_DTMF import SEND

from Protocol.Physical.Threadprog5 import LISTEN

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
        self.listen=LISTEN(baud_rate, syn, fade_P, amplitude, fs, pack=[0, 1, 1, 0, 8, 3, 11, 13, 0, 1, 0, 1, 2, 5, 3, 7, 5, 6, 3, 6, 3, 6, 5, 7, 3, 8, 6, 15, 0, 1, 0, 1, 3, 6, 6, 7, 5, 6, 12, 2, 0, 7, 2, 6, 15, 14, 10, 7, 0, 1, 0, 1, 4, 7, 5, 7, 4, 6, 5, 6, 11, 7, 0, 1])


#robot=DTMF(10)
#robot.listen.startListen()
#robot.send.send_package([0xc,0xa,0xa,0xa,0xa,0xb])
# helo

    

