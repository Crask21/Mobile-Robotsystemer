from Send_DTMF.Class_DTMF import DTMF
from Send_DTMF.Class_DTMF import synchroniazation
from Send_DTMF.Class_DTMF import rand_pack
#import protocol


# DTMF Settings
fs = 44100
amplitude = 5000
media = 'PyGame' # 'SD'
fade_P = 0.02
baud_rate = 2

# Initialization
dtmf = DTMF(fs, amplitude, fade_P, baud_rate, media)



dtmf.send_package(synchroniazation(10))





